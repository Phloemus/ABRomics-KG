# ABRomics-KG

**ABRomics-KG** is a knowledge graph that allows to store antibiotic resistance data by using the sosa ontology 
and other domain specific ontologies such as **ARO** (Antibiotic Resistance Ontology).

## Content

In this repo, you will find [rdf data](https://github.com/Phloemus/ABRomics-KG/tree/main/rdf) and [queries](https://github.com/Phloemus/ABRomics-KG/tree/main/queries) used for the article named *"A multi-modal and temporal antibiotic resistance knowledge graph"* submitted to the **SWAT4HCLS** conference (2025 edition).

<p float="left">
    <img src="https://raw.githubusercontent.com/Phloemus/ABRomics-KG/main/assets/cq1.png" alt="cq1" width="49%" align="top" />
    <img src="https://raw.githubusercontent.com/Phloemus/ABRomics-KG/main/assets/cq2.png" alt="cq2" width="49%" align="top"/>
</p>

## Launch the demo locally

Along side the rdf graph and queries, you can also explore this graph locally all by yourself !

```
bash
## Clone the ABRomics-KG repository
git clone https://github.com/Phloemus/ABRomics-KG
cd ABRomics-KG
```

### Using docker

The whole demo can simply deployed locally using a single script. For the script to work you need to have docker and docker compose installed on your computer.

```
bash
chmod +x start.sh
./start.sh
```

The demo is now disponible locally at [http://localhost:8501](http://localhost:8501)

### Without docker

It's also possible deploy the demo manually instead of using docker. In this case, two services will need to be deployed manually : the fuseki graph server which holds the 
knowledge graph data and the web demo which allows to perform requests on the knoweldge graph. 

#### Installing the knowledge graph server associated with the demo

```
bash
## download and install fuseki
wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-5.2.0.tar.gz
tar -xf apache-jena-fuseki-5.2.0.tar.gz
mv apache-jena-fuseki-5.2.0 fuseki

## launch the fuseki server
./fuseki/fuseki-server --file=rdf/samples.ttl --file=rdf/genes.ttl --file=rdf/observations.ttl --file=rdf/platforms.ttl --file=rdf/strains.ttl --file=rdf/observableProperties.ttl --file=rdf/people.ttl --file=rdf/procedures.ttl --file=rdf/sensors.ttl /abromics-kg
```

#### Installing the conda enviornment

Open a new shell and install the conda environment necessary to launch the web demo

```
bash
## Create a venv environment
cd src
python -m venv ./venv
source venv/bin/activate
```

```
bash
## Create a conda environment
cd src
conda create --name abromics-kg
conda activate abromics-kg
```

#### Installing the required packages for the demo

```
bash
## Install the required packages
pip install streamlit
pip install rdflib
```

#### Launching the demo

```
bash
## Launch the streamlit app
cd src
streamlit run app.py
```

The demo is now disponible locally at [http://localhost:8501](http://localhost:8501)

## Explore the data

Within the demo, you can execute the pre-written queries and even perform you own queries on the knowledge
graph although we encourage you to get familiar with the knowledge graph before performing your own sparql
queries. 

> To understand the structure of the graph, go read the reference paper submitted to the SWAT4HCLS conference !

## Contacts

If you have any question about this work, feel free to open a discussion on github or contacting us directly 
(brieuc.quemeneur@univ-nantes.fr)
