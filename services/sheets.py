import gspread
import os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from datetime import datetime

# Authorize as google sheets service account
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Get sheet by id
load_dotenv()
workbook_id = os.getenv('SHEET_ID')
workbook = client.open_by_key(workbook_id)
transaction_sheet = workbook.get_worksheet(1)

#export method that saves new row to spreadsheet
def save_data(data):
    # Get current date in format DD.MM.YYYY
    current_date = datetime.now().strftime('%d.%m.%Y')

    transaction_sheet.append_row([
        current_date,
        data["amount"],
        data["description"],
        data["category"]
    ])    