import os
import pathlib
import subprocess
import tkinter as tk
from tkinter import ttk

from HW2.file_management.getting_specific_user_info import get_user_info


class AP2P(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (UserAuthPage, ProfilePage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(UserAuthPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class UserAuthPage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        controller.geometry("480x270")
        controller.title("Authorization")

        button1 = ttk.Button(self, text="Login", command=self.login)
        button1.place(relx=0.5, rely=0.35, relheight=0.2, relwidth=0.3, anchor="center")

        button2 = ttk.Button(self, text="Register", command=self.signup)
        button2.place(relx=0.5, rely=0.65, relheight=0.2, relwidth=0.3, anchor="center")

    def signup(self):
        self.register_screen = tk.Toplevel(self.controller)
        self.register_screen.title("Register")
        self.register_screen.geometry("400x175")

        self.username_verify = tk.StringVar()
        self.password_verify = tk.StringVar()

        label1 = tk.Label(self.register_screen, text="Username")
        label1.place(relx=0.35, rely=0.2, relheight=0.2, relwidth=0.3, anchor="center")
        self.username_register_entry = tk.Entry(self.register_screen, textvariable=self.username_verify)
        self.username_register_entry.place(relx=0.65, rely=0.2, relheight=0.15, relwidth=0.3, anchor="center")

        label2 = tk.Label(self.register_screen, text="Password")
        label2.place(relx=0.35, rely=0.5, relheight=0.2, relwidth=0.3, anchor="center")
        self.password_register_entry = tk.Entry(self.register_screen, textvariable=self.password_verify, show='*')
        self.password_register_entry.place(relx=0.65, rely=0.5, relheight=0.15, relwidth=0.3, anchor="center")

        button = tk.Button(self.register_screen, text="Register", command=self.signup_verify)
        button.place(relx=0.5, rely=0.8, relheight=0.2, relwidth=0.4, anchor="center")

    def login(self):
        self.login_screen = tk.Toplevel(self.controller)
        self.login_screen.title("Login")
        self.login_screen.geometry("400x175")

        self.username_verify = tk.StringVar()
        self.password_verify = tk.StringVar()

        label1 = tk.Label(self.login_screen, text="Username")
        label1.place(relx=0.35, rely=0.2, relheight=0.2, relwidth=0.3, anchor="center")
        self.username_login_entry = tk.Entry(self.login_screen, textvariable=self.username_verify)
        self.username_login_entry.place(relx=0.65, rely=0.2, relheight=0.15, relwidth=0.3, anchor="center")

        label2 = tk.Label(self.login_screen, text="Password")
        label2.place(relx=0.35, rely=0.5, relheight=0.2, relwidth=0.3, anchor="center")
        self.password_login_entry = tk.Entry(self.login_screen, textvariable=self.password_verify, show='*')
        self.password_login_entry.place(relx=0.65, rely=0.5, relheight=0.15, relwidth=0.3, anchor="center")

        button = tk.Button(self.login_screen, text="Login", command=self.login_verify)
        button.place(relx=0.5, rely=0.8, relheight=0.2, relwidth=0.4, anchor="center")

    def signup_verify(self):
        username = self.username_verify.get()

        user_info = get_user_info(username)
        if user_info is None:
            # Register new user
            self.signup_user()
            self.signup_success()
        else:
            # User already exists
            self.signup_user_found()

        self.username_register_entry.delete(0, tk.END)
        self.password_register_entry.delete(0, tk.END)

    def login_verify(self):
        username = self.username_verify.get()
        password = self.password_verify.get()
        self.username_login_entry.delete(0, tk.END)
        self.password_login_entry.delete(0, tk.END)

        user_info = get_user_info(username)
        if user_info is None:
            # User doesn't exist
            self.user_not_found()
        else:
            # User exists
            username_loaded = user_info["name"]
            password_loaded = user_info["password"]
            if password == password_loaded:
                # Correct password
                self.login_success()
            else:
                # Wrong password
                self.password_not_recognised()

    def signup_success(self):
        self.register_success_screen = tk.Toplevel(self.register_screen)
        self.register_success_screen.title("Success")
        self.register_success_screen.geometry("360x120")

        label = tk.Label(self.register_success_screen, text="Registration Success")
        label.place(relx=0.5, rely=0.35, anchor="center")

        def register_close():
            self.register_success_screen.destroy()
            self.register_screen.destroy()

        button = tk.Button(self.register_success_screen, text="OK", command=register_close)
        button.place(relx=0.5, rely=0.65, anchor="center")

    def signup_user(self):
        username = self.username_verify.get()
        password = self.password_verify.get()

        try:
            path_to_dir = pathlib.Path().resolve().parent
            script_path = os.path.join(path_to_dir, "file_management", "create_user.py")
            script_args = [username, password]
            command = ['python', script_path] + script_args

            # Run the command
            subprocess.run(command, check=True)
            print("Script executed successfully")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e)

    def signup_user_found(self):
        self.register_user_found_screen = tk.Toplevel(self.register_screen)
        self.register_user_found_screen.title("Error")
        self.register_user_found_screen.geometry("360x120")

        label = tk.Label(self.register_user_found_screen, text="User already exists")
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.register_user_found_screen, text="OK", command=self.register_user_found_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")

    def login_success(self):
        self.login_screen.destroy()
        self.controller.show_frame(ProfilePage)

    def password_not_recognised(self):
        self.password_not_recog_screen = tk.Toplevel(self.login_screen)
        self.password_not_recog_screen.title("Error")
        self.password_not_recog_screen.geometry("360x120")

        label = tk.Label(self.password_not_recog_screen, text="Invalid Password")
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.password_not_recog_screen, text="OK", command=self.password_not_recog_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")

    def user_not_found(self):
        self.user_not_found_screen = tk.Toplevel(self.login_screen)
        self.user_not_found_screen.title("Error")
        self.user_not_found_screen.geometry("360x120")

        label = tk.Label(self.user_not_found_screen, text="User not found")
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.user_not_found_screen, text="OK", command=self.user_not_found_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")


class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Profile Page")
        label.place(relx=0.5, rely=0.35, anchor="center")

        button1 = ttk.Button(self, text="AuthPage", command=lambda: controller.show_frame(UserAuthPage))
        button1.place(relx=0.5, rely=0.65, anchor="center")


if __name__ == "__main__":
    app = AP2P()
    app.mainloop()
