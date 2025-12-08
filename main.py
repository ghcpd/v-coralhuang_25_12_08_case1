"""
Main entry point for SDG 4 Quality Education System
"""
import tkinter as tk
from auth import AuthWindow
from home import HomeWindow

class SDG4EducationApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#f0f0f0")
        
        # Start with login/signup
        self.show_auth()
    
    def show_auth(self):
        """Show authentication window"""
        AuthWindow(self.root, self.on_login_success)
    
    def on_login_success(self, user_info):
        """Handle successful login"""
        # Clear root and show home page
        for widget in self.root.winfo_children():
            widget.destroy()
        
        HomeWindow(self.root, user_info)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = SDG4EducationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
