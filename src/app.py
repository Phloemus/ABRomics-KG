import streamlit as st
import rdflib
import json
import os
import datetime
import time
import pandas as pd
from pandas import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON, POST


#### Page configuration
st.set_page_config(
    page_title="ABRomics-KG", layout="centered", initial_sidebar_state="collapsed"
)

#### Utils
def readJsonFromFile(path):
    with open(path) as f:
        d = json.load(f)
        return d

#### Constants #########################################################################################################
# sparql = SPARQLWrapper("http://fuseki:3030/abromics-kg") 
sparql = SPARQLWrapper("http://localhost:8030/abromics-kg") 
sparql.setReturnFormat(JSON)

countries = readJsonFromFile("data/countries.json")


#### States ############################################################################################################

if "is_exec_countqry" not in st.session_state:
    st.session_state.is_exec_countqry = False

if "df_res_countqry" not in st.session_state:
    st.session_state.df_res_countqry = ""

if "is_exec_qry1" not in st.session_state:
    st.session_state.is_exec_qry1 = False

if "df_res_qry1" not in st.session_state:
    st.session_state.df_res_qry1 = ""

if "country" not in st.session_state:
    st.session_state.country = "France"

if "is_exec_qry2" not in st.session_state:
    st.session_state.is_exec_qry2 = False

if "startTime" not in st.session_state:
    st.session_state.startTime = datetime.date(2010, 7, 6)

if "endTime" not in st.session_state:
    st.session_state.endTime = datetime.date(2019, 7, 6)

if "df_res_qry2" not in st.session_state:
    st.session_state.df_res_qry2 = ""

if "is_exec_customqry" not in st.session_state:
    st.session_state.is_exec_customqry = False

if "df_res_customqry" not in st.session_state:
    st.session_state.df_res_customqry = ""


if "is_exec_wikidatahealthqry" not in st.session_state:
    st.session_state.is_exec_wikidatahealthqry = False

if "df_res_wikidatahealthqry" not in st.session_state:
    st.session_state.df_res_wikidatahealthqry = ""


#### Queries ###########################################################################################################

countquery = f"""SELECT (COUNT(*) AS ?tripleCount)
WHERE {{
    ?subject ?predicate ?object.
}}
"""

wikidataHealthQuery = f"""
    SELECT (COUNT(*) AS ?ping) 
    WHERE {{
        SERVICE <https://query.wikidata.org/sparql> {{
            ?s ?p ?o.
        }} 
    }} 
"""

query1 = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX sio: <http://semanticscience.org/resource/>
    PREFIX go: <http://purl.org/obo/owl/GO#>
    PREFIX schema: <https://schema.org/>
    PREFIX abromics: <https://abromics.fr/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    
    # CQ1: What are the most represented antibiotic resistance genes in a specific geographical region of interest ?
    
    SELECT ?sample_id ?gene_name ?location_name (COUNT(?gene_name) as ?count) WHERE {{
        ?sample rdf:type sio:001050 ;
            schema:identifier ?sample_id ;
            prov:atLocation ?location .
    
        ?obs_prop rdf:type sosa:ObservableProperty ;
            rdfs:label "Resistance gene" . 
    
        ?observations sosa:hasObservableProperty ?obs_prop ;
            sosa:hasFeatureOfInterest ?gene ;
            sosa:hasFeatureOfInterest ?sample .
    
        ?gene rdf:type go:Gene ;
            rdfs:label ?gene_name .
    
        # fetch the id corresponding to the targeted location
        SERVICE <https://query.wikidata.org/sparql> {{
            ?location wdt:P31 wd:Q6256 .
            ?location rdfs:label ?location_name .
            FILTER(?location_name = "{st.session_state.country}"@en)
       }}
    }}
    GROUP BY ?sample_id ?gene_name ?location_name
    ORDER BY DESC(?count)
