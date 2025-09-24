import streamlit as st

import os
from rdflib import Graph, URIRef
import networkx as nx
import plotly.graph_objects as go


st.set_page_config(
    page_title="ARBormics-KG Ontologies",
    layout="wide",
    initial_sidebar_state="expanded"
)


#### Sidebar ###########################################################################################################
with st.sidebar:
    st.subheader("Summary")
    st.markdown(
    """
        1. [Generic ontologies](#generic-ontologies)
        2. [Health ontologies](#health-ontologies)
        2. [Environmental ontologies](#environmental-ontologies)
    """
    )


#### Rendered Content ##################################################################################################

st.title("Ontologies documentation")
st.markdown("")

st.header("Generic ontologies")
st.markdown("")

## Rendering the centrality of the ontologies used

def get_namespace(uri):
    if '#' in uri:
        return uri.rsplit('#', 1)[0] + '#'
    elif '_' in uri:
        return uri.rsplit('_', 1)[0] + '_'
    else:
        return uri.rsplit('/', 1)[0] + '/'

def parse_ontology(filepath):
    g = Graph()
    g.parse(filepath, format='xml')
    print(len(g))
    ## Find a way to get all the namespaces defined in the ontologies (incoming or out)
    ## Parse the ontologies in a rdflib graph one by one 
    ## Iterate through all the spo and count the number of times there is a link out and in to which namespace (Degree Centrality in the ref paper)

    ##print(list(g)[:10])
    ##for s, p, o in g: 
    ##    print(s, "n--- ", p, "n------ ", o)
    return g

def get_ontology_iri(g):
    for s in g.subjects(URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                        URIRef("http://www.w3.org/2002/07/owl#Ontology")):
        return str(s)
    return None

def extract_used_namespaces(g):
    used = set()
    for s, p, o in g:
        if isinstance(o, URIRef):
            used.add(get_namespace(str(o)))
    return used

def build_and_display_dependency_graph():
    ontologies = {}
    graphs = {}
    used_namespaces = {}

    # Step 1: Parse all ontologies
    for file in os.listdir("../ontologies/"):
        if not file.endswith('.owl'):
            continue
        path = os.path.join("../ontologies/", file)
        g = parse_ontology(path)
        iri = get_ontology_iri(g)
        if not iri:
            continue
        ns = get_namespace(iri)
        print(ns)
        ontologies[ns] = file
        graphs[ns] = g
        used_namespaces[ns] = extract_used_namespaces(g)

    # Step 2: Build dependency graph
    G = nx.DiGraph()

    for src_ns, used_ns_set in used_namespaces.items():
        for tgt_ns in ontologies:
            if src_ns != tgt_ns and tgt_ns in used_ns_set:
                G.add_edge(ontologies[src_ns], ontologies[tgt_ns])  # file names as nodes
    print(G)

    # Step 3: Display the networkx graph
    '''
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='skyblue',
            size=20,
            line_width=2),
        text=node_text,
        textposition="top center"
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40)))
    st.plotly_chart(fig)
    '''


st.button('Build dependency graph', on_click=build_and_display_dependency_graph)


## Displaying a large list of all the ontologies used in the knowledge graph

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("SOSA")
    st.markdown("Sensor, Observation, Sample, and Actuator")
    st.markdown("https://www.w3.org/TR/vocab-ssn/")
    st.markdown("""
        Primarly used in the domain of sensor networks. The SOSA ontology defines terms such 
        as Observations, Results, ObservableProperties. Coupled with the notion of Procedures, 
        also present in this ontology, SOSA offers a great framework to represent multimodal 
        observations made by a bioinformatic worflow. 
    """)

with col2:
    st.subheader("PROV-O")
    st.markdown("Provenance Ontology ")
    st.markdown("https://www.w3.org/TR/prov-o/")
    st.markdown("""
        The Provenance Ontology is a W3C standard ontology that defines many different 
        properties to define the provenance of the data and who produced them. This is
        a very helpful ontology to tag more context on the sample entities.
    """)

with col3:
    st.subheader("SIO")
    st.markdown("Semanticscience Integrated Ontology")
    st.markdown("https://www.ebi.ac.uk/ols4/ontologies/sio")
    st.markdown("""
        The semanticscience integrated ontology (SIO) provides a simple, 
        integrated ontology (types, relations) for objects, processes and their attributes
    """)

with col4:
    st.subheader("")

st.header("Health ontologies")
st.markdown("")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.subheader("ARO")
    st.markdown("Antibiotic Resistance Ontology")
    st.markdown("https://bioportal.bioontology.org/ontologies/ARO")
    st.markdown("""
        The Antibiotic Resistance Ontology describes antibiotic resistance genes and mutations, 
        their products, mechanisms, and associated phenotypes, as well as antibiotics and their 
        molecular targets. It is integrated with the Comprehensive Antibiotic Resistance Database, 
        a curated resource containing high quality reference data on the molecular basis of 
        antimicrobial resistance
    """)

with col6:
    st.subheader("NCIT")
    st.markdown("National Cancer Institute Thesaurus")
    st.markdown("https://bioportal.bioontology.org/ontologies/NCIT")
    st.markdown("""
        Vocabulary for clinical care, translational and basic research, and public information and administrative activities
    """)

with col7:
    st.subheader("NCBITAXON")
    st.markdown("NCBI taxonomy ontology")
    st.markdown("https://www.ncbi.nlm.nih.gov/taxonomy")
    st.markdown("""
        The NCBI taxonomy of species that list all the species existing
    """)

with col8:
    st.subheader("")


st.header("Environmental ontologies")
st.markdown("")

col9, col10, col11, col12 = st.columns(4)

with col9:
    st.subheader("ENVO")
    st.markdown("Environmental Ontology")
    st.markdown("https://bioportal.bioontology.org/ontologies/ENVO")
    st.markdown("""
        EnvO is an OBO Foundry and Library ontology for the concise, controlled description of environmental entities 
        such as ecosystems, environmental processes, and environmental qualities. It closely interoperates with a 
        broad collection of other OBO ontologies and is used in a diverse range of projects. 
    """)

with col10:
    st.subheader("UBERON")
    st.markdown("Uber anatomy ontology")
    st.markdown("https://bioportal.bioontology.org/ontologies/UBERON")
    st.markdown("""
        Uberon is an integrated cross-species anatomy ontology representing a variety of entities classified according 
        to traditional anatomical criteria such as structure, function and developmental lineage. The ontology 
        includes comprehensive relationships to taxon-specific anatomical ontologies, allowing integration of 
        functional, phenotype and expression data.
    """)

with col11:
    st.subheader("")
    st.markdown("")

with col12:
    st.subheader("")

