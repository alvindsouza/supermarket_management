import csv
with open("inventory_data.csv",'r') as f:
    data = csv.reader(f)
    for i in data:
        print(i)