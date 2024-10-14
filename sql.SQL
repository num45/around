-- สร้างตาราง Attendance
CREATE TABLE Attendance (
    id SERIAL PRIMARY KEY,
    employee_id INT,
    log_type VARCHAR(100),
    datetime_log TIMESTAMP,
    date_updated DATE
);

-- สร้างตาราง Payroll_Item
CREATE TABLE Payroll_Item (
    id SERIAL PRIMARY KEY,
    payroll_id INT,
    employee_id INT,
    present INT,
    absent INT,
    late INT,
    salary NUMERIC(10, 2),
    allowance_amount NUMERIC(10, 2),
    allowances TEXT,
    deduction_amount NUMERIC(10, 2),
    deductions TEXT,
    net NUMERIC(10, 2),
    date_created DATE
);

-- สร้างตาราง Payroll
CREATE TABLE Payroll (
    ref_no SERIAL PRIMARY KEY,
    date_from DATE,
    date_to DATE,
    type VARCHAR(100),
    status VARCHAR(50),
    date_created DATE
);

-- สร้างตาราง Employee
CREATE TABLE Employee (
    employee_id SERIAL PRIMARY KEY,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    region VARCHAR(50),
    nationality VARCHAR(50),
    dob DATE,
    tel VARCHAR(10)
    email VARCHAR(50)
    department_id INT,
    position_id INT,
    salary NUMERIC(10, 2)
);

-- สร้างตาราง Deductions
CREATE TABLE Deductions (
    id SERIAL PRIMARY KEY,
    deduction VARCHAR(100),
    description TEXT
);

-- สร้างตาราง Employee_Deductions
CREATE TABLE Employee_Deductions (
    employee_id INT,
    deduction_id INT,
    type VARCHAR(100),
    amount NUMERIC(10, 2),
    effective_date DATE,
    date_created DATE,
    PRIMARY KEY (employee_id, deduction_id)
);

-- สร้างตาราง Department
CREATE TABLE Department (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- สร้างตาราง Position
CREATE TABLE Position (
    id SERIAL PRIMARY KEY,
    department_id INT,
    name VARCHAR(100)
);

-- เพิ่ม Foreign Key ให้กับตาราง Attendance
ALTER TABLE Attendance
ADD CONSTRAINT fk_attendance_employee FOREIGN KEY (employee_id) REFERENCES Employee(id);

-- เพิ่ม Foreign Key ให้กับตาราง Payroll_Item
ALTER TABLE Payroll_Item
ADD CONSTRAINT fk_payroll_item_payroll FOREIGN KEY (payroll_id) REFERENCES Payroll(ref_no),
ADD CONSTRAINT fk_payroll_item_employee FOREIGN KEY (employee_id) REFERENCES Employee(id);

-- เพิ่ม Foreign Key ให้กับตาราง Employee
ALTER TABLE Employee
ADD CONSTRAINT fk_employee_department FOREIGN KEY (department_id) REFERENCES Department(id),
ADD CONSTRAINT fk_employee_position FOREIGN KEY (position_id) REFERENCES Position(id);

-- เพิ่ม Foreign Key ให้กับตาราง Employee_Deductions
ALTER TABLE Employee_Deductions
ADD CONSTRAINT fk_employee_deductions_employee FOREIGN KEY (employee_id) REFERENCES Employee(id),
ADD CONSTRAINT fk_employee_deductions_deduction FOREIGN KEY (deduction_id) REFERENCES Deductions(id);

-- เพิ่ม Foreign Key ให้กับตาราง Position
ALTER TABLE Position
ADD CONSTRAINT fk_position_department FOREIGN KEY (department_id) REFERENCES Department(id);