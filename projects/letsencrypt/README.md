# Let's Encrypt Certificates with cert-manager and Gandi LiveDNS

This document describes the Let's Encrypt certificate setup used by the
`k8` k3s cluster.

The cluster uses **cert-manager**, **Let's Encrypt**, **DNS-01
challenges**, **Gandi LiveDNS**, and a Gandi DNS webhook solver. The
cluster-wide issuer is `letsencrypt-gandi`.

## How it works

1.  A Kubernetes `Certificate` or annotated `Ingress` requests TLS.
2.  cert-manager creates an ACME order with Let's Encrypt.
3.  cert-manager sends the DNS-01 challenge to the Gandi webhook.
4.  The webhook uses a Gandi Personal Access Token (PAT) to create
    `_acme-challenge.<hostname>` as a temporary TXT record.
5.  Let's Encrypt queries the authoritative public nameservers.
6.  After validation, Let's Encrypt issues the certificate.
7.  cert-manager stores the certificate and private key in a Kubernetes
    TLS `Secret`.
8.  The temporary TXT record is removed.

DNS-01 validation does not require the application itself to be publicly
reachable for the ACME challenge.

------------------------------------------------------------------------

## 1. DNS and nameserver setup

The domain must use DNS that the Gandi API token can manage. This setup
expects the DNS zone to be hosted by **Gandi LiveDNS**.

In Gandi:

1.  Select the domain.
2.  Open **Nameservers**.
3.  Confirm the domain is using **Gandi LiveDNS**.
4.  If external nameservers are configured, switch to Gandi LiveDNS
    before using this Gandi DNS-01 solver setup.

The important distinction is that Gandi being the **domain registrar is
not enough**. The authoritative nameservers must serve the DNS zone that
the webhook modifies.

Verify delegation:

``` bash
dig NS nickhelps.tech +short
dig SOA nickhelps.tech +short
```

For a full delegation trace:

``` bash
dig +trace NS nickhelps.tech
```

If public DNS is delegated to another provider, creating a TXT record in
Gandi LiveDNS will not satisfy Let's Encrypt.

------------------------------------------------------------------------

## 2. Create a Gandi Personal Access Token

Create a Gandi Personal Access Token with access to the organization and
DNS resources containing the domain.

Do **not** commit the PAT to Git.

Create the Kubernetes secret:

``` bash
kubectl create secret generic gandi-credentials \
  --namespace cert-manager \
  --from-literal=pat='YOUR_GANDI_PAT'
```

Verify it exists:

``` bash
kubectl get secret gandi-credentials -n cert-manager
```

The secret key must be named `pat` because the `ClusterIssuer`
references that exact key.

For GitOps, use SOPS, Sealed Secrets, or an external secret manager
rather than committing the clear-text PAT.

------------------------------------------------------------------------

## 3. Install and verify cert-manager

Verify cert-manager:

``` bash
kubectl get pods -n cert-manager
```

Expected components include:

``` text
cert-manager
cert-manager-cainjector
cert-manager-webhook
```

Verify the CRDs:

``` bash
kubectl get crd | grep cert-manager
kubectl api-resources | grep -i clusterissuer
```

If Kubernetes reports:

``` text
no matches for kind "ClusterIssuer" in version "cert-manager.io/v1"
ensure CRDs are installed first
```

cert-manager or its CRDs are missing.

------------------------------------------------------------------------

## 4. Install and verify the Gandi DNS webhook

Gandi DNS-01 support uses an external cert-manager webhook solver.

Verify the webhook:

``` bash
kubectl get pods -A | grep -i gandi
```

The webhook configuration used by this cluster is:

``` yaml
groupName: acme.nickhelps.tech
solverName: gandi
```

These values must match the installed webhook configuration.

If challenges fail, find the webhook pod and inspect its logs:

``` bash
kubectl get pods -A | grep -i gandi
kubectl logs -n <namespace> <gandi-webhook-pod> --tail=200
```

------------------------------------------------------------------------

## 5. Create the Let's Encrypt ClusterIssuer

`letsencrypt-gandi-issuer.yml`:

``` yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-gandi
spec:
  acme:
    email: limeman@gmail.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-gandi-account-key
    solvers:
      - dns01:
          webhook:
            groupName: acme.nickhelps.tech
            solverName: gandi
            config:
              patSecretRef:
                name: gandi-credentials
                key: pat
```

Apply it:

``` bash
kubectl apply -f letsencrypt-gandi-issuer.yml
```

Verify:

``` bash
kubectl get clusterissuer letsencrypt-gandi
kubectl describe clusterissuer letsencrypt-gandi
```

Expected state:

``` text
NAME                READY
letsencrypt-gandi   True
```

