from customtkinter import *
from CTkTable import CTkTable

# Create a window
root = CTk()

# Create a frame to hold the table and buttons
table_frame = CTkFrame(root)
table_frame.pack(fill='both', expand=True)

# Sample data for the table
table_data = [['Product_Code ', 'Product_Name', 'Price','button'], ['001', 'Product 1', 10,CTkButton(table_frame,text = 'fail').pack()], ['002', 'Product 2', 20,CTkButton(table_frame,text = 'fail').pack()]]
# Create a table
table = CTkTable(master=table_frame, values=table_data, colors=["#191D32", "#282F44"], header_color="#2A8C55", hover_color="#030616", width=200)
table.pack()

root.mainloop()
