import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Database connection setup
def connect_to_db():
    try:
        conn = psycopg2.connect(host=host_var.get(), port=port_var.get(), user=user_var.get(),
                                password=password_var.get(), dbname=dbname_var.get())
        return conn
    except Exception as e:
        messagebox.showerror("Connection Error", f"Could not connect to the database: {e}")
        return None

# Function to fetch reference data from the database (reference tables)
def fetch_reference_data():
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()

    # Populate table names into the table list view (Treeview widget)
    for row in tables:
        table_list.insert("", "end", values=row)

    cursor.close()
    conn.close()

# Function to update reference data in the database from the GUI (for example, adding new rows to a table)
def update_reference_data():
    # Validate inputs
    if not symbol_var.get() or not name_var.get() or not price_var.get() or not market_cap_var.get() or not volume_var.get() or not record_date_var.get():
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return
    
    # Validate the price, market cap, and volume to be numeric
    try:
        price = float(price_var.get())
        market_cap = float(market_cap_var.get())
        volume = float(volume_var.get())
    except ValueError:
        messagebox.showerror("Input Error", "Price, Market Cap, and Volume must be numeric values.")
        return

    # Validate record date format
    try:
        record_date = datetime.strptime(record_date_var.get(), '%Y-%m-%d %H:%M:%S')
    except ValueError:
        messagebox.showerror("Input Error", "Record Date must be in the format 'YYYY-MM-DD HH:MM:SS'.")
        return

    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        # Insert into the crypto_current table
        cursor.execute("""
            INSERT INTO crypto_current (symbol, name, price_usd, market_cap_usd, volume_24h, record_date)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (symbol_var.get(), name_var.get(), price, market_cap, volume, record_date))

        conn.commit()
        messagebox.showinfo("Success", "Reference data updated successfully.")
    except Exception as e:
        messagebox.showerror("Update Error", f"Could not update reference data: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to run operations based on cached reference data
def run_operations():
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Example operation: fetch data from the reference table and print
        cursor.execute("SELECT * FROM crypto_current LIMIT 10;")
        data = cursor.fetchall()

        for row in data:
            print(row)  # Or do other operations with this data

        messagebox.showinfo("Operation", "Operations executed successfully.")
    except Exception as e:
        messagebox.showerror("Run Error", f"Could not run operations: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to sync the GUI data with the reference tables
def sync_data():
    conn = connect_to_db()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Example sync: ensure the reference tables are in sync (for example, check for discrepancies)
        cursor.execute("SELECT * FROM crypto_current;")
        rows = cursor.fetchall()

        for row in rows:
            print(row)  # Or apply any necessary sync logic

        messagebox.showinfo("Sync", "Data synchronized successfully.")
    except Exception as e:
        messagebox.showerror("Sync Error", f"Could not sync data: {e}")
    finally:
        cursor.close()
        conn.close()

# GUI Setup
root = tk.Tk()
root.title("Crypto Database GUI")

# Connection Info Frame
frame_conn = ttk.LabelFrame(root, text="Database Connection", padding="10")
frame_conn.grid(row=0, column=0, sticky="ew")

tk.Label(frame_conn, text="Host:").grid(row=0, column=0)
host_var = tk.StringVar(value="localhost")
tk.Entry(frame_conn, textvariable=host_var).grid(row=0, column=1)

tk.Label(frame_conn, text="Port:").grid(row=1, column=0)
port_var = tk.StringVar(value="5433")
tk.Entry(frame_conn, textvariable=port_var).grid(row=1, column=1)

tk.Label(frame_conn, text="User:").grid(row=2, column=0)
user_var = tk.StringVar(value="postgres")
tk.Entry(frame_conn, textvariable=user_var).grid(row=2, column=1)

tk.Label(frame_conn, text="Password:").grid(row=3, column=0)
password_var = tk.StringVar(value="Duck-pi3")
tk.Entry(frame_conn, textvariable=password_var, show="*").grid(row=3, column=1)

tk.Label(frame_conn, text="Database:").grid(row=4, column=0)
dbname_var = tk.StringVar(value="crypto_data")
tk.Entry(frame_conn, textvariable=dbname_var).grid(row=4, column=1)

# Buttons for actions
ttk.Button(root, text="Load Tables", command=fetch_reference_data).grid(row=1, column=0, pady=10)
ttk.Button(root, text="Update Data", command=update_reference_data).grid(row=2, column=0, pady=10)
ttk.Button(root, text="Run", command=run_operations).grid(row=3, column=0, pady=10)
ttk.Button(root, text="Sync Data", command=sync_data).grid(row=4, column=0, pady=10)

# Table to show the database tables (reference tables)
table_list = ttk.Treeview(root, columns=("table_name"), show="headings")
table_list.heading("table_name", text="Table Name")
table_list.grid(row=5, column=0, pady=10, sticky="ew")

# Entry fields for updating reference data (example: crypto_current data)
frame_update = ttk.LabelFrame(root, text="Update Reference Data", padding="10")
frame_update.grid(row=6, column=0, sticky="ew")

tk.Label(frame_update, text="Symbol:").grid(row=0, column=0)
symbol_var = tk.StringVar()
tk.Entry(frame_update, textvariable=symbol_var).grid(row=0, column=1)

tk.Label(frame_update, text="Name:").grid(row=1, column=0)
name_var = tk.StringVar()
tk.Entry(frame_update, textvariable=name_var).grid(row=1, column=1)

tk.Label(frame_update, text="Price (USD):").grid(row=2, column=0)
price_var = tk.StringVar()
tk.Entry(frame_update, textvariable=price_var).grid(row=2, column=1)

tk.Label(frame_update, text="Market Cap (USD):").grid(row=3, column=0)
market_cap_var = tk.StringVar()
tk.Entry(frame_update, textvariable=market_cap_var).grid(row=3, column=1)

tk.Label(frame_update, text="Volume (24h):").grid(row=4, column=0)
volume_var = tk.StringVar()
tk.Entry(frame_update, textvariable=volume_var).grid(row=4, column=1)

tk.Label(frame_update, text="Record Date:").grid(row=5, column=0)
record_date_var = tk.StringVar()
tk.Entry(frame_update, textvariable=record_date_var).grid(row=5, column=1)

# Start the GUI loop
root.mainloop()