------------------------------------------------------------------------

## 6. Test certificate issuance

Create `cert-test.yml`:

``` yaml
apiVersion: v1
kind: Namespace
metadata:
  name: cert-test
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: cert-test
  namespace: cert-test
spec:
  secretName: cert-test-tls
  issuerRef:
    name: letsencrypt-gandi
    kind: ClusterIssuer
  dnsNames:
    - cert-test.home.nickhelps.tech
```

Apply it:

``` bash
kubectl apply -f cert-test.yml
```

Watch the ACME flow:

``` bash
watch -n2 'kubectl get certificate,certificaterequest,order,challenge -n cert-test'
```

A successful certificate becomes `READY=True`.

Verify:

``` bash
kubectl get certificate -n cert-test
kubectl get secret cert-test-tls -n cert-test
```

Inspect the certificate:

``` bash
kubectl get secret cert-test-tls -n cert-test \
  -o jsonpath='{.data.tls\.crt}' |
base64 -d |
openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

The output should show the requested DNS name, a Let's Encrypt issuer,
and valid certificate dates.

Clean up:

``` bash
kubectl delete namespace cert-test
```

------------------------------------------------------------------------

## 7. Use the ClusterIssuer with an Ingress

Example:

``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example
  namespace: example
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-gandi
spec:
  tls:
    - hosts:
        - example.home.nickhelps.tech
      secretName: example-tls
  rules:
    - host: example.home.nickhelps.tech
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: example
                port:
                  number: 80
```

Check the resulting resources:

``` bash
kubectl get certificate -n example
kubectl get secret example-tls -n example
```

------------------------------------------------------------------------

## 8. Troubleshooting

### ClusterIssuer is not ready

``` bash
kubectl describe clusterissuer letsencrypt-gandi
kubectl logs -n cert-manager deploy/cert-manager --tail=200
```

### Certificate is stuck

``` bash
kubectl get certificate,certificaterequest,order,challenge -A
kubectl describe challenge -n <namespace> <challenge-name>
kubectl describe order -n <namespace> <order-name>
kubectl get events -A --sort-by='.lastTimestamp' | tail -100
```

### DNS TXT record is not visible

Inspect the challenge:

``` bash
kubectl get challenge -A
kubectl describe challenge -n <namespace> <challenge-name>
```

Query the ACME TXT record:

``` bash
dig TXT _acme-challenge.example.home.nickhelps.tech +short
```

Query the authoritative nameservers:

``` bash
dig NS nickhelps.tech +short
```

Then query one directly:

``` bash
dig @<authoritative-nameserver> \
  TXT _acme-challenge.example.home.nickhelps.tech \
  +short
```

If the TXT record exists in Gandi but the authoritative nameserver does
not return it, verify the domain's nameserver delegation.

### Gandi authentication failure

``` bash
kubectl get secret gandi-credentials -n cert-manager
```

Verify the secret contains a key named `pat` and that the PAT has access
to the Gandi organization and DNS zone containing the domain.

### Webhook failure

``` bash
kubectl get pods -A | grep -i gandi
kubectl logs -n <namespace> <gandi-webhook-pod> --tail=200
kubectl logs -n cert-manager deploy/cert-manager --tail=200
```

------------------------------------------------------------------------

## 9. Useful verification commands

``` bash
kubectl get clusterissuer
kubectl get certificate -A
kubectl get certificaterequest -A
kubectl get order -A
kubectl get challenge -A
```

DNS:

``` bash
dig NS nickhelps.tech +short
dig SOA nickhelps.tech +short
dig TXT _acme-challenge.example.home.nickhelps.tech +short
```

Inspect a live HTTPS certificate:

``` bash
openssl s_client \
  -connect example.home.nickhelps.tech:443 \
  -servername example.home.nickhelps.tech \
  </dev/null 2>/dev/null |
openssl x509 -noout -subject -issuer -dates -ext subjectAltName
```

------------------------------------------------------------------------

## Important notes

-   Gandi being the **registrar** is not enough; Gandi LiveDNS must be
    authoritative for this specific solver setup.
-   Never commit the Gandi PAT to Git.
-   The `gandi-credentials` secret key must be named `pat`.
-   `groupName` and `solverName` must match the installed Gandi webhook.
-   Use the Let's Encrypt staging ACME endpoint during repeated
    troubleshooting to reduce the risk of production rate limits.
-   DNS-01 validation does not require the application ingress to expose
    the ACME challenge.
-   cert-manager handles certificate renewal after successful issuance.

## References

-   Gandi: Changing nameservers
-   Gandi: Personal Access Tokens
-   Gandi LiveDNS API
-   cert-manager: DNS-01 challenges
-   cert-manager: DNS-01 webhook solvers
