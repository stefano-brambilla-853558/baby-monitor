from dotenv import load_dotenv  # Per caricare il file .env
import os
from io import StringIO
from azure.storage.blob import BlobServiceClient
from .config import data_files, data_columns
import pandas as pd
import streamlit as st


def get_env(mode):
    load_dotenv()
    # Ottieni le informazioni di connessione dal file environment
    return {
        "AZURE_STORAGE_CONNECTION_STRING": os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
        "CONTAINER_NAME": os.getenv("AZURE_CONTAINER_NAME"),
        "BLOB_NAME": data_files[mode]
    }

def get_blob(mode):
# Carica le variabili dal file .env
    env = get_env(mode)
    return BlobServiceClient \
        .from_connection_string(env["AZURE_STORAGE_CONNECTION_STRING"]) \
        .get_blob_client(container=env["CONTAINER_NAME"], blob=env["BLOB_NAME"])

# Funzione per verificare se il file esiste nel blob storage
def exists_blob(mode):
    blob_client = get_blob(mode)
    return blob_client.exists()

# Funzione per creare un file CSV vuoto nel blob storage se non esiste
def initialize_blob(mode):
    if not exists_blob(mode):
        df = pd.DataFrame(columns=data_columns[mode])  # Crea un DataFrame vuoto con le colonne richieste
        write_blob(mode, df)
    else:
        pass

# Funzione per leggere il file CSV dal blob storage
def read_blob(mode):
    try:
        initialize_blob(mode)
        blob_client = get_blob(mode)
        blob_data = blob_client.download_blob().readall()
        return pd.read_csv(StringIO(blob_data.decode('utf-8')))
    except Exception as e:
        st.error(f"Errore nel leggere il file dal blob storage: {e}")
        return pd.DataFrame(columns=data_columns[mode])

# Funzione per scrivere il file CSV nel blob storage
def write_blob(mode, df):
    try:
        blob_client = get_blob(mode)
        output = StringIO()
        df.to_csv(output, index=False)
        blob_client.upload_blob(output.getvalue(), overwrite=True)
    except Exception as e:
        st.error(f"Errore nel scrivere il file sul blob storage: {e}")

# Funzione per aggiungere una nuova riga
def add_row_blob(mode, row):
    # Row defined as dictionary of list --> {"Timestamp": ["2021-01-01 12:00:00"], "Messaggio": ["bla"]}
    df = read_blob(mode)
    
    # Crea un DataFrame con una nuova riga
    new_row = pd.DataFrame(row)
    
    # Usa pd.concat per aggiungere la nuova riga
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Scrivi il nuovo dataframe nel blob storage
    write_blob(mode, df)