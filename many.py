# pip install customtkinter 
# pip install pillow
# pip install datetime
# pip install tk

import logging
import psycopg2
from tkinter import messagebox
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from datetime import datetime
from database import check_database_connection
from database import create_table, add_employee

logging.basicConfig(level=logging.DEBUG)
#create_table()
create_table()

# Initialize the main application window
app = ctk.CTk()
app.geometry("1200x800")
app.title("Employee Salary Management")

# Function to center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

center_window(app, 1200, 800)

# List to store employee data
employees = []

# Employee ID counter
employee_id_counter = 1

# Dictionary to hold department and their corresponding positions
department_positions = {
    "Kitchen staff": ["Head Chef", "Chef", "Chef's Assistant"],
    "Managerial staff": ["Restaurant Manager", "Kitchen Manager", "Floor Manager"],
    "Floor staff": ["Cashier", "Cleaning staff", "Security guard"],
    "Bar staff": ["Bartender", "Barista"],
    "Delivery staff": ["Delivery staff", "Delivery Assistant"]
}

# Function to update position options based on selected department
def update_positions(*args):
    department = department_menu.get()
    positions = department_positions.get(department, [])
    position_menu.configure(values=positions)  # Update the position menu values
    if positions:
        position_menu.set(positions[0])  # Set the first position as default
    else:
        position_menu.set("Select Position")

def validate_date_format(date_text):
    date_text = date_text.strip()  # Remove any leading/trailing whitespace
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to calculate age based on Date of Birth
def calculate_age():
    dob = dob_entry.get().strip()
    if validate_date_format(dob):
        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        age = (datetime.now() - dob_date).days // 365
        entry_age.configure(state='normal')  # Enable age field for update
        entry_age.delete(0, ctk.END)
        entry_age.insert(0, str(age))
        entry_age.configure(state='readonly')  # Set back to read-only

# Function to generate the next employee ID
def generate_employee_id():
    global employee_id_counter
    employee_id = f"{employee_id_counter:04d}"
    employee_id_counter += 1
    return employee_id

# Modify the add_employee function
def add_employee():
    global employee_id_counter

    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    salary = entry_salary.get().strip()
    department = department_menu.get()
    position = position_menu.get()
    tel = entry_tel.get()
    email = entry_email.get()
    dob = dob_entry.get().strip()
    start_day = start_day_entry.get().strip()
    religion = entry_religion.get().strip()
    nationality = entry_nationality.get().strip()

    # Validate date format
    if not validate_date_format(dob):
        messagebox.showerror("Error", "กรุณากรอกวันที่เกิดในรูปแบบ YYYY-MM-DD ให้ถูกต้อง")
        return
    if not validate_date_format(start_day):
        messagebox.showerror("Error", "กรุณากรอกวันเริ่มงานในรูปแบบ YYYY-MM-DD ให้ถูกต้อง")
        return

    # Calculate age
    dob_date = datetime.strptime(dob, "%Y-%m-%d")
    age = (datetime.now() - dob_date).days // 365

    # Check if position is selected if required by the department
    if department in department_positions and position == "Select Position":
        messagebox.showerror("Error", f"กรุณาเลือกตำแหน่งสำหรับ {department}.")
        return

    # Ensure all required fields are filled
    if first_name and last_name and salary and department != "Select Department" and tel and email and dob and start_day:
        # Validate salary input
        if not salary.isdigit():
            messagebox.showerror("Error", "กรุณากรอกรายได้ที่ถูกต้อง ใช้เฉพาะตัวเลขที่เป็นบวกเท่านั้น")
            return

        salary = int(salary)

         # Check for duplicate employees
        if any(emp['first_name'] == first_name and emp['last_name'] == last_name for emp in employees):
            messagebox.showerror("Error", "พนักงานคนนี้มีอยู่แล้ว")
            return

       # Generate new employee ID
        employee_id = generate_employee_id()

        # Convert starting date to datetime format and calculate days worked
        start_day_date = datetime.strptime(start_day, "%Y-%m-%d")
        days_worked = (datetime.now() - start_day_date).days

        # Add employee data to the list
        employees.append({
            "employee_id": employee_id,
            "first_name": first_name,
            "last_name": last_name,
            "salary": salary,
            "department": department,
            "position": position,
            "tel": tel,
            "email": email,
            "dob": dob,
            "age": age,
            "start_day": start_day,  
            "days_worked": days_worked,
            "religion": religion,
            "nationality": nationality
        })

        # Clear input fields after adding employee
        entry_first_name.delete(0, ctk.END)
        entry_last_name.delete(0, ctk.END)
        entry_salary.delete(0, ctk.END)
        entry_tel.delete(0, ctk.END)
        entry_email.delete(0, ctk.END)
        dob_entry.delete(0, ctk.END)
        start_day_entry.delete(0, ctk.END)
        entry_religion.delete(0, ctk.END)
        entry_nationality.delete(0, ctk.END)
        department_menu.set("Select Department")
        position_menu.set("Select Position")

        # Notify user of success
        messagebox.showinfo("Success", f"พนักงาน {first_name} {last_name} ถูกเพิ่มด้วย ID {employee_id}!")
        show_employees()

