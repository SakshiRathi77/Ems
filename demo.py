import tkinter as tk
import pandas as pd  # If using pandas for CSV handling
import pypyodbc  # Import appropriate library for database connectivity
import json
from tkcalendar import DateEntry
from tkinter import ttk, filedialog , messagebox
import os

file_path = r"C:\Users\asus\OneDrive\Desktop\New_try\new-ems\ems-db\src\server_details.json"
try:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
except Exception as e:
    print("Error in opeining Json", e)
# Function to retrieve data between two date-time ranges and save to CSV
server = data['server']
database = data['database']
dailydata = data['DailyData_TableName']
trusted_connection = 'yes'  # Use 'yes' for Windows Authentication
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'

def retrieve_and_save():
    start_datetime = start_cal.get_date()
    end_datetime = end_cal.get_date()
    start_time = start_time_combo.get()  # Get selected start time
    end_time = end_time_combo.get()

    # Connect to your database
    connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'
    conn = pypyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Construct and execute SQL query to retrieve data between the date-time range
    sql_query = f"""
        SELECT *
        FROM {dailydata}
        WHERE [date] BETWEEN '{start_datetime.strftime('%Y-%m-%d')}' AND '{end_datetime.strftime('%Y-%m-%d')}'
        AND intime BETWEEN '{start_time}' AND '{end_time}'
    """
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    print(rows)

    # Convert fetched data to a DataFrame (if using pandas)
    df = pd.DataFrame(rows, columns=[column[0] for column in cursor.description])
    print(df)
    # df.describe()
    print(df.dtypes)
    folder_path = filedialog.askdirectory()
    file_path = os.path.join(folder_path, "result_data.csv")
    # Save the retrieved data to a new CSV file
    if folder_path and not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", "Records saved successfully on the given folder")
        root.destroy()  # Close the Tkinter window after saving
    else:
        df.to_csv('result_data.csv', index=False)
        messagebox.showinfo("Success", "Records saved successfully on the code folder")
        root.destroy()  # Close the Tkinter window after saving


    # Close database connection
    cursor.close()
    conn.close()

# Create the Tkinter window and widgets
root = tk.Tk()
root.title("Data Retrieval and CSV Export")

# Create and place DateEntry widgets for date selection
start_cal = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
end_cal = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)

# Create and place ttk.Combobox for time selection in HH:MM:SS format
time_values = []
for hour in range(24):
    for minute in range(60):
        for second in range(60):
            time_values.append(f"{hour:02d}:{minute:02d}:{second:02d}") # Add your time values
start_time_combo = ttk.Combobox(root, values=time_values)
end_time_combo = ttk.Combobox(root, values=time_values)
# Create button to trigger data retrieval and CSV export
retrieve_button = tk.Button(root, text="Retrieve and Save", command=retrieve_and_save)

# Place the widgets using grid method
start_cal.grid(row=0, column=0, padx=10, pady=10)
end_cal.grid(row=0, column=1, padx=10, pady=10)
start_time_combo.grid(row=1, column=0, padx=10, pady=10)
end_time_combo.grid(row=1, column=1, padx=10, pady=10)
retrieve_button.grid(row=2, columnspan=2, padx=10, pady=10)

# Run the Tkinter main loop
root.mainloop()
