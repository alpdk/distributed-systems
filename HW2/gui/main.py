from tkinter import *
import os


class UserAuthentication:
    def __init__(self):
        self.main_screen = Tk()
        self.main_screen.geometry("480x270")
        self.main_screen.title("Authorization")

        Button(text="Login", height="2", width="30", command=self.login).pack()

        Label(text="").pack()

        Button(text="Register", height="2", width="30", command=self.register).pack()

    def register(self):
        self.register_screen = Toplevel(self.main_screen)
        self.register_screen.title("Register")
        self.register_screen.geometry("400x175")

        self.username_verify = StringVar()
        self.password_verify = StringVar()

        Label(self.register_screen, text="Username").pack()
        self.username_register_entry = Entry(self.register_screen, textvariable=self.username_verify)
        self.username_register_entry.pack()

        Label(self.register_screen, text="").pack()

        Label(self.register_screen, text="Password").pack()
        self.password_register_entry = Entry(self.register_screen, textvariable=self.password_verify, show='*')
        self.password_register_entry.pack()

        Label(self.register_screen, text="").pack()

        Button(self.register_screen, text="Register", width=10, height=1, command=self.register_verify).pack()

    def login(self):
        self.login_screen = Toplevel(self.main_screen)
        self.login_screen.title("Login")
        self.login_screen.geometry("400x175")

        self.username_verify = StringVar()
        self.password_verify = StringVar()

        Label(self.login_screen, text="Username").pack()
        self.username_login_entry = Entry(self.login_screen, textvariable=self.username_verify)
        self.username_login_entry.pack()

        Label(self.login_screen, text="").pack()

        Label(self.login_screen, text="Password").pack()
        self.password_login_entry = Entry(self.login_screen, textvariable=self.password_verify, show='*')
        self.password_login_entry.pack()

        Label(self.login_screen, text="").pack()

        Button(self.login_screen, text="Login", width=10, height=1, command=self.login_verify).pack()

    def register_verify(self):
        username = self.username_verify.get()

        # Get list of usernames to check whether this user exists
        list_of_files = os.listdir()
        if username in list_of_files:
            # User already exists
            self.register_user_found()
        else:
            # Register new user
            self.register_user()
            self.register_success()

        self.username_register_entry.delete(0, END)
        self.password_register_entry.delete(0, END)

    def login_verify(self):
        username = self.username_verify.get()
        password = self.password_verify.get()

        # Get list of usernames to check whether this user exists
        list_of_files = os.listdir()
        if username in list_of_files:
            # User exists
            file1 = open(username, "r")
            verify = file1.read().splitlines()
            if password in verify:
                # Correct password
                self.login_success()
            else:
                # Wrong password
                self.password_not_recognised()
        else:
            # User doesn't exist
            self.user_not_found()

        self.username_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)

    def register_success(self):
        self.register_success_screen = Toplevel(self.register_screen)
        self.register_success_screen.title("Success")
        self.register_success_screen.geometry("360x120")

        Label(self.register_success_screen, text="Registration Success").pack()

        Button(self.register_success_screen, text="OK", command=self.delete_register_success).pack()

    def register_user(self):
        username = self.username_verify.get()
        password = self.password_verify.get()

        # Write username and password in file 'username'
        file = open(username, "w")
        file.write(username + "\n")
        file.write(password)
        file.close()

    def register_user_found(self):
        self.register_user_found_screen = Toplevel(self.register_screen)
        self.register_user_found_screen.title("Error")
        self.register_user_found_screen.geometry("360x120")
        Label(self.register_user_found_screen, text="User already exists").pack()
        Button(self.register_user_found_screen, text="OK", command=self.delete_register_user_found_screen).pack()

    def login_success(self):
        self.login_success_screen = Toplevel(self.login_screen)
        self.login_success_screen.title("Success")
        self.login_success_screen.geometry("360x120")
        Label(self.login_success_screen, text="Login Success").pack()
        Button(self.login_success_screen, text="OK", command=self.delete_login_success).pack()

    def password_not_recognised(self):
        self.password_not_recog_screen = Toplevel(self.login_screen)
        self.password_not_recog_screen.title("Error")
        self.password_not_recog_screen.geometry("360x120")
        Label(self.password_not_recog_screen, text="Invalid Password ").pack()
        Button(self.password_not_recog_screen, text="OK", command=self.delete_password_not_recognised).pack()

    def user_not_found(self):
        self.user_not_found_screen = Toplevel(self.login_screen)
        self.user_not_found_screen.title("Error")
        self.user_not_found_screen.geometry("360x120")
        Label(self.user_not_found_screen, text="User not found").pack()
        Button(self.user_not_found_screen, text="OK", command=self.delete_user_not_found_screen).pack()

    def delete_register_success(self):
        self.register_success_screen.destroy()

    def delete_register_user_found_screen(self):
        self.register_user_found_screen.destroy()

    def delete_login_success(self):
        self.login_success_screen.destroy()

    def delete_password_not_recognised(self):
        self.password_not_recog_screen.destroy()

    def delete_user_not_found_screen(self):
        self.user_not_found_screen.destroy()

    def main_account_screen(self):
        self.main_screen.mainloop()


if __name__ == "__main__":
    app = UserAuthentication()
    app.main_account_screen()
