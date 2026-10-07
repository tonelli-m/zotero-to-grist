"""
File: main.py
Project: zotero-to-grist
File Created: 2026/10/06 13:54:39
Author: Marceau Tonelli (marceau.tonelli@cerema.fr)
"""

import argparse
import sys

from zotero2grist import LOG, grist, zotero


def parse_args() -> argparse.Namespace:
    """
    Setsup arguments parser and parse arguments.

    Args:
        argv (list[str]): Input arguments (see --help output for details).

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    # Setup parser
    parser = argparse.ArgumentParser(
        description="""
        Fetch data from Zotero collections and updates a Grist table with the results
        """
    )
    parser.add_argument(
        "--zotero-api-key",
        help="Zotero API key.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--zotero-group-id",
        help="Zotero group identifier.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--grist-api-key",
        help="Grist API key.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--grist-doc-id",
        help="Grist document identifier.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--grist-table-id",
        help="Girst table identifier in the document.",
        required=True,
        type=str,
    )

    # Parse arguments
    args = parser.parse_args()
    return args


def main() -> int:
    """
    Script entry point.

    Returns:
        int: Exit code (0 if success, 1 if error)
    """
    # Parse input arguments
    args = parse_args()

    LOG.info("Parsing publications data for Zotero group %s", args.zotero_group_id)
    grist_input_data = zotero.parse_publications(
        api_key=args.zotero_api_key,
        group_id=args.zotero_group_id,
    )
    if len(grist_input_data) == 0:
        LOG.error("No publications data found. Check logs for details.")
        return 1

    return grist.update_table(
        api_key=args.grist_api_key,
        doc_id=args.grist_doc_id,
        table_id=args.grist_table_id,
        input_data=grist_input_data,
    )


if __name__ == "__main__":
    sys.exit(main())
