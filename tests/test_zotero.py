"""
File: test_zotero.py
Project: zotero-to-grist
File Created: 2026/10/07 12:02:12
Author: Marceau Tonelli (marceau.tonelli@cerema.fr)
"""

import os

from zotero2grist import zotero

ZOTERO_API_KEY = os.environ.get("ZOTERO_API_KEY")
ZOTERO_GROUP_ID = os.environ.get("ZOTERO_GROUP_ID")


def test_zotero_connection() -> int:
    """
    Tests Zotero API connection with values found in environment variables
    """
    assert ZOTERO_API_KEY, "ZOTERO_API_KEY not found in environment variables"
    assert ZOTERO_GROUP_ID, "ZOTERO_GROUP_ID not found in environment variables"

    collections = zotero._get_yearly_top_level_collections(
        api_key=ZOTERO_API_KEY,
        group_id=ZOTERO_GROUP_ID,
    )
    assert len(collections) > 0
