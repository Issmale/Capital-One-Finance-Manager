Capital One Finance Manager
This Python script processes financial transaction data from Capital One CSV files and updates a Google Sheet with categorized monthly totals.

Features
Reads transaction data from monthly CSV files.
Categorizes and sums transactions.
Updates a Google Sheet with monthly totals for each category.

Setup
Google Sheets API: Set up Google Sheets API credentials. Ensure you have a service account key in the same directory as the script.
Google Sheet: Create a Google Sheet named "Capital One Finance Manager" with a worksheet named "Sheet1".
CSV Files: Place CSV files named januaryTransaction.csv, februaryTransaction.csv, etc., in the same directory as the script.

Code Overview
Imports: Uses csv for reading CSV files, gspread for interacting with Google Sheets, and re for regular expressions.
monthTransactions(files): Iterates over CSV files, processes transactions, and updates the Google Sheet.
capitalOneFin(file): Reads and parses transaction data from a CSV file.
googleSheets(rows, month_name): Updates the Google Sheet with categorized transaction totals.
