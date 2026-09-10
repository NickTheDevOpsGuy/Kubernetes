#!/usr/bin/env python3

import os
import time
import logging
from typing import Optional, Tuple

import requests
from prometheus_client import Gauge, Info, start_http_server


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

EIA_API_KEY = os.environ["EIA_API_KEY"]

LISTEN_PORT = int(os.getenv("LISTEN_PORT", "8000"))
REFRESH_SECONDS = int(os.getenv("REFRESH_SECONDS", "21600"))  # 6 hours
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))

USER_AGENT = os.getenv(
    "USER_AGENT",
    "nick-heating-oil-exporter/1.0"
)


# -----------------------------------------------------------------------------
# EIA endpoints
# -----------------------------------------------------------------------------

# Massachusetts residential heating oil
#
# API route:
# Petroleum -> Prices -> Weekly Heating Oil and Propane Prices
#
EIA_HEATING_OIL_URL = (
    "https://api.eia.gov/v2/petroleum/pri/wfr/data/"
)

MA_HEATING_OIL_SERIES = "W_EPD2F_PRS_SMA_DPG"


# WTI and Brent
#
# EIA still exposes these through API v2 legacy-series compatibility.
#
# Official EIA series:
#   PET.RWTC.D   = WTI Cushing
#   PET.RBRTE.D  = Brent Europe
#
EIA_SERIES_URL = "https://api.eia.gov/v2/seriesid"

WTI_SERIES = "PET.RWTC.D"
BRENT_SERIES = "PET.RBRTE.D"


# -----------------------------------------------------------------------------
# HTTP session
# -----------------------------------------------------------------------------

session = requests.Session()

session.headers.update({
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
})


# -----------------------------------------------------------------------------
# Prometheus metrics
# -----------------------------------------------------------------------------

heating_oil_ma = Gauge(
    "heating_oil_ma_residential_dollars_per_gallon",
    "Latest EIA Massachusetts residential No. 2 heating oil price",
)

wti_price = Gauge(
    "crude_oil_wti_dollars_per_barrel",
    "Latest EIA WTI Cushing crude oil spot price",
)

brent_price = Gauge(
    "crude_oil_brent_dollars_per_barrel",
    "Latest EIA Brent Europe crude oil spot price",
)

oil_estimated_fill_cost = Gauge(
    "heating_oil_estimated_fill_cost_dollars",
    "Estimated heating-oil fill cost based on latest Massachusetts price",
    ["gallons"],
)

exporter_last_refresh = Gauge(
    "oil_exporter_last_refresh_unixtime",
    "Unix timestamp of the most recent refresh attempt",
)

exporter_last_success = Gauge(
    "oil_exporter_last_success_unixtime",
    "Unix timestamp of the most recent completely successful refresh",
)

exporter_errors = Gauge(
    "oil_exporter_errors",
    "Number of errors encountered during the most recent refresh",
)

oil_data_info = Info(
    "heating_oil_data",
    "Metadata describing the latest EIA data",
)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def log_http_error(
    name: str,
    response: requests.Response,
) -> None:
    """
    Log useful EIA error information without exposing the API key.
    """

    safe_url = response.url

    if EIA_API_KEY:
        safe_url = safe_url.replace(EIA_API_KEY, "REDACTED")

    logging.error(
        "%s request failed: HTTP %s URL=%s response=%s",
        name,
        response.status_code,
        safe_url,
        response.text[:1000],
    )


def parse_float(value) -> Optional[float]:
    """
    Convert an EIA value to float if possible.
    """

    if value in (None, "", "NA", "--"):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


# -----------------------------------------------------------------------------
# Massachusetts heating oil
# -----------------------------------------------------------------------------

def get_ma_heating_oil() -> Tuple[float, str]:
    """
    Retrieve the latest Massachusetts residential heating-oil price.

    Returns:
        (price, period)
    """

    params = {
        "api_key": EIA_API_KEY,
        "frequency": "weekly",
        "data[0]": "value",
        "facets[series][]": MA_HEATING_OIL_SERIES,
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "length": 10,
    }

    response = session.get(
        EIA_HEATING_OIL_URL,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )

    if not response.ok:
        log_http_error(
            "Massachusetts heating oil",
            response,
        )

    response.raise_for_status()

    payload = response.json()

    rows = payload.get(
        "response",
        {},
    ).get(
        "data",
        [],
    )

    if not rows:
        raise RuntimeError(
            "EIA returned no Massachusetts heating-oil data"
        )

    for row in rows:

        value = parse_float(
            row.get("value")
        )

        if value is None:
            continue

        period = str(
            row.get(
                "period",
                "unknown",
            )
        )

        return value, period

    raise RuntimeError(
        "EIA returned Massachusetts heating-oil rows "
        "but none contained a numeric value"
    )


