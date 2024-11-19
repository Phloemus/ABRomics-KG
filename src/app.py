import streamlit as st
import rdflib
import os


#### Page configuration
st.set_page_config(
    page_title="ABRomics-KG",
    layout="centered",
    initial_sidebar_state="collapsed"
)

#### States ############################################################################################################
if 'is_exec_qry1' not in st.session_state:
    st.session_state.is_exec_qry1 = False

if 'country' not in st.session_state:
    st.session_state.country = "France"

if 'df_res_qry1' not in st.session_state:
    st.session_state.df_res_qry1 = ""

if 'is_exec_qry2' not in st.session_state:
    st.session_state.is_exec_qry2 = False

if 'timeframe' not in st.session_state:
    st.session_state.timeframe = "2020-01-01"

if 'df_res_qry2' not in st.session_state:
    st.session_state.df_res_qry2 = ""

#### Queries ###########################################################################################################

query1 = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX sio: <http://semanticscience.org/resource/>
    PREFIX go: <http://purl.org/obo/owl/GO#>
    PREFIX schema: <https://schema.org/>
    PREFIX abromics: <https://abromics.fr/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    
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
            ?location rdfs:label ?location_name .
            FILTER(?location_name = "France" && LANG(?location_name) = "en")
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
    
    # What are actively circulating ABR genes, given a specific time-frame and at least two different sample types
    
    SELECT ?gene_name (COUNT(DISTINCT ?sampleType) as ?nb_sample_types) (GROUP_CONCAT(DISTINCT ?sampleType; separator=", ") AS ?sampleTypes) (COUNT(DISTINCT ?res) as ?total_nb_occurences) WHERE {{
        ?sample rdf:type sio:001050 ;
             abromics:sampleType ?sampleType ; # rework this
             prov:generatedAtTime ?collectedDate .
        FILTER (?collectedDate > "2010-10-23T00:00:00Z"^^xsd:dateTime && 
               ?collectedDate < "2024-10-23T00:00:00Z"^^xsd:dateTime)
    
       ?observations sosa:hasObservableProperty ?obs_prop ;
             sosa:hasFeatureOfInterest ?gene ;
             sosa:hasFeatureOfInterest ?sample ;
             sosa:hasSimpleResult ?res .
           
       ?obs_prop rdf:type sosa:ObservableProperty ;
             rdfs:label "Resistance gene" .
    
       ?gene rdf:type go:Gene ;
             rdfs:label ?gene_name .
    }} 
    GROUP BY ?gene_name ?resValue
    HAVING (COUNT(DISTINCT ?sampleType) > 1)
    ORDER BY DESC(?total_nb_occurences)
"""


#### States modifier function ##########################################################################################
def exec_qry1():
    results = graph.query(query1)
    st.session_state.df_res_qry1 = results
    st.session_state.is_exec_qry1 = not st.session_state.is_exec_qry1

def exec_qry2():
    results = graph.query(query2)
    st.session_state.df_res_qry2 = results
    st.session_state.is_exec_qry2 = not st.session_state.is_exec_qry2


#### Load Graph ########################################################################################################
graph = rdflib.Graph()

rdfDir = "../rdf"

for fileName in os.listdir(rdfDir):
    graph.parse(f"{rdfDir}/{fileName}", format="ttl")


#### Rendered Content ##################################################################################################
st.info("Check the [reference article]() and the [documentation](https://github.com/Phloemus/ABRomics-KG) of the project")

st.title("A multi-modal and temporal antibiotic resistance knowledge graph")

st.markdown("""Understanding how antibiotic resistance genes spread is essential for protecting human, animal, and
environmental health. It requires collaboration across multiple fields and expertise under One Health
initiatives, emphasizing the pressing need to consolidate diverse antibiotic data from human, animal, and
environmental samples. In this paper, we propose a domain-specific Knowledge Graph leveraging the
SOSA ontology to uniformly represent multi-modal data and their analysis while allowing the description
of provenance metadata covering both time and geographical locations. This work is driven by a national
consortium of antibiotic resistance experts (ABRomics). As experimental results, we show how this
domain knowledge can be used to answer a specific expert question as well as increasing the FAIRness
of antibiotic resistance data.""")

st.subheader("Summary")
st.markdown('''
    1. Knowledge graph structure
    2. Execute prewritten queries
    3. Perform custom queries
''')

st.markdown("")

st.header("1. Knowedge graph structure")

st.header("2. Execute prewritten queries")

st.markdown(f"""The SPARQL request corresponding to the competency question of the reference paper can be executed
                below on you the local graph containing the data. SPARQL requests corresponding to other competency 
                questions can also be performed in the graph by using this demo.""")

### Query 1 ############################################################################################################

st.subheader("CQ1: What are the most represented antibiotic resistance genes in a specific geographical region of interest ?")

st.markdown(f"Find the gene names present in a specific geographical region")

st.session_state.country = st.selectbox("Indicate the counrty you want to search resistances genes", (st.session_state.country))
st.button("Execute query", on_click=exec_qry1, key=1, type="primary", disabled=False, use_container_width=False)

qryTab1, qryTab2 = st.tabs(["Sparql query", "Result table"])

with qryTab1:
    st.markdown(f"This SPARQL query allows to get all the antibiotic resistance genes found in sample collected in {st.session_state.country}")
    st.code(query1, language="sparql", line_numbers=False)

with qryTab2:
    if st.session_state.is_exec_qry1:
        with st.spinner('Wait for it...'):
            time.sleep(2)
        st.success('Query performed correctly !')
        print(st.session_state.df_res_qry1)
        st.table(st.session_state.df_res_qry1)
    else:
        st.markdown("Execute the request to see the results !")

### Query 2 ############################################################################################################

st.subheader("CQ2: What are actively circulating ABR genes, given a specific time-frame and at least two different sample types")

st.markdown(f"Find the actively circulating resistance genes in a specific time-frame")

st.session_state.timeframe = st.selectbox("Indicate the time-frame you want to explore", (st.session_state.timeframe))
st.button("Execute query", on_click=exec_qry2, key=2, type="primary", disabled=False, use_container_width=False)

qryTab1, qryTab2 = st.tabs(["Sparql query", "Result table"])

with qryTab1:
    st.markdown(f"This SPARQL query allows to get the resistance genes found between {st.session_state.timeframe} and {st.session_state.timeframe}")
    st.code(query2, language="sparql", line_numbers=False)

with qryTab2:
    if st.session_state.is_exec_qry2:
        with st.spinner('Wait for it...'):
            time.sleep(2)
        st.success('Query performed correctly !')
        print(st.session_state.df_res_qry2)
        st.table(st.session_state.df_res_qry2)
    else:
        st.markdown("Execute the request to see the results !")


st.header("3. Perform custom queries")
