# Troubleshooting

- 404 from NGINX: Host header doesn't match Ingress host; fix curl/DNS or YAML host.
- EXTERNAL-IP pending: Wait a bit; ensure Service is type LoadBalancer and controller is healthy.
- Canary ignored: Ensure canary Ingress exists and canary-weight > 0 (or use header/cookie strategy).
