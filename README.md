# ABRomics-KG

**ABRomics-KG** is a knowledge graph that allows to store antibiotic resistance data by using the sosa ontology 
and other domain specific ontologies such as **ARO** (Antibiotic Resistance Ontology).

## Content

In this repo, you will find [rdf data](https://github.com/Phloemus/ABRomics-KG/tree/main/rdf) and [queries](https://github.com/Phloemus/ABRomics-KG/tree/main/queries) used for the article named *"A multi-modal and temporal antibiotic resistance knowledge graph"* submitted to the **SWAT4HCLS** conference (2025 edition).

## Launch the demo

Along side the rdf graph and queries, you can also explore this graph locally all by yourself !

```
bash
## Clone the ABRomics-KG repository
git clone https://github.com/Phloemus/ABRomics-KG
cd ABRomics-KG
```

```
bash
## Create the provided python environment
cd src
python -m venv ./venv
pip install -r requirements.txt
```

```
bash
## Launch the streamlit app
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
