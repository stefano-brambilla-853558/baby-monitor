import streamlit as st
import pandas as pd

diapers = st.Page("pages/diapers.py", title="Diapers", icon="💩")
contractions = st.Page("pages/contractions.py", title="Contractions", icon=":material/pregnant_woman:")
cry = st.Page("pages/cry.py", title="Cry", icon=":material/record_voice_over:")

pages = {
    "Log": [diapers, contractions, cry],
    "Analysis": []
}

pg = st.navigation(pages)
st.set_page_config(page_title="Baby Monitor", 
                   page_icon=":material/child_friendly:", 
                   layout="centered")

# Ottimizzazione del layout per i dispositivi mobili
st.markdown(
    """
    <style>
    /* Rendi i componenti più adattabili a schermi piccoli */
    .stButton button {
        width: 100%;
        font-size: 18px;
    }
    .stDataFrame {
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

pg.run()