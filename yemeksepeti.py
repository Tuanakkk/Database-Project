import tkinter as tk
from tkinter import ttk, messagebox,simpledialog
import mysql.connector

class FoodDeliveryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Food Delivery App")
        self.logged_in = False
        self.menu_items = {}
        self.selected_items = {}
        self.selected_restaurant = tk.StringVar()

        with open("yemeksepetiSQL.sql", "r") as sql_file:
            sql_statements = sql_file.read()

        # Connect to the MySQL database
        self.db = mysql.connector.connect(
            host="dbms-project.c56aae6ckavi.eu-central-1.rds.amazonaws.com",
            user="admin",
            password="N1OJAZS4YkiREmU0eqvq",
            port="3306",
            database="YemekSepetiDatabase",
        )
        self.cursor = self.db.cursor()

        # Split the SQL statements and execute them one by one
        statements = sql_statements.split(';')
        for statement in statements:
            if statement.strip():  # Skip empty statements
                self.cursor.execute(statement)

        self.db.commit()

        # If the user is not logged in, show the login window
        if not self.logged_in:
            self.show_login_screen()

        # Continue with the main application if the user is logged in
        if self.logged_in:
            self.restaurants = self.fetch_restaurants()
            self.create_widgets()

    def show_login_screen(self):
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")

        username_label = tk.Label(login_window, text="Username:")
        username_label.pack()

        username_entry = tk.Entry(login_window)
        username_entry.pack()

        password_label = tk.Label(login_window, text="Password:")
        password_label.pack()

        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack()

        login_button = tk.Button(login_window, text="Login",
                                 command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack()

        signup_button = tk.Button(login_window, text="Sign Up", command=self.show_signup_screen)
        signup_button.pack()

    def show_signup_screen(self):
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Sign Up")

        # Customer registration form fields
        address_label = tk.Label(signup_window, text="Address:")
        address_label.pack()

        address_entry = tk.Entry(signup_window)
        address_entry.pack()

        name_label = tk.Label(signup_window, text="Customer Name:")
        name_label.pack()

        name_entry = tk.Entry(signup_window)
        name_entry.pack()

        password_label = tk.Label(signup_window, text="Password:")
        password_label.pack()

        password_entry = tk.Entry(signup_window, show="*")
        password_entry.pack()

        email_label = tk.Label(signup_window, text="Email:")
        email_label.pack()

        email_entry = tk.Entry(signup_window)
        email_entry.pack()

        telephone_label = tk.Label(signup_window, text="Telephone Number:")
        telephone_label.pack()

        telephone_entry = tk.Entry(signup_window)
        telephone_entry.pack()

        signup_button = tk.Button(signup_window, text="Sign Up", command=lambda: self.signup(
            address_entry.get(),
            name_entry.get(),
            password_entry.get(),
            email_entry.get(),
            telephone_entry.get(),
        ))
        signup_button.pack()

    def login(self, username, password):
        try:
            query = "SELECT customerID FROM Customers WHERE customer_name = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()

            if result:
                self.logged_in = True
                self.customer_id = result[0]
                messagebox.showinfo("Login", "Login successful!")
                self.restaurants = self.fetch_restaurants()
                self.create_widgets()
            else:
                messagebox.showerror("Login", "Invalid username or password.")

        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def signup(self, address, name, password, email, telephone):
        try:
            # Check if the username is already taken
            check_username_query = "SELECT customerID FROM Customers WHERE customer_name = %s"
            self.cursor.execute(check_username_query, (name,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                messagebox.showerror("Sign Up", "Username already taken. Please choose a different username.")
                return

            # Insert new customer details into the Customers table
            signup_query = "INSERT INTO Customers (address, customer_name, password, email, telephoneNumber) " \
                           "VALUES (%s, %s, %s, %s, %s)"
            signup_values = (address, name, password, email, telephone)
            self.cursor.execute(signup_query, signup_values)
            self.db.commit()

            messagebox.showinfo("Sign Up", "Registration successful! Please login.")
            self.show_login_screen()

        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def create_widgets(self):
        # Restaurant Label
        restaurant_label = tk.Label(self.master, text="Select a Restaurant")
        restaurant_label.pack()

        # Restaurant Combobox
        restaurant_combobox = ttk.Combobox(self.master, textvariable=self.selected_restaurant)
        restaurant_combobox['values'] = self.restaurants
        restaurant_combobox.pack()

        # Continue Button
        continue_button = tk.Button(self.master, text="Continue", command=self.show_menu)
        continue_button.pack()

    def show_menu(self):
        selected_restaurant = self.selected_restaurant.get()

        if not selected_restaurant:
            messagebox.showinfo("Menu Selection", "Please select a restaurant first.")
            return

        # Fetch menu items for the selected restaurant from the database
        self.menu_items = self.fetch_menu_from_database(selected_restaurant)

        # Create a new window for menu selection
        menu_window = tk.Toplevel(self.master)
        menu_window.title(f"Menu - {selected_restaurant}")

        menu_label = tk.Label(menu_window, text="Menu")
        menu_label.pack()

        # Menu Listbox
        menu_listbox = tk.Listbox(menu_window, selectmode=tk.MULTIPLE)
        for item, price in self.menu_items.items():
            menu_listbox.insert(tk.END, f"{item} - ${price}")
        menu_listbox.pack()
        continue_button = tk.Button(menu_window, text="Continue",command=lambda: self.place_order(menu_listbox))
        continue_button.pack()
   
    def place_order(self,menu_listbox):
        selected_restaurant = self.selected_restaurant.get()
        print(menu_listbox.curselection)
        if not selected_restaurant:
            messagebox.showinfo("Order Placement", "Please select a restaurant first.")
            return
        selected_item = menu_listbox.curselection()
        selected_value = [menu_listbox.get(index) for index in selected_item]
        selected = [item.split(' - ')[0] for item in selected_value]
        if not selected:
            messagebox.showinfo("Order Placement", "Please select at least one item to order.")
            return

        total_amount = sum(self.menu_items[item] for item in selected)

        payment_type = simpledialog.askstring("Payment Type", "Enter payment type (Cash/Card):")
        if not payment_type:
            messagebox.showinfo("Order Placement", "Please enter a valid payment type.")
            return

        if payment_type.lower() == 'card':
            card_details = simpledialog.askstring("Card Details", "Enter card details:")
            if not card_details:
                messagebox.showinfo("Order Placement", "Please enter valid card details.")
                return

        try:
            # Insert order details into the Orders table
            order_query = "INSERT INTO Orders (totalAmount, orderDate, customerID) VALUES (%s, CURDATE(), 1)"
            order_values = (total_amount,)
            self.cursor.execute(order_query, order_values)
            self.db.commit()

            # Get the orderID of the newly inserted order
            order_id = self.cursor.lastrowid

            # Insert payment details into the Payment table
            payment_query = "INSERT INTO Payment (amount, payment_date, payment_type, orderID) VALUES (%s, CURDATE(), %s, %s)"
            payment_values = (total_amount, payment_type, order_id)
            self.cursor.execute(payment_query, payment_values)
            self.db.commit()

            # Display a confirmation message
            messagebox.showinfo("Order Placement", f"Order placed successfully. Total Amount: ${total_amount}")

        except Exception as err:
            messagebox.showerror("Database Error", f"Error placing order: {err}")

    def fetch_restaurants(self):
        try:
            query = "SELECT restaurant_name FROM Restaurant"
            self.cursor.execute(query)
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def fetch_menu_from_database(self, selected_restaurant):
        try:
            query = f"SELECT restaurantID FROM Restaurant WHERE restaurant_name = '{selected_restaurant}'"
            self.cursor.execute(query)
            restaurant_id = self.cursor.fetchone()[0]
            if restaurant_id:
                print(restaurant_id)
                query = f"SELECT menuName, menuPrice FROM Menu WHERE restaurantID = '{restaurant_id}'"
                print(query)
                self.cursor.execute(query)
            result = {row[0]: row[1] for row in self.cursor.fetchall()}
            print(result)
            return result
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return {}

    def __del__(self):
        # Close the database connection when the app is closed
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.mainloop()
