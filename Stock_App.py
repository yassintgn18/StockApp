import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple

class StoreInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Inventory Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Color scheme
        self.colors = {
            'primary': '#2C3E50',
            'secondary': '#34495E',
            'accent': '#3498DB',
            'success': '#27AE60',
            'danger': '#E74C3C',
            'warning': '#F39C12',
            'light': '#ECF0F1',
            'white': '#FFFFFF',
            'text': '#2C3E50',
            'card1': '#3498DB',
            'card2': '#27AE60',
            'card3': '#E67E22',
            'card4': '#9B59B6'
        }
        
        self.db_name = 'store_inventory.db'
        self.current_frame = None
        
        self.setup_styles()
        self.create_main_layout()
        self.show_dashboard()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Sidebar.TFrame', background=self.colors['primary'])
        style.configure('Main.TFrame', background=self.colors['light'])
        style.configure('Card.TFrame', background=self.colors['white'], relief='flat')
        
        style.configure('SidebarButton.TButton',
                       background=self.colors['secondary'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 11),
                       padding=15)
        style.map('SidebarButton.TButton',
                 background=[('active', self.colors['accent'])])
        
        style.configure('Action.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        style.map('Action.TButton',
                 background=[('active', '#2980B9')])
        
        style.configure('Delete.TButton',
                       background=self.colors['danger'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       padding=10)
        style.map('Delete.TButton',
                 background=[('active', '#C0392B')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       padding=10)
        style.map('Success.TButton',
                 background=[('active', '#229954')])
        
        style.configure('Treeview',
                       background=self.colors['white'],
                       foreground=self.colors['text'],
                       rowheight=30,
                       fieldbackground=self.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        style.configure('Treeview.Heading',
                       background=self.colors['secondary'],
                       foreground=self.colors['white'],
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'))
        style.map('Treeview.Heading',
                 background=[('active', self.colors['primary'])])
        
        style.configure('Card.TLabel',
                       background=self.colors['white'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10))
        
    def create_main_layout(self):
        # Sidebar
        self.sidebar = ttk.Frame(self.root, style='Sidebar.TFrame', width=220)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(self.sidebar, bg=self.colors['primary'], height=80)
        title_frame.pack(fill='x', pady=(0, 20))
        title_label = tk.Label(title_frame, text="Store Inventory",
                              bg=self.colors['primary'],
                              fg=self.colors['white'],
                              font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("📦 Products", self.show_products),
            ("👥 Customers", self.show_customers),
            ("💰 Sales", self.show_sales)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(self.sidebar, text=text, command=command,
                           style='SidebarButton.TButton')
            btn.pack(fill='x', padx=10, pady=5)
        
        # Main content area
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(side='right', fill='both', expand=True)
        
    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
    def get_db_connection(self):
        return sqlite3.connect(self.db_name)
    
    def show_dashboard(self):
        self.clear_main_container()
        
        # Header
        header = tk.Frame(self.main_container, bg=self.colors['light'])
        header.pack(fill='x', padx=30, pady=(30, 20))
        
        tk.Label(header, text="Dashboard", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 24, 'bold')).pack(side='left')
        
        # Date/Time
        current_time = datetime.now().strftime("%B %d, %Y - %I:%M %p")
        tk.Label(header, text=current_time, bg=self.colors['light'],
                fg=self.colors['secondary'], font=('Segoe UI', 11)).pack(side='right')
        
        # Statistics cards
        stats_frame = tk.Frame(self.main_container, bg=self.colors['light'])
        stats_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Get statistics
            cursor.execute("SELECT COUNT(*) FROM Product")
            total_products = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Customer")
            total_customers = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Sale")
            total_sales = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(total_price) FROM Sale")
            total_revenue = cursor.fetchone()[0] or 0
            
            conn.close()
            
            stats = [
                ("Total Products", total_products, self.colors['card1'], "📦"),
                ("Total Customers", total_customers, self.colors['card2'], "👥"),
                ("Total Sales", total_sales, self.colors['card3'], "💰"),
                ("Total Revenue", f"${total_revenue:.2f}", self.colors['card4'], "💵")
            ]
            
            for i, (label, value, color, icon) in enumerate(stats):
                card = tk.Frame(stats_frame, bg=color, relief='flat', bd=0)
                card.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
                
                content_frame = tk.Frame(card, bg=color)
                content_frame.pack(expand=True, pady=40, padx=30)
                
                tk.Label(content_frame, text=icon, bg=color, fg=self.colors['white'],
                        font=('Segoe UI', 32)).pack()
                
                tk.Label(content_frame, text=str(value), bg=color, fg=self.colors['white'],
                        font=('Segoe UI', 28, 'bold')).pack(pady=(10, 5))
                
                tk.Label(content_frame, text=label, bg=color, fg=self.colors['white'],
                        font=('Segoe UI', 12)).pack()
            
            stats_frame.grid_rowconfigure(0, weight=1)
            stats_frame.grid_rowconfigure(1, weight=1)
            stats_frame.grid_columnconfigure(0, weight=1)
            stats_frame.grid_columnconfigure(1, weight=1)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load statistics: {e}")
    
    def show_products(self):
        self.clear_main_container()
        
        # Header
        header = tk.Frame(self.main_container, bg=self.colors['light'])
        header.pack(fill='x', padx=30, pady=(30, 20))
        
        tk.Label(header, text="Product Management", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 24, 'bold')).pack(side='left')
        
        # Search and Add section
        control_frame = tk.Frame(self.main_container, bg=self.colors['light'])
        control_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        # Search
        search_frame = tk.Frame(control_frame, bg=self.colors['light'])
        search_frame.pack(side='left')
        
        tk.Label(search_frame, text="Search:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).pack(side='left', padx=(0, 10))
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30,
                                font=('Segoe UI', 11))
        search_entry.pack(side='left')
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg=self.colors['light'])
        button_frame.pack(side='right')
        
        ttk.Button(button_frame, text="➕ Add Product",
                  command=lambda: self.add_product_dialog(),
                  style='Action.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="✏ Edit",
                  command=lambda: self.edit_product_dialog(tree),
                  style='Success.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🗑 Delete",
                  command=lambda: self.delete_product(tree),
                  style='Delete.TButton').pack(side='left', padx=5)
        
        # Table
        table_frame = tk.Frame(self.main_container, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Price'),
                           show='headings', yscrollcommand=scrollbar.set)
        tree.pack(fill='both', expand=True)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Product Name')
        tree.heading('Price', text='Price ($)')
        
        tree.column('ID', width=80, anchor='center')
        tree.column('Name', width=300, anchor='w')
        tree.column('Price', width=150, anchor='e')
        
        def search_products(*args):
            self.load_products(tree, search_var.get())
        
        search_var.trace('w', search_products)
        
        self.load_products(tree)
        
    def load_products(self, tree, search_term=''):
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute("SELECT id_product, name, price FROM Product WHERE name LIKE ?",
                             (f'%{search_term}%',))
            else:
                cursor.execute("SELECT id_product, name, price FROM Product")
            
            for row in cursor.fetchall():
                tree.insert('', 'end', values=(row[0], row[1], f"${row[2]:.2f}"))
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load products: {e}")
    
    def add_product_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Product")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Form
        form_frame = tk.Frame(dialog, bg=self.colors['light'])
        form_frame.pack(expand=True, padx=40, pady=30)
        
        tk.Label(form_frame, text="Product Name:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        name_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        name_entry.grid(row=1, column=0, pady=(0, 20))
        name_entry.focus()
        
        tk.Label(form_frame, text="Price ($):", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        price_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        price_entry.grid(row=3, column=0, pady=(0, 20))
        
        def save_product():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            
            if not name or not price_str:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            
            try:
                price = float(price_str)
                if price < 0:
                    messagebox.showwarning("Input Error", "Price cannot be negative")
                    return
                
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Product (name, price) VALUES (?, ?)", (name, price))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Product added successfully")
                dialog.destroy()
                self.show_products()
            except ValueError:
                messagebox.showerror("Input Error", "Price must be a valid number")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to add product: {e}")
        
        button_frame = tk.Frame(form_frame, bg=self.colors['light'])
        button_frame.grid(row=4, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save", command=save_product,
                  style='Action.TButton', width=12).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy,
                  style='Delete.TButton', width=12).pack(side='left', padx=5)
    
    def edit_product_dialog(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a product to edit")
            return
        
        item = tree.item(selection[0])
        values = item['values']
        product_id = values[0]
        current_name = values[1]
        current_price = float(values[2].replace('$', ''))
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Form
        form_frame = tk.Frame(dialog, bg=self.colors['light'])
        form_frame.pack(expand=True, padx=40, pady=30)
        
        tk.Label(form_frame, text="Product Name:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        name_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        name_entry.grid(row=1, column=0, pady=(0, 20))
        name_entry.insert(0, current_name)
        name_entry.focus()
        
        tk.Label(form_frame, text="Price ($):", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        price_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        price_entry.grid(row=3, column=0, pady=(0, 20))
        price_entry.insert(0, str(current_price))
        
        def update_product():
            name = name_entry.get().strip()
            price_str = price_entry.get().strip()
            
            if not name or not price_str:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            
            try:
                price = float(price_str)
                if price < 0:
                    messagebox.showwarning("Input Error", "Price cannot be negative")
                    return
                
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE Product SET name=?, price=? WHERE id_product=?",
                             (name, price, product_id))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Product updated successfully")
                dialog.destroy()
                self.show_products()
            except ValueError:
                messagebox.showerror("Input Error", "Price must be a valid number")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to update product: {e}")
        
        button_frame = tk.Frame(form_frame, bg=self.colors['light'])
        button_frame.grid(row=4, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="Update", command=update_product,
                  style='Action.TButton', width=12).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy,
                  style='Delete.TButton', width=12).pack(side='left', padx=5)
    
    def delete_product(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a product to delete")
            return
        
        item = tree.item(selection[0])
        product_id = item['values'][0]
        product_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete",
                              f"Are you sure you want to delete '{product_name}'?"):
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Product WHERE id_product=?", (product_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Product deleted successfully")
                self.show_products()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete product: {e}")
    
    def show_customers(self):
        self.clear_main_container()
        
        # Header
        header = tk.Frame(self.main_container, bg=self.colors['light'])
        header.pack(fill='x', padx=30, pady=(30, 20))
        
        tk.Label(header, text="Customer Management", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 24, 'bold')).pack(side='left')
        
        # Search and Add section
        control_frame = tk.Frame(self.main_container, bg=self.colors['light'])
        control_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        # Search
        search_frame = tk.Frame(control_frame, bg=self.colors['light'])
        search_frame.pack(side='left')
        
        tk.Label(search_frame, text="Search:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).pack(side='left', padx=(0, 10))
        
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=30,
                                font=('Segoe UI', 11))
        search_entry.pack(side='left')
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg=self.colors['light'])
        button_frame.pack(side='right')
        
        ttk.Button(button_frame, text="➕ Add Customer",
                  command=lambda: self.add_customer_dialog(),
                  style='Action.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="✏ Edit",
                  command=lambda: self.edit_customer_dialog(tree),
                  style='Success.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🗑 Delete",
                  command=lambda: self.delete_customer(tree),
                  style='Delete.TButton').pack(side='left', padx=5)
        
        # Table
        table_frame = tk.Frame(self.main_container, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(table_frame, columns=('ID', 'Name', 'Phone'),
                           show='headings', yscrollcommand=scrollbar.set)
        tree.pack(fill='both', expand=True)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Customer Name')
        tree.heading('Phone', text='Phone')
        
        tree.column('ID', width=80, anchor='center')
        tree.column('Name', width=300, anchor='w')
        tree.column('Phone', width=200, anchor='w')
        
        def search_customers(*args):
            self.load_customers(tree, search_var.get())
        
        search_var.trace('w', search_customers)
        
        self.load_customers(tree)
    
    def load_customers(self, tree, search_term=''):
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute("SELECT id_customer, name, phone FROM Customer WHERE name LIKE ?",
                             (f'%{search_term}%',))
            else:
                cursor.execute("SELECT id_customer, name, phone FROM Customer")
            
            for row in cursor.fetchall():
                tree.insert('', 'end', values=row)
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load customers: {e}")
    
    def add_customer_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Customer")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Form
        form_frame = tk.Frame(dialog, bg=self.colors['light'])
        form_frame.pack(expand=True, padx=40, pady=30)
        
        tk.Label(form_frame, text="Customer Name:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        name_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        name_entry.grid(row=1, column=0, pady=(0, 20))
        name_entry.focus()
        
        tk.Label(form_frame, text="Phone:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        phone_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        phone_entry.grid(row=3, column=0, pady=(0, 20))
        
        def save_customer():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not name or not phone:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Customer (name, phone) VALUES (?, ?)", (name, phone))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Customer added successfully")
                dialog.destroy()
                self.show_customers()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to add customer: {e}")
        
        button_frame = tk.Frame(form_frame, bg=self.colors['light'])
        button_frame.grid(row=4, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save", command=save_customer,
                  style='Action.TButton', width=12).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy,
                  style='Delete.TButton', width=12).pack(side='left', padx=5)
    
    def edit_customer_dialog(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a customer to edit")
            return
        
        item = tree.item(selection[0])
        values = item['values']
        customer_id = values[0]
        current_name = values[1]
        current_phone = values[2]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Customer")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Form
        form_frame = tk.Frame(dialog, bg=self.colors['light'])
        form_frame.pack(expand=True, padx=40, pady=30)
        
        tk.Label(form_frame, text="Customer Name:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        name_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        name_entry.grid(row=1, column=0, pady=(0, 20))
        name_entry.insert(0, current_name)
        name_entry.focus()
        
        tk.Label(form_frame, text="Phone:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        phone_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        phone_entry.grid(row=3, column=0, pady=(0, 20))
        phone_entry.insert(0, current_phone)
        
        def update_customer():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not name or not phone:
                messagebox.showwarning("Input Error", "Please fill all fields")
                return
            
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE Customer SET name=?, phone=? WHERE id_customer=?",
                            (name, phone, customer_id))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Customer updated successfully")
                dialog.destroy()
                self.show_customers()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to update customer: {e}")
        
        button_frame = tk.Frame(form_frame, bg=self.colors['light'])
        button_frame.grid(row=4, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="Update", command=update_customer,
                  style='Action.TButton', width=12).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy,
                  style='Delete.TButton', width=12).pack(side='left', padx=5)
    
    def delete_customer(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a customer to delete")
            return
        
        item = tree.item(selection[0])
        customer_id = item['values'][0]
        customer_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete",
                              f"Are you sure you want to delete '{customer_name}'?"):
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Customer WHERE id_customer=?", (customer_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Customer deleted successfully")
                self.show_customers()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete customer: {e}")
    
    def show_sales(self):
        self.clear_main_container()
        
        # Header
        header = tk.Frame(self.main_container, bg=self.colors['light'])
        header.pack(fill='x', padx=30, pady=(30, 20))
        
        tk.Label(header, text="Sales Management", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 24, 'bold')).pack(side='left')
        
        # Buttons section
        control_frame = tk.Frame(self.main_container, bg=self.colors['light'])
        control_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        button_frame = tk.Frame(control_frame, bg=self.colors['light'])
        button_frame.pack(side='right')
        
        ttk.Button(button_frame, text="➕ Add Sale",
                  command=lambda: self.add_sale_dialog(),
                  style='Action.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="✏ Edit",
                  command=lambda: self.edit_sale_dialog(tree),
                  style='Success.TButton').pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🗑 Delete",
                  command=lambda: self.delete_sale(tree),
                  style='Delete.TButton').pack(side='left', padx=5)
        
        # Table
        table_frame = tk.Frame(self.main_container, bg=self.colors['white'])
        table_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side='right', fill='y')
        
        tree = ttk.Treeview(table_frame, columns=('ID', 'Product', 'Customer', 'Quantity', 'Total'),
                           show='headings', yscrollcommand=scrollbar.set)
        tree.pack(fill='both', expand=True)
        scrollbar.config(command=tree.yview)
        
        tree.heading('ID', text='Sale ID')
        tree.heading('Product', text='Product')
        tree.heading('Customer', text='Customer')
        tree.heading('Quantity', text='Quantity')
        tree.heading('Total', text='Total Price')
        
        tree.column('ID', width=80, anchor='center')
        tree.column('Product', width=250, anchor='w')
        tree.column('Customer', width=250, anchor='w')
        tree.column('Quantity', width=100, anchor='center')
        tree.column('Total', width=150, anchor='e')
        
        self.load_sales(tree)
    
    def load_sales(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT s.id_sale, p.name, c.name, s.quantity, s.total_price
                FROM Sale s
                JOIN Product p ON s.id_product = p.id_product
                JOIN Customer c ON s.id_customer = c.id_customer
                ORDER BY s.id_sale DESC
            """)
            
            for row in cursor.fetchall():
                tree.insert('', 'end', values=(row[0], row[1], row[2], row[3], f"${row[4]:.2f}"))
            
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load sales: {e}")
    
    def add_sale_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Sale")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Get products and customers
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id_product, name, price FROM Product")
            products = cursor.fetchall()
            
            cursor.execute("SELECT id_customer, name FROM Customer")
            customers = cursor.fetchall()
            
            conn.close()
            
            if not products:
                messagebox.showwarning("No Products", "Please add products first")
                dialog.destroy()
                return
            
            if not customers:
                messagebox.showwarning("No Customers", "Please add customers first")
                dialog.destroy()
                return
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load data: {e}")
            dialog.destroy()
            return
        
        # Form
        form_frame = tk.Frame(dialog, bg=self.colors['light'])
        form_frame.pack(expand=True, padx=40, pady=30)
        
        # Product selection
        tk.Label(form_frame, text="Select Product:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(form_frame, textvariable=product_var, 
                                    state='readonly', width=28, font=('Segoe UI', 11))
        product_combo['values'] = [f"{p[1]} - ${p[2]:.2f}" for p in products]
        product_combo.grid(row=1, column=0, pady=(0, 20))
        if products:
            product_combo.current(0)
        
        # Customer selection
        tk.Label(form_frame, text="Select Customer:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(form_frame, textvariable=customer_var,
                                     state='readonly', width=28, font=('Segoe UI', 11))
        customer_combo['values'] = [c[1] for c in customers]
        customer_combo.grid(row=3, column=0, pady=(0, 20))
        if customers:
            customer_combo.current(0)
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        quantity_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        quantity_entry.grid(row=5, column=0, pady=(0, 20))
        quantity_entry.insert(0, "1")
        
        # Total price display
        total_label = tk.Label(form_frame, text="Total: $0.00", bg=self.colors['light'],
                              fg=self.colors['success'], font=('Segoe UI', 14, 'bold'))
        total_label.grid(row=6, column=0, pady=(0, 20))
        
        def update_total(*args):
            try:
                quantity = int(quantity_entry.get())
                product_index = product_combo.current()
                if product_index >= 0 and quantity > 0:
                    price = products[product_index][2]
                    total = price * quantity
                    total_label.config(text=f"Total: ${total:.2f}")
            except ValueError:
                total_label.config(text="Total: $0.00")
        
        quantity_entry.bind('<KeyRelease>', update_total)
        product_combo.bind('<<ComboboxSelected>>', update_total)
        update_total()
        
        def save_sale():
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    messagebox.showwarning("Input Error", "Quantity must be positive")
                    return
                
                product_index = product_combo.current()
                customer_index = customer_combo.current()
                
                if product_index < 0 or customer_index < 0:
                    messagebox.showwarning("Input Error", "Please select product and customer")
                    return
                
                product_id = products[product_index][0]
                customer_id = customers[customer_index][0]
                price = products[product_index][2]
                total_price = price * quantity
                
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Sale (id_product, id_customer, quantity, total_price)
                    VALUES (?, ?, ?, ?)
                """, (product_id, customer_id, quantity, total_price))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Sale added successfully")
                dialog.destroy()
                self.show_sales()
            except ValueError:
                messagebox.showerror("Input Error", "Quantity must be a valid number")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to add sale: {e}")
        
        button_frame = tk.Frame(form_frame, bg=self.colors['light'])
        button_frame.grid(row=7, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="Save", command=save_sale,
                  style='Action.TButton', width=12).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy,
                  style='Delete.TButton', width=12).pack(side='left', padx=5)
    
    def edit_sale_dialog(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a sale to edit")
            return
        
        item = tree.item(selection[0])
        values = item['values']
        sale_id = values[0]
        
        # Get current sale data
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id_product, id_customer, quantity
                FROM Sale WHERE id_sale = ?
            """, (sale_id,))
            current_sale = cursor.fetchone()
            
            cursor.execute("SELECT id_product, name, price FROM Product")
            products = cursor.fetchall()
            
            cursor.execute("SELECT id_customer, name FROM Customer")
            customers = cursor.fetchall()
            
            conn.close()
            
            if not current_sale:
                messagebox.showerror("Error", "Sale not found")
                return
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load data: {e}")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Sale")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        dialog.configure(bg=self.colors['light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Form
        form_frame = tk.Frame(dialog, bg=self.colors['light'])
        form_frame.pack(expand=True, padx=40, pady=30)
        
        # Product selection
        tk.Label(form_frame, text="Select Product:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(form_frame, textvariable=product_var,
                                    state='readonly', width=28, font=('Segoe UI', 11))
        product_combo['values'] = [f"{p[1]} - ${p[2]:.2f}" for p in products]
        product_combo.grid(row=1, column=0, pady=(0, 20))
        
        # Set current product
        for i, p in enumerate(products):
            if p[0] == current_sale[0]:
                product_combo.current(i)
                break
        
        # Customer selection
        tk.Label(form_frame, text="Select Customer:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(form_frame, textvariable=customer_var,
                                     state='readonly', width=28, font=('Segoe UI', 11))
        customer_combo['values'] = [c[1] for c in customers]
        customer_combo.grid(row=3, column=0, pady=(0, 20))
        
        # Set current customer
        for i, c in enumerate(customers):
            if c[0] == current_sale[1]:
                customer_combo.current(i)
                break
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", bg=self.colors['light'],
                fg=self.colors['text'], font=('Segoe UI', 11)).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        quantity_entry = ttk.Entry(form_frame, width=30, font=('Segoe UI', 11))
        quantity_entry.grid(row=5, column=0, pady=(0, 20))
        quantity_entry.insert(0, str(current_sale[2]))
        
        # Total price display
        total_label = tk.Label(form_frame, text="Total: $0.00", bg=self.colors['light'],
                              fg=self.colors['success'], font=('Segoe UI', 14, 'bold'))
        total_label.grid(row=6, column=0, pady=(0, 20))
        
        def update_total(*args):
            try:
                quantity = int(quantity_entry.get())
                product_index = product_combo.current()
                if product_index >= 0 and quantity > 0:
                    price = products[product_index][2]
                    total = price * quantity
                    total_label.config(text=f"Total: ${total:.2f}")
            except ValueError:
                total_label.config(text="Total: $0.00")
        
        quantity_entry.bind('<KeyRelease>', update_total)
        product_combo.bind('<<ComboboxSelected>>', update_total)
        update_total()
        
        def update_sale():
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    messagebox.showwarning("Input Error", "Quantity must be positive")
                    return
                
                product_index = product_combo.current()
                customer_index = customer_combo.current()
                
                if product_index < 0 or customer_index < 0:
                    messagebox.showwarning("Input Error", "Please select product and customer")
                    return
                
                product_id = products[product_index][0]
                customer_id = customers[customer_index][0]
                price = products[product_index][2]
                total_price = price * quantity
                
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Sale 
                    SET id_product=?, id_customer=?, quantity=?, total_price=?
                    WHERE id_sale=?
                """, (product_id, customer_id, quantity, total_price, sale_id))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Sale updated successfully")
                dialog.destroy()
                self.show_sales()
            except ValueError:
                messagebox.showerror("Input Error", "Quantity must be a valid number")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to update sale: {e}")
        
        button_frame = tk.Frame(form_frame, bg=self.colors['light'])
        button_frame.grid(row=7, column=0, pady=(10, 0))
        
        ttk.Button(button_frame, text="Update", command=update_sale,
                  style='Action.TButton', width=12).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy,
                  style='Delete.TButton', width=12).pack(side='left', padx=5)
    
    def delete_sale(self, tree):
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a sale to delete")
            return
        
        item = tree.item(selection[0])
        sale_id = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete",
                              f"Are you sure you want to delete Sale #{sale_id}?"):
            try:
                conn = self.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Sale WHERE id_sale=?", (sale_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Sale deleted successfully")
                self.show_sales()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete sale: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StoreInventoryApp(root)
    root.mainloop()
