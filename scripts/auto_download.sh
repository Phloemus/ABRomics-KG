###### Auto download ######
#
# Download all the reports and all the ontologies
# Also convert the raw reports to rdf files
#

## Create the environment
python -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt

## Launching the setup scripts
python download_reports.py
python download_ontologies.py
python create_rdf_graph.py
