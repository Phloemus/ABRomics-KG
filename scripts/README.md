# Setup scripts

Before launching the knowledge graph we need to fetch data from the ABRomics platform, download the ontologies needed for the knowledge graph and to convert the raw data from the ABRomics to a well structured graph in **rdf** format

>[Note]
>These scripts download and format the data used for the demo of this project. You have to run them *BEFORE* launching the knowledge graph

Representing multi-modal data using the *SOSA* ontology can be applied to any project involving entities being observed and multiple characteristic of that entity being measured. 
But for a demonstration purposes, the scripts in this directory will only download the public analysis reports of the [ABRomics plateform](https://abromics.fr) and perform the **rdf** conversion on these reports alone.

## Fast setup 

We encourage you to perform the downloading process by executing the scripts one by one to understand what you are downloading and how the 
conversion process to rdf works. But if you just want a fast way of installing everything just run: 

```
bash
chmod +x auto_setup.sh
./auto_setup.sh
```

Afterwards, you are ready to launch the knowledge graph (see the [main readme file](https://github.com/Phloemus/ABRomics-KG/blob/main/README.md) for more info)

## Manual downloading 

To download the data manually using the *setup scripts* you first need to install the python environment. 
The main packages installed in this environments are : 

- time (to make the loading bar)
- alive_progress (to make the loading bar)
- requests (used to perform http requests)
- getpass4 (to allow the user to write the password of his ABRomics account safely)

- json (for reading/writting cache files)
- uuid (to generate a unique identifier for every node in the graph)
- datetime (to perform date conversion)
- jinja2 (used to create a large rdf file using a smaller jinja template)
- sparql-wrapper (used to perform SPARQL queries on already existant SPARQL endpoint)
- dotenv (for reading data provided by .env file. Mainly used to indicate where are the jinja template files used to create the knowledge graph)

To get the full list of packages, you can check the **requirements.txt*

### Creating the environment

```
bash
python -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt
```

### Downloading the ABRomics public reports

```
bash
python download_reports.py
```

### Downloading the ontologies

```
bash
python download_ontologies.sh
```

### Creating the rdf files

```
bash
python create_rdf_graph.py
```

Afterwards, you are ready to launch the knowledge graph (see the [main readme file](https://github.com/Phloemus/ABRomics-KG/blob/main/README.md) for more info)
