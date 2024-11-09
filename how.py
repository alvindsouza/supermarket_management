import pass_encrpt
import csv 
with open("csv_files/emails.csv", "r") as f:
    with open("csv_files/login.csv", "w",newline='\n') as s:  
        writer = csv.writer(s)  
        reader = csv.reader(f)
        a  = []
        for row in reader:
            writer.writerow(pass_encrpt.encrypt(row[::-1][0],row[::-1][1]))

