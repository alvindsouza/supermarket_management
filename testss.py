from customtkinter import *
from CTkTable import CTkTable

prev = ''
current = ''
table_data = [['name']]

def update_entry():
    global prev, current, table_data
    global table
    current = entry.get()
    if prev != current:
        table.destroy()
        prev = current
        print(current)
        table_data = [['name'], [current]]
        table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4")
        table.pack(expand=True)
        table.update_values(table_data)

    root.after(500, update_entry)  # Update every 500 milliseconds

root = CTk()
root.title("CTkEntry Example")
root.geometry("300x200")

table_frame = CTkScrollableFrame(master=root, fg_color="transparent")
table_frame.pack(expand=True, fill="both", padx=20, pady=20)

table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4")
table.pack(expand=True)

entry = CTkEntry(root, width=200)
entry.pack(pady=20)

# Start updating the entry
update_entry()

root.mainloop()
