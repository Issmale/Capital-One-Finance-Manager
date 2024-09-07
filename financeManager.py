import csv
import gspread
import os
import time
import re

files = [
    "januaryTransaction.csv", 
    "februaryTransaction.csv", 
    "marchTransaction.csv", 
    "aprilTransaction.csv", 
    "mayTransaction.csv", 
    "juneTransaction.csv", 
    "julyTransaction.csv", 
    "augustTransaction.csv", 
    "septemberTransaction.csv", 
    "octoberTransaction.csv", 
    "novemberTransaction.csv", 
    "decemberTransaction.csv"
]

def monthTransactions(files):
    for file in files:
        try:
            month_name = re.sub(r'Transaction\.csv$', '', file)
            rows = capitalOneFin(file)
            googleSheets(rows, month_name)
        except FileNotFoundError:
            print("No data for ", file)

def capitalOneFin(file):
    transactions = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            transactionDate = row[0]
            transactionDescription = row[3]
            debit = row[5]
            credit = row[6]
            category = row[4]
            if category == 'Payment/Credit' or debit == '':
                transaction = (transactionDate, transactionDescription, credit, 'Payment/Credit')
            else:
                transaction = (transactionDate, transactionDescription, debit, category)
            transactions.append(transaction)
        return transactions
    
def googleSheets(rows, month_name):
    category_totals = {
        'Payment/Credit': 0,
        'Phone/Cable': 0,
        'Grocery': 0,
        'Entertainment': 0,
        'Dining': 0,
        'Merchandise': 0,
        'Other Services': 0,
        'Airfare': 0,
        'Internet': 0,
    }
    
    for row in rows:
        if row[3] in category_totals:
            category_totals[row[3]] += float(row[2])
    
    cells = {
        'Payment/Credit': ['B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3', 'K3', 'L3', 'M3'],
        'Phone/Cable': ['B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4', 'J4', 'K4', 'L4', 'M4'],
        'Grocery': ['B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5', 'K5', 'L5', 'M5'],
        'Entertainment': ['B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6', 'J6', 'K6', 'L6', 'M6'],
        'Dining': ['B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7', 'J7', 'K7', 'L7', 'M7'],
        'Merchandise': ['B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8', 'J8', 'K8', 'L8', 'M8'],
        'Other Services': ['B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9', 'J9', 'K9', 'L9', 'M9'],
        'Airfare': ['B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10', 'J10', 'K10', 'L10', 'M10'],
        'Internet': ['B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11', 'I11', 'J11', 'K11', 'L11', 'M11']
    }
    
    column_index = {
        'january': 0,
        'february': 1,
        'march': 2,
        'april': 3,
        'may': 4,
        'june': 5,
        'july': 6,
        'august': 7,
        'september': 8,
        'october': 9,
        'november': 10,
        'december': 11
    }[month_name]
    
    # Prepare batch update data
    update_data = []
    for category, total in category_totals.items():
        cell = cells[category][column_index]
        update_data.append({
            'range': cell,
            'values': [[total]]
        })
    
    # Batch update the values
    wks.batch_update(update_data)

# Set up Google Sheets API
sa = gspread.service_account()
sh = sa.open("Capital One Finance Manager")
wks = sh.worksheet("Sheet1")

# Process transactions
monthTransactions(files)
