import os
import sys
import pathlib
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

path_to_proj_dir = pathlib.Path().resolve().parent

path_to_file_management = os.path.join(path_to_proj_dir, "file_management")
sys.path.insert(1, str(path_to_file_management))

path_to_network = os.path.join(path_to_proj_dir, "network")
sys.path.insert(2, str(path_to_network))

from getting_specific_user_info import get_user_info
from peer import Peer

sidebar_color = '#263238'
header_color = '#62A8EA'
header_shadow_color = '#5897D3'
gray_color = "#868E96"
light_gray_color = '#526069'


class AP2P(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.username = tk.StringVar()

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1280x720")
        self.resizable(False, False)
        self.title("P2P")
        self.config(bg=header_color)
        self.path_to_dir = pathlib.Path().resolve().parent
        self.image_path = os.path.join(self.path_to_dir, "gui", "images")
        logo_icon = tk.PhotoImage(file=os.path.join(self.image_path, "NUP_logo.png"))
        header_icon = tk.PhotoImage(file=os.path.join(self.image_path, "NUP_header.png"))
        self.iconphoto(True, logo_icon)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=0, rely=0, relwidth=1, relheight=0.3)

        # UNIVERSITY LOGO AND NAME
        self.brand_frame = tk.Frame(self.header, bg=header_color)
        self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)
        self.uni_logo = logo_icon.subsample(9)
        logo = tk.Label(self.brand_frame, image=self.uni_logo, bg=header_color)
        logo.place(x=5, y=20)

        self.uni_name = header_icon.subsample(2)
        uni_name = tk.Label(self.brand_frame, image=self.uni_name, bg=header_color)
        uni_name.place(x=5, y=0)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0.1, relwidth=0.25, relheight=1)

        # SUBMENUS IN SIDE BAR

        # # SUBMENU 1
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        self.submenu_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        submenu1 = AuthSidebarSubMenu(self.submenu_frame,
                                      sub_menu_heading='User Authorization',
                                      sub_menu_options=["Login",
                                                        "Register",
                                                        ]
                                      )
        submenu1.options["Login"].config(
            command=lambda: self.show_frame(LoginPage)
        )
        submenu1.options["Register"].config(
            command=lambda: self.show_frame(SignupPage)
        )

        submenu1.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="gray", highlightthickness=0.5)
        container.place(relx=0.25, rely=0.1, relwidth=0.75, relheight=0.9)

        self.frames = {}

        for F in (LoginPage,
                  WelcomePage,
                  SignupPage,
                  ProfilePage
                  ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.show_frame(WelcomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.config(bg='white')

        label = tk.Label(self, text='Welcome to P2P client', font=("", 15), bg='white')
        label.place(relx=0.5, rely=0.25, anchor='center')


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        self.config(bg='white')

        self.username_verify = tk.StringVar()
        self.password_verify = tk.StringVar()

        label0 = tk.Label(self, text='Login', font=("", 15), bg='white')
        label0.place(relx=0.5, rely=0.1, relheight=0.2, relwidth=0.4, anchor="center")

        label1 = tk.Label(self, text="Username", font=("", 10), bg='white')
        label1.place(relx=0.2, rely=0.4, relheight=0.2, relwidth=0.3, anchor="center")
        self.username_login_entry = tk.Entry(self, textvariable=self.username_verify, font=("", 10))
        self.username_login_entry.place(relx=0.5, rely=0.4, relheight=0.075, relwidth=0.3, anchor="center")

        label2 = tk.Label(self, text="Password", font=("", 10), bg='white')
        label2.place(relx=0.2, rely=0.55, relheight=0.2, relwidth=0.3, anchor="center")
        self.password_login_entry = tk.Entry(self, textvariable=self.password_verify, font=("", 10), show='*')
        self.password_login_entry.place(relx=0.5, rely=0.55, relheight=0.075, relwidth=0.3, anchor="center")

        button = tk.Button(self, text="Login", font=("", 10), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white', command=self.login_verify)
        button.place(relx=0.5, rely=0.7, relheight=0.1, relwidth=0.2, anchor="center")

    def login_verify(self):
        username = self.username_verify.get()
        password = self.password_verify.get()
        self.username_login_entry.delete(0, tk.END)
        self.password_login_entry.delete(0, tk.END)

        if not username:
            self.no_name()
        else:
            user_info = get_user_info(username)
            if user_info is None:
                # User doesn't exist
                self.user_not_found()
            else:
                # User exists
                password_loaded = user_info["password"]
                if password == password_loaded:
                    # Correct password
                    self.login_success(username)
                else:
                    # Wrong password
                    self.password_not_recognised()

    def login_success(self, username):
        self.controller.username.set(username)
        self.controller.frames[ProfilePage].peer = Peer(username)
        self.controller.frames[ProfilePage].peer.start()
        self.controller.frames[ProfilePage].update_file_listbox_filtered()
        self.controller.frames[ProfilePage].update_file_online_listbox_filtered()
        self.controller.show_frame(ProfilePage)

    def password_not_recognised(self):
        self.password_not_recog_screen = tk.Toplevel(self)
        self.password_not_recog_screen.config(bg='white')
        self.password_not_recog_screen.title("Error")
        self.password_not_recog_screen.geometry("360x120")

        label = tk.Label(self.password_not_recog_screen, text="Invalid Password", font=("", 8), bg='white')
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.password_not_recog_screen, text="OK", font=("", 8), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white',
                           command=self.password_not_recog_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")

    def user_not_found(self):
        self.user_not_found_screen = tk.Toplevel(self)
        self.user_not_found_screen.config(bg='white')
        self.user_not_found_screen.title("Error")
        self.user_not_found_screen.geometry("360x120")

        label = tk.Label(self.user_not_found_screen, text="User not found", font=("", 8), bg='white')
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.user_not_found_screen, text="OK", font=("", 8), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white',
                           command=self.user_not_found_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")

    def no_name(self):
        self.no_name_screen = tk.Toplevel(self)
        self.no_name_screen.config(bg='white')
        self.no_name_screen.title("Error")
        self.no_name_screen.geometry("360x120")

        label = tk.Label(self.no_name_screen, text="Username field is empty", font=("", 8), bg='white')
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.no_name_screen, text="OK", font=("", 8), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white',
                           command=self.no_name_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")


class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent)

        self.config(bg='white')

        self.username_verify = tk.StringVar()
        self.password_verify = tk.StringVar()

        label0 = tk.Label(self, text='Registration', font=("", 15), bg='white')
        label0.place(relx=0.5, rely=0.1, relheight=0.2, relwidth=0.4, anchor="center")

        label1 = tk.Label(self, text="Username", font=("", 10), bg='white')
        label1.place(relx=0.2, rely=0.4, relheight=0.2, relwidth=0.3, anchor="center")
        self.username_register_entry = tk.Entry(self, textvariable=self.username_verify, font=("", 10))
        self.username_register_entry.place(relx=0.5, rely=0.4, relheight=0.075, relwidth=0.3, anchor="center")

        label2 = tk.Label(self, text="Password", font=("", 10), bg='white')
        label2.place(relx=0.2, rely=0.55, relheight=0.2, relwidth=0.3, anchor="center")
        self.password_register_entry = tk.Entry(self, textvariable=self.password_verify, font=("", 10), show='*')
        self.password_register_entry.place(relx=0.5, rely=0.55, relheight=0.075, relwidth=0.3, anchor="center")

        button = tk.Button(self, text="Register", font=("", 10), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white', command=self.signup_verify)
        button.place(relx=0.5, rely=0.7, relheight=0.1, relwidth=0.2, anchor="center")

    def signup_verify(self):
        username = self.username_verify.get()
        password = self.password_verify.get()

        if not username:
            self.no_name()
        elif not password:
            self.no_password()
        else:
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

    def signup_success(self):
        self.register_success_screen = tk.Toplevel(self)
        self.register_success_screen.config(bg='white')
        self.register_success_screen.title("Success")
        self.register_success_screen.geometry("360x120")

        label = tk.Label(self.register_success_screen, text="Registration Success", font=("", 8), bg='white')
        label.place(relx=0.5, rely=0.35, anchor="center")

        def register_close():
            self.register_success_screen.destroy()

        button = tk.Button(self.register_success_screen, text="OK", font=("", 8), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white', command=register_close)
        button.place(relx=0.5, rely=0.65, anchor="center")

    def signup_user(self):
        username = self.username_verify.get()
        password = self.password_verify.get()

        try:
            script_path = os.path.join(self.controller.path_to_dir, "file_management", "create_user.py")
            script_args = [username, password]
            command = ['python', script_path] + script_args

            # Run the command
            subprocess.run(command, check=True)
            print("Script executed successfully")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e)

    def signup_user_found(self):
        self.register_user_found_screen = tk.Toplevel(self)
        self.register_user_found_screen.config(bg='white')
        self.register_user_found_screen.title("Error")
        self.register_user_found_screen.geometry("360x120")

        label = tk.Label(self.register_user_found_screen, text="User already exists", font=("", 8), bg='white')
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.register_user_found_screen, text="OK", font=("", 8), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white',
                           command=self.register_user_found_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")

    def no_name(self):
        self.no_name_screen = tk.Toplevel(self)
        self.no_name_screen.config(bg='white')
        self.no_name_screen.title("Error")
        self.no_name_screen.geometry("360x120")

        label = tk.Label(self.no_name_screen, text="Username field is empty", font=("", 8), bg='white')
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.no_name_screen, text="OK", font=("", 8), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white',
                           command=self.no_name_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")

    def no_password(self):
        self.no_password_screen = tk.Toplevel(self)
        self.no_password_screen.config(bg='white')
        self.no_password_screen.title("Error")
        self.no_password_screen.geometry("360x120")

        label = tk.Label(self.no_password_screen, text="Password field is empty", font=("", 8), bg='white')
        label.place(relx=0.5, rely=0.35, anchor="center")

        button = tk.Button(self.no_password_screen, text="OK", font=("", 8), bg=header_color, fg='white',
                           activebackground=header_shadow_color, activeforeground='white',
                           command=self.no_password_screen.destroy)
        button.place(relx=0.5, rely=0.65, anchor="center")


class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.peer = None

        tk.Frame.__init__(self, parent)

        self.config(bg='white')

        search_icon = tk.PhotoImage(file=os.path.join(self.controller.image_path, "search_icon.png"))
        self.search_icon = search_icon.subsample(12)

        label = tk.Label(self, textvariable=self.controller.username, bg='white', font=("", 8))
        label.place(relx=0.85, rely=0.075, relwidth=0.2, relheight=0.1, anchor="center")

        self.logout_button = tk.Button(self, text="Logout", font=("", 4), bg=header_color, fg='white',
                                       activebackground=header_shadow_color, activeforeground='white',
                                       command=self.logout)
        self.logout_button.place(relx=0.8, rely=0.15, relwidth=0.1, anchor="center")

        self.delete_account_button = tk.Button(self, text="Delete account", font=("", 4), bg=header_color, fg='white',
                                               activebackground=header_shadow_color, activeforeground='white',
                                               command=self.delete_account)
        self.delete_account_button.place(relx=0.9, rely=0.15, relwidth=0.1, anchor="center")

        label_uploaded = tk.Label(self, text="Files online", bg='white', font=("", 10))
        label_uploaded.place(relx=0.2, rely=0.15, relwidth=0.25, relheight=0.1, anchor="center")

        self.online_search = tk.StringVar()

        label_online_search = tk.Label(self, text="Search", font=("", 8), bg='white')
        label_online_search.place(relx=0.1, rely=0.25, relheight=0.1, relwidth=0.2, anchor="center")
        self.online_search_entry = tk.Entry(self, textvariable=self.online_search, font=("", 8))
        self.online_search_entry.place(relx=0.23, rely=0.25, relheight=0.05, relwidth=0.15, anchor="center")

        self.online_search_button = tk.Button(self, image=self.search_icon, bg=header_color,
                                              activebackground=header_shadow_color,
                                              command=self.update_file_online_listbox_filtered)
        self.online_search_button.place(relx=0.33, rely=0.25, relwidth=0.035, relheight=0.05, anchor="center")

        self.online_files = []
        self.online_files_filtered = []

        self.file_online_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.file_online_listbox.place(relx=0.2, rely=0.55, relheight=0.5, relwidth=0.3, anchor="center")

        self.list_files_online()
        self.update_file_online_listbox()

        self.download_button = tk.Button(self, text="Download", font=("", 5), bg=header_color, fg='white',
                                         activebackground=header_shadow_color, activeforeground='white',
                                         command=self.download_files)
        self.download_button.place(relx=0.2, rely=0.85, relwidth=0.29, anchor="center")

        label_uploaded = tk.Label(self, text="Uploaded files", bg='white', font=("", 10))
        label_uploaded.place(relx=0.55, rely=0.15, relwidth=0.25, relheight=0.1, anchor="center")

        self.offline_search = tk.StringVar()

        label_offline_search = tk.Label(self, text="Search", font=("", 8), bg='white')
        label_offline_search.place(relx=0.45, rely=0.25, relheight=0.1, relwidth=0.2, anchor="center")
        self.offline_search_entry = tk.Entry(self, textvariable=self.offline_search, font=("", 8))
        self.offline_search_entry.place(relx=0.58, rely=0.25, relheight=0.05, relwidth=0.15, anchor="center")

        self.offline_search_button = tk.Button(self, image=self.search_icon, bg=header_color,
                                               activebackground=header_shadow_color,
                                               command=self.update_file_listbox_filtered)
        self.offline_search_button.place(relx=0.68, rely=0.25, relwidth=0.035, relheight=0.05, anchor="center")

        self.uploaded_files = []
        self.uploaded_files_filtered = []

        self.file_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.file_listbox.place(relx=0.55, rely=0.55, relheight=0.5, relwidth=0.3, anchor="center")

        self.upload_button = tk.Button(self, text="Upload File", font=("", 5), bg=header_color, fg='white',
                                       activebackground=header_shadow_color, activeforeground='white',
                                       command=self.upload_file)
        self.upload_button.place(relx=0.48, rely=0.85, relwidth=0.14, anchor="center")

        self.delete_button = tk.Button(self, text="Delete", font=("", 5), bg=header_color, fg='white',
                                       activebackground=header_shadow_color, activeforeground='white',
                                       command=self.delete_files)
        self.delete_button.place(relx=0.62, rely=0.85, relwidth=0.14, anchor="center")

    def logout(self):
        self.controller.show_frame(WelcomePage)
        self.controller.username.set("")

    def delete_account(self):
        try:
            script_path = os.path.join(self.controller.path_to_dir, "file_management", "delete_user.py")
            script_args = [self.controller.username.get()]
            command = ['python', script_path] + script_args

            # Run the command
            subprocess.run(command, check=True)
            print("Script executed successfully")
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e)
        self.controller.show_frame(WelcomePage)
        self.controller.username.set("")

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            filename = os.path.basename(file_path)
            if filename in self.uploaded_files:
                messagebox.showinfo("Error", "File already uploaded.")
                return
            self.uploaded_files.append(filename)
            try:
                script_path = os.path.join(self.controller.path_to_dir, "file_management", "add_file.py")
                script_args = [self.controller.username.get(), filename, file_path]
                command = ['python', script_path] + script_args

                # Run the command
                subprocess.run(command, check=True)
                print("Script executed successfully")
            except subprocess.CalledProcessError as e:
                print("Error executing script:", e)
            self.update_file_listbox_filtered()
            self.update_file_online_listbox_filtered()

    def update_file_listbox(self):
        self.list_files_uploaded()
        self.file_listbox.delete(0, tk.END)
        for file_path in self.uploaded_files:
            self.file_listbox.insert(tk.END, file_path)

    def update_file_online_listbox(self):
        self.list_files_online()
        self.file_online_listbox.delete(0, tk.END)
        for file_path in self.online_files:
            self.file_online_listbox.insert(tk.END, file_path)

    def download_files(self):
        selected_indices = self.file_online_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Error", "No files selected.")
            return

        for index in selected_indices:
            file_path = self.online_files_filtered[index]
            print("Downloading:", file_path)
            self.peer.get_request(file_path)

    def delete_files(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Error", "No files selected.")
            return

        for index in selected_indices[::-1]:
            try:
                script_path = os.path.join(self.controller.path_to_dir, "file_management", "delete_file.py")
                script_args = [self.controller.username.get(), self.uploaded_files_filtered[index]]
                command = ['python', script_path] + script_args

                # Run the command
                subprocess.run(command, check=True)
                print("Script executed successfully")
            except subprocess.CalledProcessError as e:
                print("Error executing script:", e)

        self.update_file_listbox_filtered()
        self.update_file_online_listbox_filtered()

    def list_files_online(self):
        files = {}
        files_path = os.path.join(self.controller.path_to_dir, "users_data")
        users = os.listdir(files_path)
        if "port_to_hosts.json" in users:
            users.remove("port_to_hosts.json")
        if "free_ports.json" in users:
            users.remove("free_ports.json")
        for user in users:
            user_data_path = os.path.join(files_path, user)
            user_data = os.listdir(user_data_path)
            if "user_info.json" in user_data:
                user_data.remove("user_info.json")
            if "combined_files" in user_data:
                user_data.remove("combined_files")
            for file in user_data:
                if file in files.keys():
                    files[file].append(user)
                else:
                    files[file] = [user]
        self.online_files = files.keys()

    def list_files_uploaded(self):
        files = []
        files_path = os.path.join(self.controller.path_to_dir, "users_data", str(self.controller.username.get()))
        user_data = os.listdir(files_path)
        if "combined_files" in user_data:
            user_data.remove("combined_files")
        if "user_info.json" in user_data:
            user_data.remove("user_info.json")
        for file in user_data:
            files.append(file)
        self.uploaded_files = files

    def update_file_listbox_filtered(self):
        self.list_files_uploaded()
        self.file_listbox.delete(0, tk.END)
        self.uploaded_files_filtered = []
        for file_path in self.uploaded_files:
            if self.offline_search.get() in file_path:
                self.uploaded_files_filtered.append(file_path)
                self.file_listbox.insert(tk.END, file_path)

    def update_file_online_listbox_filtered(self):
        self.list_files_online()
        self.file_online_listbox.delete(0, tk.END)
        self.online_files_filtered = []
        for file_path in self.online_files:
            if self.online_search.get() in file_path:
                self.online_files_filtered.append(file_path)
                self.file_online_listbox.insert(tk.END, file_path)


class AuthSidebarSubMenu(tk.Frame):
    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        tk.Frame.__init__(self, parent)
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(self,
                                               text=sub_menu_heading,
                                               bg=sidebar_color,
                                               fg=gray_color,
                                               font=("", 10, "bold")
                                               )
        self.sub_menu_heading_label.place(x=15, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=17, y=30, relwidth=0.9, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(self,
                                        text=x,
                                        bg=sidebar_color,
                                        fg=gray_color,
                                        font=("", 8, "bold"),
                                        bd=0,
                                        cursor='hand2',
                                        activebackground=light_gray_color,
                                        activeforeground='white',
                                        highlightthickness=0,
                                        )
            self.options[x].place(x=15, y=30 + 45 * (n + 1), anchor="w")


if __name__ == "__main__":
    app = AP2P()
    app.mainloop()
