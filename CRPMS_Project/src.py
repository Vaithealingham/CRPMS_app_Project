import sqlite3
import mysql.connector
from datetime import datetime
import streamlit as st
class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(host='127.0.0.1',database='crm_app',user='root',password='admin')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        queries = [
            '''CREATE TABLE IF NOT EXISTS Customer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                age INT NOT NULL,
                city VARCHAR(20) NOT NULL,
                is_active BOOLEAN DEFAULT 1
            )''',
            '''CREATE TABLE IF NOT EXISTS Product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT,
                stock INT,
                is_active BOOLEAN DEFAULT 1
            )''',
            '''CREATE TABLE IF NOT EXISTS Sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES Product(id),
                is_active BOOLEAN DEFAULT 1
            )'''
        ]
        for query in queries:
            self.cursor.execute(query)
        self.conn.commit()

class Customer(Database):
    
    def add_customer(self, name, email, phone, age, city):
        query = "INSERT INTO Customer (name, email, phone, age, city, is_active) VALUES (%s, %s, %s, %s, %s, 1)"
        self.cursor.execute(query, (name, email, phone, age, city))
        self.conn.commit()
        return self.cursor.lastrowid

    def view_customers(self):
        query = "SELECT * FROM Customer WHERE is_active = 1"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_customer(self, customer_id):
        query = "DELETE FROM Customer WHERE id = %s"
        self.cursor.execute(query, (customer_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def deactivate_customer(self, customer_id):
        query = "UPDATE Customer SET is_active = 0 WHERE id = %s"
        self.cursor.execute(query, (customer_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0


class Product(Database):
    def add_product(self, name, price, description):
        query = '''INSERT INTO Product (name, price, description, stock, is_active) VALUES (%s, %s, %s, 100, 1)'''
        self.cursor.execute(query, (name, price, description))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def view_products(self):
        query = "SELECT * FROM Product WHERE is_active = 1"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_product(self, product_id):
        query = "DELETE FROM Product WHERE id = %s"
        self.cursor.execute(query, (product_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def deactivate_product(self, product_id):
        query = "UPDATE Product SET is_active = 0 WHERE id = %s"
        self.cursor.execute(query, (product_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

class Sale(Database):
    def record_sale(self, customer_id, product_id, quantity):
        query = '''INSERT INTO Sales (customer_id, product_id, quantity, is_active) VALUES ( %s, %s, %s, 1)'''
        self.cursor.execute(query, (customer_id, product_id, quantity))

        # Update product stock
        stock_query = "UPDATE Product SET stock = stock - %s WHERE id = %s"
        self.cursor.execute(stock_query, (quantity, product_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def view_sales(self):
        query = "SELECT * FROM Sales WHERE is_active = 1"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_sale(self, sale_id):
        query = "DELETE FROM Sales WHERE id = %s"
        self.cursor.execute(query, (sale_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def deactivate_sale(self, sale_id):
        query = "UPDATE Sales SET is_active = 0 WHERE id = %s"
        self.cursor.execute(query, (sale_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def generate_sales_report(self):
        query = """
            SELECT SUM(Product.price * Sales.quantity) AS total_revenue, COUNT(Sales.id) AS total_sales
            FROM Sales
            JOIN Product ON Sales.product_id = Product.id
            where Sales.is_active = 1
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_top_customers(self):
        query = """
            SELECT distinct(Customer.name) as Names, SUM(Product.price * Sales.quantity) AS total_spent
            FROM Sales
            JOIN Customer ON Sales.customer_id = Customer.id
            JOIN Product ON Sales.product_id = Product.id
            GROUP BY Customer.id
            ORDER BY total_spent DESC LIMIT 5;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_product_performance(self):
        query = """
            SELECT Product.name, SUM(Sales.quantity) AS total_sold
            FROM Sales
            JOIN Product ON Sales.product_id = Product.id
            GROUP BY Product.id
            ORDER BY total_sold DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()


# customer = Customer()
# product = Product()
# sale = Sale()

# # Add customer and get customer_id
# customer_id = customer.add_customer("John Doe", "john@example.com", "9876543210", 25, "Chennai")
# # Add product and get product_id
# product_id = product.add_product("Smartphone", 999.99, "128GB Storage")
# # Record sale using the actual IDs
# sale.record_sale(customer_id, product_id, 1)      

# # Entry 2
# customer_id = customer.add_customer("Kevin Spacey", "kevin@google.com", "8956848576", 35, "Mumbai")
# product_id = product.add_product("TV", 35000.00, "OLED TV")
# sale.record_sale(customer_id, product_id, 1)

# # Entry 3
# customer_id = customer.add_customer("Jhon Cena", "cena@yahoo.com", "9658694751", 45, "Delhi")
# product_id = product.add_product("PS5", 55000.00, "PlayStation Console")
# sale.record_sale(customer_id, product_id, 1)

# # Entry 4
# customer_id = customer.add_customer("Virat Kholi", "kholi@google.com", "9574135684", 60, "Banglore")
# product_id = product.add_product("SmartWatch", 19999.99, "I Watch")
# sale.record_sale(customer_id, product_id, 5)

# # Entry 5
# customer_id = customer.add_customer("RajiniKanth", "rajini@google.com", "9965688564", 75, "Chennai")
# product_id = product.add_product("Bluetooth Speaker", 45000.00, "Marshall Pro")
# sale.record_sale(customer_id, product_id, 2)

# Entry 6
# customer_id = customer.add_customer("Sharukh Khan", "sharuk@google.com", "9995698978", 70, "Mumbai")
# product_id = product.add_product("Washing Machine", 50000.00, "Samsung - Front Load")
# sale.record_sale(customer_id, product_id, 10)
