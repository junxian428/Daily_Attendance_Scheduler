import pyodbc
import requests

# --- Telegram Bot Info ---
bot_token = 'XXX:XXX'  # Your Bot Token
chat_id = '-XXXX'  # Use '@channelusername' or '-100...' for groups

# --- SQL Server Connection Info ---
server = ''     # e.g. 'localhost\\SQLEXPRESS'
database = ''
username = ''
password = ''

# --- SQL Query ---
sql_query = """
SELECT 
    [EE#],
    [Name], 
    [Date], 
    [SC], 
    [DT], 
    [TI1], 
    [TO1], 
    [Work],
    [LI], 
    [EO], 
    [Leave],
    [Brch],  
    [ABS2]
FROM [dbo].[HR_AttendaceRecord]
WHERE 
    Name = 'Ho Weng Yin'
    AND CAST([Date] AS DATE) >= CAST(DATEADD(DAY, -6, GETDATE()) AS DATE)
    AND CAST([Date] AS DATE) <= CAST(GETDATE() AS DATE)
ORDER BY [Date] ASC;

"""

try:
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    message_lines = []

    if rows:
        columns = [col[0] for col in cursor.description]

        #for idx, row in enumerate(rows):
        #    message_lines.append(f"Record {idx+1}:")
        #    for key, value in zip(columns, row):
        #        message_lines.append(f"{key}: {value}")
        #    message_lines.append("")  # blank line between records
        for idx, row in enumerate(rows):
                record_parts = [f"{key.strip()}: {str(value).strip()}" for key, value in zip(columns, row)]
                message_lines.append(f"Record {idx+1}: " + ', '.join(record_parts))
                message_text = '\n'.join(message_lines)

        # Truncate if too long for Telegram
        if len(message_text) > 4000:
            message_text = message_text[:3996] + '...'

    else:
        message_text = "No results found for 'Ho Weng Yin'."

    conn.close()

except Exception as e:
    message_text = f"Error running query: {e}"

# --- Send One Telegram Message ---
url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
params = {
    'chat_id': chat_id,
    'text': message_text
}

response = requests.post(url, params=params)
print(response.json())
