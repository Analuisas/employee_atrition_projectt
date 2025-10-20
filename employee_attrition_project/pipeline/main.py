
import os, json
import pandas as pd 
import gspread
from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from pipeline.data_transform import transform_dataframe


def load_data_from_drive(folder_id: str):
    filename = "credentials.json"
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)
    creds_path = os.getenv("GOOGLE_CREDS_PATH")

    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scopes)
    client = gspread.authorize(creds)

    drive = build('drive', 'v3', credentials=creds)
    folder_id = os.getenv("DRIVE_FOLDER_ID")

    results = drive.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'",
        fields="files(id, name)"
        ).execute()

    files = results.get('files', [])

    dataframes = {}
    for file in files:
        sheet = client.open_by_key(file['id']).sheet1
        df = pd.DataFrame(sheet.get_all_records())
        dataframes[file['name']] = df

    return dataframes

from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import Session 
import pandas as pd 

def save_data_to_postgres(dataframes, db_url):
    engine = create_engine(db_url)
    
    # Inicializa table_name ANTES do loop. ESSENCIAL para evitar UnboundLocalError
    table_name = None 
    
    try:
        for name, df in dataframes.items():
            # 1. Checagem de validade e atribuição
            if df is None or df.empty:
                 print(f"AVISO: DataFrame '{name}' está vazio e será ignorado.")
                 continue # Pula para o próximo item
                 
            table_name = name.lower().replace(" ", "_")
            print(f"Processando tabela: {table_name}")
            
            # --- Bloco TRUNCATE (Limpeza) ---
            try:
                with Session(engine) as session:
                    session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY;"))
                    session.commit()
                    print(f"Tabela '{table_name}' limpa.")
            except Exception as e:
                # O TRUNCATE falha se a tabela não existe. Isso é OK.
                print(f"Aviso: Tabela '{table_name}' será criada, pois a limpeza falhou. {e}")
                
            # --- INSERÇÃO/CRIAÇÃO ---
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Dados inseridos/atualizados com sucesso.")
            
    except Exception as e:
        # Este bloco captura erros que ocorreram ANTES ou DURANTE o loop
        if table_name:
            print(f"\nERRO FATAL: Falha ao processar a tabela {table_name}. Causa: {e}")
        else:
            print(f"\nERRO FATAL: O loop não iniciou. Verifique se 'dataframes' é um dicionário válido. Causa: {e}")
        # Relança a exceção para ver o traceback completo
        raise e