import customtkinter as ctk
from PIL import Image
import pywinstyles

# Initialize the main window
root = ctk.CTk()
root.geometry("800x600")

# Load the background image using CTkImage
bg_image = ctk.CTkImage(light_image=Image.open("images/side-img.png"), size=(800, 600))

# Create a label to display the background image
bg_label = ctk.CTkLabel(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Create a frame on top of the background
frame = ctk.CTkFrame(root, width=400, height=300, corner_radius=20, fg_color="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Set the opacity of the frame using pywinstyles
pywinstyles.set_opacity(frame, value=0.5)  # 0.5 for 50% transparency

# Add some widgets to the frame (optional)
label = ctk.CTkLabel(frame, text="This is a frame")
label.pack(pady=20)

button = ctk.CTkButton(frame, text="Click Me")
button.pack(pady=20)

# Run the application
root.mainloop()
