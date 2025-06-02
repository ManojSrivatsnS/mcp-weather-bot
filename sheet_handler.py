# sheet_handler.py

import gspread
from google.oauth2.service_account import Credentials

# Define your spreadsheet name
SHEET_NAME = "MCP Weather Users"

# Define your column headers (should match sheet)
HEADERS = ["name", "email", "city", "location", "timezone"]

# Define the scope for Google Sheets + Drive API
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

# Authenticate with service account JSON
def connect_to_sheet():
    creds = Credentials.from_service_account_file("sheet-writer.json", scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet

# Add a new user to the sheet
def add_user_to_sheet(name, email, city, location, timezone):
    sheet = connect_to_sheet()
    
    # Avoid duplicate emails
    all_emails = [row[1].lower() for row in sheet.get_all_values()[1:]]
    if email.lower() in all_emails:
        return False

    sheet.append_row([name, email, city, location, timezone])
    return True

# Remove user by email
def remove_user_from_sheet(email):
    sheet = connect_to_sheet()
    all_data = sheet.get_all_values()
    
    for i, row in enumerate(all_data[1:], start=2):  # skip header row
        if row[1].lower() == email.lower():
            sheet.delete_rows(i)
            return True
    return False
