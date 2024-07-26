import sql.connector as ms
mydb = ms.connect(host = 'local host',user = 'root',passwd = '12345')
myc = mydb.cursor()
def accept():
    empno = int(input('Enter employee no:'))
    name = (input('Enter employee name:'))
    dept =  (input('Enter employee dept:'))
    salary = int(input('Enter employee salary:'))
    myc.execute(f'INSERT into EMPLOYEE VALUES ("{empno}",{name},{dept},"{salary}"')
    mydb.commit()
    myc.execute('SELECT * from EMPLOYEE')
    for i in myc.fetchall():
        print(i)
def display():
    query = "SELECT * FROM employee WHERE employee_number = %s"
    myc.execute("SELECT * FROM employee WHERE employee_number = %s", (employee_number,))
    row = myc.fetchone()

    if row is not None:
        print(row)
    else:
        print("Employee not found")
def update_salary(employee_number, salary):
    query = "UPDATE employee SET salary = %s WHERE employee_number = %s"
    myc.execute("UPDATE employee SET salary = %s WHERE employee_number = %s", (salary, employee_number))
    mydb.commit()
    print("Salary updated successfully")
def delete_record( employee_number):
    query = "DELETE FROM employee WHERE employee_number = %s"
    myc.execute(query, (employee_number,))
    mydb.commit()
    print("Record deleted successfully")
while True:
    print("\n1. Add new employee")
    print("2. Display all employees")
    print("3. Display employee by employee number")
    print("4. Update salary by employee number")
    print("5. Delete record by employee number")
    print("6. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        accept()
    elif choice == 2:
        display()
    elif choice == 3:
        employee_number = int(input("Enter employee number: "))
        display_employee_by_number(employee_number)
    elif choice == 4:
        employee_number = int(input("Enter employee number: "))
        salary = float(input("Enter new salary: "))
        update_salary_by_number(employee_number, salary)
    elif choice == 5:
        break