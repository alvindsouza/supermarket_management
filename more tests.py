from datetime import datetime
import datetime as dt
from tabulate import tabulate

employee_name = input("Enter the name of the Employee: ")
date = dt.date.today()
employee_id = input("Enter the Id: ")
time = datetime.now().strftime("%H:%M")
print(type(str(date)))

print("Scan the products")
billlist = []
count = 0

def purchase():
    global count
    count += 1
    while True:
        product_name = input("Enter the product name: ")
        if product_name:
            break
    while True:
        quantity = input(f"Enter the number of {product_name}'s purchased: ")
        if quantity:
            break
    while True:
        price = input(f"Enter the price of {product_name}: ")
        if price:
            break
    total_price = float(quantity) * float(price)
    billlist.append([count, product_name, quantity, price, total_price])

while True:
    purchase()
    new_purch = input("Enter 1 to add a new product and 0 to print the bill: ")
    if new_purch == "0":
        break

headers = ["Sn", "Description", "Qty", "Price", "Amount"]
total = sum(item[4] for item in billlist)
billlist.insert(0, ['يكلف', 'سعر', 'كمية', 'وصف السلعة', 'الرقم'])
vatamt = total * 0.05
amt = total + vatamt

bill_text = f"""
       Madinatain   Supermarket
    TAX INVOICE الفاتورة الضريبية
    TRN
      Tel : +971 05x xxxxxxx

- - - - - - - - - - - - - - - - - - - - - - - - 
{tabulate(billlist, headers=headers, tablefmt="plain")}
- - - - - - - - - - - - - - - - - - - - - - - - 

{tabulate([[str(5), str(total), f"{vatamt:.2f}", f"{amt:.2f}"]], headers=["Vat%", "Net_Amt", "Vat Net Amt", "Amount"], tablefmt="plain")}
- - - - - - - - - - - - - - - - - - - - - - - - 
  Staff: {employee_name}
- - - - - - - - - - - - - - - - - - - - - - - - 
  date: {date}  time: {time}
- - - - - - - - - - - - - - - - - - - - - - - - 
        ||||||||||||||||||||||
        ||||||||||||||||||||||
"""

with open("bill.txt", "w", encoding="utf-8") as file:
    file.write(bill_text)