"""

query2 = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX sio: <http://semanticscience.org/resource/>
    PREFIX go: <http://purl.org/obo/owl/GO#>
    PREFIX schema: <https://schema.org/>
    PREFIX abromics: <https://abromics.fr/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    # What are actively circulating ABR genes, given a specific time-frame
    
    SELECT ?gene_name (COUNT(DISTINCT ?res) as ?total_nb_occurences) WHERE {{
        ?sample rdf:type sio:001050 ;
             prov:generatedAtTime ?collectedDate .
        FILTER (?collectedDate > "{st.session_state.startTime}T00:00:00Z"^^xsd:dateTime && 
           ?collectedDate < "{st.session_state.endTime}T00:00:00Z"^^xsd:dateTime)
    
       ?observations sosa:hasObservableProperty ?obs_prop ;
             sosa:hasFeatureOfInterest ?gene ;
             sosa:hasFeatureOfInterest ?sample ;
             sosa:hasSimpleResult ?res .
    
       ?obs_prop rdf:type sosa:ObservableProperty ;
             rdfs:label "Resistance gene" .
    
       ?gene rdf:type go:Gene ;
             rdfs:label ?gene_name .
    }} 
    GROUP BY ?gene_name ?res
    ORDER BY DESC(?total_nb_occurences)
"""


#### States modifier function ##########################################################################################
def exec_count_qry():
    sparql.setQuery(countquery)
    try:
        res = sparql.query().convert()
        recs = res["results"]["bindings"]
        st.session_state.df_res_countqry = json_normalize(recs)
    except Exception as e:
        print(e)
    st.session_state.is_exec_countqry = not st.session_state.is_exec_countqry

def exec_qry1():
    sparql.setQuery(query1)
    try:
        res = sparql.query().convert()
        recs = res["results"]["bindings"]
        st.session_state.df_res_qry1 = json_normalize(recs)
    except Exception as e:
        print(e)
    st.session_state.is_exec_qry1 = not st.session_state.is_exec_qry1

def exec_qry2():
    sparql.setQuery(query2)
    try:
        res = sparql.query().convert()
        recs = res["results"]["bindings"]
        st.session_state.df_res_qry2 = json_normalize(recs)
    except Exception as e:
        print(e)
    st.session_state.is_exec_qry2 = not st.session_state.is_exec_qry2

def exec_customqry():
    sparql.setQuery(customquery)
    try:
        res = sparql.query().convert()
        recs = res["results"]["bindings"]
        st.session_state.df_res_customqry = json_normalize(recs)
    except Exception as e:
        print(e)
    st.session_state.is_exec_customqry = not st.session_state.is_exec_customqry

## impossible to perform a federeated query with rdflib
def exec_wikidatahealthqry():
    sparql.setQuery(wikidataHealthQuery)
    try:
        res = sparql.query().convert()
        recs = res["results"]["bindings"]
        st.session_state.df_res_wikidatahealthqry = json_normalize(recs)
    except Exception as e:
        print(e)
    st.session_state.is_exec_wikidatahealthqry = not st.session_state.is_exec_wikidatahealthqry


#### Sidebar ###########################################################################################################
with st.sidebar:
    st.title("Status of the remote SPARQL endpoint")
    with st.spinner("Wait for it..."):
        time.sleep(2)
    st.success("Query performed correctly !")
    print(st.session_state.df_res_wikidatahealthqry) ## do not give the expected result


#### Rendered Content ##################################################################################################
st.info(
    "Check the [reference article]() and the [documentation](https://github.com/Phloemus/ABRomics-KG) of the project"
)

st.title("A multi-modal and temporal antibiotic resistance knowledge graph")

st.markdown(
    """Understanding how antibiotic resistance genes spread is essential for protecting human, animal, and
environmental health. It requires collaboration across multiple fields and expertise under One Health
initiatives, emphasizing the pressing need to consolidate diverse antibiotic data from human, animal, and
environmental samples. In this paper, we propose a domain-specific Knowledge Graph leveraging the
SOSA ontology to uniformly represent multi-modal data and their analysis while allowing the description
of provenance metadata covering both time and geographical locations. This work is driven by a national
consortium of antibiotic resistance experts (ABRomics). As experimental results, we show how this
domain knowledge can be used to answer a specific expert question as well as increasing the FAIRness
of antibiotic resistance data."""
)

st.subheader("Summary")
st.markdown(
    """
    1. Knowledge graph structure
    2. Execute demo queries
    3. Perform custom queries
"""
)

st.markdown("")

st.header("1. Knowedge graph structure")


st.header("2. Execute demo queries")