# Function to display the list of employees
def show_employees():
    # Clear existing widgets in the right frame
    for widget in frame_right.winfo_children():
        widget.destroy()

    # Check if the employees list is empty
    if not employees:
        no_employees_label = ctk.CTkLabel(frame_right, text="No employees to display", text_color="#EEEEEE", font=("Arial", 16))
        no_employees_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    else:
        global checkbox_vars
        checkbox_vars = []

        # Loop through the employees and display their information
        for i, employee in enumerate(employees):
            checkbox_var = ctk.IntVar()
            checkbox_vars.append(checkbox_var)
            
            employee_info = (f"{employee['employee_id']} : {employee['first_name']} {employee['last_name']}\n"
                 f"Position : {employee['position']} ({employee['department']})\n"
                 f"Salary : ฿{employee['salary']:.2f}\n"
                 f"Date of Birth : {employee['dob']} (Age : {employee['age']})\n"
                 f"Tel : {employee['tel']}, Email : {employee['email']}\n"
                 f"Religion : {employee['religion']}, Nationality : {employee['nationality']}\n"
                 f"Start Day : {employee['start_day']}, Days Worked : {employee['days_worked']}")
            
            employee_checkbox = ctk.CTkCheckBox(
                frame_right, 
                text=employee_info, 
                variable=checkbox_var,
                text_color="#EEEEEE",  # Set text color to #EEEEEE
                font=("Arial", 18)      # Increase font size to 12
            )
            employee_checkbox.grid(row=i, column=0, padx=10, pady=10, sticky="w")

def search_employees(search_term):
    search_term = search_term.lower().strip()
    filtered_employees = [emp for emp in employees if search_term in (emp['first_name'].lower() + " " + emp['last_name'].lower())]
    
    # Clear existing widgets in the right frame
    for widget in frame_right.winfo_children():
        widget.destroy()

    if not filtered_employees:
        no_employees_label = ctk.CTkLabel(frame_right, text="No matching employees found", text_color="#EEEEEE", font=("Arial", 16))
        no_employees_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    else:
        global checkbox_vars
        checkbox_vars = []

        # Loop through the filtered employees and display their information
        for i, employee in enumerate(filtered_employees):
            checkbox_var = ctk.IntVar()
            checkbox_vars.append(checkbox_var)
            
            employee_info = (f"{employee['employee_id']} : {employee['first_name']} {employee['last_name']}\n"
                 f"Position : {employee['position']} ({employee['department']})\n"
                 f"Salary : ฿{employee['salary']:.2f}\n"
                 f"Date of Birth : {employee['dob']} (Age : {employee['age']})\n"
                 f"Tel : {employee['tel']}, Email : {employee['email']}\n"
                 f"Religion : {employee['religion']}, Nationality : {employee['nationality']}\n"
                 f"Start Day : {employee['start_day']}, Days Worked : {employee['days_worked']}")
            
            employee_checkbox = ctk.CTkCheckBox(
                frame_right, 
                text=employee_info, 
                variable=checkbox_var,
                text_color="#EEEEEE",
                font=("Arial", 18)
            )
            employee_checkbox.grid(row=i, column=0, padx=10, pady=10, sticky="w")

# Create frames for layout
frame_left = ctk.CTkFrame(app, width=600, height=800)
frame_left.grid(row=0, column=0, sticky="nsew")

frame_right = ctk.CTkFrame(app, width=600, height=800)
frame_right.grid(row=0, column=1, sticky="nsew")

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Add logo and title to the header frame
#logo_image = ctk.CTkImage(Image.open("logo.png"), size=(150, 150))

header_frame = ctk.CTkFrame(frame_left)
header_frame.pack(pady=20, padx=20, anchor="nw", fill="x")

#logo_label = ctk.CTkLabel(header_frame, image=logo_image, text="")
#logo_label.pack(side="left", padx=10)

