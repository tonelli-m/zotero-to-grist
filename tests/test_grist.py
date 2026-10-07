"""
File: test_grist.py
Project: zotero-to-grist
File Created: 2026/10/07 12:02:12
Author: Marceau Tonelli (marceau.tonelli@cerema.fr)
"""

import os

from zotero2grist import grist

GRIST_API_KEY = os.environ.get("GRIST_API_KEY")
GRIST_DOC_ID = os.environ.get("GRIST_DOC_ID")
GRIST_TABLE_ID = os.environ.get("GRIST_TABLE_ID")


def test_grist_connection() -> int:
    """
    Tests Grist table API connection
    """
    assert GRIST_API_KEY, "GRIST_API_KEY not found in environment variables"
    assert GRIST_DOC_ID, "GRIST_DOC_ID not found in environment variables"
    assert GRIST_TABLE_ID, "GRIST_TABLE_ID not found in environment variables"

    records = grist._fetch_existing_records(
        api_key=GRIST_API_KEY,
        doc_id=GRIST_DOC_ID,
        table_id=GRIST_TABLE_ID,
    )
    assert records is not None or len(records) == 0
