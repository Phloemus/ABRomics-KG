import streamlit as st

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

