from datetime import datetime
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Config database
config = {
    'host': os.getenv('MYSQL_DATABASE_HOST'),
    'port': os.getenv('MYSQL_DATABASE_PORT'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}



def total_reservations():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "SELECT id, name, totalPerson, day, time, email FROM reservation"
    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def delete_reservation():
    selected_item = table.selection()[0]
    reservation_id = table.item(selected_item, 'values')[0]
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "DELETE FROM reservation WHERE id = %s"
    cursor.execute(query, (reservation_id,))
    conn.commit()

    cursor.close()
    conn.close()
    
    table.delete(selected_item)



def date_change():
    selected_item = table.selection()[0]
    reservation_id = table.item(selected_item, 'values')[0]
    new_date = entry_date.get()
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "UPDATE reservation SET day = %s WHERE id = %s"
    cursor.execute(query, (new_date, reservation_id))
    conn.commit()

    cursor.close()
    conn.close()

    values = table.item(selected_item, 'values')
    table.item(selected_item, values=(reservation_id, values[1], values[2], new_date, values[4], values[5]))

def disable_mondays(event):
    global prev_date
    try:
        selected_date = entry_date.get_date()
        if selected_date.weekday() == 0:  # Monday == 0
            show_custom_messagebox("Invalid Date", "Ristorante 'Il Capo' is closed on Mondays. Please choose a date between Tuesday and Sunday.")
            entry_date.set_date(prev_date)
        else:
            prev_date = selected_date
    except KeyError:
        pass  # Handle the KeyError when 'popdown' is not found

def show_custom_messagebox(title, message):
    custom_window = ctk.CTkToplevel()
    custom_window.title(title)
    
    # Disable close, minimize, and maximize buttons
    custom_window.overrideredirect(True)

    screen_width = custom_window.winfo_screenwidth()
    screen_height = custom_window.winfo_screenheight()

    window_width = 300
    window_height = 150

    position_top = int(screen_height / 2 - window_height / 200)
    position_right = int(screen_width / 3 - window_width / 2)

    # Set position
    custom_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    lbl_message = ctk.CTkLabel(custom_window, text=message, wraplength=250, justify="center")
    lbl_message.pack(expand=True, pady=20)

    btn_ok = ctk.CTkButton(custom_window, text="OK", command=custom_window.destroy)
    btn_ok.pack(pady=10)

    custom_window.transient(window)  # Make the window modal
    custom_window.grab_set()  # Capture all events for this window
    window.wait_window(custom_window)


def time_change():
    selected_item = table.selection()[0]
    reservation_id = table.item(selected_item, 'values')[0]
    new_time = entry_time.get()
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "UPDATE reservation SET time = %s WHERE id = %s"
    cursor.execute(query, (new_time, reservation_id))
    conn.commit()

    cursor.close()
    conn.close()

    values = table.item(selected_item, 'values')
    table.item(selected_item, values=(reservation_id, values[1], values[2], values[3], new_time, values[5]))

def adjust_columns(event):
    total_width = window.winfo_width()
    fixed_column_width = 200  
    dynamic_columns = [col for col in table["columns"] if col != "Email"]
    dynamic_column_width = (total_width - fixed_column_width) // len(dynamic_columns)

    for col in dynamic_columns:
        table.column(col, width=dynamic_column_width)
    table.column("Email", width=fixed_column_width)

def on_row_select(event):
    selected_item = table.selection()[0]
    values = table.item(selected_item, 'values')
    details = (f"Reservation number: {values[0]}\n"
               f"Name: {values[1]}\n"
               f"Total person: {values[2]}\n"
               f"Day: {values[3]}\n"
               f"Time: {values[4]}\n"
               f"Email: {values[5]}")
    lbl_details.config(text=details)


window = tk.Tk()
window.title("Reservation")
window.geometry("1200x900")
window.minsize(1200, 900)
window.maxsize(1200, 900)

# Create a frame for the Treeview and scrollbar
table_frame = ttk.Frame(window, width=800, height=200)
table_frame.pack(side=tk.TOP, pady=50)
table_frame.pack_propagate(False)

# Create a vertical scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

# Create the Treeview widget
max_visible_rows = 10
table = ttk.Treeview(table_frame, columns=("Reservation Number", "Name", "Total Person", "Day", "Time", "Email"), show='headings', height=max_visible_rows, yscrollcommand=scrollbar.set)
scrollbar.config(command=table.yview)

table.grid(row=0, column=0, sticky='ns')
scrollbar.grid(row=0, column=1, sticky='ns')

table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

table.heading("Reservation Number", text="Reservation number")
table.heading("Name", text="Name")
table.heading("Total Person", text="Total person")
table.heading("Day", text="Day")
table.heading("Time", text="Time")
table.heading("Email", text="Email")

reservations = total_reservations()
for reservation in reservations:
    table.insert('', 'end', values=reservation)

details_frame = ttk.Frame(window)
details_frame.pack(pady=10)

lbl_details = ttk.Label(details_frame, text="", justify=tk.LEFT)
lbl_details.grid(row=0, column=0, sticky=tk.W)

center_frame = ttk.Frame(window)
center_frame.pack(pady=10)

frame = ttk.Frame(center_frame)
frame.pack()



btn_supprimer = ttk.Button(frame, text="Delete", command=delete_reservation)
btn_supprimer.grid(row=0, column=0, padx=5)

entry_date = DateEntry(frame, date_pattern='yyyy-mm-dd', showweeknumbers=False)
entry_date.grid(row=0, column=1, padx=5)

prev_date = entry_date.get_date()
entry_date.bind("<<DateEntrySelected>>", disable_mondays)


hours = [f"{h:02d}:{m:02d}" for h in range(12, 24) for m in (0, 30)]
entry_time = ttk.Combobox(frame, values=hours, state="readonly")
entry_time.grid(row=0, column=3, padx=5)

btn_change_date = ttk.Button(frame, text="Change date", command=date_change)
btn_change_date.grid(row=0, column=2, padx=5)

btn_time_change = ttk.Button(frame, text="Change time", command=time_change)
btn_time_change.grid(row=0, column=4, padx=5)



table.bind("<<TreeviewSelect>>", on_row_select)


window.bind("<Configure>", adjust_columns)

window.mainloop()
