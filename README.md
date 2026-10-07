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


### Format

The output columns are the following:

| Column name           | Description |
| --------------------- | ----------- |
| Annee                 | Year (4 digits) |
| Type_de_publication   | Publication type abbreviated |
| Nombre_items          | Total number of publications in this type for this year |
| Nombre_Cerema         | Number of publications with the "Cerema" tag |
| Nombre_Uni_Eiffel     | Number of publications with the "Uni Eiffel" tag |
| Zotero_Key            | Zotero key for this sub collection |

Currently editing the formatting of the columns is not possible other than modifying the source code.


## Github actions setup

The Github action workflow in `.github/workflows/` is configured to run this script on **every Monday morning at 06:00 UTC**. API keys and other credentials are passed via [Github secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets).

The value of each parameter must be stored in a secret corresponding to its name in uppercase letters. For instance `--zotero-api-key` value should be stored in the `ZOTERO_API_KEY` secret.