label_title = ctk.CTkLabel(header_frame, text="Employee Salary Management", font=("Arial", 24))
label_title.pack(side="left", padx=15)

# Create input fields for employee details
label_name_frame = ctk.CTkFrame(frame_left)
label_name_frame.pack(pady=5)

label_first_name = ctk.CTkLabel(label_name_frame, text="First Name")
label_first_name.grid(row=0, column=0, padx=10)
entry_first_name = ctk.CTkEntry(label_name_frame, width=150)
entry_first_name.grid(row=0, column=1, padx=10)

label_last_name = ctk.CTkLabel(label_name_frame, text="Last Name")
label_last_name.grid(row=0, column=2, padx=10)
entry_last_name = ctk.CTkEntry(label_name_frame, width=150)
entry_last_name.grid(row=0, column=3, padx=10)

# Create frame for Date of Birth, Age, Department, and Position
info_frame = ctk.CTkFrame(frame_left)
info_frame.pack(pady=5)

label_dob = ctk.CTkLabel(info_frame, text="Date of Birth")
label_dob.grid(row=0, column=0, padx=10)
dob_entry = ctk.CTkEntry(info_frame, width=150)
dob_entry.grid(row=0, column=1, padx=10)
dob_entry.bind("<FocusOut>", lambda event: calculate_age())  # Trigger age calculation when leaving DOB field

label_age = ctk.CTkLabel(info_frame, text="Age")
label_age.grid(row=0, column=2, padx=10)
entry_age = ctk.CTkEntry(info_frame, width=150, state='readonly')
entry_age.grid(row=0, column=3, padx=10)

# Create frame for Religion and Nationality
religion_nationality_frame = ctk.CTkFrame(frame_left)
religion_nationality_frame.pack(pady=5)

# Religion input field
label_religion = ctk.CTkLabel(religion_nationality_frame, text="Religion")
label_religion.grid(row=0, column=0, padx=10)
entry_religion = ctk.CTkEntry(religion_nationality_frame, width=150)
entry_religion.grid(row=0, column=1, padx=10)

# Nationality input field
label_nationality = ctk.CTkLabel(religion_nationality_frame, text="Nationality")
label_nationality.grid(row=0, column=2, padx=10)
entry_nationality = ctk.CTkEntry(religion_nationality_frame, width=150)
entry_nationality.grid(row=0, column=3, padx=10)

# Create frame for Department and Position
department_position_frame = ctk.CTkFrame(frame_left)
department_position_frame.pack(pady=5)

# Department selection
label_department = ctk.CTkLabel(department_position_frame, text="Department")
label_department.grid(row=1, column=0, padx=10)
department_menu = ctk.CTkComboBox(department_position_frame, values=list(department_positions.keys()), width=200)
department_menu.set("Select Department")
department_menu.grid(row=1, column=1, padx=10)

# Position selection
label_position = ctk.CTkLabel(department_position_frame, text="Position")
label_position.grid(row=1, column=2, padx=10)
position_menu = ctk.CTkComboBox(department_position_frame, values=["Select Position"]+ [pos for sublist in department_positions.values() for pos in sublist], width=200)
position_menu.set("Select Position")
position_menu.grid(row=1, column=3, padx=10)

# Create frame for Salary
salary_frame = ctk.CTkFrame(frame_left)
salary_frame.pack(pady=5)

label_salary = ctk.CTkLabel(salary_frame, text="Salary")
label_salary.grid(row=0, column=0, padx=10)
entry_salary = ctk.CTkEntry(salary_frame, width=150)  # Define entry_salary here
entry_salary.grid(row=0, column=1, padx=10)

label_start_day = ctk.CTkLabel(salary_frame, text="Starting Day")
label_start_day.grid(row=0, column=2, padx=10)
start_day_entry = ctk.CTkEntry(salary_frame, width=150)
start_day_entry.grid(row=0, column=3, padx=10)

# Create frame for Telephone, Email, and Starting Day
contact_frame = ctk.CTkFrame(frame_left)
contact_frame.pack(pady=5)

label_tel = ctk.CTkLabel(contact_frame, text="Telephone")
label_tel.grid(row=0, column=0, padx=10)
entry_tel = ctk.CTkEntry(contact_frame, width=150)
entry_tel.grid(row=0, column=1, padx=10)

label_email = ctk.CTkLabel(contact_frame, text="Email")
label_email.grid(row=0, column=2, padx=10)
entry_email = ctk.CTkEntry(contact_frame, width=150)
entry_email.grid(row=0, column=3, padx=10)

