import os, json
import pandas as pd 
import gspread
from dotenv import load_dotenv
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

def convert_yes_no_to_boolean(df: pd.DataFrame) -> pd.DataFrame:
    yes_no_cols = df.columns[df.isin(['Yes', 'No']).any()]
    for col in yes_no_cols:
        df[col] = df[col].map({'Yes': True, 'No': False})
    return df

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('-', '_')
    )
    return df

def transform_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_column_names(df)
    df = convert_yes_no_to_boolean(df)
    return df
