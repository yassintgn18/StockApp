import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Management System")
        self.root.geometry("1200x700")
        
        # Colors and style
        self.bg_color = "#f0f0f0"
        self.accent_color = "#2c3e50"
        self.card_color = "#ffffff"
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background=self.card_color,
                      fieldbackground=self.card_color, foreground=self.accent_color)
        style.configure("TNotebook", background=self.bg_color)
        style.configure("Sidebar.TFrame", background=self.accent_color)
        
        # Main layout
        self.create_sidebar()
        self.create_main_content()
        
        # Initialize database connection
        self.db = sqlite3.connect("store_inventory.db")
        self.db.row_factory = sqlite3.Row
        
        # Show dashboard initially
        self.show_dashboard()

    def create_sidebar(self):
        sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Sidebar buttons
        btn_config = {'width': 20, 'pady': 5, 'padx': 5}
        
        tk.Button(sidebar, text="🏠 Dashboard", command=self.show_dashboard,
                 bg=self.accent_color, fg="white", **btn_config).pack(pady=5)
        tk.Button(sidebar, text="📦 Products", command=self.show_products,
                 bg=self.accent_color, fg="white", **btn_config).pack(pady=5)
        tk.Button(sidebar, text="👥 Customers", command=self.show_customers,
                 bg=self.accent_color, fg="white", **btn_config).pack(pady=5)
        tk.Button(sidebar, text="💰 Sales", command=self.show_sales,
                 bg=self.accent_color, fg="white", **btn_config).pack(pady=5)

    def create_main_content(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_stat_card(self, parent, title, value, row, column):
        card = ttk.Frame(parent, style="Card.TFrame")
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(pady=5)
        ttk.Label(card, text=str(value), style="CardValue.TLabel").pack(pady=5)
        
        return card

    def show_dashboard(self):
        self.clear_main_frame()
        
        # Dashboard title
        ttk.Label(self.main_frame, text="Dashboard", font=("Helvetica", 24)).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Current date/time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ttk.Label(self.main_frame, text=current_time, font=("Helvetica", 12)).grid(row=1, column=0, columnspan=2)
        
        # Statistics
        cursor = self.db.cursor()
        
        # Products count
        cursor.execute("SELECT COUNT(*) FROM Product")
        products_count = cursor.fetchone()[0]
        self.create_stat_card(self.main_frame, "Total Products", products_count, 2, 0)
        
        # Customers count
        cursor.execute("SELECT COUNT(*) FROM Customer")
        customers_count = cursor.fetchone()[0]
        self.create_stat_card(self.main_frame, "Total Customers", customers_count, 2, 1)
        
        # Sales count
        cursor.execute("SELECT COUNT(*) FROM Sale")
        sales_count = cursor.fetchone()[0]
        self.create_stat_card(self.main_frame, "Total Sales", sales_count, 3, 0)
        
        # Total revenue
        cursor.execute("SELECT SUM(total_price) FROM Sale")
        total_revenue = cursor.fetchone()[0] or 0
        self.create_stat_card(self.main_frame, f"Total Revenue (€)", f"{total_revenue:.2f}", 3, 1)
        
        # Configure grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    def show_products(self):
        self.clear_main_frame()
        
        # Products frame
        products_frame = ttk.Frame(self.main_frame)
        products_frame.pack(fill="both", expand=True)
        
        # Search frame
        search_frame = ttk.Frame(products_frame)
        search_frame.pack(fill="x", pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side="left")
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side="left", padx=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(products_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="➕ Add Product", command=lambda: self.add_product_dialog()).pack(side="left", padx=5)
        
        # Products table
        columns = ("ID", "Name", "Price")
        self.products_tree = ttk.Treeview(products_frame, columns=columns, show="headings")
        
        for col in columns:
            self.products_tree.heading(col, text=col)
        
        self.products_tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(products_frame, orient="vertical", command=self.products_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        # Populate table
        self.refresh_products()
        
        # Bind search
        search_var.trace("w", lambda name, index, mode: self.search_products(search_var.get()))
        
        # Bind double-click for editing
        self.products_tree.bind("<Double-1>", self.edit_product_dialog)

    def show_customers(self):
        self.clear_main_frame()
        
        # Customers frame
        customers_frame = ttk.Frame(self.main_frame)
        customers_frame.pack(fill="both", expand=True)
        
        # Search frame
        search_frame = ttk.Frame(customers_frame)
        search_frame.pack(fill="x", pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side="left")
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side="left", padx=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(customers_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="➕ Add Customer", command=lambda: self.add_customer_dialog()).pack(side="left", padx=5)
        
        # Customers table
        columns = ("ID", "Name", "Phone")
        self.customers_tree = ttk.Treeview(customers_frame, columns=columns, show="headings")
        
        for col in columns:
            self.customers_tree.heading(col, text=col)
        
        self.customers_tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(customers_frame, orient="vertical", command=self.customers_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.customers_tree.configure(yscrollcommand=scrollbar.set)
        
        # Populate table
        self.refresh_customers()
        
        # Bind search
        search_var.trace("w", lambda name, index, mode: self.search_customers(search_var.get()))
        
        # Bind double-click for editing
        self.customers_tree.bind("<Double-1>", self.edit_customer_dialog)

    def show_sales(self):
        self.clear_main_frame()
        
        # Sales frame
        sales_frame = ttk.Frame(self.main_frame)
        sales_frame.pack(fill="both", expand=True)
        
        # Buttons frame
        btn_frame = ttk.Frame(sales_frame)
        btn_frame.pack(fill="x", pady=10)
        
        ttk.Button(btn_frame, text="➕ Add Sale", command=lambda: self.add_sale_dialog()).pack(side="left", padx=5)
        
        # Sales table
        columns = ("ID", "Product", "Customer", "Quantity", "Total Price")
        self.sales_tree = ttk.Treeview(sales_frame, columns=columns, show="headings")
        
        for col in columns:
            self.sales_tree.heading(col, text=col)
        
        self.sales_tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(sales_frame, orient="vertical", command=self.sales_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        # Populate table
        self.refresh_sales()
        
        # Bind double-click for editing
        self.sales_tree.bind("<Double-1>", self.edit_sale_dialog)

    def add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Product")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)
        
        ttk.Label(dialog, text="Price:").pack(pady=5)
        price_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=price_var).pack(pady=5)
        
        def save():
            try:
                cursor = self.db.cursor()
                cursor.execute("INSERT INTO Product (name, price) VALUES (?, ?)",
                             (name_var.get(), float(price_var.get())))
                self.db.commit()
                self.refresh_products()
                dialog.destroy()
                messagebox.showinfo("Success", "Product added successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)

    def edit_product_dialog(self, event):
        item = self.products_tree.selection()[0]
        product_id = self.products_tree.item(item)['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product")
        dialog.geometry("300x200")
        
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Product WHERE id_product=?", (product_id,))
        product = cursor.fetchone()
        
        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_var = tk.StringVar(value=product['name'])
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)
        
        ttk.Label(dialog, text="Price:").pack(pady=5)
        price_var = tk.StringVar(value=str(product['price']))
        ttk.Entry(dialog, textvariable=price_var).pack(pady=5)
        
        def save():
            try:
                cursor.execute("UPDATE Product SET name=?, price=? WHERE id_product=?",
                             (name_var.get(), float(price_var.get()), product_id))
                self.db.commit()
                self.refresh_products()
                dialog.destroy()
                messagebox.showinfo("Success", "Product updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
                try:
                    cursor.execute("DELETE FROM Product WHERE id_product=?", (product_id,))
                    self.db.commit()
                    self.refresh_products()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Product deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Save", command=save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑 Delete", command=delete).pack(side="left", padx=5)

    def add_customer_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Customer")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)
        
        ttk.Label(dialog, text="Phone:").pack(pady=5)
        phone_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=phone_var).pack(pady=5)
        
        def save():
            try:
                cursor = self.db.cursor()
                cursor.execute("INSERT INTO Customer (name, phone) VALUES (?, ?)",
                             (name_var.get(), phone_var.get()))
                self.db.commit()
                self.refresh_customers()
                dialog.destroy()
                messagebox.showinfo("Success", "Customer added successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)

    def edit_customer_dialog(self, event):
        item = self.customers_tree.selection()[0]
        customer_id = self.customers_tree.item(item)['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Customer")
        dialog.geometry("300x200")
        
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Customer WHERE id_customer=?", (customer_id,))
        customer = cursor.fetchone()
        
        ttk.Label(dialog, text="Name:").pack(pady=5)
        name_var = tk.StringVar(value=customer['name'])
        ttk.Entry(dialog, textvariable=name_var).pack(pady=5)
        
        ttk.Label(dialog, text="Phone:").pack(pady=5)
        phone_var = tk.StringVar(value=customer['phone'])
        ttk.Entry(dialog, textvariable=phone_var).pack(pady=5)
        
        def save():
            try:
                cursor.execute("UPDATE Customer SET name=?, phone=? WHERE id_customer=?",
                             (name_var.get(), phone_var.get(), customer_id))
                self.db.commit()
                self.refresh_customers()
                dialog.destroy()
                messagebox.showinfo("Success", "Customer updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?"):
                try:
                    cursor.execute("DELETE FROM Customer WHERE id_customer=?", (customer_id,))
                    self.db.commit()
                    self.refresh_customers()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Customer deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Save", command=save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑 Delete", command=delete).pack(side="left", padx=5)

    def add_sale_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Sale")
        dialog.geometry("400x300")
        
        # Get products and customers for dropdowns
        cursor = self.db.cursor()
        cursor.execute("SELECT id_product, name, price FROM Product")
        products = {f"{row['name']} (€{row['price']})": (row['id_product'], row['price']) for row in cursor.fetchall()}
        
        cursor.execute("SELECT id_customer, name FROM Customer")
        customers = {row['name']: row['id_customer'] for row in cursor.fetchall()}
        
        # Product selection
        ttk.Label(dialog, text="Product:").pack(pady=5)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(dialog, textvariable=product_var, values=list(products.keys()))
        product_combo.pack(pady=5)
        
        # Customer selection
        ttk.Label(dialog, text="Customer:").pack(pady=5)
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(dialog, textvariable=customer_var, values=list(customers.keys()))
        customer_combo.pack(pady=5)
        
        # Quantity
        ttk.Label(dialog, text="Quantity:").pack(pady=5)
        quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Entry(dialog, textvariable=quantity_var)
        quantity_entry.pack(pady=5)
        
        # Total price label
        total_label = ttk.Label(dialog, text="Total Price: €0.00")
        total_label.pack(pady=5)
        
        def update_total(*args):
            try:
                product_name = product_var.get()
                quantity = int(quantity_var.get())
                if product_name:
                    price = products[product_name][1]
                    total = price * quantity
                    total_label.config(text=f"Total Price: €{total:.2f}")
            except:
                total_label.config(text="Total Price: €0.00")
        
        product_var.trace("w", update_total)
        quantity_var.trace("w", update_total)
        
        def save():
            try:
                product_name = product_var.get()
                customer_name = customer_var.get()
                quantity = int(quantity_var.get())
                
                product_id = products[product_name][0]
                customer_id = customers[customer_name]
                total_price = products[product_name][1] * quantity
                
                cursor = self.db.cursor()
                cursor.execute("INSERT INTO Sale (id_product, id_customer, quantity, total_price) VALUES (?, ?, ?, ?)",
                             (product_id, customer_id, quantity, total_price))
                self.db.commit()
                self.refresh_sales()
                dialog.destroy()
                messagebox.showinfo("Success", "Sale added successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Save", command=save).pack(pady=20)

    def edit_sale_dialog(self, event):
        item = self.sales_tree.selection()[0]
        sale_id = self.sales_tree.item(item)['values'][0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Sale")
        dialog.geometry("400x300")
        
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT s.*, p.name as product_name, p.price as product_price, c.name as customer_name 
            FROM Sale s 
            JOIN Product p ON s.id_product = p.id_product 
            JOIN Customer c ON s.id_customer = c.id_customer 
            WHERE s.id_sale=?
        """, (sale_id,))
        sale = cursor.fetchone()
        
        # Get products and customers for dropdowns
        cursor.execute("SELECT id_product, name, price FROM Product")
        products = {f"{row['name']} (€{row['price']})": (row['id_product'], row['price']) for row in cursor.fetchall()}
        
        cursor.execute("SELECT id_customer, name FROM Customer")
        customers = {row['name']: row['id_customer'] for row in cursor.fetchall()}
        
        # Product selection
        ttk.Label(dialog, text="Product:").pack(pady=5)
        product_var = tk.StringVar(value=f"{sale['product_name']} (€{sale['product_price']})")
        product_combo = ttk.Combobox(dialog, textvariable=product_var, values=list(products.keys()))
        product_combo.pack(pady=5)
        
        # Customer selection
        ttk.Label(dialog, text="Customer:").pack(pady=5)
        customer_var = tk.StringVar(value=sale['customer_name'])
        customer_combo = ttk.Combobox(dialog, textvariable=customer_var, values=list(customers.keys()))
        customer_combo.pack(pady=5)
        
        # Quantity
        ttk.Label(dialog, text="Quantity:").pack(pady=5)
        quantity_var = tk.StringVar(value=str(sale['quantity']))
        quantity_entry = ttk.Entry(dialog, textvariable=quantity_var)
        quantity_entry.pack(pady=5)
        
        # Total price label
        total_label = ttk.Label(dialog, text=f"Total Price: €{sale['total_price']:.2f}")
        total_label.pack(pady=5)
        
        def update_total(*args):
            try:
                product_name = product_var.get()
                quantity = int(quantity_var.get())
                if product_name:
                    price = products[product_name][1]
                    total = price * quantity
                    total_label.config(text=f"Total Price: €{total:.2f}")
            except:
                total_label.config(text="Total Price: €0.00")
        
        product_var.trace("w", update_total)
        quantity_var.trace("w", update_total)
        
        def save():
            try:
                product_name = product_var.get()
                customer_name = customer_var.get()
                quantity = int(quantity_var.get())
                
                product_id = products[product_name][0]
                customer_id = customers[customer_name]
                total_price = products[product_name][1] * quantity
                
                cursor.execute("""
                    UPDATE Sale 
                    SET id_product=?, id_customer=?, quantity=?, total_price=? 
                    WHERE id_sale=?
                """, (product_id, customer_id, quantity, total_price, sale_id))
                self.db.commit()
                self.refresh_sales()
                dialog.destroy()
                messagebox.showinfo("Success", "Sale updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def delete():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this sale?"):
                try:
                    cursor.execute("DELETE FROM Sale WHERE id_sale=?", (sale_id,))
                    self.db.commit()
                    self.refresh_sales()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Sale deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Save", command=save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑 Delete", command=delete).pack(side="left", padx=5)

    def refresh_products(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Product")
        
        self.products_tree.delete(*self.products_tree.get_children())
        for row in cursor:
            self.products_tree.insert("", "end", values=(row['id_product'], row['name'], f"€{row['price']:.2f}"))

    def refresh_customers(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Customer")
        
        self.customers_tree.delete(*self.customers_tree.get_children())
        for row in cursor:
            self.customers_tree.insert("", "end", values=(row['id_customer'], row['name'], row['phone']))

    def refresh_sales(self):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT s.id_sale, p.name as product_name, c.name as customer_name, 
                   s.quantity, s.total_price 
            FROM Sale s
            JOIN Product p ON s.id_product = p.id_product
            JOIN Customer c ON s.id_customer = c.id_customer
        """)
        
        self.sales_tree.delete(*self.sales_tree.get_children())
        for row in cursor:
            self.sales_tree.insert("", "end", values=(
                row['id_sale'], 
                row['product_name'],
                row['customer_name'],
                row['quantity'],
                f"€{row['total_price']:.2f}"
            ))

    def search_products(self, search_text):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Product WHERE name LIKE ?", (f"%{search_text}%",))
        
        self.products_tree.delete(*self.products_tree.get_children())
        for row in cursor:
            self.products_tree.insert("", "end", values=(row['id_product'], row['name'], f"€{row['price']:.2f}"))

    def search_customers(self, search_text):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Customer WHERE name LIKE ?", (f"%{search_text}%",))
        
        self.customers_tree.delete(*self.customers_tree.get_children())
        for row in cursor:
            self.customers_tree.insert("", "end", values=(row['id_customer'], row['name'], row['phone']))

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()