# Customer Relationship and Product Management System Application

This is a simple CRM (Customer Relationship Management) application built using Python, MySQL, and Streamlit. It allows you to manage customers, products, and sales while providing analytics and reports on customer activity, product performance, and total revenue.

## Features

### Customer Management
- **Add Customers**: Add customer details like Name, Email, Phone Number, Age, and City.
- **View Customers**: Display a list of all customers stored in the database.
- **Update Customer Details**: Modify customer information using their unique Customer ID.
- **Delete/Deactivate Customers**: Remove or deactivate customers from the system (using `is_active` flag).

### Product Management
- **Add Products**: Add products with details like Name, Price, and Description.
- **View Products**: Display a list of all available products.
- **Update Product Details**: Edit product details such as name, price, and description.
- **Delete/Deactivate Products**: Remove or deactivate products from the system (using `is_active` flag).

### Sales Management
- **Record Sales**: Record a sale by linking customers with products and specifying quantities.
- **View Sales**: Display all recorded sales, including customer and product details.
- **Delete Sales**: Delete recorded sales.

### Analytics and Reports
- **Total Revenue & Sales**: View total revenue generated and total sales made.
- **Top 5 Customers**: View the top 5 customers based on total spend.
- **Best-selling Products**: Display products that are selling the most.
