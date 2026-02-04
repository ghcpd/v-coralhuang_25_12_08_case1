import os
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
MODULES_DIR = os.path.join(ROOT_DIR, 'modules')
ACCOUNTS_FILE = os.path.join(DATA_DIR, 'accounts.json')

SAMPLE_MODULES = [
    {
        'id': 'M01',
        'title': 'Foundations of Quality Education',
        'file': 'module_foundations.txt',
        'description': 'An overview of core principles, education equity, and SDG 4 goals.'
    },
    {
        'id': 'M02',
        'title': 'Modern Teaching Methods',
        'file': 'module_teaching_methods.txt',
        'description': 'Suggested pedagogies and tools for effective learning.'
    },
    {
        'id': 'M03',
        'title': 'Assessment & Learning Outcomes',
        'file': 'module_assessment.txt',
        'description': 'Assessment strategies and measuring learning outcomes.'
    }
]


def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MODULES_DIR, exist_ok=True)
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)


def create_account(username, password):
    ensure_directories()
    with open(ACCOUNTS_FILE, 'r+', encoding='utf-8') as f:
        try:
            accounts = json.load(f)
        except json.JSONDecodeError:
            accounts = {}
        if username in accounts:
            return False, 'Username already exists.'
        accounts[username] = password
        f.seek(0)
        json.dump(accounts, f, indent=2)
        f.truncate()
    return True, 'Account created.'


def authenticate_user(username, password):
    ensure_directories()
    try:
        with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
            accounts = json.load(f)
    except Exception:
        accounts = {}
    pwd = accounts.get(username)
    if pwd is None:
        return False
    return pwd == password


class LoginFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.columnconfigure(0, weight=1)

        title = ttk.Label(self, text='SDG 4 – Quality Education', font=('Segoe UI', 16, 'bold'))
        title.grid(row=0, column=0, pady=(10,10))

        form = ttk.Frame(self)
        form.grid(row=1, column=0, padx=20, pady=10)

        ttk.Label(form, text='Username:').grid(row=0, column=0, sticky='w')
        self.username = ttk.Entry(form)
        self.username.grid(row=0, column=1, pady=5)

        ttk.Label(form, text='Password:').grid(row=1, column=0, sticky='w')
        self.password = ttk.Entry(form, show='*')
        self.password.grid(row=1, column=1, pady=5)

        btnframe = ttk.Frame(self)
        btnframe.grid(row=2, column=0, pady=10)

        login_btn = ttk.Button(btnframe, text='Sign in', command=self.do_signin)
        login_btn.grid(row=0, column=0, padx=5)
        signup_btn = ttk.Button(btnframe, text="Create account", command=self.open_signup)
        signup_btn.grid(row=0, column=1, padx=5)

    def do_signin(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        if not user or not pwd:
            messagebox.showwarning('Missing', 'Please enter both username and password.')
            return
        ok = authenticate_user(user, pwd)
        if ok:
            self.app.current_user = user
            self.app.show_home()
        else:
            messagebox.showerror('Sign in failed', 'Incorrect username or password.')

    def open_signup(self):
        SignupWindow(self)


class SignupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Create Account')
        self.resizable(False, False)
        self.transient(parent)
        ttk.Label(self, text='Create new account', font=('Segoe UI', 12)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text='Username:').grid(row=1, column=0)
        self.username = ttk.Entry(self)
        self.username.grid(row=1, column=1, pady=5)

        ttk.Label(self, text='Password:').grid(row=2, column=0)
        self.password = ttk.Entry(self, show='*')
        self.password.grid(row=2, column=1, pady=5)

        self.msg = ttk.Label(self, text='', foreground='red')
        self.msg.grid(row=3, column=0, columnspan=2)

        create_btn = ttk.Button(self, text='Create', command=self.create)
        create_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def create(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        if not user or not pwd:
            self.msg['text'] = 'Please provide both username and password.'
            return
        ok, text = create_account(user, pwd)
        if not ok:
            self.msg['text'] = text
            return
        messagebox.showinfo('Success', text)
        self.destroy()


class ModuleItem(ttk.Frame):
    def __init__(self, parent, info):
        super().__init__(parent)
        self.info = info
        self.columnconfigure(0, weight=1)
        title = ttk.Label(self, text=info['title'], font=('Segoe UI', 11, 'bold'))
        title.grid(row=0, column=0, sticky='w')
        desc = ttk.Label(self, text=info['description'], wraplength=400)
        desc.grid(row=1, column=0, sticky='w')
        self.down_btn = ttk.Button(self, text='Download', command=self.download)
        self.down_btn.grid(row=0, column=1, rowspan=2, padx=10)

    def download(self):
        src = os.path.join(MODULES_DIR, self.info['file'])
        if not os.path.exists(src):
            messagebox.showerror('Not found', 'The module file is missing.')
            return
        dest = filedialog.asksaveasfilename(title='Save module as', initialfile=self.info['file'])
        if not dest:
            return
        try:
            shutil.copy(src, dest)
            messagebox.showinfo('Downloaded', f"Saved '{self.info['title']}' to {dest}")
        except Exception as e:
            messagebox.showerror('Error', str(e))


class HomeFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        header = ttk.Label(self, text='Available Modules', font=('Segoe UI', 14, 'bold'))
        header.grid(row=0, column=0, pady=(8, 8), sticky='w')

        welcome = ttk.Label(self, text=f'Welcome — {app.current_user}', foreground='gray')
        welcome.grid(row=1, column=0, sticky='w')

        container = ttk.Frame(self)
        container.grid(row=2, column=0, pady=10)

        for i, m in enumerate(SAMPLE_MODULES):
            item = ModuleItem(container, m)
            item.grid(row=i, column=0, pady=8, sticky='w')

        signout = ttk.Button(self, text='Sign out', command=self.signout)
        signout.grid(row=3, column=0, pady=8, sticky='w')

    def signout(self):
        self.app.current_user = None
        self.app.show_login()


class EducationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        ensure_directories()
        self.title('SDG 4 - Quality Education')
        self.geometry('600x420')
        self.resizable(False, False)
        self.current_user = None

        self.main = ttk.Frame(self)
        self.main.pack(fill='both', expand=True, padx=20, pady=20)

        self.login = LoginFrame(self.main, self)
        self.home = None

        self.login.pack(fill='both', expand=True)

    def show_home(self):
        if self.login is not None:
            self.login.pack_forget()
        if self.home:
            self.home.pack_forget()
        self.home = HomeFrame(self.main, self)
        self.home.pack(fill='both', expand=True)

    def show_login(self):
        if self.home is not None:
            self.home.pack_forget()
            self.home = None
        self.login = LoginFrame(self.main, self)
        self.login.pack(fill='both', expand=True)


def create_sample_modules():
    ensure_directories()
    for m in SAMPLE_MODULES:
        path = os.path.join(MODULES_DIR, m['file'])
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"{m['title']}\n\n{m['description']}\n\n(Example content about SDG 4.)\n")


if __name__ == '__main__':
    create_sample_modules()
    app = EducationApp()
    app.mainloop()
