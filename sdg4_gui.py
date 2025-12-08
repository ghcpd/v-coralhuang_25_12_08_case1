import os
import sqlite3
import hashlib
import secrets
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

DB = "users.db"
MODULE_DIR = "modules"

MODULES = [
    ("Foundations of Learning", "Intro to pedagogy, inclusive practices and assessment.", "foundations.txt"),
    ("Literacy & Communication", "Reading strategies, curriculum integration and language support.", "literacy.txt"),
    ("Digital Skills for Learning", "Basic digital literacy, using ed-tech, safe internet practices.", "digital.txt"),
]

# --- setup ---
os.makedirs(MODULE_DIR, exist_ok=True)
for _, content, fname in MODULES:
    path = os.path.join(MODULE_DIR, fname)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content + "\n\nSample content for module: " + fname)

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    salt TEXT,
    pw_hash TEXT
)
""")
conn.commit()

# --- auth helpers ---
def hash_pw(password, salt):
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def register_user(username, password):
    salt = secrets.token_hex(16)
    pw_hash = hash_pw(password, salt)
    try:
        cur.execute("INSERT INTO users (username, salt, pw_hash) VALUES (?, ?, ?)", (username, salt, pw_hash))
        conn.commit()
        return True, "Account created."
    except sqlite3.IntegrityError:
        return False, "Username already exists."


def check_login(username, password):
    cur.execute("SELECT salt, pw_hash FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    if not row:
        return False
    salt, pw_hash = row
    return hash_pw(password, salt) == pw_hash

# --- GUI ---
class App:
    def __init__(self, root):
        self.root = root
        root.title("SDG4 - Quality Education")
        self.show_login()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        tk.Label(self.root, text="Sign in").pack(pady=8)
        tk.Label(self.root, text="Username").pack()
        self.user_e = tk.Entry(self.root); self.user_e.pack()
        tk.Label(self.root, text="Password").pack()
        self.pw_e = tk.Entry(self.root, show="*"); self.pw_e.pack()
        tk.Button(self.root, text="Sign In", command=self.attempt_login).pack(pady=6)
        tk.Button(self.root, text="Create account", command=self.show_register).pack()

    def show_register(self):
        self.clear()
        tk.Label(self.root, text="Create account").pack(pady=8)
        tk.Label(self.root, text="Username").pack()
        self.reg_user = tk.Entry(self.root); self.reg_user.pack()
        tk.Label(self.root, text="Password").pack()
        self.reg_pw = tk.Entry(self.root, show="*"); self.reg_pw.pack()
        tk.Label(self.root, text="Confirm password").pack()
        self.reg_pw2 = tk.Entry(self.root, show="*"); self.reg_pw2.pack()
        tk.Button(self.root, text="Register", command=self.attempt_register).pack(pady=6)
        tk.Button(self.root, text="Back to Sign In", command=self.show_login).pack()

    def attempt_register(self):
        u = self.reg_user.get().strip()
        p = self.reg_pw.get()
        p2 = self.reg_pw2.get()
        if not u or not p:
            messagebox.showerror("Error", "Enter username and password.")
            return
        if p != p2:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        ok, msg = register_user(u, p)
        if ok:
            messagebox.showinfo("Success", msg)
            self.show_login()
        else:
            messagebox.showerror("Error", msg)

    def attempt_login(self):
        u = self.user_e.get().strip()
        p = self.pw_e.get()
        if check_login(u, p):
            self.username = u
            self.show_home()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def show_home(self):
        self.clear()
        tk.Label(self.root, text=f"Welcome, {self.username}").pack(pady=6)
        tk.Label(self.root, text="Modules").pack()
        for title, desc, fname in MODULES:
            frm = tk.Frame(self.root, bd=1, relief="groove", padx=6, pady=4)
            frm.pack(fill="x", padx=8, pady=4)
            tk.Label(frm, text=title, font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
            tk.Label(frm, text=desc).pack(anchor="w")
            btn = tk.Button(frm, text="Download", command=lambda f=fname: self.download_module(f))
            btn.pack(anchor="e")
        tk.Button(self.root, text="Sign Out", command=self.show_login).pack(pady=8)

    def download_module(self, fname):
        src = os.path.join(MODULE_DIR, fname)
        if not os.path.exists(src):
            messagebox.showerror("Error", "Module not found.")
            return
        dest = filedialog.asksaveasfilename(initialfile=fname, defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if dest:
            try:
                shutil.copy(src, dest)
                messagebox.showinfo("Downloaded", f"Saved to {dest}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x360")
    App(root)
    root.mainloop()
