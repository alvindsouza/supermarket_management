from customtkinter import *
import tkinter
from CTkTable import CTkTable
from PIL import Image

class User:
    def __init__(self):
        self.root = CTk()
        self.root.geometry("1056x650")
        self.widget_color = '#2e3440'
        self.selected_float_color = '#d8dee9'#same as widget_color
        self.float_color = '#2f6690'
        self.button_color = '#3b4252'
        self.dttxt_color = '#1a1a1a' 
        self.secondary_widget_color = '#36414c'
        self.inter_widget_color = '#241d25'
        self.root.title("SuperMarket Management System")
        self.root.geometry("1056x650")
        self.root.resizable(0,0)

    def light(self):
        theme = 'light'
        main_frame.configure( fg_color="#fff")
        self.root.set_appearance_mode(theme)

    def dark(self):
        theme = 'dark'
        # main_frame.configure( fg_color="#f2f7fb")
        self.root.set_appearance_mode(theme)

    def clear_frame(frame):
        for wid in frame.winfo_children():
            wid.destroy()
    def sidebar_reset():
        create_order_button.configure(fg_color=button_color, text_color='white' , hover_color=self.float_color)
        order_button.configure(fg_color=button_color, text_color='white' ,hover_color=self.float_color)  
        settings_button.configure(fg_color=button_color, text_color='white' ,hover_color=self.float_color)    

    def order_clicked():
        sidebar_reset()
        clear_frame(main_frame) 
        order_button.configure(fg_color='white', text_color=dttxt_color, hover_color=selected_float_color)

        title_frame = CTkFrame(master=main_frame, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Orders", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")

        CTkButton(master=title_frame, text="+ New Order",  font=("Arial Black", 15), text_color="#fff", fg_color=inter_widget_color, hover_color="#207244").pack(anchor="ne", side="right")

        metrics_frame = CTkFrame(master=main_frame, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x",  padx=27, pady=(36, 0))

        orders_metric = CTkFrame(master=metrics_frame, fg_color=inter_widget_color, width=200, height=60)
        orders_metric.grid_propagate(0)
        orders_metric.pack(side="left")

        logitics_img_data = Image.open("logistics_icon.png")
        logistics_img = CTkImage(light_image=logitics_img_data, dark_image=logitics_img_data, size=(43, 43))

        CTkLabel(master=orders_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

        CTkLabel(master=orders_metric, text="Orders", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=orders_metric, text="123", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))


        shipped_metric = CTkFrame(master=metrics_frame, fg_color=inter_widget_color, width=200, height=60)
        shipped_metric.grid_propagate(0)
        shipped_metric.pack(side="left",expand=True, anchor="center")

        shipping_img_data = Image.open("shipping_icon.png")
        shipping_img = CTkImage(light_image=shipping_img_data, dark_image=shipping_img_data, size=(43, 43))

        CTkLabel(master=shipped_metric, image=shipping_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

        CTkLabel(master=shipped_metric, text="Shipping", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=shipped_metric, text="91", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

        delivered_metric = CTkFrame(master=metrics_frame, fg_color=inter_widget_color, width=200, height=60)
        delivered_metric.grid_propagate(0)
        delivered_metric.pack(side="right",)

        delivered_img_data = Image.open("delivered_icon.png")
        delivered_img = CTkImage(light_image=delivered_img_data, dark_image=delivered_img_data, size=(43, 43))

        CTkLabel(master=delivered_metric, image=delivered_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

        CTkLabel(master=delivered_metric, text="Delivered", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=delivered_metric, text="23", text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))

        search_container = CTkFrame(master=main_frame, height=50, fg_color=secondary_widget_color)
        search_container.pack(fill="x", pady=(45, 0), padx=27)

        CTkEntry(master=search_container, width=305, placeholder_text="Search Order", border_color="#2A8C55", border_width=2).pack(side="left", padx=(13, 0), pady=15)

        CTkComboBox(master=search_container, width=125, values=["Date", "Most Recent Order", "Least Recent Order"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)
        CTkComboBox(master=search_container, width=125, values=["Status", "Processing", "Confirmed", "Packing", "Shipping", "Delivered", "Cancelled"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff").pack(side="left", padx=(13, 0), pady=15)

        table_data = [
            ["Order ID", "Item Name", "Customer", "Address", "Status", "Quantity"],
            ['3833', 'Smartphone', 'Alice', '123 Main St', 'Confirmed', '8'],
        ]

        table_frame = CTkScrollableFrame(master=main_frame, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21)
        if theme == 'light':
            table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4")
        else:
            table = CTkTable(master=table_frame, values=table_data, colors=["#191D32", "#282F44"], header_color="#2A8C55", hover_color="#030616")
        table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        table.pack(expand=True)
    def create_clicked(self):
        sidebar_reset()
        clear_frame(main_frame) 

        create_order_button.configure(fg_color='#fff', text_color="#2A8C55", hover_color="#eee")  


        CTkLabel(master=main_frame, text="Create Order", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=main_frame, text="Item Name", font=("Arial Bold", 17), text_color="#52A476").pack(anchor="nw", pady=(25,0), padx=27)

        CTkEntry(master=main_frame, fg_color="#F0F0F0", border_width=0).pack(fill="x", pady=(12,0), padx=27, ipady=10)


        grid = CTkFrame(master=main_frame, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31,0))

        CTkLabel(master=grid, text="Customer", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=0, sticky="w")
        CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0, width=300).grid(row=1, column=0, ipady=10)

        CTkLabel(master=grid, text="Address", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=1, sticky="w", padx=(25,0))
        CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0, width=300).grid(row=1, column=1, ipady=10, padx=(24,0))

        CTkLabel(master=grid, text="Status", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=2, column=0, sticky="w", pady=(38, 0))

        status_var = tkinter.IntVar(value=0)

        CTkRadioButton(master=grid, variable=status_var, value=0, text="Confirmed", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(row=3, column=0, sticky="w", pady=(16,0))
        CTkRadioButton(master=grid, variable=status_var, value=1,text="Pending", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(row=4, column=0, sticky="w", pady=(16,0))
        CTkRadioButton(master=grid, variable=status_var, value=2,text="Cancelled", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(row=5, column=0, sticky="w", pady=(16,0))

        CTkLabel(master=grid, text="Quantity", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=6, column=0, sticky="w", pady=(42, 0))

        quantity_frame = CTkFrame(master=grid, fg_color="transparent")
        quantity_frame.grid(row=7, column=0, pady=(21,0), sticky="w")
        CTkButton(master=quantity_frame, text="-", width=25, fg_color="#2A8C55", hover_color="#207244", font=("Arial Black", 16)).pack(side="left", anchor="w")
        CTkLabel(master=quantity_frame, text="01", text_color="#2A8C55", font=("Arial Black", 16)).pack(side="left", anchor="w", padx=10)
        CTkButton(master=quantity_frame, text="+", width=25,  fg_color="#2A8C55",hover_color="#207244", font=("Arial Black", 16)).pack(side="left", anchor="w")

        CTkLabel(master=grid, text="Description", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=2, column=1, sticky="w", pady=(42, 0), padx=(25,0))

        CTkTextbox(master=grid, fg_color="#F0F0F0", width=300, corner_radius=8).grid(row=3, column=1, rowspan=5, sticky="w", pady=(16, 0), padx=(25,0), ipady=10)

        actions= CTkFrame(master=main_frame, fg_color="transparent")
        actions.pack(fill="both")

        CTkButton(master=actions, text="Back", width=300, fg_color="transparent", font=("Arial Bold", 17), border_color="#2A8C55", hover_color="#eee", border_width=2, text_color="#2A8C55").pack(side="left", anchor="sw", pady=(30,0), padx=(27,24))
        CTkButton(master=actions, text="Create", width=300, font=("Arial Bold", 17), hover_color="#207244", fg_color="#2A8C55", text_color="#fff").pack(side = "left", anchor="se", pady=(30,0), padx=(0,27))
    def settings_clicked(self):
        sidebar_reset()
        clear_frame(main_frame) 
        settings_button.configure(fg_color='#fff', text_color="#2A8C55", hover_color="#eee")  

        CTkLabel(master=main_frame, text="Settings", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29,0), padx=27)
        grid = CTkFrame(master=main_frame, fg_color="#EEEEEE")
        grid.pack(fill="both", padx=(30,650), pady=(20,100))
        status_var = tkinter.IntVar(value=0)
        CTkLabel(master=grid, text="Theme", font=("Arial Bold", 17), text_color="#52A476").grid(row=1, column=0, sticky="w",padx=10, pady=(10,0))
        CTkRadioButton(master=grid, variable=status_var, value=0, text="Light", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244",command=light).grid(row=3, column=0, sticky="w",padx=15, pady=(16,0))
        CTkRadioButton(master=grid, variable=status_var, value=1,text="Dark", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244",command=dark).grid(row=4, column=0, sticky="w",padx=15 ,pady=(16,10))
    
    def sidebar():
        theme = 'let'
        if theme == 'light':
            main_frame = CTkFrame(master=self.root, fg_color=widget_color,  width=820, height=650, corner_radius=0)
            light()
        else:
            main_frame = CTkFrame(master=self.root, fg_color=widget_color,  width=820, height=630, corner_radius=30)
            dark()
        main_frame.pack_propagate(0)
        main_frame.pack(side='right')
        main_frame.place(x= 225,y=10)

        # intial_login()

        sidebar_frame = CTkFrame(master=self.root, fg_color=widget_color,  width=206, height=630, corner_radius=30)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")
        sidebar_frame.place(x= 10,y=10)
        # logo_img_data = Image.open("logo.png")
        # logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

        # CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        person_img_data = Image.open("person_icon.png")
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data, size=(60, 60))
        CTkButton(master=sidebar_frame, image=person_img, text="Account", fg_color=button_color, font=("Arial Bold", 20), hover_color=self.float_color, anchor="w",corner_radius=30,width=180).pack(anchor="center", ipady=5, pady=(16, 0))
        analytics_img_data = Image.open("analytics_icon.png")
        analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

        CTkButton(master=sidebar_frame, image=analytics_img, text="Dashboard", fg_color=button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180).pack(anchor="center", ipady=5, pady=(60, 0))

        package_img_data = Image.open("package_icon.png")
        package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)
        order_button = CTkButton(master=sidebar_frame, image=package_img, text="Orders", fg_color=button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=order_clicked)
        order_button.pack(anchor="center", ipady=5, pady=(16, 0))

        list_img_data = Image.open("list_icon.png")
        list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
        create_order_button = CTkButton(master=sidebar_frame, image=list_img, text="Create Order", fg_color=button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=create_clicked)
        create_order_button.pack(anchor="center", ipady=5, pady=(16, 0))
        returns_img_data = Image.open("returns_icon.png")
        returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
        CTkButton(master=sidebar_frame, image=returns_img, text="Returns", fg_color=button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180).pack(anchor="center", ipady=5, pady=(16, 0))

        settings_img_data = Image.open("settings_icon.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        settings_button = CTkButton(master=sidebar_frame, image=settings_img, text="Settings", fg_color=button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=settings_clicked)
        settings_button.pack(anchor="center", ipady=5, pady=(16, 0))
    def run(self):
        self.root.mainloop()

user = User()
user.run()
