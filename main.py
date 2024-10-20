import streamlit as st
import pandas as pd
import os
from io import StringIO
from azure.storage.blob import BlobServiceClient
from datetime import datetime
from dotenv import load_dotenv  # Per caricare il file .env

# Carica le variabili dal file .env
load_dotenv()

# Ottieni le informazioni di connessione dal file environment
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "baby-monitor" # os.getenv("AZURE_CONTAINER_NAME")
BLOB_NAME = "temp.csv"

# Funzione per connettersi ad Azure Blob Storage
def get_blob_service_client():
    return BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# Funzione per verificare se il file esiste nel blob storage
def blob_exists():
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
    return blob_client.exists()

# Funzione per creare un file CSV vuoto nel blob storage se non esiste
def create_empty_csv():
    df = pd.DataFrame(columns=["Timestamp", "Messaggio"])  # Crea un DataFrame vuoto con le colonne richieste
    write_csv_to_blob(df)

# Funzione per leggere il file CSV dal blob storage
def read_csv_from_blob():
    try:
        if not blob_exists():
            st.warning("Il file non esiste, sto creando un file vuoto.")
            create_empty_csv()
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
        blob_data = blob_client.download_blob().readall()
        return pd.read_csv(StringIO(blob_data.decode('utf-8')))
    except Exception as e:
        st.error(f"Errore nel leggere il file dal blob storage: {e}")
        return pd.DataFrame(columns=["Timestamp", "Messaggio"])

# Funzione per scrivere il file CSV nel blob storage
def write_csv_to_blob(df):
    try:
        blob_service_client = get_blob_service_client()
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
        output = StringIO()
        df.to_csv(output, index=False)
        blob_client.upload_blob(output.getvalue(), overwrite=True)
    except Exception as e:
        st.error(f"Errore nel scrivere il file sul blob storage: {e}")

# Funzione per aggiungere una nuova riga
def add_new_row():
    df = read_csv_from_blob()
    
    # Crea un DataFrame con una nuova riga
    new_row = pd.DataFrame({"Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Messaggio": ["ho fatto la cacca!"]})
    
    # Usa pd.concat per aggiungere la nuova riga
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Scrivi il nuovo dataframe nel blob storage
    write_csv_to_blob(df)

# Configurazione layout per dispositivi mobili
st.set_page_config(
    page_title="App Blob Storage",
    page_icon="💩",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Titolo dell'app
st.title("💩 Tracker - Blob Storage App")

# Bottone per aggiungere una nuova riga
if st.button("Aggiungi una nuova riga"):
    add_new_row()
    st.success("Nuova riga aggiunta!")

# Mostra il contenuto del file CSV
st.subheader("Contenuto del file CSV:")
df = read_csv_from_blob()
st.dataframe(df)

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
