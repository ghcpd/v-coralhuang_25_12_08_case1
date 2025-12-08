"""
Home page GUI showing modules and download functionality
"""
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
from database import Database

class HomeWindow:
    def __init__(self, root, user_info):
        self.root = root
        self.user_id, self.username = user_info
        self.db = Database()
        
        self.root.title(f"SDG 4 Quality Education System - Welcome {self.username}")
        self.root.geometry("900x700")
        self.root.configure(bg="#ecf0f1")
        
        self.create_home_page()
    
    def create_home_page(self):
        """Create the home page layout"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x", side="top")
        
        title = tk.Label(header_frame, text="SDG 4 - Quality Education Portal",
                        font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=10)
        
        user_label = tk.Label(header_frame, text=f"Logged in as: {self.username}",
                             font=("Arial", 10), bg="#2c3e50", fg="#ecf0f1")
        user_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#ecf0f1")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = tk.Label(content_frame, 
                               text="Welcome to the SDG 4 Quality Education System!\n"
                                    "Explore and download educational modules below.",
                               font=("Arial", 11), bg="#ecf0f1", fg="#2c3e50", justify="center")
        instructions.pack(pady=10)
        
        # Modules section
        modules_label = tk.Label(content_frame, text="Available Modules",
                                font=("Arial", 13, "bold"), bg="#ecf0f1", fg="#2c3e50")
        modules_label.pack(anchor="w", pady=(20, 10))
        
        # Get all modules
        modules = self.db.get_all_modules()
        
        # Create module cards
        for module_id, title, description in modules:
            self.create_module_card(content_frame, module_id, title, description)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#34495e", height=50)
        footer_frame.pack(fill="x", side="bottom")
        
        logout_btn = tk.Button(footer_frame, text="Logout", bg="#e74c3c", fg="white",
                              font=("Arial", 10, "bold"), width=15, command=self.logout)
        logout_btn.pack(side="right", padx=20, pady=10)
    
    def create_module_card(self, parent, module_id, title, description):
        """Create a module card widget"""
        card = tk.Frame(parent, bg="white", relief="ridge", borderwidth=2)
        card.pack(fill="x", pady=10)
        
        # Module title
        title_label = tk.Label(card, text=title, font=("Arial", 12, "bold"),
                              bg="white", fg="#2c3e50", justify="left")
        title_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Module description
        desc_label = tk.Label(card, text=description, font=("Arial", 10),
                             bg="white", fg="#34495e", justify="left", wraplength=700)
        desc_label.pack(anchor="w", padx=15, pady=5)
        
        # Button frame
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(anchor="e", padx=15, pady=(5, 10))
        
        # View button
        view_btn = tk.Button(btn_frame, text="View Content", bg="#3498db", fg="white",
                            font=("Arial", 9, "bold"), width=12,
                            command=lambda: self.view_module(module_id, title))
        view_btn.pack(side="left", padx=5)
        
        # Download button
        download_btn = tk.Button(btn_frame, text="Download", bg="#27ae60", fg="white",
                                font=("Arial", 9, "bold"), width=12,
                                command=lambda: self.download_module(module_id, title))
        download_btn.pack(side="left", padx=5)
    
    def view_module(self, module_id, title):
        """Open module content in a new window"""
        module_data = self.db.get_module_content(module_id)
        
        if not module_data:
            messagebox.showerror("Error", "Module not found!")
            return
        
        # Create new window
        view_window = tk.Toplevel(self.root)
        view_window.title(f"View - {title}")
        view_window.geometry("800x600")
        view_window.configure(bg="#ecf0f1")
        
        # Header
        header = tk.Label(view_window, text=title, font=("Arial", 14, "bold"),
                         bg="#2c3e50", fg="white", pady=10)
        header.pack(fill="x")
        
        # Content
        content_frame = tk.Frame(view_window, bg="white")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Text widget with scrollbar
        scrollbar = ttk.Scrollbar(content_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = tk.Text(content_frame, wrap="word", yscrollcommand=scrollbar.set,
                             font=("Arial", 10), bg="white", fg="#2c3e50")
        text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Insert content
        _, _, content = module_data
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        
        # Close button
        close_btn = tk.Button(view_window, text="Close", bg="#95a5a6", fg="white",
                             font=("Arial", 10, "bold"), command=view_window.destroy)
        close_btn.pack(pady=10)
    
    def download_module(self, module_id, title):
        """Download module as text file"""
        module_data = self.db.get_module_content(module_id)
        
        if not module_data:
            messagebox.showerror("Error", "Module not found!")
            return
        
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile=f"{title.replace(' ', '_')}.txt"
        )
        
        if file_path:
            try:
                module_title, module_desc, content = module_data
                
                # Create file content
                file_content = f"""
================================================================================
                    SDG 4 QUALITY EDUCATION MODULE
================================================================================

Title: {module_title}

Description:
{module_desc}

================================================================================
CONTENT
================================================================================

{content}

================================================================================
Downloaded from: SDG 4 Quality Education System
================================================================================
"""
                
                # Write to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                
                # Record download in database
                self.db.record_download(self.user_id, module_id)
                
                messagebox.showinfo("Success", f"Module downloaded successfully!\nSaved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download: {str(e)}")
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
