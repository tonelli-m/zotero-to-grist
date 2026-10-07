"""
File: __init__.py
Project: zotero-to-grist
File Created: 2026/10/06 13:52:42
Author: Marceau Tonelli (marceau.tonelli@cerema.fr)
"""

# Configure logger format and log level
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)

LOG = logging.getLogger()
