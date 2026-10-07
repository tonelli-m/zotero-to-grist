# Zotero2Grist

Sync UMRAE Zotero collections with a Grist table.


## Installation

To use locally, clone this repository, setup a virtual environment, and install dependencies.

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


### API keys Setup

You will need to setup (or have access to) API keys in order to run this script.

**Zotero API Key**: Go to your [profile security settings](https://www.zotero.org/settings/security), then scroll down to the *Applications* section. Click `Create new private key`, and check *Allow library access* and *Read Only* as default group permission.

**Grist API Key**: Go to your [profile developer settings](https://grist.numerique.gouv.fr/o/docs/account/developer). Under *API Key*, click the `Create` button.


## Usage

The script is usable with command line interface like so:

```sh
python -m zotero2grist \
    --zotero-api-key="your_key_here" \  # see section above for details 
    --zotero-group-id="group_id_here" \  # https://www.zotero.org/groups/[THIS_PART]/group_name
    --grist-api-key="your_key_here" \ # see section above for details
    --grist-doc-id="doc_id" \ # can be found in the document's settings page
    --grist-table-id="table_id" # can be found in the Raw data page of the Grist document
```
