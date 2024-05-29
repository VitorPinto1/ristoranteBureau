from datetime import datetime
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk
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

window = tk.Tk()
window.title("Reservation")
window.geometry("1200x900")
window.minsize(1000, 800)

table = ttk.Treeview(window, columns=("Reservation Number", "Name", "Total Person", "Day", "Time", "Email"), show='headings')
table.heading("Reservation Number", text="Reservation Number")
table.heading("Name", text="Name")
table.heading("Total Person", text="Total Person")
table.heading("Day", text="Day")
table.heading("Time", text="Time")
table.heading("Email", text="Email")
table.pack(fill=tk.BOTH, expand=True)

reservations = total_reservations()
for reservation in reservations:
    table.insert('', 'end', values=reservation)

center_frame = ttk.Frame(window)
center_frame.pack(pady=20)

frame = ttk.Frame(center_frame)
frame.pack()

btn_supprimer = ttk.Button(frame, text="Delete", command=delete_reservation)
btn_supprimer.pack(side=tk.LEFT, padx=5)

entry_date = DateEntry(frame, date_pattern='yyyy-mm-dd')
entry_date.pack(side=tk.LEFT, padx=5)

btn_mettre_a_jour = ttk.Button(frame, text="Change date", command=date_change)
btn_mettre_a_jour.pack(side=tk.LEFT, padx=5)

window.mainloop()
