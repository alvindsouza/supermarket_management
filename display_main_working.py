from customtkinter import *
import tkinter
from CTkTable import CTkTable
from PIL import ImageTk,Image

import csv
import mysql.connector as ms
import sys
import os
import time
def CenterWindowToDisplay(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"
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

            employees = []
            with open("csv_files/csv_emp_data.csv",'r') as f:
                info = csv.reader(f)
                for i in info:
                    employees.append(i)

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
                Product_Code INT PRIMARY KEY AUTO_INCREMENT,
                Product_Name VARCHAR(50),
                Expiry_Date DATE,
                Price DECIMAL(5, 2),
                Quantity INT,
                Supplier_Code VARCHAR(10)
            )
            ''')

            # Data to be inserted
            data = []
            with open("csv_files/inventory_data.csv",'r') as f:
                info = csv.reader(f)
                for i in info:
                    data.append(i)
            # Insert data into the inventory table
            self.cursor.executemany('''
            INSERT INTO Product (Product_Name, Expiry_Date, Price, Quantity, Supplier_Code)
            VALUES (%s, %s, %s, %s, %s)
            ''', data) 
            self.db.commit()

    def fetch(self, condition=None):
        if condition[1] == 'Availability' and condition[2] == 'Shift' :
            self.cursor.execute(f"SELECT * FROM employee WHERE employee_name LIKE '{'%' + condition[0] + '%'}' order by employee_name")
        elif condition[1] != 'Availability' and condition[2] == 'Shift' :
            self.cursor.execute(f"SELECT * FROM employee WHERE employee_name LIKE '{'%' + condition[0] + '%'}' and employee_availability = '{condition[1]}' order by employee_name")
        elif  condition[1] == 'Availability' and condition[2] != 'Shift' :
            self.cursor.execute(f"SELECT * FROM employee WHERE employee_name LIKE '{'%' + condition[0] + '%'}'and employee_shift_type = '{condition[2]}'  order by employee_name")
        else:
            self.cursor.execute(f"SELECT * FROM employee WHERE employee_name LIKE '{'%' + condition[0] + '%'}'and employee_availability = '{condition[1]}' and employee_shift_type = '{condition[2]}' order by employee_name")
        for element in self.cursor.fetchall():
            yield element
    def fetch_inv(self,condition=None):
        if condition[1] == 'Order by' and condition[2] == 'Supplier Code' :
            self.cursor.execute(f"SELECT * FROM product WHERE Product_Name LIKE '{'%' + condition[0] + '%'}' order by Product_Name")
        elif condition[1] != 'Order by' and condition[2] == 'Supplier Code' :
            self.cursor.execute(f"SELECT * FROM product WHERE Product_Name LIKE '{'%' + condition[0] + '%'}'  order by {condition[1]}")
        elif  condition[1] == 'Order by' and condition[2] != 'Supplier Code' :
            self.cursor.execute(f"SELECT * FROM product WHERE Product_Name LIKE '{'%' + condition[0] + '%'}' and Supplier_Code = '{condition[2]}'  order by Product_Name")
        else:
            self.cursor.execute(f"SELECT * FROM product WHERE Product_Name LIKE '{'%' + condition[0] + '%'}' and Supplier_Code = '{condition[2]}' order by {condition[1]}")
        for element in self.cursor.fetchall():
            yield element
    def fetch_available(self):
        self.cursor.execute("select Count(*) from employee where employee_availability = 'available'")
        return self.cursor.fetchall()

class display(Functions):
    def __init__(self):
        self.logn  = CTk()
        self.logn.geometry(CenterWindowToDisplay(self.logn,600, 417))

        set_appearance_mode("light")  # Modes: system (default), light, dark
      
        self.text_color = '#4cc9f0'
        

        self.float_color = '#2f6690'
        self.dttxt_color = '#415a77' 
        self.widget_color = '#415a77'
        self.secondary_widget_color = '#2b2d42'
        self.inter_widget_color = '#2b2d42'
        self.table_hover_color = '#e4d9ff'
        self.table_color_light = ('#191D32','#282F44')
        self.table_color_dark = ('#89909f','#a9b4c2')
        self.table_color_light = self.table_color_dark

        self.logn.title("Login")
        self.logn.resizable(0,0)
        
        self.prev= ''
        self.current = ''
        self.cur_condition1=''
        self.prev_condition1=''
        self.cur_condition2=''
        self.prev_condition2=''
        self.run_search = None
        self.logn.protocol('WM_DELETE_WINDOW',self.logn.destroy)  
    def dark_mode(self):
        set_appearance_mode("dark")
        self.table_hover_color = '#e4d9ff'
        self.table_color_dark = ('#191D32','#282F44')
        self.table_color_light = self.table_color_dark
    def light_mode(self):
        set_appearance_mode("light")
        self.table_color_light = ('#89909f','#a9b4c2')
        self.table_hover_color = '#a9d6e5'

    def clear_frame(self,frame):
        for wid in frame.winfo_children():
            wid.destroy()
    def Login(self):
        found = False
        with open("csv_files/login.csv", 'r') as f:
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
        side_img_data = Image.open("images/side-img.png")
        email_icon_data = Image.open("images/email-icon.png")
        password_icon_data = Image.open("images/password-icon.png")
        google_icon_data = Image.open("images/google-icon.png")

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
                with open("csv_files/login.csv", "r") as f:
                    reader = csv.reader(f)
                    sucess = True
                
                    for row in reader:
                        if row[0] == self.email.get():
                            self.error.configure(text="*Email already registered", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
                            sucess = False
                            break

                        # call login_page using dialog box
                    if sucess ==  True:             
                        with open("csv_files/login.csv", "a+",newline= '') as f:
                            writer = csv.writer(f)
                            writer.writerow([self.email.get(),a])
                        self.intial_login()
    
    def remove_emp_sql(self):
        try:
    
            values = eval(self.emp.get())
            self.database.cursor.execute(f"SELECT * FROM employee WHERE employee_id = '{values}'")
            row = self.database.cursor.fetchone()

            if row:
                # Row exists, delete it
                self.database.cursor.execute(f"DELETE FROM employee WHERE employee_id  = '{values}'")
                self.database.db.commit()
                self.error.configure(text="Employee Successfully removed", text_color=self.dttxt_color, anchor="w", justify="left", font=("Arial Bold", 15))
            else:
                # Row does not exist
                self.error.configure(text="*Employee ID is incorrect", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
                # self.error.pack()
        except:
            self.error.configure(text="*Employee ID is incorrect", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
    def remove_prod_sql(self,k = 0):
        try:
            if k ==0:
                k = self.prod.get()
    
            values = eval(k)
            self.database.cursor.execute(f"SELECT * FROM product WHERE Product_Code = '{values}'")
            row = self.database.cursor.fetchone()

            if row:
                # Row exists, delete it
                self.database.cursor.execute(f"DELETE FROM product WHERE Product_Code  = '{values}'")
                self.database.db.commit()
                try:
                    self.error.configure(text="Product Successfully removed", text_color=self.dttxt_color, anchor="w", justify="left", font=("Arial Bold", 15))
                except:
                    pass

            else:
                try:

                    self.error.configure(text="*Employee ID is incorrect", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
                
                except:
                    pass
        except:
            try:

                self.error.configure(text="*Employee ID is incorrect", text_color="#d11149", anchor="w", justify="left", font=("Arial Bold", 15))
            except:
                pass

    def add_employee_sql(self):

        self.database.cursor.execute(f'''
        INSERT INTO employee (employee_name, employee_type, employee_availability, employee_shift_type, employee_pay) 
        VALUES ('{(self.emp_name.get())}','{str(self.con_type.get())}','available', '{str(self.shift_type.get())}', {int(self.salary.get())})
        ''')
        self.database.db.commit()
        self.error.configure(text="Employee Successfully Added", text_color=self.dttxt_color, anchor="w", justify="left", font=("Arial Bold", 15))
    def create_account(self):
        self.clear_frame(self.logn)

        side_img_data = Image.open("images/background_img2.png")
        email_icon_data = Image.open("images/email-icon.png")
        password_icon_data = Image.open("images/password-icon.png")
        google_icon_data = Image.open("images/google-icon.png")

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
        self.prev = 'test'
        title_frame = CTkFrame(master=self.mainframe, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Inventory", font=("Arial Black", 25), text_color=self.text_color).pack(anchor="nw", side="left")

        metrics_frame = CTkFrame(master=self.mainframe, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x",  padx=27, pady=(36, 0))

        search_container = CTkFrame(master=self.mainframe, height=50, fg_color=self.secondary_widget_color)
        search_container.pack(fill="x", pady=(45, 0), padx=27)

        self.search = CTkEntry(master=search_container, width=305, placeholder_text="Search Products", border_color=self.text_color)
        self.search.pack(side="left", padx=(13, 0), pady=15)
        self.avail =  CTkComboBox(master=search_container, width=125,state= 'readonly',values=["Order by", "Expiry_Date", "Quantity","Product_Code"], button_color=self.text_color, border_color=self.text_color, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color=self.text_color, dropdown_text_color="#fff")
        self.avail.set('Order by')
        self.avail.pack(side="left", padx=(13, 0), pady=15)
        self.shift =  CTkComboBox(master=search_container, width=125,state= 'readonly', values=["Supplier Code", "S001", "S002","S003","S004","S005"], button_color=self.text_color, border_color=self.text_color, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color=self.text_color, dropdown_text_color="#fff")
        self.shift.set("Supplier Code")
        self.shift.pack(side="left", padx=(13, 0), pady=15)
        CTkButton(master=metrics_frame, text="Add Product", text_color="#fff", font=("Arial Black", 15),fg_color= self.inter_widget_color,width=250, height=60,command = self.add_product ).pack(side = 'left',padx=10)
        CTkButton(master=metrics_frame, text="Remove Product", text_color="#fff", font=("Arial Black", 15),fg_color= self.inter_widget_color,width=250, height=60,command = self.remove_product).pack(side = 'left')
        self.table_data = [
            ['Product_Code ', 'Product_Name','Expiry_Date', 'Price','Quantity','Supplier_Code']
        ]
        self.table_frame = CTkScrollableFrame(master=self.mainframe, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=20, pady=21)
        
        self.table = CTkTable(master=self.table_frame, values=self.table_data, colors=self.table_color_light, header_color=self.widget_color, hover_color=self.table_hover_color)
        self.table.edit_row(0, text_color="#fff", hover_color=self.text_color)
        self.table.pack(expand=True)
        self.update_entry(condition = 'product')
    def update_entry(self,condition): 
        if self.prev != self.search.get() or self.prev_condition1 != self.avail.get() or self.prev_condtition2 != self.shift.get():

            self.current = self.prev = self.search.get()
            self.cur_condition1 = self.prev_condition1 = self.avail.get()
            self.cur_condition2 = self.prev_condtition2 = self.shift.get()

            if condition == "employee":
                self.table_data = [['employee_id','employee_name', 'employee_type', 'employee_availability', 'employee_shift_type', 'employee_pay']
                ]
                for emp in self.database.fetch((self.current,self.cur_condition1,self.cur_condition2)):
                    self.table_data.append(list(emp))
            else:
                self.table_data = [['Product_Code ', 'Product_Name','Expiry_Date', 'Price','Quantity','Supplier_Code']]
                for product in self.database.fetch_inv((self.current,self.cur_condition1,self.cur_condition2)):
                    self.table_data.append(list(product))
            self.table.destroy()
            self.table = CTkTable(master=self.table_frame, values=self.table_data, colors=self.table_color_light, header_color=self.text_color, hover_color=self.table_hover_color)
            self.table.pack(expand=True)

        self.run_search = self.root.after(500,lambda: self.update_entry(condition = condition))  # Update every 1 second
    def add_product(self):
        self.new_win = CTkToplevel(self.root)
        self.new_win.protocol('WM_DELETE_WINDOW',lambda: (self.refresh('product'),self.new_win.destroy()))
        self.new_win.resizable(0,0) 
        self.new_win.title('Add Product')
        self.new_win.wm_transient(self.root)
        self.uni_frame = CTkFrame(master = self.new_win,fg_color = self.widget_color,corner_radius = 30)
        CTkLabel(master=self.uni_frame, text="Add Product", font=("Arial Black", 25), text_color=self.text_color).pack(anchor="nw", pady=(29,0), padx=27)
        
        grid = CTkFrame(master=self.uni_frame, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31,0))
        
        CTkLabel(master=grid, text="Product Name", font=("Arial Bold", 17), text_color="#52A476").grid(row=0, column=0)

        self.prod_name  = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.prod_name.grid(row=1, column=0)

        CTkLabel(master=grid, text="Expiry_Date", font=("Arial Bold", 17), text_color="#52A476").grid(row=0, column=4)

        self.exp_date  = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.exp_date.grid(row=1, column=4)

        CTkLabel(master=grid, text="Price", font=("Arial Bold", 17), text_color="#52A476").grid(row=3, column=0)

        self.price  = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.price.grid(row=4, column=0)
        
        CTkLabel(master=grid, text="Quantity", font=("Arial Bold", 17), text_color="#52A476").grid(row=3, column=4)

        self.prod_quantity  = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.prod_quantity.grid(row=4, column=4)

        CTkLabel(master=grid, text="Supplier Code", font=("Arial Bold", 17), text_color="#52A476").grid(row=6, column=0)

        self.sup_code  = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.sup_code.grid(row=7, column=0)
        self.error = CTkLabel(master=grid,text="",font=("Arial Bold", 15),justify="left",anchor= 'w')
        self.error.grid(row=8, column=0)

        CTkButton(master=self.uni_frame, text="Create", width=300, font=("Arial Bold", 17), hover_color="#207244", fg_color=self.text_color, text_color="#fff",command= self.add_item_sql).pack(pady=(30,30))
        self.uni_frame.pack()
   
    def add_item_sql(self):
        
        c= ''
        for i in str(self.exp_date.get()).split('/')[::-1]:
            c+=i + '/'
        c= c[:-1]
        self.database.cursor.execute(f'''
            INSERT INTO Product (Product_Name, Expiry_Date, Price, Quantity, Supplier_Code)
            VALUES ('{self.prod_name.get()}', '{c}', {self.price.get()}, {self.prod_quantity.get()}, '{self.sup_code.get()}')
            ''') 
        self.database.db.commit()

    def add_employee(self):
        self.new_win = CTkToplevel(self.root)
        self.new_win.protocol('WM_DELETE_WINDOW',lambda: (self.refresh('employee'),self.new_win.destroy()))
        self.new_win.resizable(0,0) 
        self.new_win.title('Add Employee')
        self.new_win.wm_transient(self.root)
        self.uni_frame = CTkFrame(master = self.new_win,fg_color = self.widget_color,corner_radius = 30)
        CTkLabel(master=self.uni_frame, text="Add Employee", font=("Arial Black", 25), text_color=self.text_color).pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=self.uni_frame, text="Employee Name", font=("Arial Bold", 17), text_color="#52A476").pack(anchor="nw", pady=(25,0), padx=27)

        self.emp_name  = CTkEntry(master=self.uni_frame, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.emp_name.pack(fill="x", pady=(12,0), padx=27, ipady=10)

        grid = CTkFrame(master=self.uni_frame, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31,0))

        CTkLabel(master=grid, text="Contract type", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=0, sticky="w")
        self.con_type =  CTkComboBox(master=grid, width=125,state= 'readonly',values=["Contract Type",'full-time', 'part-time', 'contractor'], button_color=self.text_color, border_color=self.text_color, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color=self.text_color, dropdown_text_color="#fff")
        self.con_type.set('Contract Type')
        self.con_type.grid(row=3, column=0 ,sticky="w",pady=5)

        CTkLabel(master=grid, text="Shift Type", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=1, sticky="w",padx = (150,250))
        self.shift_type =  CTkComboBox(master=grid, width=125,state= 'readonly', values=["Shift", "Morning", "Evening", "Night"], button_color=self.text_color, border_color=self.text_color, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color=self.text_color, dropdown_text_color="#fff")
        self.shift_type.set("Shift")
        self.shift_type.grid(row=3, column=1 , sticky="w",pady=5,padx = 150)
        CTkLabel(master=grid, text="Salary", font=("Arial Bold", 17), text_color="#52A476", justify="left").grid(row=0, column=2, sticky="w")
        self.salary = CTkEntry(master=grid, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.salary.grid(row=3, column=2, sticky="w")
        self.error = CTkLabel(master=self.uni_frame,text="",font=("Arial Bold", 15),justify="left",anchor= 'w')
        self.error.pack(anchor="w", padx=(25, 0),pady=(20,5))
        actions= CTkFrame(master=self.uni_frame, fg_color="transparent")
        actions.pack(fill="both")

        CTkButton(master=actions, text="Create", width=300, font=("Arial Bold", 17), hover_color="#207244", fg_color=self.text_color, text_color="#fff",command= self.add_employee_sql).pack(pady=(30,30))
        self.uni_frame.pack()
    def remove_product(self):
        self.new_win = CTkToplevel(self.root)
        self.new_win.protocol('WM_DELETE_WINDOW',lambda: (self.refresh('product'),self.new_win.destroy()))
        self.new_win.resizable(0,0) 
        self.new_win.geometry('400x310')
        self.new_win.title('Remove Employee')
        self.new_win.wm_transient(self.root)
        self.uni_frame = CTkFrame(master = self.new_win,fg_color = self.widget_color,corner_radius = 30, width=250)
        self.uni_frame.pack(padx=(10,10),pady=(10,10),fill="y")
        # self.manage_employee_button.configure(fg_color='#fff', text_color=self.text_color, hover_color="#eee")  

        CTkLabel(master=self.uni_frame, text="Remove Product", font=("Arial Black", 25), text_color=self.text_color).pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=self.uni_frame, text="Product ID", font=("Arial Bold", 17), text_color="#52A476").pack(anchor="nw", pady=(25,0), padx=27)

        self.prod =CTkEntry(master=self.uni_frame, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.prod.pack(fill="x", pady=(12,0), padx=27, ipady=10)
        self.error = CTkLabel(master=self.uni_frame,text="",font=("Arial Bold", 15),justify="left",anchor= 'w')
        self.error.pack(anchor="w", padx=(25, 0),pady=(20,5))

        CTkButton(master=self.uni_frame, text="Remove", width=300, font=("Arial Bold", 17), hover_color="#207244", fg_color=self.text_color, text_color="#fff",command = self.remove_prod_sql).pack(anchor="s",pady=(5,20), padx=(100,100))
    
    def remove_employee(self):
        self.new_win = CTkToplevel(self.root)
        self.new_win.protocol('WM_DELETE_WINDOW',lambda: (self.refresh('employee'),self.new_win.destroy()))
        self.new_win.resizable(0,0) 
        self.new_win.geometry('400x310')
        self.new_win.title('Remove Employee')
        self.new_win.wm_transient(self.root)
        self.uni_frame = CTkFrame(master = self.new_win,fg_color = self.widget_color,corner_radius = 30, width=250)
        self.uni_frame.pack(padx=(10,10),pady=(10,10),fill="y")
        # self.manage_employee_button.configure(fg_color='#fff', text_color=self.text_color, hover_color="#eee")  

        CTkLabel(master=self.uni_frame, text="Delete Employee", font=("Arial Black", 25), text_color=self.text_color).pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=self.uni_frame, text="Employee ID", font=("Arial Bold", 17), text_color="#52A476").pack(anchor="nw", pady=(25,0), padx=27)

        self.emp =CTkEntry(master=self.uni_frame, fg_color="#F0F0F0", border_width=0,text_color="#000000")
        self.emp.pack(fill="x", pady=(12,0), padx=27, ipady=10)
        self.error = CTkLabel(master=self.uni_frame,text="",font=("Arial Bold", 15),justify="left",anchor= 'w')
        self.error.pack(anchor="w", padx=(25, 0),pady=(20,5))

        CTkButton(master=self.uni_frame, text="Remove", width=300, font=("Arial Bold", 17), hover_color="#207244", fg_color=self.text_color, text_color="#fff",command = self.remove_emp_sql).pack(anchor="s",pady=(5,20), padx=(100,100))
    def refresh(self,condition): 
        if condition == "employee":
            self.table_data = [['employee_id','employee_name', 'employee_type', 'employee_availability', 'employee_shift_type', 'employee_pay']
            ]
            for emp in self.database.fetch((self.current,self.cur_condition1,self.cur_condition2)):
                self.table_data.append(list(emp))
        else:
            self.table_data = [['Product_Code ', 'Product_Name','Expiry_Date', 'Price','Quantity','Supplier_Code']]
            for product in self.database.fetch_inv((self.current,self.cur_condition1,self.cur_condition2)):
                self.table_data.append(list(product))
        self.table.destroy()
        self.table = CTkTable(master=self.table_frame, values=self.table_data, colors=self.table_color_light, header_color=self.text_color, hover_color=self.table_hover_color)
        self.table.pack(expand=True)
    def billing(self):
        self.bill_items={}
        self.root.after_cancel(self.run_search)
        self.clear_frame(self.mainframe)

        self.prev = 'test'
        title_frame = CTkFrame(master=self.mainframe, fg_color="transparent",width = 200)
        
        title_frame.pack(anchor="n", fill="x",  padx=(27,0), pady=(29, 0))
        

        CTkLabel(master=title_frame, text="Billing", font=("Arial Black", 25), text_color=self.text_color).pack(anchor="nw", side="left")
        CTkButton(title_frame, text="Add Bill",width= 200,height = 30,command = self.bill_print).pack(anchor="ne", side="right",padx=100,fill = 'y',pady = 10)
        search_box = CTkFrame(master=self.mainframe, height=500,width = 350,fg_color="transparent")
        search_box.pack(expand=True,side ='left',anchor = 'w',pady=(45, 0),padx=(27,0))

        search_container = CTkFrame(master=search_box, height=50,width = 20,fg_color=self.secondary_widget_color)
        search_container.pack(anchor = 'w',pady=(45, 0))

        self.search = CTkEntry(master=search_container, width=350, placeholder_text="Search Products", border_color=self.text_color)
        self.search.pack(anchor ='w', padx=13, pady=15)      
        self.table_data = [
            ['Product_Code ', 'Product_Name','Price']
        ]
        self.bill_frame = CTkFrame(master=search_box, height=400,width = 400,fg_color='transparent') 
        self.bill_frame.pack(anchor = 'w',pady=(45, 0))
        self.table_frame = CTkScrollableFrame(master=self.bill_frame, fg_color="transparent",width = 400,height = 400)
        self.table_frame.pack(expand=True,anchor= 'w',side = 'left',fill='both')
        
        self.mini_frame = CTkFrame(master=self.mainframe, height=450,fg_color=self.secondary_widget_color) 
        # self.mini_frame.pack_propagate(False) 
        # self.mini_frame.grid_propagate(False)
      
        
        CTkLabel(master=self.mini_frame, text="Bill Counter", font=("Arial Black", 25), text_color=self.text_color).grid(row = 0 ,column = 0,padx= 20,pady= (20,0))
        
        self.mini_frame.pack(expand=True,anchor='nw',side = 'left',padx=(0,27),fill='both')
        
        self.update_bill()
    def add_to_bill(self,condition = None,element = None):
        if self.table_data != None:
            if condition == None:

                #save price as a val in dict

                if element in self.bill_items.keys():
                    self.bill_items[element][0] += 1
                    self.bill_items[element][2] += self.bill_items[element][1]
                    self.bill_items[element][3].configure(text=element + f' ({self.bill_items[element][0]}) '+ str(self.bill_items[element][2]))
                    
                else:
                    # bill_items[item_name] = qty,price,amt,addbutton,removebutton
                    self.bill_items[element] = [1,
                    self.table_data[1][2],
                    self.table_data[1][2],
                    CTkLabel(master=self.mini_frame, text= element + ' (1) '+ str(self.table_data[1][2]),
                    font=("Arial Black", 20), text_color=self.text_color),
                    CTkButton(self.mini_frame, text=f"+",width= 30,command= lambda:(self.add_to_bill(element = element))),
                    CTkButton(self.mini_frame, text=f"-",width= 30,command= lambda:(self.add_to_bill(element))
                    )]
                    self.bill_items[element][3].grid(row = len(self.bill_items) + 1,column = 0,padx= (20,0),pady= (5,0))
                    self.bill_items[element][4].grid(row = len(self.bill_items) + 1,column = 2,padx=(10,0))
                    self.bill_items[element][5].grid(row = len(self.bill_items) + 1,column = 3,padx=(5,5))
            else :
                self.bill_items[condition][0] -= 1
                self.bill_items[condition][2] -= self.bill_items[condition][1]
                self.bill_items[condition][3].configure(text=condition + f' ({self.bill_items[condition][0]}) '+ str(self.bill_items[condition][2]))
                if self.bill_items[condition][0] <=0:
                    self.bill_items[condition][3].destroy()
                    self.bill_items[condition][4].destroy()
                    self.bill_items[condition][5].destroy()
                    self.bill_items.pop(condition) 
    def bill_print(self):
        self.root.after_cancel(self.run_search)
        self.bill_sql()
        
        if len(self.bill_items) != 0 :
            with open('bill_new.txt', "w+",encoding = 'utf-8') as f:
                f.write('''

        Madinatain   Supermarket
        TAX INVOICE الفاتورة الضريبية
        TRN
        Tel : +971 05x xxxxxxx

    - - - - - - - - - - - - - - - - - - - - - - - - 
    Sn    Description    Qty    Price       Amount
    يكلف  سعر            كمية   وصف السلعة  الرقم
                
                ''')

                total = 0
                for index,key in enumerate(self.bill_items.keys()):
                    f.write(f'\n    {index+1:<4}{key:<20}{self.bill_items[key][0]:<8}{self.bill_items[key][1]:<8}{self.bill_items[key][2]:<10}')
                    total += self.bill_items[key][2]
                f.write(f'''
            \n    - - - - - - - - - - - - - - - - - - - - - - - - 
            \n    Vat%  Net_Amt       Vat Net Amt  Amount
            \n     5    {total:<14.2f}{total * 5 / 100:<14.2f}{total + total * 5 / 100:<14.2f}
            \n    - - - - - - - - - - - - - - - - - - - - - - - - 
            \n    date: 2024-08-23  time: 20:36
            \n    - - - - - - - - - - - - - - - - - - - - - - - - 
            \n    ||||||||||||||||||||||
            \n    ||||||||||||||||||||||
                        ''')
        os.startfile('bill_new.txt')            
    def bill_sql(self):
        for key in self.bill_items:
            try :
                
                self.database.cursor.execute(f'update product set Quantity = Quantity - {self.bill_items[key][0]} where product_name = "{key}";')
                self.database.db.commit()
            except: 
                print('error')
                self.database.db.rollback()
                pass
    def update_bill(self):
        if self.prev != self.search.get():
            self.current = self.prev = self.search.get()
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            self.table_data = [['Product_Code ', 'Product_Name','Price']]
            c= 0
            for index,product in enumerate(self.database.fetch_inv((self.current,'Order by','Supplier Code' ))):
                self.table_data.append([product[0],product[1],product[3]])
            self.table.destroy()
            self.table = CTkTable(master=self.table_frame, values=self.table_data, colors=self.table_color_light, header_color=self.text_color, hover_color=self.table_hover_color,width = 100)
            self.table.pack( padx=(27,5), pady=5, side ='left')

            button = CTkButton(self.table_frame, text=f"+",width= 30,command=lambda: self.add_to_bill(element = self.table_data[1][1]))
            button.pack(padx=5,pady=100, side = 'left',anchor='n') 
        self.run_search = self.root.after(500,self.update_bill)  # Update every 1 second
    def settings_clicked(self):
        self.clear_frame(self.mainframe)

        CTkLabel(master=self.mainframe, text="Settings", font=("Arial Black", 25), text_color=self.text_color).pack(anchor="nw", pady=(29,0), padx=27)
        grid = CTkFrame(master=self.mainframe, fg_color=self.widget_color)
        grid.pack(fill="both", padx=(30,650), pady=(20,100))
        status_var = tkinter.IntVar(value=0)
        CTkLabel(master=grid, text="Theme", font=("Arial Bold", 17), text_color=self.text_color).grid(row=1, column=0, sticky="w",padx=10, pady=(10,0))
        CTkRadioButton(master=grid, variable=status_var, value=0, text="Light", font=("Arial Bold", 14), text_color=self.text_color, fg_color=self.text_color, border_color=self.text_color, hover_color="#207244",command = self.light_mode).grid(row=3, column=0, sticky="w",padx=15, pady=(16,0))
        CTkRadioButton(master=grid, variable=status_var, value=1,text="Dark", font=("Arial Bold", 14), text_color=self.text_color, fg_color=self.text_color, border_color=self.text_color, hover_color="#207244",command = self.dark_mode).grid(row=4, column=0, sticky="w",padx=15 ,pady=(16,10))
        
    

    def emp_search(self):
        print('test')
        for wid in self.mainframe.winfo_children():
            print(wid)
            wid.destroy()
        self.prev = 'test'
        time.sleep(1)
        for wid in self.mainframe.winfo_children():
            print(wid)
        title_frame = CTkFrame(master=self.mainframe, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Employees", font=("Arial Black", 25), text_color=self.text_color).pack(anchor="nw", side="left")

        metrics_frame = CTkFrame(master=self.mainframe, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x",  padx=27, pady=(36, 0))

        orders_metric = CTkFrame(master=metrics_frame, fg_color=self.inter_widget_color, width=250, height=60)
        orders_metric.grid_propagate(0)
        orders_metric.pack(side="left")

        logitics_img_data = Image.open("images/logistics_icon.png")
        logistics_img = CTkImage(light_image=logitics_img_data, dark_image=logitics_img_data, size=(43, 43))

        CTkLabel(master=orders_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12,5), pady=10)

        CTkLabel(master=orders_metric, text="Available Employees", text_color="#fff", font=("Arial Black", 15)).grid(row=0, column=1, sticky="sw")
        CTkLabel(master=orders_metric, text=str(self.database.fetch_available()[0][0]), text_color="#fff",font=("Arial Black", 15), justify="left").grid(row=1, column=1, sticky="nw", pady=(0,10))
        
        

        CTkButton(master=metrics_frame, text="Add Employees", text_color="#fff", font=("Arial Black", 15),fg_color= self.inter_widget_color,width=250, height=60,command = self.add_employee ).pack(side = 'left',padx=10)
       
        CTkButton(master=metrics_frame, text="Remove Employees", text_color="#fff", font=("Arial Black", 15),fg_color= self.inter_widget_color,width=250, height=60,command = self.remove_employee).pack(side = 'left')
       


        search_container = CTkFrame(master=self.mainframe, height=50, fg_color=self.secondary_widget_color)
        search_container.pack(fill="x", pady=(45, 0), padx=27)

        self.search = CTkEntry(master=search_container, width=305, placeholder_text="Search Employee", border_color=self.text_color, border_width=2)
        self.search.pack(side="left", padx=(13, 0), pady=15)
        self.avail =  CTkComboBox(master=search_container, width=125,state= 'readonly',values=["Availability", "Available", "Unavailable"], button_color=self.text_color, border_color=self.text_color, border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color=self.text_color, dropdown_text_color="#fff")
        self.avail.set('Availability')
        self.avail.pack(side="left", padx=(13, 0), pady=15)
        self.shift =  CTkComboBox(master=search_container, width=125,state= 'readonly', values=["Shift", "Morning", "Evening", "Night"], button_color=self.text_color, border_color=self.text_color, border_width=2, button_hover_color="#207244",dropdown_hover_color="#207244" , dropdown_fg_color=self.text_color, dropdown_text_color="#fff")
        self.shift.set("Shift")
        self.shift.pack(side="left", padx=(13, 0), pady=15)

        self.table_data = [
            ['employee_id','employee_name', 'employee_type', 'employee_availability', 'employee_shift_type', 'employee_pay']
        ]

        self.table_frame = CTkScrollableFrame(master=self.mainframe, fg_color="transparent")
        self.table_frame.pack(expand=True, fill="both", padx=20, pady=21)
        
        self.table = CTkTable(master=self.table_frame, values=self.table_data, colors=self.table_color_light, header_color=self.text_color, hover_color=self.table_hover_color)
        self.table.edit_row(0, text_color="#fff", hover_color=self.text_color)
        self.table.pack(expand=True)
        self.update_entry('employee')
    def new_app(self):
        self.clear_frame(self.logn)
        self.logn.destroy()
        self.root = CTk()
        self.root.geometry("1050x650")
        self.root.resizable(0,0)
        self.root.title('SuperMarket Management System')
        self.root.protocol('WM_DELETE_WINDOW',self.root.destroy)
        self.database = Functions("test_db")
        self.database.create_database_if_not_exists()
        Functions('test_db')

        theme = 'let'
        if theme == 'light':
            self.mainframe = CTkFrame(master=self.root, fg_color=self.widget_color,  width=820, height=650, corner_radius=0)
        else:
            self.mainframe = CTkFrame(master=self.root, fg_color='transparent',  width=835, height=630, corner_radius=20)

        self.mainframe.pack_propagate(0)
        self.mainframe.pack(side='right')
        self.mainframe.place(x= 212,y=10)
        self.sidebar_frame = CTkFrame(master=self.root, fg_color=self.widget_color,  width=206, height=650, corner_radius=0)
        self.sidebar_frame.pack_propagate(0)
        self.sidebar_frame.pack(fill="y", anchor="w", side="left")
        self.sidebar_frame.place(x= 0,y=0)

        person_img_data = Image.open("images/person_icon.png")
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data, size=(60, 60))
        CTkButton(master=self.sidebar_frame, image=person_img, text="Account", fg_color='transparent', font=("Arial Bold", 20), hover_color=self.float_color, anchor="w",corner_radius=30,width=180).pack(anchor="center", ipady=5, pady=(16, 0))
        analytics_img_data = Image.open("images/analytics_icon.png")
        analytics_img = CTkImage(dark_image=analytics_img_data, light_image=analytics_img_data)

        
        package_img_data = Image.open("images/package_icon.png")
        package_img = CTkImage(dark_image=package_img_data, light_image=package_img_data)
        self.order_button = CTkButton(master=self.sidebar_frame, image=package_img, text="Employees", fg_color='transparent', font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=self.emp_search)
        self.order_button.pack(anchor="center", ipady=5, pady=(16, 0))

        list_img_data = Image.open("images/list_icon.png")
        list_img = CTkImage(dark_image=list_img_data, light_image=list_img_data)
        self.billing_button = CTkButton(master=self.sidebar_frame, image=list_img, text="Billing", fg_color='transparent', font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=self.billing)
        self.billing_button.pack(anchor="center", ipady=5, pady=(16, 0))
        returns_img_data = Image.open("images/returns_icon.png")
        returns_img = CTkImage(dark_image=returns_img_data, light_image=returns_img_data)
        CTkButton(master=self.sidebar_frame, image=returns_img, text="Inventory", fg_color='transparent', font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command= self.inventory).pack(anchor="center", ipady=5, pady=(16, 0))

        settings_img_data = Image.open("images/settings_icon.png")
        settings_img = CTkImage(dark_image=settings_img_data, light_image=settings_img_data)
        self.settings_button = CTkButton(master=self.sidebar_frame, image=settings_img, text="Settings", fg_color='transparent', font=("Arial Bold", 14), hover_color=self.float_color, anchor="w",width=180,command=self.settings_clicked)
        self.settings_button.pack(anchor="center", ipady=5, pady=(16, 0))
        self.emp_search()
        self.root.mainloop()
    
    def run (self) :
        self.intial_login()
        self.logn.mainloop()

        self.new_app()
display().run()
