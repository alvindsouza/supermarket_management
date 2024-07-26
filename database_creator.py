import mysql.connector as ms
def create_database(a):      
    mydb = ms.connect(host = 'localhost',password = '12345',user = 'root')
    myc= mydb.cursor()
    myc.execute('create database SUPERMARKET')
    mydb.commit()
    myc.execute('use SUPERMARKET')
    myc.execute('''create table orders(
        Order_ID varchar(5) primary key,
        Item_Name varchar(30) not null,
        Customer varchar(20) not null,
        Address varchar(30),
        Status varchar(10) Default "inactive",
        Quantity int not null)''')
    mydb.commit()
    myc.execute('''
    INSERT INTO orders (Order_ID, Item_Name, Customer, Address, Status, Quantity)
    VALUES
    ('O001', 'Apple Watch', 'John Doe', '123 Main St', 'Pending', 2),
    ('O002', 'Samsung TV', 'Jane Smith', '456 Elm St', 'Shipped', 1),
    ('O003', 'Nike Shoes', 'Bob Brown', '789 Oak St', 'Processing', 3),
    ('O004', 'Canon Camera', 'Alice Lee', '321 Park Ave', 'Pending', 1),
    ('O005', 'Sony Headphones', 'Mike Davis', '901 Broadway', 'Shipped', 2)
    ''')
    mydb.commit()