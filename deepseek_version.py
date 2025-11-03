import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Inventory Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f5f6fa')
        
        # Database connection
        self.conn = sqlite3.connect('store_inventory.db')
        self.create_tables()
        
        # Color scheme
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'success': '#27ae60'
        }
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.colors['light'])
        self.style.configure('TLabel', background=self.colors['light'], font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground=self.colors['dark'])
        self.style.configure('Card.TFrame', background='white', relief='raised', borderwidth=1)
        
        self.setup_ui()
        self.show_dashboard()
        
    def create_tables(self):
        """Ensure tables exist with proper structure"""
        try:
            cursor = self.conn.cursor()
            
            # Create Product table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Product (
                    id_product INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL
                )
            ''')
            
            # Create Customer table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Customer (
                    id_customer INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT
                )
            ''')
            
            # Create Sale table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Sale (
                    id_sale INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_product INTEGER,
                    id_customer INTEGER,
                    quantity INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_product) REFERENCES Product(id_product),
                    FOREIGN KEY (id_customer) REFERENCES Customer(id_customer)
                )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating tables: {e}")
    
    def setup_ui(self):
        """Setup the main UI components"""
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sidebar
        self.setup_sidebar()
        
        # Content area
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
    def setup_sidebar(self):
        """Setup the navigation sidebar"""
        sidebar = ttk.Frame(self.main_container, width=200, style='TFrame')
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # App title
        title_label = ttk.Label(sidebar, text="Store Manager", style='Header.TLabel')
        title_label.pack(pady=20)
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("📦 Products", self.show_products),
            ("👥 Customers", self.show_customers),
            ("💰 Sales", self.show_sales)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(sidebar, text=text, command=command, bg=self.colors['primary'], 
                          fg='white', font=('Arial', 11), relief='flat', height=2,
                          cursor='hand2')
            btn.pack(fill=tk.X, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors['dark']))
            btn.bind("<Leave>", lambda e, b=btn, c=self.colors['primary']: b.configure(bg=c))
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Display dashboard with statistics"""
        self.clear_content()
        
        # Header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Dashboard", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Current date
        current_date = tk.Label(header_frame, text=datetime.now().strftime("%Y-%m-%d %H:%M"), 
                               bg=self.colors['light'], fg=self.colors['dark'], font=('Arial', 10))
        current_date.pack(side=tk.RIGHT)
        
        # Statistics cards
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        try:
            cursor = self.conn.cursor()
            
            # Get statistics
            cursor.execute("SELECT COUNT(*) FROM Product")
            total_products = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Customer")
            total_customers = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Sale")
            total_sales = cursor.fetchone()[0]
            
            cursor.execute("SELECT COALESCE(SUM(total_price), 0) FROM Sale")
            total_revenue = cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error fetching statistics: {e}")
            return
        
        # Create cards
        stats_data = [
            ("Total Products", total_products, self.colors['primary'], '📦'),
            ("Total Customers", total_customers, self.colors['secondary'], '👥'),
            ("Total Sales", total_sales, self.colors['warning'], '💰'),
            ("Total Revenue", f"${total_revenue:.2f}", self.colors['success'], '💵')
        ]
        
        for i, (title, value, color, icon) in enumerate(stats_data):
            card = tk.Frame(stats_frame, bg='white', relief='raised', borderwidth=1)
            card.grid(row=0, column=i, padx=10, sticky='nsew')
            stats_frame.columnconfigure(i, weight=1)
            
            # Card content
            icon_label = tk.Label(card, text=icon, bg='white', font=('Arial', 24))
            icon_label.pack(pady=(15, 5))
            
            value_label = tk.Label(card, text=str(value), bg='white', font=('Arial', 20, 'bold'), fg=color)
            value_label.pack()
            
            title_label = tk.Label(card, text=title, bg='white', font=('Arial', 10), fg=self.colors['dark'])
            title_label.pack(pady=(0, 15))
    
    def show_products(self):
        """Display product management interface"""
        self.clear_content()
        
        # Header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Product Management", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Search and Add frame
        search_add_frame = ttk.Frame(self.content_frame)
        search_add_frame.pack(fill=tk.X, pady=10)
        
        # Search
        search_frame = ttk.Frame(search_add_frame)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.product_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.product_search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.search_products)
        
        # Add Product button
        add_btn = tk.Button(search_add_frame, text="➕ Add Product", command=self.add_product_dialog,
                           bg=self.colors['success'], fg='white', font=('Arial', 10), relief='flat')
        add_btn.pack(side=tk.RIGHT)
        
        # Products table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Price')
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100)
        
        self.products_tree.column('Name', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click for editing
        self.products_tree.bind('<Double-1>', self.edit_product_dialog)
        
        # Load products
        self.load_products()
    
    def load_products(self, search_term=""):
        """Load products into the treeview"""
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        try:
            cursor = self.conn.cursor()
            if search_term:
                cursor.execute("SELECT * FROM Product WHERE name LIKE ?", (f'%{search_term}%',))
            else:
                cursor.execute("SELECT * FROM Product")
            
            products = cursor.fetchall()
            
            for product in products:
                self.products_tree.insert('', tk.END, values=product)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading products: {e}")
    
    def search_products(self, event=None):
        """Search products by name"""
        search_term = self.product_search_var.get()
        self.load_products(search_term)
    
    def add_product_dialog(self):
        """Show add product dialog"""
        self.product_dialog("Add Product")
    
    def edit_product_dialog(self, event=None):
        """Show edit product dialog"""
        selection = self.products_tree.selection()
        if not selection:
            return
        
        item = self.products_tree.item(selection[0])
        product_id, name, price = item['values']
        self.product_dialog("Edit Product", product_id, name, price)
    
    def product_dialog(self, title, product_id=None, name="", price=""):
        """Product add/edit dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x200")
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        ttk.Label(dialog, text="Name:", background=self.colors['light']).pack(pady=10)
        name_var = tk.StringVar(value=name)
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=30)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Price:", background=self.colors['light']).pack(pady=10)
        price_var = tk.StringVar(value=str(price))
        price_entry = ttk.Entry(dialog, textvariable=price_var, width=30)
        price_entry.pack(pady=5)
        
        def save_product():
            name_val = name_var.get().strip()
            price_val = price_var.get().strip()
            
            if not name_val or not price_val:
                messagebox.showwarning("Validation Error", "Please fill in all fields")
                return
            
            try:
                price_val = float(price_val)
                if price_val < 0:
                    raise ValueError("Price cannot be negative")
            except ValueError:
                messagebox.showwarning("Validation Error", "Please enter a valid price")
                return
            
            try:
                cursor = self.conn.cursor()
                if product_id:
                    # Update existing product
                    cursor.execute("UPDATE Product SET name = ?, price = ? WHERE id_product = ?", 
                                 (name_val, price_val, product_id))
                    messagebox.showinfo("Success", "Product updated successfully")
                else:
                    # Insert new product
                    cursor.execute("INSERT INTO Product (name, price) VALUES (?, ?)", 
                                 (name_val, price_val))
                    messagebox.showinfo("Success", "Product added successfully")
                
                self.conn.commit()
                self.load_products()
                dialog.destroy()
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error saving product: {e}")
        
        def delete_product():
            if product_id and messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM Product WHERE id_product = ?", (product_id,))
                    self.conn.commit()
                    self.load_products()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Product deleted successfully")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Error deleting product: {e}")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=save_product).pack(side=tk.LEFT, padx=5)
        
        if product_id:
            ttk.Button(button_frame, text="Delete", command=delete_product).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        name_entry.focus()
    
    def show_customers(self):
        """Display customer management interface"""
        self.clear_content()
        
        # Header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Customer Management", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Search and Add frame
        search_add_frame = ttk.Frame(self.content_frame)
        search_add_frame.pack(fill=tk.X, pady=10)
        
        # Search
        search_frame = ttk.Frame(search_add_frame)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.customer_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.customer_search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.search_customers)
        
        # Add Customer button
        add_btn = tk.Button(search_add_frame, text="➕ Add Customer", command=self.add_customer_dialog,
                           bg=self.colors['success'], fg='white', font=('Arial', 10), relief='flat')
        add_btn.pack(side=tk.RIGHT)
        
        # Customers table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Phone')
        self.customers_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=100)
        
        self.customers_tree.column('Name', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.customers_tree.yview)
        self.customers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.customers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click for editing
        self.customers_tree.bind('<Double-1>', self.edit_customer_dialog)
        
        # Load customers
        self.load_customers()
    
    def load_customers(self, search_term=""):
        """Load customers into the treeview"""
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        try:
            cursor = self.conn.cursor()
            if search_term:
                cursor.execute("SELECT * FROM Customer WHERE name LIKE ?", (f'%{search_term}%',))
            else:
                cursor.execute("SELECT * FROM Customer")
            
            customers = cursor.fetchall()
            
            for customer in customers:
                self.customers_tree.insert('', tk.END, values=customer)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading customers: {e}")
    
    def search_customers(self, event=None):
        """Search customers by name"""
        search_term = self.customer_search_var.get()
        self.load_customers(search_term)
    
    def add_customer_dialog(self):
        """Show add customer dialog"""
        self.customer_dialog("Add Customer")
    
    def edit_customer_dialog(self, event=None):
        """Show edit customer dialog"""
        selection = self.customers_tree.selection()
        if not selection:
            return
        
        item = self.customers_tree.item(selection[0])
        customer_id, name, phone = item['values']
        self.customer_dialog("Edit Customer", customer_id, name, phone)
    
    def customer_dialog(self, title, customer_id=None, name="", phone=""):
        """Customer add/edit dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x200")
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        ttk.Label(dialog, text="Name:", background=self.colors['light']).pack(pady=10)
        name_var = tk.StringVar(value=name)
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=30)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Phone:", background=self.colors['light']).pack(pady=10)
        phone_var = tk.StringVar(value=phone)
        phone_entry = ttk.Entry(dialog, textvariable=phone_var, width=30)
        phone_entry.pack(pady=5)
        
        def save_customer():
            name_val = name_var.get().strip()
            phone_val = phone_var.get().strip()
            
            if not name_val:
                messagebox.showwarning("Validation Error", "Please enter a name")
                return
            
            try:
                cursor = self.conn.cursor()
                if customer_id:
                    # Update existing customer
                    cursor.execute("UPDATE Customer SET name = ?, phone = ? WHERE id_customer = ?", 
                                 (name_val, phone_val, customer_id))
                    messagebox.showinfo("Success", "Customer updated successfully")
                else:
                    # Insert new customer
                    cursor.execute("INSERT INTO Customer (name, phone) VALUES (?, ?)", 
                                 (name_val, phone_val))
                    messagebox.showinfo("Success", "Customer added successfully")
                
                self.conn.commit()
                self.load_customers()
                dialog.destroy()
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error saving customer: {e}")
        
        def delete_customer():
            if customer_id and messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?"):
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM Customer WHERE id_customer = ?", (customer_id,))
                    self.conn.commit()
                    self.load_customers()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Customer deleted successfully")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Error deleting customer: {e}")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=save_customer).pack(side=tk.LEFT, padx=5)
        
        if customer_id:
            ttk.Button(button_frame, text="Delete", command=delete_customer).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        name_entry.focus()
    
    def show_sales(self):
        """Display sales management interface"""
        self.clear_content()
        
        # Header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Sales Management", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Add Sale button
        add_btn = tk.Button(header_frame, text="➕ Add Sale", command=self.add_sale_dialog,
                           bg=self.colors['success'], fg='white', font=('Arial', 10), relief='flat')
        add_btn.pack(side=tk.RIGHT)
        
        # Sales table
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Product', 'Customer', 'Quantity', 'Total Price', 'Date')
        self.sales_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click for editing
        self.sales_tree.bind('<Double-1>', self.edit_sale_dialog)
        
        # Load sales
        self.load_sales()
    
    def load_sales(self):
        """Load sales into the treeview"""
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT s.id_sale, p.name, c.name, s.quantity, s.total_price, s.sale_date
                FROM Sale s
                JOIN Product p ON s.id_product = p.id_product
                JOIN Customer c ON s.id_customer = c.id_customer
                ORDER BY s.sale_date DESC
            ''')
            
            sales = cursor.fetchall()
            
            for sale in sales:
                # Format date and price
                formatted_sale = (
                    sale[0],  # ID
                    sale[1],  # Product name
                    sale[2],  # Customer name
                    sale[3],  # Quantity
                    f"${sale[4]:.2f}",  # Total Price
                    sale[5]   # Date
                )
                self.sales_tree.insert('', tk.END, values=formatted_sale)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading sales: {e}")
    
    def add_sale_dialog(self):
        """Show add sale dialog"""
        self.sale_dialog("Add Sale")
    
    def edit_sale_dialog(self, event=None):
        """Show edit sale dialog"""
        selection = self.sales_tree.selection()
        if not selection:
            return
        
        item = self.sales_tree.item(selection[0])
        sale_id = item['values'][0]  # Get ID from first column
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT s.id_sale, s.id_product, s.id_customer, s.quantity, s.total_price, p.name, c.name
                FROM Sale s
                JOIN Product p ON s.id_product = p.id_product
                JOIN Customer c ON s.id_customer = c.id_customer
                WHERE s.id_sale = ?
            ''', (sale_id,))
            
            sale_data = cursor.fetchone()
            if sale_data:
                self.sale_dialog("Edit Sale", sale_data[0], sale_data[1], sale_data[2], sale_data[3], sale_data[4])
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading sale: {e}")
    
    def sale_dialog(self, title, sale_id=None, product_id=None, customer_id=None, quantity=1, total_price=0):
        """Sale add/edit dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Product selection
        ttk.Label(dialog, text="Product:", background=self.colors['light']).pack(pady=10)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(dialog, textvariable=product_var, width=30, state='readonly')
        product_combo.pack(pady=5)
        
        # Customer selection
        ttk.Label(dialog, text="Customer:", background=self.colors['light']).pack(pady=10)
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(dialog, textvariable=customer_var, width=30, state='readonly')
        customer_combo.pack(pady=5)
        
        # Quantity
        ttk.Label(dialog, text="Quantity:", background=self.colors['light']).pack(pady=10)
        quantity_var = tk.IntVar(value=quantity)
        quantity_spinbox = ttk.Spinbox(dialog, from_=1, to=1000, textvariable=quantity_var, width=30)
        quantity_spinbox.pack(pady=5)
        
        # Total price display
        ttk.Label(dialog, text="Total Price:", background=self.colors['light']).pack(pady=10)
        total_price_var = tk.StringVar(value=f"${total_price:.2f}")
        total_price_label = ttk.Label(dialog, textvariable=total_price_var, background=self.colors['light'],
                                     font=('Arial', 12, 'bold'), foreground=self.colors['success'])
        total_price_label.pack(pady=5)
        
        # Load products and customers
        products = self.get_products()
        customers = self.get_customers()
        
        product_combo['values'] = [f"{p[0]} - {p[1]} (${p[2]:.2f})" for p in products]
        customer_combo['values'] = [f"{c[0]} - {c[1]}" for c in customers]
        
        # Set current values if editing
        if product_id:
            for p in products:
                if p[0] == product_id:
                    product_combo.set(f"{p[0]} - {p[1]} (${p[2]:.2f})")
                    break
        
        if customer_id:
            for c in customers:
                if c[0] == customer_id:
                    customer_combo.set(f"{c[0]} - {c[1]}")
                    break
        
        def calculate_total(*args):
            """Calculate total price based on selected product and quantity"""
            try:
                product_text = product_var.get()
                if product_text:
                    product_price = float(product_text.split('$')[-1].split(')')[0])
                    qty = quantity_var.get()
                    total = product_price * qty
                    total_price_var.set(f"${total:.2f}")
            except (ValueError, IndexError):
                pass
        
        # Bind events for auto-calculation
        product_var.trace('w', calculate_total)
        quantity_var.trace('w', calculate_total)
        
        def save_sale():
            product_text = product_var.get()
            customer_text = customer_var.get()
            qty = quantity_var.get()
            
            if not product_text or not customer_text:
                messagebox.showwarning("Validation Error", "Please select both product and customer")
                return
            
            if qty <= 0:
                messagebox.showwarning("Validation Error", "Quantity must be greater than 0")
                return
            
            try:
                # Extract IDs from combobox text
                product_id_val = int(product_text.split(' - ')[0])
                customer_id_val = int(customer_text.split(' - ')[0])
                total_price_val = float(total_price_var.get().replace('$', ''))
                
                cursor = self.conn.cursor()
                if sale_id:
                    # Update existing sale
                    cursor.execute('''
                        UPDATE Sale SET id_product = ?, id_customer = ?, quantity = ?, total_price = ?
                        WHERE id_sale = ?
                    ''', (product_id_val, customer_id_val, qty, total_price_val, sale_id))
                    messagebox.showinfo("Success", "Sale updated successfully")
                else:
                    # Insert new sale
                    cursor.execute('''
                        INSERT INTO Sale (id_product, id_customer, quantity, total_price)
                        VALUES (?, ?, ?, ?)
                    ''', (product_id_val, customer_id_val, qty, total_price_val))
                    messagebox.showinfo("Success", "Sale added successfully")
                
                self.conn.commit()
                self.load_sales()
                dialog.destroy()
                
            except (ValueError, sqlite3.Error) as e:
                messagebox.showerror("Error", f"Error saving sale: {e}")
        
        def delete_sale():
            if sale_id and messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this sale?"):
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM Sale WHERE id_sale = ?", (sale_id,))
                    self.conn.commit()
                    self.load_sales()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Sale deleted successfully")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Error deleting sale: {e}")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Save", command=save_sale).pack(side=tk.LEFT, padx=5)
        
        if sale_id:
            ttk.Button(button_frame, text="Delete", command=delete_sale).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Initial calculation
        calculate_total()
    
    def get_products(self):
        """Get all products for combobox"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id_product, name, price FROM Product ORDER BY name")
            return cursor.fetchall()
        except sqlite3.Error:
            return []
    
    def get_customers(self):
        """Get all customers for combobox"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id_customer, name FROM Customer ORDER BY name")
            return cursor.fetchall()
        except sqlite3.Error:
            return []
    
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()