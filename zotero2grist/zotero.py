"""
File: zotero.py
Project: zotero-to-grist
File Created: 2026/10/06 13:55:28
Author: Marceau Tonelli (marceau.tonelli@cerema.fr)
"""

import requests

from zotero2grist import LOG

ZOTERO_BASE_URL = "https://api.zotero.org"


def _get_yearly_top_level_collections(api_key: str, group_id: str) -> list[dict]:
    """
    Fetches top level collections that starts with "Année"

    Args:
        api_key (str): Zotero API key
        group_id (str): Zotero group identifier

    Returns:
        list: Top level collections with "key" and "name" attributes
    """
    url = f"{ZOTERO_BASE_URL}/groups/{group_id}/collections/top"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(url, headers=headers, timeout=60)

    if response.status_code != 200:
        LOG.error(
            "Error while fetching top level collections: %d, %s",
            response.status_code,
            response.text,
        )
        return []

    try:
        response_data = response.json()
    except ValueError as err:
        LOG.error(err)
        return []

    return [
        collection["data"]
        for collection in response_data
        if collection["data"]["name"].startswith("Année ")
    ]


def _get_sub_collections(
    api_key: str,
    group_id: str,
    collection_key: str,
) -> list[dict]:
    """
    Lists all sub-collections for a given collection key.

    Args:
        api_key (str): Zotero API key
        group_id (str): Zotero group identifier
        collection_key (str): Collection identifier

    Returns:
        list[dict]: Sub-collections with "name" and "key" attributes.
    """
    url = (
        f"{ZOTERO_BASE_URL}/groups/{group_id}/collections/{collection_key}/collections"
    )
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(url, headers=headers, timeout=60)

    if response.status_code != 200:
        LOG.error(
            "Error while fetching sub-collections: %d, %s",
            response.status_code,
            response.text,
        )
        return []

    try:
        response_data = response.json()
    except ValueError as err:
        LOG.error(err)
        return []

    result = []
    for subcollection in response_data:
        result.append(subcollection["data"])
        # If sub collection contains sub collections, add them to the list recursively
        if int(subcollection["meta"]["numCollections"]) > 0:
            result.extend(
                _get_sub_collections(api_key, group_id, subcollection["data"]["key"])
            )

    return result


def _get_collection_items(
    api_key: str,
    group_id: str,
    collection_key: str,
    start: int = 0,
    limit: int = 25,
) -> list[dict]:
    """
    Lists items in given a collection.

    Args:
        api_key (str): Zotero API key
        group_id (str): Zotero group identifier
        collection_key (str): Collection identifier

    Returns:
        list[dict]: Items found in collection
    """
    url = f"{ZOTERO_BASE_URL}/groups/{group_id}/collections/{collection_key}/items"
    headers = {
        "Zotero-API-Version": "3",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(
        url,
        headers=headers,
        timeout=60,
        params={"start": start, "limit": limit},
    )

    if response.status_code != 200:
        LOG.error(
            "Error while fetching collection items: %d, %s",
            response.status_code,
            response.text,
        )
        return []

    try:
        response_data = response.json()
    except ValueError as err:
        LOG.error(err)
        return []

    result = [item["data"] for item in response_data if len(item["data"]["tags"]) > 0]
    # If a link to the next page is present, append following items recursively
    if response.links.get("next"):
        result.extend(
            _get_collection_items(
                api_key, group_id, collection_key, start + limit, limit
            )
        )

    return result


def parse_publications(
    api_key: str,
    group_id: str,
) -> list[dict]:
    """
    Takes yearly top level collections as input, and for each collections extracts
    the following information:
        - Annee (str): Year as 4 digit number
        - Type_de_publication (str): Publication type abbreviated
        - Nombre_items (int): Total number of publications
        - Nombre_Cerema (int): Number of Cerema publications
        - Nombre_Uni_Eiffel (int): Number of UGE publications
        - Zotero_key (str): Zotero sub-collection key

    Each yearly collection contains a sub collection for each publication type.

    Args:
        api_key (str): Zotero API key
        group_id (str): Zotero group identifier

    Returns:
        list[dict]: Parsed data formatted for grist as a list of dict. Each element in the list
                    corresponds to one row, each key in the dict to one column.
    """
    result = []
    collections = _get_yearly_top_level_collections(api_key, group_id)
    if len(collections) == 0:
        LOG.error("No collection found. Check logs for details.")
        return []
    LOG.info("Found %d yearly collections.", len(collections))

    # FOR TESTING PURPOSE
    collections = [collections[1]]

    for index, collection in enumerate(collections):
        year = int(str(collection["name"]).removeprefix("Année "))

        print("\n\n")
        LOG.info("%d / %d", index + 1, len(collections))

        LOG.info("Parsing collection %s ...", collection["name"])
        sub_collections = _get_sub_collections(api_key, group_id, collection["key"])
        LOG.info("\tFound %d sub-collections.", len(sub_collections))

        for sub_index, sub_collection in enumerate(sub_collections):
            print()
            LOG.info(
                "\t%d / %d  in  %d / %d",
                sub_index + 1,
                len(sub_collections),
                index + 1,
                len(collections),
            )

            LOG.info("\tParsing sub-collection %s ...", sub_collection["name"])
            items = _get_collection_items(api_key, group_id, sub_collection["key"])
            LOG.info("\tFound %d items.", len(items))

            pub_type = str(sub_collection["name"]).split(" : ", maxsplit=1)[0]
            grist_entry = {
                "Annee": year,
                "Type_de_publication": pub_type,
                "Nombre_items": len(items),
                "Nombre_Cerema": len(
                    [i for i in items if {"tag": "Cerema"} in i["tags"]]
                ),
                "Nombre_Uni_Eiffel": len(
                    [i for i in items if {"tag": "Uni Eiffel"} in i["tags"]]
                ),
                "Zotero_Key": sub_collection["key"],
            }
            LOG.info("\tEntry: %s", grist_entry)
            result.append(grist_entry)

    return result
