import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import sqlite3
import hashlib
import os

DB = 'users.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(username: str, password: str) -> bool:
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return False
    return row[0] == hash_password(password)

MODULES_DIR = 'modules'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('SDG4 Quality Education')
        self.current_user = None

        self.frame = tk.Frame(root, padx=12, pady=12)
        self.frame.pack()
        self.show_login()

    def clear(self):
        for w in self.frame.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        tk.Label(self.frame, text='Welcome — SDG4 Education', font=('Arial', 14)).pack(pady=6)
        tk.Button(self.frame, text='Sign In', width=20, command=self.sign_in).pack(pady=4)
        tk.Button(self.frame, text="Create Account", width=20, command=self.sign_up).pack(pady=4)

    def sign_up(self):
        username = simpledialog.askstring('Create Account', 'Choose a username:', parent=self.root)
        if not username:
            return
        password = simpledialog.askstring('Create Account', 'Choose a password:', show='*', parent=self.root)
        if not password:
            return
        ok = create_user(username.strip(), password)
        if ok:
            messagebox.showinfo('Account Created', 'Your account was created. Please sign in.')
        else:
            messagebox.showerror('Error', 'Username already exists.')

    def sign_in(self):
        username = simpledialog.askstring('Sign In', 'Username:', parent=self.root)
        if not username:
            return
        password = simpledialog.askstring('Sign In', 'Password:', show='*', parent=self.root)
        if not password:
            return
        if authenticate(username.strip(), password):
            self.current_user = username.strip()
            self.show_home()
        else:
            messagebox.showerror('Sign In Failed', 'Invalid username or password.')

    def show_home(self):
        self.clear()
        tk.Label(self.frame, text=f'Hello, {self.current_user}', font=('Arial', 12)).pack()
        tk.Label(self.frame, text='Available Modules:', font=('Arial', 11, 'underline')).pack(pady=(8,4))

        modules = []
        if os.path.isdir(MODULES_DIR):
            for fname in os.listdir(MODULES_DIR):
                if fname.endswith('.txt'):
                    modules.append(fname)

        for m in modules:
            frm = tk.Frame(self.frame)
            frm.pack(fill='x', pady=2)
            tk.Label(frm, text=m.replace('.txt',''), anchor='w').pack(side='left', padx=(2,8))
            tk.Button(frm, text='Open', command=lambda mm=m: self.open_module(mm)).pack(side='left')
            tk.Button(frm, text='Download', command=lambda mm=m: self.download_module(mm)).pack(side='left', padx=6)

        tk.Button(self.frame, text='Log Out', command=self.logout).pack(pady=(10,0))

    def open_module(self, module_file):
        path = os.path.join(MODULES_DIR, module_file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            top = tk.Toplevel(self.root)
            top.title(module_file.replace('.txt',''))
            txt = tk.Text(top, wrap='word', width=60, height=20)
            txt.insert('1.0', content)
            txt.config(state='disabled')
            txt.pack(padx=8, pady=8)
        except Exception as e:
            messagebox.showerror('Error', f'Could not open module: {e}')

    def download_module(self, module_file):
        path = os.path.join(MODULES_DIR, module_file)
        save_to = filedialog.asksaveasfilename(initialfile=module_file, defaultextension='.txt')
        if not save_to:
            return
        try:
            with open(path, 'rb') as src, open(save_to, 'wb') as dst:
                dst.write(src.read())
            messagebox.showinfo('Downloaded', f'Module saved to {save_to}')
        except Exception as e:
            messagebox.showerror('Error', f'Could not save module: {e}')

    def logout(self):
        self.current_user = None
        self.show_login()


if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
