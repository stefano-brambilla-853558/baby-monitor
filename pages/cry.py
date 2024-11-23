import streamlit as st
import numpy as np
import os
import random
import string
from pydub import AudioSegment
from pydub.playback import play
import pandas as pd
from datetime import datetime
from src.utils import read_blob, write_blob, add_row_blob, exists_blob, initialize_blob, list_blob_files, delete_blob
from src.config import data_columns, data_files, Keys



mode = Keys.CRY
def generate_name(timestamp, extension=".mp4"):
    """Genera un nome file casuale con estensione specificata."""
    return str(timestamp) + extension

# Interfaccia utente
st.title("Registra i pianti")

# Registra l'audio
audio_bytes = st.audio_input("Premi per registrare l'audio")

if audio_bytes:
    if st.button("### Salva l'audio registrato"):
        # Genera un nome file casuale
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cry/{generate_name(timestamp)}"
        st.write(f"Nome file: {filename}")
        write_blob(mode, audio_bytes, "audio", filename)

        
        row =  {
        "Timestamp": timestamp,
        "Filename": filename,
        "Note": ""
        },
        add_row_blob(mode, row)

with st.expander("Visualizza gli audio"):
    df = read_blob(mode)
    df = st.data_editor(df, num_rows="dynamic")
    write_blob(mode, df)

# Mostra i file salvati
st.write("### Riproduci un file audio salvato")
audio_files = [blob for blob in list_blob_files() if blob.startswith("cry/")]

# Se ci sono file salvati, permetti di scegliere e riprodurre
if audio_files:
    selected_file = st.selectbox("Seleziona un file audio da riprodurre", audio_files)
    
    col1, col2 = st.columns(2)
    # Aggiungi un pulsante per riprodurre il file selezionato
    if st.button("Riproduci Audio"):
        st.audio(read_blob(Keys.CRY, "audio", selected_file), format="audio/mp4")
    # if col2.button("Cancella Audio"):
    #     # Cancella il file selezionato
    #     st.warning("Sei sicuro di voler cancellare il file selezionato?")
    #     if st.button("Conferma"):
    #         st.write(f"Cancellazione di {selected_file}...")
    #         delete_blob(Keys.CRY, selected_file)
else:
    st.warning("Nessun file audio salvato.")
