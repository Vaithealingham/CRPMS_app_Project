import streamlit as st
import pandas as pd
from src import Customer, Product, Sale
import os

current_dir = os.path.dirname(__file__)

img_path = os.path.join(current_dir, 'crpms.jpg')

# Instantiate database models
customer = Customer()
product = Product()
sale = Sale()

# Main menu in the sidebar
st.sidebar.title("Main Menu")
page = st.sidebar.radio("Navigation", ["Home", "Features"])

# Display content based on the selection
if page == "Home":
    st.markdown("""
    <div style='text-align: center; font-size: 40px; color:white'>
          Customer Relationship and Product Management System
        </div>
    """, unsafe_allow_html=True)
    st.image(img_path, width=800,clamp=True)

elif page == "Features":
    st.title("CRPM Application")

    st.sidebar.title("Feature Options")
    page = st.sidebar.radio("Select an Option", ["Customer", "Product", "Sales", "Analytics"])

    # --- Customer Section ---
    if page == "Customer":
        st.header("Customer Management")
        action = st.radio("Select an Option:", ["Add a Customer", "View Customers", "Delete/Deactivate a Customer"], horizontal=True)

        if action == "Add a Customer":
            st.subheader("Add a New Customer")
            customer_name = st.text_input("Name")
            customer_email = st.text_input("Email")
            customer_phone = st.text_input("Phone")
            customer_age = st.text_input("Age")
            customer_city = st.text_input("City")
            if st.button("Add Customer"):
                if customer_name:
                    customer_id = customer.add_customer(customer_name, customer_email, customer_phone, customer_age, customer_city)
                    st.success(f"Customer added with ID: {customer_id}")
                else:
                    st.error("Please fill in all customer fields.")

        elif action == "View Customers":
            st.subheader("View Customers")
            customers = customer.view_customers()
            if customers:
                df_customers = pd.DataFrame(customers, columns=['Id','Name','Email','Phone','Age','City','Active'])
                df_customers = df_customers[['Id','Name','Email','Phone','Age','City']]
                st.table(df_customers)
            else:
                st.info("No Customers Found.")

        elif action == "Delete/Deactivate a Customer":
            st.header("Delete or Deactivate a Customer")
            customer_id_to_modify = st.number_input("Enter Customer ID", min_value=1, step=1)
            action_type = st.radio("Choose Action", ["Delete", "Deactivate"])

            if st.button("Confirm Action"):
                if action_type == "Delete":
                    customer.delete_customer(customer_id_to_modify)
                    st.success(f"Customer with ID {customer_id_to_modify} deleted successfully.")
                elif action_type == "Deactivate":
                    customer.deactivate_customer(customer_id_to_modify)
                    st.success(f"Customer with ID {customer_id_to_modify} deactivated successfully.")


    # --- Product Section ---
    elif page == "Product":
        st.header("Product Management")
        action = st.radio("Select an Option:", ["Add a Product", "View Products", "Delete/Deactivate a Product"], horizontal=True)

        if action == "Add a Product":
            st.subheader("Add a New Product")
            product_name = st.text_input("Product Name")
            product_price = st.number_input("Price", min_value=0.0, step=0.01)
            product_description = st.text_input("Description")
            if st.button("Add Product"):
                if product_name:
                    product_id = product.add_product(product_name, product_price, product_description)
                    st.success(f"Product added with ID: {product_id}")
                else:
                    st.error("Please fill in all product fields.")

        elif action == "View Products":
            st.subheader("View Products")
            products = product.view_products()
            if products:
                df_products = pd.DataFrame(products, columns=['Id','Product Name','Price','Description','Active','Stock'])
                df_products = df_products[['Id','Product Name','Price','Description','Stock']]
                st.table(df_products)
            else:
                st.info("No Products Found.")

        elif action == "Delete/Deactivate a Product":
            st.header("Delete or Deactivate a Product")
            product_id_to_modify = st.number_input("Enter Product ID", min_value=1, step=1)
            action_type = st.radio("Choose Action", ["Delete", "Deactivate"])

            if st.button("Confirm Action"):
                if action_type == "Delete":
                    product.delete_product(product_id_to_modify)
                    st.success(f"Product with ID {product_id_to_modify} deleted successfully.")
                elif action_type == "Deactivate":
                    product.deactivate_product(product_id_to_modify)
                    st.success(f"Product with ID {product_id_to_modify} deactivated successfully.")


    # --- Sales Section ---
    elif page == "Sales":
        st.header("Sales Management")
        action = st.radio("Select an Option:", ["Record a Sale", "View Sales", "Delete/Deactivate a Sale"], horizontal=True)

        if action == "Record a Sale":
            st.subheader("Record a Sale")
            sale_customer_id = st.number_input("Customer ID", min_value=1, step=1)
            sale_product_id = st.number_input("Product ID", min_value=1, step=1)
            sale_quantity = st.number_input("Quantity", min_value=1, step=1)
            if st.button("Record Sale"):
                if sale_customer_id > 0 and sale_product_id > 0:
                    sale_id = sale.record_sale(sale_customer_id, sale_product_id, sale_quantity)
                    st.success(f"Sale recorded successfully with Sale ID: {sale_id}")
                else:
                    st.error("Invalid customer or product ID.")

        elif action == "View Sales":
            st.subheader("View Sales")
            sales = sale.view_sales()
            if sales:
                df_sales = pd.DataFrame(sales, columns=['Sale Id','Customer_Id','Product_ID','Quantity','Date_Time','Active'])
                df_sales = df_sales[['Sale Id','Customer_Id','Product_ID','Quantity','Date_Time']]
                st.table(df_sales)
            else:
                st.info("No Sales Found.")

        elif action == "Delete/Deactivate a Sale":
            st.header("Delete or Deactivate a Sale")
            sale_id_to_modify = st.number_input("Enter Sale ID", min_value=1, step=1)
            action_type = st.radio("Choose Action", ["Delete", "Deactivate"])

            if st.button("Confirm Action"):
                if action_type == "Delete":
                    sale.delete_sale(sale_id_to_modify)
                    st.success(f"Sale with ID {sale_id_to_modify} deleted successfully.")
                elif action_type == "Deactivate":
                    sale.deactivate_sale(sale_id_to_modify)
                    st.success(f"Sale with ID {sale_id_to_modify} deactivated successfully.")


    # --- Analytics Section ---
    elif page == "Analytics":
        st.header("Analytics and Reports")

        st.subheader("Total Revenue and Sales")
        revenue, total_sales = sale.generate_sales_report()
        st.metric("Total Revenue", f"${revenue}")
        st.metric("Total Sales", total_sales)

        st.subheader("Top 5 Customers")
        top_customers = sale.get_top_customers()
        if top_customers:
            df_top_customers = pd.DataFrame(top_customers, columns=["Names", "Total_Spent"])
            df_top_customers = df_top_customers[["Names", "Total_Spent"]]
            st.table(df_top_customers)
        else:
            st.info("No customers found.")

        st.subheader("Best-Selling Products")
        best_selling_products = sale.get_product_performance()
        if best_selling_products:
            df_best_products = pd.DataFrame(best_selling_products,columns=["ProductName", "Quantity"])
            df_best_products = df_best_products[["ProductName", "Quantity"]]
            st.table(df_best_products)
        else:
            st.info("No Products Found.")