# Add button to submit employee data
btn_add = ctk.CTkButton(frame_left, text="Add Employee", command=add_employee)
btn_add.pack(pady=10)

# Create frame for Search
search_frame = ctk.CTkFrame(frame_left)
search_frame.pack(pady=10)

# Search input field
label_search = ctk.CTkLabel(search_frame, text="Search by Name")
label_search.grid(row=0, column=0, padx=10)
search_entry = ctk.CTkEntry(search_frame, width=150)
search_entry.grid(row=0, column=1, padx=10)

# Search button
btn_search = ctk.CTkButton(search_frame, text="Search", command=lambda: search_employees(search_entry.get()))
btn_search.grid(row=0, column=2, padx=10)

show_employees()

cool_palette = {
    "background": "#222831", 
    "frame_bg": "#393E46",    
    "button_bg": "#00ADB5",   
    "button_fg": "#EEEEEE",   
    "label_text": "#EEEEEE",  
    "entry_bg": "#EEEEEE",    
    "entry_fg": "#222831",    
    "highlight": "#71C9CE",   
    "warning": "#EEEEEE"      
}

# Apply cool-tone colors to the app and frames
app.configure(fg_color=cool_palette["background"])
header_frame.configure(fg_color=cool_palette["frame_bg"])
frame_left.configure(fg_color=cool_palette["frame_bg"])
frame_right.configure(fg_color=cool_palette["frame_bg"])
label_name_frame.configure(fg_color=cool_palette["frame_bg"])
info_frame.configure(fg_color=cool_palette["frame_bg"])
religion_nationality_frame.configure(fg_color=cool_palette["frame_bg"])
department_position_frame.configure(fg_color=cool_palette["frame_bg"])
salary_frame.configure(fg_color=cool_palette["frame_bg"])
contact_frame.configure(fg_color=cool_palette["frame_bg"])
salary_frame.configure(fg_color=cool_palette["frame_bg"])
search_frame.configure(fg_color=cool_palette["frame_bg"])

# Apply color to the labels
label_title.configure(text_color=cool_palette["label_text"])
label_first_name.configure(text_color=cool_palette["label_text"])
label_last_name.configure(text_color=cool_palette["label_text"])
label_dob.configure(text_color=cool_palette["label_text"])
label_age.configure(text_color=cool_palette["label_text"])
label_religion.configure(text_color=cool_palette["label_text"])
label_nationality.configure(text_color=cool_palette["label_text"])
label_department.configure(text_color=cool_palette["label_text"])
label_salary.configure(text_color=cool_palette["label_text"])
label_tel.configure(text_color=cool_palette["label_text"])
label_email.configure(text_color=cool_palette["label_text"])
label_start_day.configure(text_color=cool_palette["label_text"])
label_search.configure(text_color=cool_palette["label_text"])

# Apply colors to buttons
btn_add.configure(
    fg_color=cool_palette["button_bg"], 
    hover_color=cool_palette["highlight"], 
    text_color=cool_palette["button_fg"]
)
btn_search.configure(
    fg_color=cool_palette["button_bg"], 
    hover_color=cool_palette["highlight"], 
    text_color=cool_palette["button_fg"]
)

# Customize the input fields
entry_first_name.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
entry_last_name.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
dob_entry.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
entry_age.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
entry_salary.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
entry_tel.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
entry_email.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
start_day_entry.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
entry_religion.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
entry_nationality.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
search_entry.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])

# Apply cool tone to the dropdowns (ComboBoxes)
label_title.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
department_menu.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
position_menu.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])

department_menu.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])
position_menu.configure(fg_color=cool_palette["entry_bg"], text_color=cool_palette["entry_fg"])

# Function to open comment window
def open_comment_window():
    # Create a new top-level window
    comment_window = ctk.CTkToplevel(app)
    comment_window.geometry("400x300")
    comment_window.title("Add Comment")

    # Create label and entry for Employee ID
    label_emp_id = ctk.CTkLabel(comment_window, text="Enter Employee ID:")
    label_emp_id.pack(pady=10)

    entry_emp_id = ctk.CTkEntry(comment_window, width=200)
    entry_emp_id.pack(pady=10)

    # Create label and entry for Comment
    label_comment = ctk.CTkLabel(comment_window, text="Enter Comment:")
    label_comment.pack(pady=10)

    entry_comment = ctk.CTkEntry(comment_window, width=200)
    entry_comment.pack(pady=10)

