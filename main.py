import tkinter as tk
from datetime import datetime
from tkinter import ttk
from PIL import Image, ImageTk
import cairosvg
from tkcalendar import DateEntry
from database import total_reservations, delete_reservation, update_reservation_date, update_reservation_time
from reservation import show_custom_messagebox, on_row_select, update_button_states, disable_mondays, prev_date

window = tk.Tk()
window.title("Reservation")
window.geometry("900x800")
window.minsize(900, 800)
window.maxsize(900, 800)
window.configure(bg='#f4f1e4')

def delete():
    selected_items = table.selection()
    if not selected_items:
        show_custom_messagebox("Error", "No reservation selected", window)
        return
    
    selected_item = selected_items[0]
    reservation_id = table.item(selected_item, 'values')[0]
    
    delete_reservation(reservation_id)
    table.delete(selected_item)
    update_button_states(table, btn_delete, btn_change_date, btn_time_change, lbl_details, entry_date, entry_time)

def date_change():
    if not table.selection():
        show_custom_messagebox("Error", "No reservation selected", window)
        return
    selected_item = table.selection()[0]
    reservation_id = table.item(selected_item, 'values')[0]
    new_date = entry_date.get()
    
    update_reservation_date(reservation_id, new_date)

    values = table.item(selected_item, 'values')
    table.item(selected_item, values=(reservation_id, values[1], values[2], new_date, values[4], values[5]))
    update_button_states(table, btn_delete, btn_change_date, btn_time_change, lbl_details, entry_date, entry_time)

def time_change():
    if not table.selection():
        show_custom_messagebox("Error", "No reservation selected", window)
        return
    selected_item = table.selection()[0]
    reservation_id = table.item(selected_item, 'values')[0]
    new_time = entry_time.get()

    if len(new_time) == 5:
        new_time += ":00"
    
    update_reservation_time(reservation_id, new_time)

    values = table.item(selected_item, 'values')
    table.item(selected_item, values=(reservation_id, values[1], values[2], values[3], new_time, values[5]))
    update_button_states(table, btn_delete, btn_change_date, btn_time_change, lbl_details, entry_date, entry_time)

# Create a frame for the Treeview and scrollbar
table_frame = ttk.Frame(window, width=800, height=200)
table_frame.pack(side=tk.TOP, pady=50)
table_frame.pack_propagate(False)

scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
table = ttk.Treeview(table_frame, columns=("Reservation Number", "Name", "Total Person", "Day", "Time", "Email"), show='headings', height=10, yscrollcommand=scrollbar.set)
scrollbar.config(command=table.yview)

table.grid(row=0, column=0, sticky='ns')
scrollbar.grid(row=0, column=1, sticky='ns')

table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

col_widths = {
    "Reservation Number": 100,
    "Name": 100,
    "Total Person": 100,
    "Day": 100,
    "Time": 100,
    "Email": 200
}

for col, width in col_widths.items():
    table.heading(col, text=col)
    table.column(col, width=width, stretch=False, anchor='center')

reservations = total_reservations()
for reservation in reservations:
    table.insert('', 'end', values=reservation)

details_frame = tk.Frame(window, bg='#f4f1e4')
details_frame.pack(pady=10)

lbl_details = tk.Label(details_frame, text="", justify=tk.LEFT,  bg='#f4f1e4')
lbl_details.grid(row=0, column=0, sticky=tk.W)

center_frame = tk.Frame(window,  bg='#f4f1e4')
center_frame.pack(pady=10)

frame = tk.Frame(center_frame, bg='#f4f1e4')
frame.pack()

btn_delete = tk.Button(frame, text="Delete", command=delete,  fg="red")
btn_delete.grid(row=2, column=1, padx=5)
btn_delete.config(state=tk.DISABLED)

current_date = datetime.now()

entry_date = DateEntry(frame, date_pattern='yyyy-mm-dd', showweeknumbers=False, mindate=current_date)
entry_date.grid(row=0, column=0, padx=5)
entry_date.bind("<<DateEntrySelected>>", lambda event: disable_mondays(event, entry_date, show_custom_messagebox, window))

prev_date = entry_date.get_date()

hours = [f"{h:02d}:{m:02d}" for h in range(12, 24) for m in (0, 30)]
entry_time = ttk.Combobox(frame, values=hours, state="readonly")
entry_time.grid(row=1, column=0, padx=5)
entry_time.bind("<<ComboboxSelected>>", lambda event: update_button_states(table, btn_delete, btn_change_date, btn_time_change, lbl_details, entry_date, entry_time))

btn_change_date = tk.Button(frame, text="Change date", command=date_change)
btn_change_date.grid(row=0, column=1, padx=5)
btn_change_date.config(state=tk.DISABLED)

btn_time_change = tk.Button(frame, text="Change time", command=time_change)
btn_time_change.grid(row=1, column=1, padx=5)
btn_time_change.config(state=tk.DISABLED)

table.bind("<<TreeviewSelect>>", lambda event: on_row_select(event, table, lbl_details, entry_date))

# Deselect data
table.bind("<Double-1>", lambda event: table.selection_remove(table.selection()[0]) if table.selection() else None)

def prevent_resize(event):
    for col in table["columns"]:
        table.column(col, width=col_widths[col], stretch=False)

table.bind("<ButtonRelease-1>", prevent_resize)
table.bind("<B1-Motion>", prevent_resize)

logo_frame = tk.Frame(window, bg='#f4f1e4')
logo_frame.pack(side=tk.BOTTOM, pady=10)

svg_path = "ressources/RistoranteIndex.svg"
png_path = "logo.png"
cairosvg.svg2png(url=svg_path, write_to=png_path)
logo_image = Image.open(png_path)
logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)  
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(logo_frame, image=logo_photo, bg='#f4f1e4')
logo_label.image = logo_photo  
logo_label.pack()

window.mainloop()
