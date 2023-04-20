import persistence
from persistence import *

def main():
    #TODO: implement
    employees_name_list = []

    print('Activities') # print activities table
    sorted_activities = sorted(repo.activities.find_all(), key=lambda x: x.date)
    for ac in sorted_activities:
        activity_as_tuple = (ac.product_id, ac.quantity, ac.activator_id, ac.date.decode())
        print(activity_as_tuple)

    print('Branches') # print branches table
    for bran in repo.branches.find_all():
        branche_as_tuple = (bran.id, bran.location.decode(), bran.number_of_employees)
        print(branche_as_tuple)

    print('Employees') # print employees table
    for emp in repo.employees.find_all():
        employees_name_list.append(emp)
        employee_as_tuple = (emp.id, emp.name.decode(), emp.salary, emp.branche)
        print(employee_as_tuple)

    print('Products') # print products table
    for prod in repo.products.find_all():
        product_as_tuple = (prod.id, prod.description.decode(), prod.price, prod.quantity)
        print(product_as_tuple)

    print('Suppliers') # print suppliers table
    for sup in repo.suppliers.find_all():
        supplier_as_tuple = (sup.id, sup.name.decode(), sup.contact_information.decode())
        print(supplier_as_tuple)

    print('\nEmployees report')
    sorted_list = sorted(employees_name_list, key=lambda x: x.name) # sort employees name list lexicographically

    for employee in sorted_list:
        total_sales_income = 0
        id = employee.id
        cursor = repo._conn.cursor()
        cursor.execute("""
                    SELECT product_id, quantity
                    FROM activities JOIN employees ON activities.activator_id = employees.id
                    WHERE activities.activator_id=(?)
                    """, [id,])
        for record in cursor.fetchall():
            product_id = record[0]
            quantity = record[1]
            cursor.execute("""
                        SELECT price
                        FROM products
                        WHERE id=(?)
                        """, [product_id,])
            total_sales_income += cursor.fetchone()[0] * -(quantity)
        cursor.execute("""
                    SELECT branches.location
                    FROM employees JOIN branches ON employees.branche = branches.id
                    WHERE branches.id=(?)
                    """, [employee.branche,])
        location = cursor.fetchone()[0]
        print(employee.name.decode(), employee.salary, location.decode(), total_sales_income)

    print('\nActivities report')
    cursor = repo._conn.cursor()
    cursor.execute("""
                SELECT activities.date, products.description, activities.quantity, employees.name, suppliers.name
                FROM activities JOIN products ON activities.product_id = products.id
                LEFT JOIN employees ON activities.activator_id = employees.id 
                LEFT JOIN suppliers ON activities.activator_id = suppliers.id
                """)

    for record in sorted(cursor, key=lambda x: x[0]):
        date = record[0].decode()
        product_name = record[1].decode()
        product_quantity = record[2]
        employee_name = record[3]
        supplier_name = record[4]

        if employee_name is not None:
            employee_name = employee_name.decode()
        if supplier_name is not None:
            supplier_name = supplier_name.decode()

        record_as_tuple = (date, product_name, product_quantity, employee_name, supplier_name)
        print(record_as_tuple)

if __name__ == '__main__':
    main()