st.markdown(
    f"""The SPARQL request corresponding to the competency question of the reference paper can be executed
                below on you the local graph containing the data. SPARQL requests corresponding to other competency 
                questions can also be performed in the graph by using this demo."""
)

### Count query #######################################################################################################

st.subheader("Exploration request")

st.markdown(f"Count the number of nodes in the local knowledge graph")

st.button(
    "Execute query",
    on_click=exec_count_qry,
    key=0,
    type="primary",
    disabled=False,
    use_container_width=False,
)

qryTab1, qryTab2 = st.tabs(["Sparql query", "Result table"])

with qryTab1:
    st.markdown(
        f"This SPARQL query allows to get the number of nodes present in the graph"
    )
    st.code(countquery, language="sparql", line_numbers=False)

with qryTab2:
    if st.session_state.is_exec_countqry:
        with st.spinner("Wait for it..."):
            time.sleep(2)
        st.success("Query performed correctly !")
        print(st.session_state.df_res_countqry)
        st.table(st.session_state.df_res_countqry)
    else:
        st.markdown("Execute the request to see the results !")


### Query 1 ############################################################################################################

st.subheader(
    "CQ1: What are the most represented antibiotic resistance genes in a specific geographical region of interest ?"
)

st.markdown(f"Find the gene names present in a specific geographical region")

st.selectbox(
    "Indicate the counrty you want to search resistances genes",
    countries,
    key="country",
)  # the key is auto-mapped to the st.session_state.key by streamlit
st.button(
    "Execute query",
    on_click=exec_qry1,
    key=1,
    type="primary",
    disabled=False,
    use_container_width=False,
)

qryTab1, qryTab2 = st.tabs(["Sparql query", "Result table"])

with qryTab1:
    st.markdown(
        f"This SPARQL query allows to get all the antibiotic resistance genes found in sample collected in {st.session_state.country}"
    )
    st.code(query1, language="sparql", line_numbers=False)

with qryTab2:
    if st.session_state.is_exec_qry1:
        with st.spinner("Wait for it..."):
            time.sleep(2)
        st.success("Query performed correctly !")
        print(st.session_state.df_res_qry1)
        st.table(st.session_state.df_res_qry1)
    else:
        st.markdown("Execute the request to see the results !")

### Query 2 ############################################################################################################

st.subheader(
    "CQ2: What are actively circulating ABR genes, given a specific time-frame and at least two different sample types"
)

st.markdown(f"Find the actively circulating resistance genes in a specific time-frame")

col1, col2 = st.columns(2)

with col1:
    start = st.date_input("Timeframe start", key="startTime")

with col2:
    end = st.date_input("Timeframe end", key="endTime")

st.write("Samples from ", start, " to ", end)

st.button(
    "Execute query",
    on_click=exec_qry2,
    key=2,
    type="primary",
    disabled=False,
    use_container_width=False,
)

qryTab1, qryTab2 = st.tabs(["Sparql query", "Result table"])

with qryTab1:
    st.write(
        f"This SPARQL query allows to get the resistance genes found in samples collected between the ",
        st.session_state.startTime,
        " and the ",
        st.session_state.endTime,
    )
    st.code(query2, language="sparql", line_numbers=False)

with qryTab2:
    if st.session_state.is_exec_qry2:
        with st.spinner("Wait for it..."):
            time.sleep(2)
        st.success("Query performed correctly !")
        print(st.session_state.df_res_qry2)
        st.table(st.session_state.df_res_qry2)
    else:
        st.markdown("Execute the request to see the results !")

st.header("3. Perform custom queries")

qryTab1, qryTab2 = st.tabs(["Custom SPARQL query", "Query preview"])

with qryTab1:
    customquery = st.text_area("Edit you SPARQL query", value=countquery, height=400)

with qryTab2:
    st.markdown("Preview of your custom SPARQL query")
    st.code(customquery, language="sparql", line_numbers=False)

st.button(
    "Execute query",
    on_click=exec_customqry,
    key=3,
    type="primary",
    disabled=False,
    use_container_width=False,
)

if st.session_state.is_exec_customqry:
    with st.spinner("Wait for it..."):
        time.sleep(2)
    st.success("Query performed correctly !")
    print(st.session_state.df_res_customqry)
    st.table(st.session_state.df_res_customqry)
