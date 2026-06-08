from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ["Name", "MC_USD_Billion"]
db_name = 'Banks.db'
table_name = 'Largest_banks'
csv_path = 'F:\Data Topics\Data Engineering\Python project for Data Engineering\Banks_Project.csv'

def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the 
    code execution to a log file. Function returns nothing.'''
    timestamp_format = '%Y-%h-%d-%H:%M:%S' 
    now = datetime.now() 
    timestamp = now.strftime(timestamp_format) 
    with open("code_log.txt", "a") as f: 
        f.write(timestamp + ' : ' + message + '\n') 

def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('table', {'class': 'wikitable'})
    target_table = None
    for table in tables:
        if 'market cap' in table.text.lower() or 'market capitalization' in table.text.lower():
            target_table = table
            break
            
    if target_table is None:
        print("didn't Exist")
        return df
    rows = target_table.find_all('tr') 
    
    for row in rows:
        col = row.find_all('td')
        if len(col) >= 3:
            bank_name = col[1].text.strip()
            if '-' not in col[2].text and '\u2014' not in col[2].text:
                market_cap_str = col[2].text.replace('\n', '').replace(',', '').strip()
                try:
                    market_cap = float(market_cap_str)
                    data_dict = {"Name": bank_name, "MC_USD_Billion": market_cap}
                    df1 = pd.DataFrame(data_dict, index=[0])
                    df = pd.concat([df, df1], ignore_index=True)
                except ValueError:
                    pass
    return df

def transform(df, csv_path):
    ''' This function converts the Market Cap information to different currencies
    based on exchange rates and rounds to 2 decimal places.'''

    exchange_rate = pd.read_csv(csv_path)
    exchange_dict = exchange_rate.set_index(exchange_rate.columns[0]).to_dict()[exchange_rate.columns[1]]
    df['MC_GBP_Billion'] = [np.round(x * exchange_dict['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * exchange_dict['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * exchange_dict['INR'], 2) for x in df['MC_USD_Billion']]

    return df

def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a CSV file.'''
    df.to_csv(csv_path, index=False)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table.'''
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and prints the output.'''
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)
    print("\n")


# --- Execution Steps ---

log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url, table_attribs)

log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df, 'exchange_rate.csv')

log_progress('Data transformation complete. Initiating Loading process')

load_to_csv(df, csv_path)

log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect(db_name)

log_progress('SQL Connection initiated')

load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as a table, Executing queries')
run_query('SELECT * FROM Largest_banks', sql_connection)
run_query('SELECT AVG(MC_GBP_Billion) FROM Largest_banks', sql_connection)
run_query('SELECT Name from Largest_banks LIMIT 5', sql_connection) 

log_progress('Process Complete')
sql_connection.close()
log_progress('Server Connection closed')