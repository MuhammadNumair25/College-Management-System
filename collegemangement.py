import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import copy
students = {}
courses = {}
new_entries= []

class LoginSystem:
    def __init__(self):
        self.logged_in = False
        self.current_user = None
        self.role = None
        self.root = tk.Tk()
        self.root.title("International College System")
        self.root.geometry("300x200")
        self.root.configure(bg="#f2f2f2")

        self.register_button = tk.Button(self.root, text="Register", command=self.show_register_window, width=20)
        self.register_button.pack(pady=20)

        self.login_button = tk.Button(self.root, text="Login", command=self.show_login_window, width=20)
        self.login_button.pack(pady=10)

    def register(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if not first_name or not last_name or not username or not password or not role:
            messagebox.showerror("Registration Failed", "Please fill in all the fields.")
            return

        if role == "Student":
            student_id = "IC" + str(random.randint(1000, 9999))
            students[student_id] = {
                'first_name': first_name,
                'last_name': last_name,
                'courses': [],
                'grades': ""
            }
            data = f"{student_id},{first_name},{last_name},{username},{password},{role}\n"
        else:
            subject = self.subject_var.get()
            if subject == "Select a Subject":
                messagebox.showerror("Registration Failed", "Please select a subject for the teacher.")
                return
            data = f",{first_name},{last_name},{username},{password},{role},{subject}\n"

        with open("users.txt", "a") as file:
            file.write(data)

        messagebox.showinfo("Registration Successful", "Registration successful!")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open("users.txt", "r") as file:
            for line in file:
                user_data = line.strip().split(",")
                print(user_data)
                if user_data[3] == username and user_data[4] == password:
                    self.logged_in = True
                    self.current_user = {
                        'student_id': user_data[0],
                        'first_name': user_data[1],
                        'last_name': user_data[2],
                        'username': username,
                        'role': user_data[5]
                    }
                    self.role = user_data[5]

                    self.login_window.destroy()
                    if self.role == "Student":
                        self.load_student_data()
                        self.show_student_menu()
                    else:
                        self.load_student_data()
                        self.show_teacher_menu()
                    return

        messagebox.showerror("Login Failed", "Invalid username or password.")

    def logout(self):
        self.logged_in = False
        self.current_user = None
        self.role = None
        self.menu_window.destroy()
        self.show_login_window()

    def show_register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Registration")
        register_window.geometry("300x300")
        register_window.configure(bg="#f2f2f2")

        tk.Label(register_window, text="First Name:", bg="#f2f2f2").pack()
        self.first_name_entry = tk.Entry(register_window)
        self.first_name_entry.pack(pady=5)

        tk.Label(register_window, text="Surname:", bg="#f2f2f2").pack()
        self.last_name_entry = tk.Entry(register_window)
        self.last_name_entry.pack(pady=5)

        tk.Label(register_window, text="Username:", bg="#f2f2f2").pack()
        self.username_entry = tk.Entry(register_window)
        self.username_entry.pack(pady=5)

        tk.Label(register_window, text="Password:", bg="#f2f2f2").pack()
        self.password_entry = tk.Entry(register_window, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(register_window, text="Role:", bg="#f2f2f2").pack()
        self.role_var = tk.StringVar(register_window)
        self.role_var.set("Select a Role")
        role_dropdown = tk.OptionMenu(register_window, self.role_var, "Student", "Teacher", command=self.on_role_select)
        role_dropdown.config(bg="#f2f2f2")
        role_dropdown.pack(pady=5)

        self.subject_label = tk.Label(register_window, text="Subject:", bg="#f2f2f2")
        self.subject_var = tk.StringVar(register_window)
        self.subject_var.set("Select a Subject")
        self.subject_dropdown = tk.OptionMenu(register_window, self.subject_var, "Math", "IT", "ET")
        self.subject_dropdown.config(bg="#f2f2f2")
        self.subject_label.pack(pady=5)

        register_button = tk.Button(register_window, text="Register", command=self.register, width=20)
        register_button.pack(pady=10)

    def on_role_select(self, role):
        if role == "Teacher":
            self.subject_label.pack()
            self.subject_dropdown.pack()
        else:
            self.subject_label.pack_forget()
            self.subject_dropdown.pack_forget()

    def show_login_window(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")
        self.login_window.geometry("300x200")
        self.login_window.configure(bg="#f2f2f2")

        tk.Label(self.login_window, text="Username:", bg="#f2f2f2").pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_window, text="Password:", bg="#f2f2f2").pack()
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.login_window, text="Login", command=self.login, width=20)
        login_button.pack(pady=10)

    def show_student_menu(self):
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("Menu")
        self.menu_window.geometry("300x300")
        self.menu_window.configure(bg="#f2f2f2")

        welcome_label = tk.Label(self.menu_window, text=f"Welcome, {self.current_user['first_name']} {self.current_user['last_name']}!", bg="#f2f2f2")
        welcome_label.pack(pady=10)

        view_student_button = tk.Button(self.menu_window, text="View Student Details", command=self.view_student_details, width=20)
        view_student_button.pack(pady=5)

        logout_button = tk.Button(self.menu_window, text="Logout", command=self.logout, width=20)
        logout_button.pack(pady=5)

    def show_teacher_menu(self):
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("Menu")
        self.menu_window.geometry("300x300")
        self.menu_window.configure(bg="#f2f2f2")

        welcome_label = tk.Label(self.menu_window, text=f"Welcome, {self.current_user['first_name']} {self.current_user['last_name']}!", bg="#f2f2f2")
        welcome_label.pack(pady=10)

        add_courses_button = tk.Button(self.menu_window, text="Add or Change Courses", command=self.add_courses, width=20)
        add_courses_button.pack(pady=5)

        change_grades_button = tk.Button(self.menu_window, text="Add or Change Grades", command=self.change_grades, width=20)
        change_grades_button.pack(pady=10)

        view_student_button = tk.Button(self.menu_window, text="View Student Details", command=self.view_student_details, width=20)
        view_student_button.pack(pady=5)

        view_student_button = tk.Button(self.menu_window, text="View Student List", command=self.view_student_list, width=20)
        view_student_button.pack(pady=5)


        logout_button = tk.Button(self.menu_window, text="Logout", command=self.logout, width=20)
        logout_button.pack(pady=5)

   


    def add_courses(self):
        student_id = simpledialog.askstring("Change or Add Courses", "Enter student ID:")
        if student_id is None:
            return
        if student_id not in students:
            messagebox.showerror("Invalid Student ID", "Student ID not found.")
            return

        courses = simpledialog.askstring("Change or Add Courses", "Enter courses (comma-separated):")
        if courses is None:
            return

        courses = courses.split(",")
        print(students[student_id])
        print(student_id)
        print(courses)
        # append the student_id with the course id and add it to students dictionary with the new key
        for i in range(len(courses)):
            key = f"{student_id}-{courses[i]}"
            print(key)
            t = copy.deepcopy(students[student_id])
            t['student_id'] = key
            t['courses'] = courses[i]
            t['grades'] = ''
            new_entries.append(t)
        messagebox.showinfo("Courses Added/Changed", "Courses have been changed/added successfully.")

    def change_grades(self):
        student_id = simpledialog.askstring("Change or Add Grades", "Enter student ID:")
        if student_id is None:
            return
        if student_id not in students:
            messagebox.showerror("Invalid Student ID", "Student ID not found.")
            return

        grades = simpledialog.askstring("Change or Add Grades", "Enter grades (comma-separated):")
        if grades is None:
            return

        grades = grades.split(",")

        # loop on new_entries array and update the grades for the student
        for i in range(len(new_entries)):
            # check if index exist in grades array
            if i < len(grades):
                new_entries[i]['grades'] = grades[i]
            else:
                new_entries[i]['grades'] = ''
            print(new_entries[i])

        messagebox.showinfo("Grades Changed/Added", "Grades has been changed/added successfully.")

        print(new_entries)
        self.save_courses_and_grades()

    def save_courses_and_grades(self):
        with open("coursesandgrades.txt", "a") as file:
            for i in range(len(new_entries)):
                student_data = new_entries[i]
                first_name = student_data['first_name']
                last_name = student_data['last_name']
                course = student_data['courses']
                grades = student_data['grades']
                student_id = student_data['student_id']
                students[student_id] = student_data
                file.write(f"{student_id},{first_name},{last_name},{course},{grades}\n")


    def view_student_details(self):
        student_id = simpledialog.askstring("View Student Details", "Enter student ID:")
        if student_id is None:
            return
        if student_id not in students:
            messagebox.showerror("Invalid Student ID", "Student ID not found.")
            return
        if (self.role == 'Student' and self.current_user['student_id'] != student_id):
            messagebox.showerror("Invalid Student ID", "Student not authorized.")
            return
      
        print(self.role == 'Student')
        print(self.current_user['student_id'] != student_id)
        print(self.current_user['student_id'] , student_id)
        student = students[student_id]
        # details = f"Student ID: {student_id}\n" \
        #           f"Name: {student['first_name']} {student['last_name']}\n" \
        #           f"Courses: {', '.join(student['courses'])}\n" \
        #           f"Grades: {student['grades']}"
        details = ''
        # loop on dictionary and get items with course = subject
        for key, value in students.items():
            print(value['courses'])
            if student['first_name'] == value['first_name'] and student['last_name'] == value['last_name']:
                print(key, value)
                details += f"Student ID: {key}\n" \
                          f"Name: {value['first_name']} {value['last_name']}\n" \
                          f"Courses: {value['courses']}\n" \
                          f"Grades: {value['grades']}\n"

        # student = students[student_id]
        # details = f"Student ID: {student_id}\n" \
        #           f"Name: {student['first_name']} {student['last_name']}\n" \
        #           f"Courses: {', '.join(student['courses'])}\n" \
        #           f"Grades: {student['grades']}"
        messagebox.showinfo("Student Details", details)

    def view_student_list(self):
        subject = simpledialog.askstring("View Student List", "Enter Subject:")
        if subject is None:
            return

        details = ''
        subject= subject.split(",")
        # loop on dictionary and get items with course = subject
        for key, value in students.items():
            if  value['courses'] in subject:
                details += f"Student ID: {key}\n" \
                          f"Name: {value['first_name']} {value['last_name']}\n" \
                          f"Courses: {value['courses']}\n" \
                          f"Grades: {value['grades']}\n"

        messagebox.showinfo("Student Details", details)


    # write a function show the student list enrolled in one course
    def show_student_list(self):
        course = simpledialog.askstring("View Student List", "Enter course:")
        if course is None:
            return
        if course not in courses:
            messagebox.showerror("Invalid Course", "Course not found.")
            return

        student_list = courses[course]
        details = f"Course: {course}\n" \
                  f"Student List: {', '.join(student_list)}\n" \

        messagebox.showinfo("Student List", details)


    def load_student_data(self):
      with open("coursesandgrades.txt", "r") as file:
        for line in file:
            user_data = line.strip().split(",")
            print(user_data)
            if user_data[0].startswith("IC"):
                student_id = user_data[0]
                courses = user_data[3]  # Extract the courses from the user_data list
                grades = user_data[4]  # Extract the grades from the last element of user_data
                students[student_id] = {
                    'first_name': user_data[1],
                    'last_name': user_data[2],
                    'courses': courses,  # Join the courses with a comma separator
                    'grades':grades  # Join the grades with a comma separator
                }



    



    


login_system = LoginSystem()
login_system.root.mainloop()
