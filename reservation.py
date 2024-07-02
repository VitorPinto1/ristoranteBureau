from datetime import datetime
import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry

prev_date = None

def show_custom_messagebox(title, message, window):
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

    # Make the window modal
    custom_window.transient(window)  
    custom_window.grab_set()  
    window.wait_window(custom_window)

def on_row_select(event, table, lbl_details, entry_date):
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

        selected_date = datetime.strptime(values[3], '%Y-%m-%d')
        entry_date.set_date(selected_date)

def update_button_states(table, btn_delete, btn_change_date, btn_time_change, lbl_details, entry_date, entry_time):
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

def disable_mondays(event, entry_date, show_custom_messagebox, window):
    global prev_date
    try:
        selected_date = entry_date.get_date()
        if selected_date.weekday() == 0:  # Monday == 0
            show_custom_messagebox("Invalid Date", "Ristorante 'Il Capo' is closed on Mondays. Please choose a date between Tuesday and Sunday.", window)
            entry_date.set_date(prev_date)
        else:
            prev_date = selected_date
    except KeyError:
        pass