# -----------------------------------------------------------------------------
# WTI / Brent
# -----------------------------------------------------------------------------

def get_eia_series(
    series_id: str,
) -> Tuple[float, str]:
    """
    Retrieve latest value from an EIA API v2 legacy-series endpoint.

    Example:
        PET.RWTC.D
        PET.RBRTE.D
    """

    url = f"{EIA_SERIES_URL}/{series_id}"

    params = {
        "api_key": EIA_API_KEY,
        "length": 10,
    }

    response = session.get(
        url,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )

    if not response.ok:
        log_http_error(
            series_id,
            response,
        )

    response.raise_for_status()

    payload = response.json()

    rows = payload.get(
        "response",
        {},
    ).get(
        "data",
        [],
    )

    if not rows:
        raise RuntimeError(
            f"EIA returned no data for {series_id}"
        )

    #
    # Usually EIA returns newest first here, but do not
    # blindly assume that.
    #
    valid_rows = []

    for row in rows:

        value = parse_float(
            row.get("value")
        )

        if value is None:
            continue

        period = str(
            row.get(
                "period",
                "",
            )
        )

        valid_rows.append(
            (
                period,
                value,
            )
        )

    if not valid_rows:
        raise RuntimeError(
            f"EIA returned rows for {series_id} "
            "but no numeric values"
        )

    #
    # ISO date periods sort correctly as strings.
    #
    valid_rows.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    period, value = valid_rows[0]

    return value, period


# -----------------------------------------------------------------------------
# Refresh metrics
# -----------------------------------------------------------------------------

def refresh_metrics() -> None:

    logging.info(
        "Refreshing oil-price metrics"
    )

    exporter_last_refresh.set_to_current_time()

    errors = 0

    metadata = {}


    # -------------------------------------------------------------------------
    # Massachusetts heating oil
    # -------------------------------------------------------------------------

    try:

        price, period = get_ma_heating_oil()

        heating_oil_ma.set(
            price
        )

        metadata[
            "ma_heating_oil_period"
        ] = period

        logging.info(
            "Massachusetts heating oil: $%.3f/gal period=%s",
            price,
            period,
        )

        #
        # Estimated fill prices for Grafana
        #
        for gallons in (
            100,
            150,
            200,
            225,
            250,
        ):

            oil_estimated_fill_cost.labels(
                gallons=str(gallons)
            ).set(
                price * gallons
            )

    except Exception:

        errors += 1

        logging.exception(
            "Unable to retrieve Massachusetts heating-oil price"
        )


    # -------------------------------------------------------------------------
    # WTI
    # -------------------------------------------------------------------------

    try:

        price, period = get_eia_series(
            WTI_SERIES
        )

        wti_price.set(
            price
        )

        metadata[
            "wti_period"
        ] = period

        logging.info(
            "WTI: $%.2f/barrel period=%s",
            price,
            period,
        )

    except Exception:

        errors += 1

        logging.exception(
            "Unable to retrieve WTI price"
        )


    # -------------------------------------------------------------------------
    # Brent
    # -------------------------------------------------------------------------

    try:

        price, period = get_eia_series(
            BRENT_SERIES
        )

        brent_price.set(
            price
        )

        metadata[
            "brent_period"
        ] = period

        logging.info(
            "Brent: $%.2f/barrel period=%s",
            price,
            period,
        )

    except Exception:

        errors += 1

        logging.exception(
            "Unable to retrieve Brent price"
        )


    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    metadata[
        "source"
    ] = "eia"

    oil_data_info.info(
        metadata
    )

    exporter_errors.set(
        errors
    )

    if errors == 0:

        exporter_last_success.set_to_current_time()

        logging.info(
            "Refresh completed successfully"
        )

    else:

        logging.warning(
            "Refresh completed with %d error(s)",
            errors,
        )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> None:

    logging.basicConfig(
        level=os.getenv(
            "LOG_LEVEL",
            "INFO",
        ),
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(message)s"
        ),
    )

    logging.info(
        "Starting heating-oil Prometheus exporter"
    )

    logging.info(
        "Metrics endpoint: http://0.0.0.0:%d/metrics",
        LISTEN_PORT,
    )

    logging.info(
        "Refresh interval: %d seconds",
        REFRESH_SECONDS,
    )

    start_http_server(
        LISTEN_PORT
    )

    #
    # Fetch immediately at startup.
    #
    refresh_metrics()

    while True:

        time.sleep(
            REFRESH_SECONDS
        )

        try:

            refresh_metrics()

        except Exception:

            logging.exception(
                "Unexpected top-level refresh failure"
            )


if __name__ == "__main__":
    main()
