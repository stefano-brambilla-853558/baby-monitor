import streamlit as st
import pandas as pd
from datetime import datetime
from src.utils import read_blob, write_blob, add_row_blob
from src.config import data_columns, data_files, Keys

mode = Keys.DIAPERS


# Bottone per aggiungere una nuova riga
if st.button("Aggiungi una nuova riga"):
    
    row =  {
        "Timestamp": datetime.now(),
        "Content": "Pannolino",
        "Note": "",
        "Metadata": ""
    },
    add_row_blob(mode, row)
    st.success("Nuova riga aggiunta!")

# Mostra il contenuto del file CSV
st.subheader("Contenuto del file CSV:")
df = read_blob(mode)
df = st.data_editor(df)
write_blob(mode, df)