# ตัวแปรเก็บคอมเมนต์
comments = {}

# Function to open comment window
def open_comment_window():
    # Create a new top-level window
    comment_window = ctk.CTkToplevel(app)
    comment_window.geometry("400x300")
    comment_window.title("Add Comment")

    # Create label and entry for Employee ID
    label_emp_id = ctk.CTkLabel(comment_window, text="Enter Employee ID:")
    label_emp_id.pack(pady=10)

    entry_emp_id = ctk.CTkEntry(comment_window, width=200)
    entry_emp_id.pack(pady=10)

    # Create label and entry for Comment
    label_comment = ctk.CTkLabel(comment_window, text="Enter Comment:")
    label_comment.pack(pady=10)

    entry_comment = ctk.CTkEntry(comment_window, width=200)
    entry_comment.pack(pady=10)

    # Label to display the added comment
    label_display_comment = ctk.CTkLabel(comment_window, text="", wraplength=300)
    label_display_comment.pack(pady=10)

    # Function to save the comment
    def save_comment():
        emp_id = entry_emp_id.get().strip()
        comment = entry_comment.get().strip()

        # Validate Employee ID
        employee = next((emp for emp in employees if emp['employee_id'] == emp_id), None)
        if not employee:
            messagebox.showerror("Error", "Employee ID not found.")
            return
        
        # Save the comment
        if emp_id not in comments:
            comments[emp_id] = []
        comments[emp_id].append(comment)

        messagebox.showinfo("Success", f"Comment added for {employee['first_name']} {employee['last_name']}: {comment}")
        label_display_comment.configure(text=f"Comment for {employee['first_name']} {employee['last_name']}: {comment}")
        
        # Clear entries
        entry_emp_id.delete(0, 'end')
        entry_comment.delete(0, 'end')

    # Create button to submit comment
    btn_submit_comment = ctk.CTkButton(comment_window, text="Submit Comment", command=save_comment)
    btn_submit_comment.pack(pady=20)

# Function to open view comments window
def open_view_comments_window():
    view_window = ctk.CTkToplevel(app)
    view_window.geometry("400x300")
    view_window.title("View Comments")

    # Create label and combobox for selecting Employee ID
    label_select_emp = ctk.CTkLabel(view_window, text="Select Employee ID:")
    label_select_emp.pack(pady=10)

    combobox_emp_id = ctk.CTkComboBox(view_window, width=200)
    combobox_emp_id.pack(pady=10)

    # Populate combobox with employee IDs that have comments
    commented_emp_ids = [emp['employee_id'] for emp in employees if emp['employee_id'] in comments]
    combobox_emp_id.configure(values=['Please select ID'] + commented_emp_ids)
    combobox_emp_id.set('Please select ID')  # Set default text

    # Label to display selected comments
    label_selected_comments = ctk.CTkLabel(view_window, text="", wraplength=300)
    label_selected_comments.pack(pady=10)

    # Function to show comments for selected Employee ID
    def show_comments():
        selected_emp_id = combobox_emp_id.get()
        if selected_emp_id in comments:
            comments_text = "\n".join(comments[selected_emp_id])
            label_selected_comments.configure(text=f"Comments for ID {selected_emp_id}:\n{comments_text}")
        else:
            label_selected_comments.configure(text=f"No comments found for ID {selected_emp_id}.")

    # Create button to view comments
    btn_view_comments = ctk.CTkButton(view_window, text="View Comments", command=show_comments)
    btn_view_comments.pack(pady=20)

# Add the Comment button
btn_comment = ctk.CTkButton(frame_left, text="Comment on Employee", command=open_comment_window)
btn_comment.pack(pady=10)

# Add the View Comments button
btn_view_comments = ctk.CTkButton(frame_left, text="View Comments", command=open_view_comments_window)
btn_view_comments.pack(pady=10)

# (Other existing UI code follows here...)



# Add this in the search frame section of your existing code

# Edit input field for Employee ID
label_edit_id = ctk.CTkLabel(search_frame, text="Edit Employee ID")
label_edit_id.grid(row=1, column=0, padx=10)
edit_id_entry = ctk.CTkEntry(search_frame, width=150)
edit_id_entry.grid(row=1, column=1, padx=10)

# Edit button
btn_edit = ctk.CTkButton(search_frame, text="Edit", command=lambda: edit_employee(edit_id_entry.get()))
btn_edit.grid(row=1, column=2, padx=10)

