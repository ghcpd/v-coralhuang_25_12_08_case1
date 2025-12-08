import tkinter as tk
from tkinter import messagebox, filedialog
import hashlib, json, os, shutil

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
MODULES_DIR = os.path.join(DATA_DIR, "modules")

MODULES = [
    {
        "id": "module1",
        "title": "Early Childhood Foundations",
        "desc": "Principles for high-quality early childhood care & learning. Activities, lesson plans and assessment templates.",
        "file": "early_childhood.txt"
    },
    {
        "id": "module2",
        "title": "Inclusive Classroom Strategies",
        "desc": "Practical guidance for inclusive teaching — adaptations, classroom management and assessment for diverse learners.",
        "file": "inclusive_classroom.txt"
    },
    {
        "id": "module3",
        "title": "Digital Pedagogy & Literacy",
        "desc": "Blended learning, digital literacy, safe use of edtech and sample digital lesson designs.",
        "file": "digital_pedagogy.txt"
    }
]


def ensure_data():
    os.makedirs(MODULES_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    for m in MODULES:
        path = os.path.join(MODULES_DIR, m["file"]) 
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"{m['title']}\n\n{m['desc']}\n\nSample content for {m['title']}.\n")


def hash_pw(pw):
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(u):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(u, f, indent=2)


class LoginApp:
    def __init__(self, root):
        self.root = root
        root.title("SDG4 — Sign in")
        tk.Label(root, text="Username").grid(row=0, column=0, sticky="e")
        tk.Label(root, text="Password").grid(row=1, column=0, sticky="e")
        self.u = tk.Entry(root)
        self.p = tk.Entry(root, show="*")
        self.u.grid(row=0, column=1)
        self.p.grid(row=1, column=1)
        tk.Button(root, text="Sign In", command=self.sign_in).grid(row=2, column=0, pady=8)
        tk.Button(root, text="Create account", command=self.open_signup).grid(row=2, column=1)

    def sign_in(self):
        username = self.u.get().strip()
        pw = self.p.get()
        if not username or not pw:
            messagebox.showwarning("Input", "Enter username and password")
            return
        users = load_users()
        if username in users and users[username]["hash"] == hash_pw(pw):
            HomeWindow(self.root, username)
        else:
            messagebox.showerror("Auth failed", "Wrong username or password")

    def open_signup(self):
        SignupWindow(self.root)


class SignupWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Create account")
        tk.Label(self.top, text="New username").grid(row=0, column=0)
        tk.Label(self.top, text="Password").grid(row=1, column=0)
        self.u = tk.Entry(self.top)
        self.p = tk.Entry(self.top, show="*")
        self.u.grid(row=0, column=1)
        self.p.grid(row=1, column=1)
        tk.Button(self.top, text="Create", command=self.create).grid(row=2, column=0, columnspan=2, pady=6)

    def create(self):
        username = self.u.get().strip()
        pw = self.p.get()
        if not username or not pw:
            messagebox.showwarning("Input", "Enter username and password")
            return
        users = load_users()
        if username in users:
            messagebox.showerror("Exists", "Username already exists")
            return
        users[username] = {"hash": hash_pw(pw)}
        save_users(users)
        messagebox.showinfo("Success", "Account created — you can sign in now")
        self.top.destroy()


class HomeWindow:
    def __init__(self, root, username):
        self.win = tk.Toplevel(root)
        self.win.title("Home — Modules")
        tk.Label(self.win, text=f"Welcome, {username}", font=("Helvetica", 12, "bold")).pack(pady=6)
        frame = tk.Frame(self.win)
        frame.pack(padx=10, pady=4)
        for m in MODULES:
            bf = tk.Frame(frame, relief="groove", bd=1, padx=6, pady=6)
            bf.pack(fill="x", pady=4)
            tk.Label(bf, text=m["title"], font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w")
            tk.Label(bf, text=m["desc"], wraplength=420, justify="left").grid(row=1, column=0, sticky="w")
            tk.Button(bf, text="Download", command=lambda mm=m: self.download(mm)).grid(row=0, column=1, rowspan=2, padx=8)

    def download(self, module):
        src = os.path.join(MODULES_DIR, module["file"])
        if not os.path.exists(src):
            messagebox.showerror("Not found", "Module content is missing")
            return
        dest_dir = filedialog.askdirectory(title="Choose folder to save module")
        if not dest_dir:
            return
        dest = os.path.join(dest_dir, module["file"])
        try:
            shutil.copy(src, dest)
            messagebox.showinfo("Saved", f"{module['title']} saved to {dest_dir}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    ensure_data()
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()
