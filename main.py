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
    selected_items = table.selection()
    if not selected_items:
        show_custom_messagebox("Error", "No reservation selected")
        return
    
    selected_item = selected_items[0]
    reservation_id = table.item(selected_item, 'values')[0]
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "DELETE FROM reservation WHERE id = %s"
    cursor.execute(query, (reservation_id,))
    conn.commit()

    cursor.close()
    conn.close()
    
    table.delete(selected_item)
    update_button_states()

def date_change():
    if not table.selection():
        show_custom_messagebox("Error", "No reservation selected")
        return
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
    update_button_states()

def disable_mondays(event):
    global prev_date
    try:
        selected_date = entry_date.get_date()
        if selected_date.weekday() == 0:  # Monday == 0
            show_custom_messagebox("Invalid Date", "Ristorante 'Il Capo' is closed on Mondays. Please choose a date between Tuesday and Sunday.")
            entry_date.set_date(prev_date)
        else:
            prev_date = selected_date
        update_button_states()
    except KeyError:
        pass  # Handle the KeyError when 'popdown' is not found

def show_custom_messagebox(title, message):
    custom_window = ctk.CTkToplevel()
    custom_window.title(title)
    
    # Disable close, minimize, and maximize buttons
    custom_window.overrideredirect(True)

    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    window_x = window.winfo_x()
    window_y = window.winfo_y()

    messagebox_width = 300
    messagebox_height = 150

    position_right = window_x + (window_width // 2) - (messagebox_width // 2)
    position_top = window_y + (window_height // 2) - (messagebox_height // 2) + 250

    # Set position
    custom_window.geometry(f'{messagebox_width}x{messagebox_height}+{position_right}+{position_top}')


    lbl_message = ctk.CTkLabel(custom_window, text=message, wraplength=250, justify="center")
    lbl_message.pack(expand=True, pady=20)

    btn_ok = ctk.CTkButton(custom_window, text="OK", command=custom_window.destroy)
    btn_ok.pack(pady=10)
    btn_ok.configure(fg_color="red")

    custom_window.transient(window)  # Make the window modal
    custom_window.grab_set()  # Capture all events for this window
    window.wait_window(custom_window)

def time_change():
    if not table.selection():
        show_custom_messagebox("Error", "No reservation selected")
        return
    selected_item = table.selection()[0]
    reservation_id = table.item(selected_item, 'values')[0]
    new_time = entry_time.get()

    if len(new_time) == 5:
        new_time += ":00"
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "UPDATE reservation SET time = %s WHERE id = %s"
    cursor.execute(query, (new_time, reservation_id))
    conn.commit()

    cursor.close()
    conn.close()

    values = table.item(selected_item, 'values')
    table.item(selected_item, values=(reservation_id, values[1], values[2], values[3], new_time, values[5]))
    update_button_states()


def on_row_select(event):
    update_button_states()
    selected_items = table.selection()
    if selected_items:
        selected_item = selected_items[0]
        values = table.item(selected_item, 'values')
        details = (f"Reservation number: {values[0]}\n"
                   f"Name: {values[1]}\n"
                   f"Total person: {values[2]}\n"
                   f"Day: {values[3]}\n"
                   f"Time: {values[4]}\n"
                   f"Email: {values[5]}")
        lbl_details.config(text=details)

        # Update DateEntry with the selected date 
        selected_date = datetime.strptime(values[3], '%Y-%m-%d')
        entry_date.set_date(selected_date)

def update_button_states():
    selected_items = table.selection()
    if selected_items:
        btn_delete.config(state=tk.NORMAL)
        if entry_date.get_date():
            btn_change_date.config(state=tk.NORMAL)
        else:
            btn_change_date.config(state=tk.DISABLED)
        if entry_time.get():
            btn_time_change.config(state=tk.NORMAL)
        else:
            btn_time_change.config(state=tk.DISABLED)

        selected_item = selected_items[0]
        values = table.item(selected_item, 'values')
        details = (f"Reservation number: {values[0]}\n"
                   f"Name: {values[1]}\n"
                   f"Total person: {values[2]}\n"
                   f"Day: {values[3]}\n"
                   f"Time: {values[4]}\n"
                   f"Email: {values[5]}")
        lbl_details.config(text=details)
    else:
        btn_delete.config(state=tk.DISABLED)
        btn_change_date.config(state=tk.DISABLED)
        btn_time_change.config(state=tk.DISABLED)
        lbl_details.config(text="")
    
def on_double_click(event):
    selected_items = table.selection()
    if selected_items:
        selected_item = selected_items[0]
        table.selection_remove(selected_item)
        update_button_states()

window = tk.Tk()
window.title("Reservation")
window.geometry("900x800")
window.minsize(900, 800)
window.maxsize(900, 800)

window.configure(bg='#f4f1e4')





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

table.heading("Reservation Number", text="Reservation")
table.heading("Name", text="Name")
table.heading("Total Person", text="Total person")
table.heading("Day", text="Day")
table.heading("Time", text="Time")
table.heading("Email", text="Email")

table.column("Reservation Number", width=100, stretch=False)
table.column("Name", width=100, stretch=False)
table.column("Total Person", width=100, stretch=False)
table.column("Day", width=100, stretch=False)
table.column("Time", width=100, stretch=False)
table.column("Email", width=200, stretch=False)


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

btn_delete = ttk.Button(frame, text="Delete", command=delete_reservation)
btn_delete.grid(row=2, column=1, padx=5)
btn_delete.config(state=tk.DISABLED)

entry_date = DateEntry(frame, date_pattern='yyyy-mm-dd', showweeknumbers=False)
entry_date.grid(row=0, column=0, padx=5)
entry_date.bind("<<DateEntrySelected>>", disable_mondays)

prev_date = entry_date.get_date()

hours = [f"{h:02d}:{m:02d}" for h in range(12, 24) for m in (0, 30)]
entry_time = ttk.Combobox(frame, values=hours, state="readonly")
entry_time.grid(row=1, column=0, padx=5)
entry_time.bind("<<ComboboxSelected>>", lambda event: update_button_states())

btn_change_date = ttk.Button(frame, text="Change date", command=date_change)
btn_change_date.grid(row=0, column=1, padx=5)
btn_change_date.config(state=tk.DISABLED)

btn_time_change = ttk.Button(frame, text="Change time", command=time_change)
btn_time_change.grid(row=1, column=1, padx=5)
btn_time_change.config(state=tk.DISABLED)

table.bind("<<TreeviewSelect>>", on_row_select)

table.bind("<Double-1>", on_double_click)



window.mainloop()
