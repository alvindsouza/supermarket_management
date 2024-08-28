import customtkinter as ctk

# Create the main window
root = ctk.CTk()

# Create a CTkEntry widget
entry = ctk.CTkEntry(root, placeholder_text="Enter text here")
entry.pack(padx=20, pady=20)

# Insert data into the CTkEntry widget
entry.insert(0, "Hello, CustomTkinter!")

# Run the main loop
root.mainloop()