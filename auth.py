"""
Authentication GUI module for login and signup
"""
import tkinter as tk
from tkinter import messagebox, ttk
from database import Database

class AuthWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.db = Database()
        self.on_login_success = on_login_success
        
        self.root.title("SDG 4 Education System - Login")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        
        self.show_login_page()
    
    def clear_frame(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_page(self):
        """Display login page"""
        self.clear_frame()
        
        # Title
        title = tk.Label(self.root, text="SDG 4 Quality Education System", 
                        font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root, text="Login to Your Account", 
                           font=("Arial", 12), bg="#f0f0f0", fg="#34495e")
        subtitle.pack(pady=5)
        
        # Frame for inputs
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Username
        tk.Label(frame, text="Username:", bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(10, 0))
        self.username_entry = tk.Entry(frame, width=30, font=("Arial", 10))
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(frame, text="Password:", bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(10, 0))
        self.password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 10))
        self.password_entry.pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        # Login button
        login_btn = tk.Button(btn_frame, text="Login", width=15, bg="#3498db", fg="white",
                             font=("Arial", 10, "bold"), command=self.login)
        login_btn.pack(pady=5)
        
        # Signup button
        signup_btn = tk.Button(btn_frame, text="Create New Account", width=15, bg="#27ae60", fg="white",
                              font=("Arial", 10, "bold"), command=self.show_signup_page)
        signup_btn.pack(pady=5)
    
    def show_signup_page(self):
        """Display signup page"""
        self.clear_frame()
        
        # Title
        title = tk.Label(self.root, text="SDG 4 Quality Education System", 
                        font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root, text="Create New Account", 
                           font=("Arial", 12), bg="#f0f0f0", fg="#34495e")
        subtitle.pack(pady=5)
        
        # Frame for inputs
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Username
        tk.Label(frame, text="Username:", bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(10, 0))
        self.new_username_entry = tk.Entry(frame, width=30, font=("Arial", 10))
        self.new_username_entry.pack(pady=5)
        
        # Email
        tk.Label(frame, text="Email:", bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(10, 0))
        self.email_entry = tk.Entry(frame, width=30, font=("Arial", 10))
        self.email_entry.pack(pady=5)
        
        # Password
        tk.Label(frame, text="Password:", bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(10, 0))
        self.new_password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 10))
        self.new_password_entry.pack(pady=5)
        
        # Confirm Password
        tk.Label(frame, text="Confirm Password:", bg="#f0f0f0", fg="#2c3e50").pack(anchor="w", pady=(10, 0))
        self.confirm_password_entry = tk.Entry(frame, width=30, show="*", font=("Arial", 10))
        self.confirm_password_entry.pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        # Signup button
        signup_btn = tk.Button(btn_frame, text="Create Account", width=15, bg="#27ae60", fg="white",
                              font=("Arial", 10, "bold"), command=self.signup)
        signup_btn.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(btn_frame, text="Back to Login", width=15, bg="#95a5a6", fg="white",
                            font=("Arial", 10, "bold"), command=self.show_login_page)
        back_btn.pack(pady=5)
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        success, user = self.db.login_user(username, password)
        
        if success:
            messagebox.showinfo("Success", f"Welcome {user[1]}!")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid username or password!")
    
    def signup(self):
        """Handle signup"""
        username = self.new_username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters!")
            return
        
        success, message = self.db.register_user(username, email, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.show_login_page()
        else:
            messagebox.showerror("Error", message)
