import pandas as pd 
import gspread
import oauth2client.service_account 
import ServiceAccountCredentials

filename = "double-kite-475110-i2-ecba07a5f7a0.json"
scopes = [
    "https://spreadsheets.google.com/feeds"
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    filename=filename, 
    scopes=scopes
    )
client = gspread.authorize(creds)
print(client)
