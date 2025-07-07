###### Auto setup ######
#
# Download all the reports and all the ontologies
# Also convert the raw reports to rdf files
#

## Create the environment
python -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt

## Donwload the required documents
python download_reports.py
bash download_ontologies.sh

## Generate the rdf files from the ABRomics reports
python create_rdf_graph.py
