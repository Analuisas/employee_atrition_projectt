import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

def upload_df_to_drive(df, sheet_name, folder_id, creds_path):
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scopes)
    client = gspread.authorize(creds)
    drive = build('drive', 'v3', credentials=creds)

    results = drive.files().list(
        q=f"'{folder_id}' in parents and name='{sheet_name}' and mimeType='application/vnd.google-apps.spreadsheet'",
        fields="files(id, name)"
    ).execute()

    files = results.get('files', [])

    if files:
        sheet_id = files[0]['id']
        sheet = client.open_by_key(sheet_id).sheet1
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
    else:
        spreadsheet = client.create(sheet_name)
        spreadsheet.share('', role='reader', type='anyone')  # público, opcional
        sheet = spreadsheet.sheet1
        sheet.update([df.columns.values.tolist()] + df.values.tolist())

        drive.files().update(
            fileId=spreadsheet.id,
            addParents=folder_id,
            removeParents='root',
            fields='id, parents'
        ).execute()
