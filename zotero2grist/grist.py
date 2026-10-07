"""
File: grist.py
Project: zotero-to-grist
File Created: 2026/10/06 16:02:03
Author: Marceau Tonelli (marceau.tonelli@cerema.fr)
"""

import requests

from zotero2grist import LOG

GRIST_BASE_URL = "https://grist.numerique.gouv.fr/api"


def _fetch_existing_records(
    api_key: str,
    doc_id: str,
    table_id: str,
) -> list | None:
    """
    Fetches existing records in the given Grist table.

    Args:
        api_key (str): Grist API key
        doc_id (str): Grist document identifier
        table_id (str): Grist document table identifier

    Returns:
        list: Exisiting records
    """
    url = f"{GRIST_BASE_URL}/docs/{doc_id}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=60)

    if response.status_code != 200:
        LOG.error(
            "Error while fetching Grist records: %d, %s",
            response.status_code,
            response.text,
        )
        return None

    try:
        response_data = response.json()
    except ValueError as err:
        LOG.error(err)
        return None

    return response_data["records"]


def _update_grist_records(
    api_key: str,
    doc_id: str,
    table_id: str,
    payload: dict,
) -> list | None:
    """
    Updates existing Grist records with given payload.

    Args:
        api_key (str): Grist API key
        doc_id (str): Grist document identifier
        table_id (str): Grist document table identifier
        payload (dict): Records to update

    Returns:
        int: Status code, 0 for success, 1 for error.
    """
    LOG.info("Updating %d existing records...", len(payload["records"]))

    url = f"{GRIST_BASE_URL}/docs/{doc_id}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.patch(url, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        LOG.error(
            "Error while updating Grist records: %d, %s",
            response.status_code,
            response.text,
        )
        return 1

    LOG.info("Done.")
    return 0


def _create_grist_records(
    api_key: str,
    doc_id: str,
    table_id: str,
    payload: dict,
) -> list | None:
    """
    Creates Grist records from given payload.

    Args:
        api_key (str): Grist API key
        doc_id (str): Grist document identifier
        table_id (str): Grist document table identifier
        payload (dict): Records to create

    Returns:
        int: Status code, 0 for success, 1 for error.
    """
    LOG.info("Creating %d new records...", len(payload["records"]))

    url = f"{GRIST_BASE_URL}/docs/{doc_id}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        LOG.error(
            "Error while updating Grist records: %d, %s",
            response.status_code,
            response.text,
        )
        return 1

    LOG.info("Done.")
    return 0


def update_table(
    api_key: str,
    doc_id: str,
    table_id: str,
    input_data: list[dict],
) -> int:
    """
    Updates the target Grist table with given input data.
    Input data must be a list of dicts, each dict representing a row with column names as keys.

    Existing rows will be updated, missing rows will be created.

    Args:
        api_key (str): Grist API key
        doc_id (str): Grist document identifier
        table_id (str): Grist document table identifier
        input_data (list[dict]): Input data.

    Returns:
        int: Status code, 0 if success, 1 if error.
    """
    existing_records = _fetch_existing_records(api_key, doc_id, table_id)
    if existing_records is None:
        LOG.error("Error while connecting to Grist document. Check logs for details.")
        return 1

    # Map existing records to a dictionary with Zotero key as key
    existing_records = {r["fields"]["Zotero_Key"]: r["id"] for r in existing_records}

    records_to_update = [
        {"fields": r, "id": existing_records[r["Zotero_Key"]]}
        for r in input_data
        if r["Zotero_Key"] in existing_records
    ]
    if len(records_to_update) == 0:
        LOG.warning("0 new records to update.")
    elif _update_grist_records(
        api_key,
        doc_id,
        table_id,
        payload={"records": records_to_update},
    ):
        LOG.error("Error while updating existing records. Check logs for details.")
        return 1

    records_to_create = [
        {"fields": r} for r in input_data if r["Zotero_Key"] not in existing_records
    ]
    if len(records_to_create) == 0:
        LOG.warning("0 new records to create.")
    elif _create_grist_records(
        api_key,
        doc_id,
        table_id,
        payload={"records": records_to_create},
    ):
        LOG.error("Error while creating records. Check logs for details.")
        return 1

    return 0
