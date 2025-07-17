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
        2. [health ontologies](#health-ontologies)
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

with col2:
    st.subheader("PROV-O")
    st.markdown("Provenance Ontology ")

with col3:
    st.subheader("SIO")
    st.markdown("Semanticscience Integrated Ontology")

with col4:
    st.subheader("")

st.header("Health ontologies")
st.markdown("")

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.subheader("ARO")
    st.markdown("Antibiotic Resistance Ontology")

with col6:
    st.subheader("")
    st.markdown("")

with col7:
    st.subheader("")
    st.markdown("")

with col8:
    st.subheader("")

