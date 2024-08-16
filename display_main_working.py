from customtkinter import *
import tkinter
from CTkTable import CTkTable
from PIL import Image
import csv
import mysql.connector as ms
import sys

def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

import mysql.connector as ms

class Functions:
    def __init__(self, database):
        self.database = database
        self.db = ms.connect(
            user='root',
            password='12345',
            host='localhost'
        )
        self.cursor = self.db.cursor()
        self.create_database_if_not_exists()
        self.cursor.execute('USE ' + self.database)

    def create_database_if_not_exists(self):
        self.cursor.execute("SHOW DATABASES LIKE %s", (self.database,))
        if self.cursor.fetchone() is None:
            # Create the database if it doesn't exist
            self.cursor.execute("CREATE DATABASE " + self.database)
            
            self.cursor.execute('USE ' + self.database)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS employee (
                    employee_id INT PRIMARY KEY AUTO_INCREMENT,
                    employee_name VARCHAR(50) NOT NULL,
                    employee_type ENUM('full-time', 'part-time', 'contractor') NOT NULL,
                    employee_availability ENUM('available', 'unavailable'),
                    employee_shift_type ENUM('morning','evening','night' ,'flexible' ) NOT NULL,
                    employee_pay DECIMAL(10, 2) NOT NULL
                )
            """)

            employees = [
            ("Olivia Lee", "full-time", "available", "morning", 22.00),
            ("Ethan Hall", "part-time", "unavailable", "night", 18.00),
            ("Lily Patel", "contractor", "available", "evening", 35.00),
            ("Alexander Brown", "full-time", "available", "morning", 28.00),
            ("Sophia Martin", "part-time", "unavailable", "night", 19.00),
            ("Jackson Davis", "contractor", "available", "evening", 38.00),
            ("Mia White", "full-time", "available", "morning", 25.00),
            ("Isabella Taylor", "part-time", "unavailable", "night", 20.00),
            ("Noah Harris", "contractor", "available", "evening", 42.00),
            ("Charlotte Walker", "full-time", "available", "morning", 30.00),
            ("Gabriel Jackson", "part-time", "unavailable", "night", 21.00),
            ("Julia Thompson", "contractor", "available", "evening", 45.00),
            ("Logan Brooks", "full-time", "available", "flexible", 32.00),
            ("Ava Lewis", "part-time", "unavailable", "night", 22.00),
            ("Elijah Hall", "contractor", "available", "night", 48.00),
            ("Harper Davis", "full-time", "available", "morning", 29.00),
            ("Landon Martin", "part-time", "unavailable", "night", 23.00),
            ("Piper Brown", "contractor", "available", "evening", 50.00),
            ("Riley Taylor", "full-time", "available", "morning", 31.00),
            ("Savannah White", "part-time", "unavailable", "night", 24.00)
            ]

            insert_query = """
                INSERT INTO employee 
                (employee_name, employee_type, employee_availability, employee_shift_type, employee_pay) 
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.executemany(insert_query, employees)

            # Commit the changes
            self.db.commit()
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                Product_Code INT PRIMARY KEY,
                Product_Name VARCHAR(50),
                Expiry_Date DATE,
                Price DECIMAL(5, 2),
                Supplier_Code VARCHAR(10)
            )
            ''')

            # Data to be inserted
            data = [ (8147, 'Whole Wheat', '2024-02-20', 2.5, 5, 'S001'),
                    (3519, 'Brown Sugar', '2024-08-15', 1.8, 2, 'S002'),
                    (2701, 'Green Tea', '2024-11-10', 3.2, 5, 'S003'),
                    (9318, 'Almond Milk', '2024-05-25', 4.5, 13, 'S004'),
                    (1189, 'Quinoa', '2024-09-01', 5.0, 15, 'S005'),
                    (4672, 'Olive Oil', '2024-03-18', 8.0, 15, 'S001'),
                    (6192, 'Coconut Oil', '2024-06-22', 7.5, 7, 'S002'),
                    (8231, 'Apple Cider', '2024-10-15', 6.0, 2, 'S003'),
                    (2756, 'Banana Bread', '2024-04-12', 3.5, 3, 'S004'),
                    (9821, 'Granola', '2024-07-20', 4.2, 6, 'S005'),
                    (1174, 'Protein Powder', '2024-01-15', 15.0, 3, 'S001'),
                    (6582, 'Peanut Butter', '2024-09-25', 8.5, 12, 'S002'),
                    (3819, 'Jelly', '2024-05-10', 2.0, 3, 'S003'),
                    (1928, 'Honey', '2024-11-05', 5.5, 13, 'S004'),
                    (7421, 'Almond Butter', '2024-03-25', 10.0, 11, 'S005'),
                    (2684, 'Cashew Nuts', '2024-08-01', 12.0, 5, 'S001'),
                    (9832, 'Walnuts', '2024-06-15', 11.0, 1, 'S002'),
                    (1181, 'Pecans', '2024-10-01', 10.5, 1, 'S003'),
                    (4675, 'Brazil Nuts', '2024-04-20', 9.0, 10, 'S004'),
                    (6195, 'Pistachios', '2024-07-15', 8.5, 6, 'S005'),
                    (3511, 'Dried Cran', '2024-02-15', 5.0, 8, 'S001'),
                    (8142, 'Apricots', '2024-09-10', 4.5, 4, 'S002'),
                    (2708, 'Prunes', '2024-05-25', 4.0, 6, 'S003'),
                    (9315, 'Raisins', '2024-11-15', 3.5, 2, 'S004'),
                    (1186, 'Figs', '2024-03-10', 6.0, 8, 'S005'),
                    (4678, 'Dates', '2024-08-20', 5.5, 14, 'S001'),
                    (6198, 'Coconut Flakes', '2024-06-10', 4.2, 6, 'S002'),
                    (8235, 'Oatmeal', '2024-10-20', 4.0, 12, 'S003'),
                    (2759, 'Brown Rice', '2024-04-15', 2.5, 11, 'S004'),
                    (9825, 'Quinoa Flakes', '2024-07-25', 5.0, 11, 'S005'),
                    (1177, 'Cereal', '2024-01-20', 3.0, 5, 'S001'),
                    (3822, 'Energy Bars', '2024-05-20', 5.0, 13, 'S003'),
                    (1929, 'Trail Mix', '2024-11-10', 4.2, 13, 'S004'),
                    (7423, 'Dried Fruits', '2024-03-15', 6.0, 10, 'S005'),
                    (2687, 'Nuts Mix', '2024-08-25', 7.5, 7, 'S001'),
                    (9834, 'Seeds Mix', '2024-06-20', 6.5, 4, 'S002'),
                    (1183, 'Coffee', '2024-10-25', 8.0, 4, 'S003'),
                    (4679, 'Tea', '2024-04-25', 7.0, 14, 'S004'),
                    (6199, 'Chocolate', '2024-07-20', 9.0, 2, 'S005'),
                    (3513, 'Baking Powder', '2024-02-25', 2.0, 4, 'S001'),
                    (8144, 'Baking Soda', '2024-09-20', 1.8, 12, 'S002'),
                    (2710, 'Salt', '2024-05-30', 1.5, 9, 'S003'),
                    (9317, 'Sugar', '2024-11-20', 2.2, 4, 'S004'),
                    (1188, 'Flour', '2024-03-20', 3.0, 11, 'S005'),
                    (4681, 'Yeast', '2024-08-30', 2.5, 1, 'S001'),
                    (6201, 'Vanilla', '2024-06-25', 3.5, 9, 'S002'),
                    (8237, 'Cinnamon', '2024-10-30', 4.0, 9, 'S003'),
                    (2761, 'Nutmeg', '2024-04-30', 3.8, 5, 'S004'),
                    (9827, 'Ginger', '2024-07-30', 4.2, 3, 'S005'),
                    (1179, 'Turmeric', '2024-01-25', 3.5, 14, 'S001'),
                    (6587, 'Paprika', '2024-09-25', 4.0, 10, 'S002'),
                    (3824, 'Garlic Powder', '2024-05-30', 3.2, 3, 'S003'),
                    (1931, 'Onion Powder', '2024-11-25', 3.0, 7, 'S004'),
                    (7425, 'Chili Powder', '2024-03-25', 3.5, 3, 'S005'),
                    (2690, 'Cumin', '2024-08-30', 3.8, 6, 'S001'),
                    (9836, 'Coriander', '2024-06-30', 4.2, 9, 'S002'),
                    (1185, 'Basil', '2024-10-30', 4.5, 5, 'S003'),
                    (4683, 'Oregano', '2024-04-30', 4.0, 2, 'S004'),
                    (6203, 'Thyme', '2024-07-30', 4.2, 7, 'S005'),
                    (3515, 'Rosemary', '2024-02-28', 4.5, 7, 'S001'),
                    (8146, 'Sage', '2024-09-28', 4.2, 13, 'S002'),
                    (2712, 'Parsley', '2024-05-31', 4.0, 4, 'S003'),
                    (9319, 'Dill', '2024-11-28', 4.2, 15, 'S004'),
                    (1190, 'Bay Leaves', '2024-03-28', 4.5, 5, 'S005'),
                    (1011, 'Ground Beef', '2024-03-15', 6.99, 15, 'M001'),
                    (1022, 'Boneless Chicken', '2024-04-10', 5.99, 12, 'M002'),
                    (1033, 'Pork Sausages', '2024-05-05', 7.49, 7, 'M003'),
                    (1044, 'Ribeye Steaks', '2024-06-01', 12.99, 7, 'M004'),
                    (1055, 'Salmon Fillets', '2024-07-15', 14.99, 13, 'M005'),
                    (1066, 'Bacon Strips', '2024-08-10', 4.99, 1, 'M001'),
                    (1077, 'Turkey Breast', '2024-09-05', 6.49, 5, 'M002'),
                    (1088, 'Lamb Chops', '2024-10-01', 10.99, 13, 'M003'),
                    (1099, 'Chicken Wings', '2024-11-15', 5.99, 9, 'M004')]
            # Insert data into the inventory table
            self.cursor.executemany('''
            INSERT INTO Product (Product_Code, Product_Name, Expiry_Date, Price, Supplier_Code)
            VALUES (%s, %s, %s, %s, %s)
            ''', data) 
            self.db.commit()

    def fetch(self, condition='',fun='employee',optional_condition = ''):

        if condition == '':
            self.cursor.execute(f'SELECT * FROM {fun}')
        else:
            print(f"SELECT * FROM {fun} WHERE {fun +'_name'} LIKE '{'%' + condition + '%'}'{optional_condition} order by {fun +'_name'};")
            self.cursor.execute(f"SELECT * FROM {fun} WHERE {fun+'_name'} LIKE '{'%' + condition + '%'}' order by {fun+'_name'}")
        for element in self.cursor.fetchall():
            yield element

    def fetch_available(self):
        self.cursor.execute("select Count(*) from employee where employee_availability = 'available'")
        return self.cursor.fetchall()



class display(Functions):
    def __init__(self):
        self.logn  = CTk()
        self.logn.geometry(CenterWindowToDisplay(self.logn,600, 417, self.logn._get_window_scaling()))
        self.widget_color = '#2e3440'
        self.float_color = '#d8dee9'#same as widget_color
        self.float_color = '#2f6690'
        self.button_color = '#3b4252'
        self.dttxt_color = '#1a1a1a' 
        self.secondary_widget_color = '#36414c'
        self.inter_widget_color = '#241d25'
        self.logn.title("SuperMarket Management System")
        self.logn.resizable(0,0)
        self.prev= ''
        self.current = ''
        self.cur_condition1=''
        self.prev_condition1=''
        self.cur_condition2=''
        self.prev_condition2=''
        self.logn.protocol('WM_DELETE_WINDOW',self.shutwindow)  
    def clear_frame(self,frame):
        for wid in frame.winfo_children():
            wid.destroy()
    def Login(self):
        found = False
        with open('login.csv', 'r') as f:
            reader = csv.reader(f) 
            for row in reader:
                if row[0] == self.log_email.get():
                    found = True
                    if row[1] == self.log_password.get():
                        print('login sucessful')
                        self.new_app()
                    else:
                        self.error.configure(text="*Password entered \n is incorrect", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
            if found == False:
                self.error.configure(text="*Email entered does not \n have an account", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15) )
    def intial_login(self):
        self.clear_frame(self.logn)
        side_img_data = Image.open("side-img.png")
        email_icon_data = Image.open("email-icon.png")
        password_icon_data = Image.open("password-icon.png")
        google_icon_data = Image.open("google-icon.png")

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
        password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))
        google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))

        CTkLabel(master=self.logn, text="", image=side_img).pack(expand=True, side="left")

        self.frame = CTkFrame(master=self.logn, width=300, height=480, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(expand=True, side="right")

        CTkLabel(master=self.frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(30, 5), padx=(25, 0))
        CTkLabel(master=self.frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=self.frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        self.log_email = CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.log_email.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=self.frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.log_password = CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
        self.log_password.pack(anchor="w", padx=(25, 0))
        
        self.error = CTkLabel(master=self.frame, text=" \n ",font=("Arial Bold", 15))
        self.error.pack(anchor="w", padx=(25, 0),pady=(20,5))
        CTkButton(master=self.frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=225,command=self.Login).pack(anchor="w", pady=(5, 0), padx=(25, 0))
        CTkButton(master=self.frame, text="Create Account", fg_color='#3b4252', hover_color='#2f6690', font=("Arial Bold", 12), text_color="#ffffff", width=225,command=self.create_account).pack(anchor="w", pady=(20, 0), padx=(25, 0))
    def check_pass(self):
            a,b =self.password.get(),self.confim_password.get()
            print(a,b)
            if '@' not in self.email.get():
                self.error.configure(text="*Enter Valid Email", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
            elif a != b:
                    self.error.configure(text="*Password is not equal to\n confirm password", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
            elif len(a)<8:
                self.error.configure(text="*Password length should \n be at least 8", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
            else:
                with open("login.csv", "r") as f:
                    reader = csv.reader(f)
                    sucess = True
                
                    for row in reader:
                        if row[0] == self.email.get():
                            self.error.configure(text="*Email already registered", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
                            sucess = False
                            break

                        # call login_page using dialog box
                    if sucess ==  True:             
                        with open("login.csv", "a+",newline= '') as f:
                            writer = csv.writer(f)
                            writer.writerow([self.email.get(),a])
                        self.intial_login()
                                
    def create_account(self):
        self.clear_frame(self.logn)

        side_img_data = Image.open("background_img2.png")
        email_icon_data = Image.open("email-icon.png")
        password_icon_data = Image.open("password-icon.png")
        google_icon_data = Image.open("google-icon.png")

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(314, 417))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
        password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))
        google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))

        CTkLabel(master=self.logn, text="", image=side_img).pack(expand=True, side="right")

        self.frame = CTkFrame(master=self.logn, width=300, height=480, fg_color="#ffffff")
        self.frame.pack_propagate(0)
        self.frame.pack(expand=True, side="right")

        CTkLabel(master=self.frame, text="Create Account", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(30, 5), padx=(25, 0))
        CTkLabel(master=self.frame, text="Enter your Details", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=self.frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(18, 0), padx=(25, 0))
        self.email = CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
        self.email.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=self.frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.password=CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
        self.password.pack(anchor="w", padx=(25, 0))

        CTkLabel(master=self.frame, text=" Confirm Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        self.confim_password=CTkEntry(master=self.frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*")
        self.confim_password.pack(anchor="w", padx=(25, 0))
        self.error = CTkLabel(master=self.frame, text=" \n ",font=("Arial Bold", 15))
        self.error.pack(anchor="w", padx=(25, 0),pady=(10,5))

        CTkButton(master=self.frame, text="Create Account", fg_color='#3b4252', hover_color='#2f6690', font=("Arial Bold", 12), text_color="#ffffff", width=225,command= self.check_pass).pack(anchor="w", pady=(10, 0), padx=(25, 0))
    def inventory(self):
        self.clear_frame(self.mainframe)
        title_frame = CTkFrame(master=self.mainframe, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Employees", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")

        metrics_frame = CTkFrame(master=self.mainframe, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x",  padx=27, pady=(36, 0))

        orders_metric = CTkFrame(master=metrics_frame, fg_color=self.inter_widget_color, width=300, height=60)
        orders_metric.grid_propagate(0)
        orders_metric.pack(side="left")

        logitics_img_data = Image.open("logistics_icon.png")
        logistics_img = CTkImage(light_image=logitics_img_data, dark_image=logitics_img_data, size=(43, 43))

        CTkLabel(master=orders_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

        CTkLabel(master=orders_metric, text="Available Employees", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=orders_metric, text=str(self.database.fetch_available()[0][0]), text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))


#SEARCH BAR

        search_container = CTkFrame(master=self.mainframe, height=50, fg_color=self.secondary_widget_color)
        search_container.pack(fill="x", pady=(45, 0), padx=27)

        self.search = CTkEntry(master=search_container, width=305, placeholder_text="Search Employee", border_color="#2A8C55", border_width=2)
        self.search.pack(side="left", padx=(13, 0), pady=15)
        self.avail =  CTkComboBox(master=search_container, width=125,state= 'readonly',values=["Availability", "Available", "Unavailable"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff")
        self.avail.set('Availability')
        self.avail.pack(side="left", padx=(13, 0), pady=15)
        self.shift =  CTkComboBox(master=search_container, width=125,state= 'readonly', values=["Shift", "Morning", "Evening", "Night"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff")
        self.shift.set("Shift")
        self.shift.pack(side="left", padx=(13, 0), pady=15)

        self.table_data = [
            ['Product_Code ', 'Product_Name','Expiry_Date', 'Price','Quantity','Supplier_Code']
        ]
        for emp in self.database.fetch(fun='Product'):
            self.table_data.append(list(emp))

        self.update_entry(condition = 'product')
        self.table_frame = CTkScrollableFrame(master=self.mainframe, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=20, pady=21)
        
        self.table = CTkTable(master=self.table_frame, values=self.table_data, colors=["#191D32", "#282F44"], header_color="#2A8C55", hover_color="#030616")
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True)
    def update_entry(self,condition): 
        if self.prev != self.search.get() or self.prev_condition1 != self.avail.get() or self.prev_condtition2 != self.shift.get():

            self.current = self.prev = self.search.get()
            self.cur_condition1 = self.prev_condition1 = self.avail.get()
            self.cur_condition2 = self.prev_condtition2 = self.shift.get()

            if condition == "employee":
                self.table_data = [['employee_id','employee_name', 'employee_type', 'employee_availability', 'employee_shift_type', 'employee_pay']
                ]
            else:
                self.table_data = [['Product_Code ', 'Product_Name','Expiry_Date', 'Price','Supplier_Code']]
            for emp in self.database.fetch(self.current,fun=condition):
                self.table_data.append(list(emp))
                self.table.destroy()
            self.table = CTkTable(master=self.table_frame, values=self.table_data, colors=["#191D32", "#282F44"], header_color="#2A8C55", hover_color="#030616")
            self.table.pack(expand=True)

        self.root.after(500,lambda: self.update_entry(condition = condition))  # Update every 1 second

    def add_employee(self):
        self.new_win = CTkToplevel(self.root)
        self.new_win.protocol('WM_DELETE_WINDOW',self.shutwindow)
        self.new_win.resizable(0,0) 
        self.uni_frame = CTkFrame(master = self.new_win,fg_color = self.widget_color,corner_radius = 30)
        CTkLabel(master=self.uni_frame, text="Add Employee", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=self.uni_frame, text="Employee Name", font=("Arial Bold", 17), text_color="#52A476").pack(anchor="nw", pady=(25,0), padx=27)

        CTkEntry(master=self.uni_frame, fg_color="#F0F0F0", border_width=0).pack(fill="x", pady=(12,0), padx=27, ipady=10)

        grid = CTkFrame(master=self.uni_frame, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31,0))

        CTkLabel(master=grid, text="Contract type", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=0, sticky="w")
        self.avail =  CTkComboBox(master=grid, width=125,state= 'readonly',values=["Contract Type",'full-time', 'part-time', 'contractor'], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff")
        self.avail.set('Contract Type')
        self.avail.grid(row=3, column=0 ,sticky="w",pady=5)

        CTkLabel(master=grid, text="Shift Type", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=1, sticky="w",padx = (150,250))
        self.shift =  CTkComboBox(master=grid, width=125,state= 'readonly', values=["Shift", "Morning", "Evening", "Night"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff")
        self.shift.set("Shift")
        self.shift.grid(row=3, column=1 , sticky="w",pady=5,padx = 150)
        CTkLabel(master=grid, text="Salary", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=2, sticky="w")
        CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0).grid(row=3, column=2, sticky="w")
     
        actions= CTkFrame(master=self.uni_frame, fg_color="transparent")
        actions.pack(fill="both")

        CTkButton(master=actions, text="Back", width=300, fg_color="transparent", font=("Arial Bold", 17), border_color="#2A8C55", hover_color="#eee", border_width=2, text_color="#2A8C55").pack(side="left", anchor="sw", pady=(50,0), padx=(100,24))
        CTkButton(master=actions, text="Create", width=300, font=("Arial Bold", 17), hover_color="#207244", fg_color="#2A8C55", text_color="#fff").pack(side = "left", anchor="se", pady=(30,0), padx=(0,27))
        self.uni_frame.pack()
    def remove_employee(self):
        self.clear_frame(self.mainframe)
        # self.manage_employee_button.configure(fg_color='#fff', text_color="#2A8C55", hover_color="#eee")  

        CTkLabel(master=self.mainframe, text="Delete Employee", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=self.mainframe, text="Employee Name or ID22222222222222222222222", font=("Arial Bold", 17), text_color="#52A476").pack(anchor="nw", pady=(25,0), padx=27)

        CTkEntry(master=self.mainframe, fg_color="#F0F0F0", border_width=0).pack(fill="x", pady=(12,0), padx=27, ipady=10)

        actions= CTkFrame(master=self.mainframe, fg_color="transparent")
        actions.pack(fill="both")

        CTkButton(master=actions, text="Back", width=300, fg_color="transparent", font=("Arial Bold", 17), border_color="#2A8C55", hover_color="#eee", border_width=2, text_color="#2A8C55").pack(side="left", anchor="sw", pady=(50,0), padx=(100,24))
        CTkButton(master=actions, text="Delete", width=300, font=("Arial Bold", 17), hover_color="#207244", fg_color="#2A8C55", text_color="#fff").pack(side = "left", anchor="se", pady=(30,0), padx=(0,27))
        
    def settings_clicked(self):
        self.clear_frame(self.mainframe)

        self.settings_button.configure(fg_color='#fff', text_color="#2A8C55", hover_color="#eee")  

        CTkLabel(master=self.mainframe, text="Settings", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", pady=(29,0), padx=27)
        grid = CTkFrame(master=self.mainframe, fg_color=self.inter_widget_color)
        grid.pack(fill="both", padx=(30,650), pady=(20,100))
        status_var = tkinter.IntVar(value=0)
        CTkLabel(master=grid, text="Theme", font=("Arial Bold", 17), text_color="#52A476").grid(row=1, column=0, sticky="w",padx=10, pady=(10,0))
        CTkRadioButton(master=grid, variable=status_var, value=0, text="Light", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(row=3, column=0, sticky="w",padx=15, pady=(16,0))
        CTkRadioButton(master=grid, variable=status_var, value=1,text="Dark", font=("Arial Bold", 14), text_color="#52A476", fg_color="#52A476", border_color="#52A476", hover_color="#207244").grid(row=4, column=0, sticky="w",padx=15 ,pady=(16,10))
        
    

    def order_clicked(self):
        self.database = Functions("test_db")
        self.database.create_database_if_not_exists()
        self.clear_frame(self.mainframe)
        title_frame = CTkFrame(master=self.mainframe, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Employees", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", side="left")

        metrics_frame = CTkFrame(master=self.mainframe, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x",  padx=27, pady=(36, 0))

        orders_metric = CTkFrame(master=metrics_frame, fg_color=self.inter_widget_color, width=300, height=60)
        orders_metric.grid_propagate(0)
        orders_metric.pack(side="left")

        logitics_img_data = Image.open("logistics_icon.png")
        logistics_img = CTkImage(light_image=logitics_img_data, dark_image=logitics_img_data, size=(43, 43))

        CTkLabel(master=orders_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

        CTkLabel(master=orders_metric, text="Available Employees", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=orders_metric, text=str(self.database.fetch_available()[0][0]), text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))
        
        

        CTkButton(master=metrics_frame, text="Add Employees", text_color="#fff", font=("Arial Black", 15),fg_color= self.inter_widget_color,image= logistics_img,width=300, height=60,command = self.add_employee ).pack(side = 'left',padx=27)
       
        

#SEARCH BAR

        search_container = CTkFrame(master=self.mainframe, height=50, fg_color=self.secondary_widget_color)
        search_container.pack(fill="x", pady=(45, 0), padx=27)

        self.search = CTkEntry(master=search_container, width=305, placeholder_text="Search Employee", border_color="#2A8C55", border_width=2)
        self.search.pack(side="left", padx=(13, 0), pady=15)
        self.avail =  CTkComboBox(master=search_container, width=125,state= 'readonly',values=["Availability", "Available", "Unavailable"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff")
        self.avail.set('Availability')
        self.avail.pack(side="left", padx=(13, 0), pady=15)
        self.shift =  CTkComboBox(master=search_container, width=125,state= 'readonly', values=["Shift", "Morning", "Evening", "Night"], button_color="#2A8C55", border_color="#2A8C55", border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color="#2A8C55", dropdown_text_color="#fff")
        self.shift.set("Shift")
        self.shift.pack(side="left", padx=(13, 0), pady=15)

        self.table_data = [
            ['employee_id','employee_name', 'employee_type', 'employee_availability', 'employee_shift_type', 'employee_pay']
        ]
        for emp in self.database.fetch():
            self.table_data.append(list(emp))
        self.table_frame = CTkScrollableFrame(master=self.mainframe, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=20, pady=21)
        
        self.table = CTkTable(master=self.table_frame, values=self.table_data, colors=["#191D32", "#282F44"], header_color="#2A8C55", hover_color="#030616")
        self.table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        self.table.pack(expand=True)
        self.update_entry('employee')
    def new_app(self):
        self.logn.destroy()
        self.root = CTk()
        self.root.geometry("1050x650")
        self.root.resizable(0,0)
        self.root.protocol('WM_DELETE_WINDOW',self.shutwindow)
        theme = 'let'
        if theme == 'light':
            self.mainframe = CTkFrame(master=self.root, fg_color=self.widget_color,  width=820, height=650, corner_radius=0)
            # light()
        else:
            self.mainframe = CTkFrame(master=self.root, fg_color=self.widget_color,  width=820, height=630, corner_radius=30)
            # dark()
        self.mainframe.pack_propagate(0)
        self.mainframe.pack(side='right')
        self.mainframe.place(x= 225,y=10)

        # intial_login()

        self.sidebar_frame = CTkFrame(master=self.root, fg_color=self.widget_color,  width=206, height=630, corner_radius=30)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")
        self.sidebar_frame.place(x= 10,y=10)
        # logo_img_data = Image.open("logo.png")
        # logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

        # CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        person_img_data = Image.open("person_icon.png")
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data, size=(60, 60))
        CTkButton(master=self.sidebar_frame, image=person_img, text="Account", fg_color=self.button_color, font=("Arial Bold", 20), hover_color=self.float_color, anchor="w",corner_radius=30,width=180).pack(anchor="center", ipady=5, pady=(16, 0))
        analytics_img_data = Image.open("analytics_icon.png")
        analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

        CTkButton(master=self.sidebar_frame, image=analytics_img, text="", fg_color=self.button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180).pack(anchor="center", ipady=5, pady=(60, 0))

        package_img_data = Image.open("package_icon.png")
        package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)
        self.order_button = CTkButton(master=self.sidebar_frame, image=package_img, text="Employees", fg_color=self.button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=self.order_clicked)
        self.order_button.pack(anchor="center", ipady=5, pady=(16, 0))

        list_img_data = Image.open("list_icon.png")
        list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
        self.manage_employee_button = CTkButton(master=self.sidebar_frame, image=list_img, text="Manage Employee", fg_color=self.button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=self.add_employee)
        self.manage_employee_button.pack(anchor="center", ipady=5, pady=(16, 0))
        returns_img_data = Image.open("returns_icon.png")
        returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
        CTkButton(master=self.sidebar_frame, image=returns_img, text="Inventory", fg_color=self.button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command= self.inventory).pack(anchor="center", ipady=5, pady=(16, 0))

        settings_img_data = Image.open("settings_icon.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        self.settings_button = CTkButton(master=self.sidebar_frame, image=settings_img, text="Settings", fg_color=self.button_color, font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=self.settings_clicked)
        self.settings_button.pack(anchor="center", ipady=5, pady=(16, 0))
        self.order_clicked()
        self.root.mainloop()
    
   
    def shutwindow(self):
        sys.exit()
        self.root.destroy()
        self.logn.destroy() 
    def run (self) :
        self.new_app()
        # self.intial_login()
        # self.logn.mainloop()

display().run()