# Function to edit an employee
def edit_employee(employee_id):
    global employees
    # Find the employee by ID
    employee = next((emp for emp in employees if emp['employee_id'] == employee_id), None)

    if not employee:
        messagebox.showerror("Error", "No employee found with the given ID.")
        return

    # Create a new window for editing
    edit_window = ctk.CTkToplevel(app)
    edit_window.title("Edit Employee Information")
    edit_window.geometry("400x500")

    # Create input fields pre-filled with employee data
    ctk.CTkLabel(edit_window, text="First Name").grid(row=0, column=0, padx=10)
    edit_first_name = ctk.CTkEntry(edit_window, width=150)
    edit_first_name.grid(row=0, column=1, padx=10)
    edit_first_name.insert(0, employee['first_name'])

    ctk.CTkLabel(edit_window, text="Last Name").grid(row=1, column=0, padx=10)
    edit_last_name = ctk.CTkEntry(edit_window, width=150)
    edit_last_name.grid(row=1, column=1, padx=10)
    edit_last_name.insert(0, employee['last_name'])

    ctk.CTkLabel(edit_window, text="Salary").grid(row=2, column=0, padx=10)
    edit_salary = ctk.CTkEntry(edit_window, width=150)
    edit_salary.grid(row=2, column=1, padx=10)
    edit_salary.insert(0, str(employee['salary']))

    ctk.CTkLabel(edit_window, text="Telephone").grid(row=3, column=0, padx=10)
    edit_tel = ctk.CTkEntry(edit_window, width=150)
    edit_tel.grid(row=3, column=1, padx=10)
    edit_tel.insert(0, employee['tel'])

    ctk.CTkLabel(edit_window, text="Email").grid(row=4, column=0, padx=10)
    edit_email = ctk.CTkEntry(edit_window, width=150)
    edit_email.grid(row=4, column=1, padx=10)
    edit_email.insert(0, employee['email'])

    ctk.CTkLabel(edit_window, text="Religion").grid(row=5, column=0, padx=10)
    edit_religion = ctk.CTkEntry(edit_window, width=150)
    edit_religion.grid(row=5, column=1, padx=10)
    edit_religion.insert(0, employee['religion'])

    ctk.CTkLabel(edit_window, text="Nationality").grid(row=6, column=0, padx=10)
    edit_nationality = ctk.CTkEntry(edit_window, width=150)
    edit_nationality.grid(row=6, column=1, padx=10)
    edit_nationality.insert(0, employee['nationality'])

    # Save button to update employee information
    def save_changes():
        # Update employee details
        employee['first_name'] = edit_first_name.get()
        employee['last_name'] = edit_last_name.get()
        employee['salary'] = int(edit_salary.get())
        employee['tel'] = edit_tel.get()
        employee['email'] = edit_email.get()
        employee['religion'] = edit_religion.get()
        employee['nationality'] = edit_nationality.get()

        messagebox.showinfo("Success", "Employee information updated successfully!")
        edit_window.destroy()
        show_employees()  # Refresh employee list

    btn_save = ctk.CTkButton(edit_window, text="Save Changes", command=save_changes)
    btn_save.grid(row=7, column=0, columnspan=2, pady=20)

# Add this in the search frame section of your existing code

# Delete input field for Employee ID
label_delete_id = ctk.CTkLabel(search_frame, text="Delete Employee ID")
label_delete_id.grid(row=2, column=0, padx=10)
delete_id_entry = ctk.CTkEntry(search_frame, width=150)
delete_id_entry.grid(row=2, column=1, padx=10)

# Delete button
btn_delete = ctk.CTkButton(search_frame, text="Delete", command=lambda: delete_employee(delete_id_entry.get()))
btn_delete.grid(row=2, column=2, padx=10)

# Function to delete an employee
def delete_employee(employee_id):
    global employees
    # Find the employee by ID
    employee = next((emp for emp in employees if emp['employee_id'] == employee_id), None)

    if not employee:
        messagebox.showerror("Error", "No employee found with the given ID.")
        return

    # Confirm deletion
    if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete employee ID {employee_id}?"):
        employees.remove(employee)
        messagebox.showinfo("Success", f"Employee ID {employee_id} has been deleted.")
        show_employees()  # Refresh the employee list

# สร้างปุ่มสำหรับตรวจสอบการเชื่อมต่อฐานข้อมูล
btn_check_db = ctk.CTkButton(frame_left, text="Check Database Connection", command=check_database_connection)
btn_check_db.pack(pady=10)

# Display existing employees
show_employees()

# Start the application
app.mainloop()
