
from abc import ABC, abstractmethod


# ==========================================================================================
# ABSTRACT BASE CLASS
# ==========================================================================================
class Employee(ABC):
    total_employee = 0

    def __init__(self, employee_id, name, email, department, basic_salary):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.department = department

        # Encapsulation: private attribute
        self.__basic_salary = basic_salary

        Employee.total_employee += 1

    # Getter
    @property
    def salary(self):
        return self.__basic_salary

    # Setter
    @salary.setter
    def salary(self, value):
        if value > 0:
            self.__basic_salary = value
        else:
            raise ValueError("Salary must be greater than 0")

    # Abstract method
    @abstractmethod
    def calculate_salary(self):
        pass

    # Common method
    def display_employee(self):
        print("\n" + "-" * 50)
        print("Employee ID   :", self.employee_id)
        print("Name          :", self.name)
        print("Email         :", self.email)
        print("Department    :", self.department)
        print("Employee Type :", self.__class__.__name__)
        print("Basic Salary  :", self.salary)
        print("Final Salary  :", f"{self.calculate_salary():.2f}")
        print("-" * 50)

    # Static methods
    @staticmethod
    def validate_employee_id(employee_id):
        return (
            employee_id.startswith("EMP")
            and employee_id[3:].isdigit()
        )

    @staticmethod
    def validate_email(email):
        return "@" in email and "." in email.split("@")[-1]


# ==========================================================
# FULL-TIME EMPLOYEE
# ==========================================================
class FullTimeEmployee(Employee):
    def __init__(
        self, employee_id, name, email, department,
        basic_salary, allowance, annual_bonus
    ):
        super().__init__(
            employee_id, name, email, department, basic_salary
        )

        self.allowance = allowance
        self.annual_bonus = annual_bonus

    def calculate_salary(self):
        return self.salary + self.allowance + self.annual_bonus


# ==========================================================
# PART-TIME EMPLOYEE
# ==========================================================
class PartTimeEmployee(Employee):
    def __init__(
        self, employee_id, name, email, department,
        basic_salary, hours_worked, hourly_rate
    ):
        super().__init__(
            employee_id, name, email, department, basic_salary
        )

        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    def calculate_salary(self):
        return self.hours_worked * self.hourly_rate


# ==========================================================
# INTERN
# ==========================================================
class Intern(Employee):
    def __init__(
        self, employee_id, name, email, department,
        basic_salary, internship_duration, stipend
    ):
        super().__init__(
            employee_id, name, email, department, basic_salary
        )

        self.internship_duration = internship_duration
        self.stipend = stipend

    def calculate_salary(self):
        return self.stipend


# ==========================================================
# MANAGER
# ==========================================================
class Manager(FullTimeEmployee):
    def __init__(
        self, employee_id, name, email, department,
        basic_salary, allowance, annual_bonus,
        team_size, management_bonus
    ):
        super().__init__(
            employee_id, name, email, department,
            basic_salary, allowance, annual_bonus
        )

        self.team_size = team_size
        self.management_bonus = management_bonus

    def calculate_salary(self):
        return (
            self.salary
            + self.allowance
            + self.annual_bonus
            + self.management_bonus
        )


# ==========================================================
# EMPLOYEE MANAGEMENT SYSTEM
# ==========================================================
class EmployeeManagementSystem:
    def __init__(self):
        # Employee ID -> Employee object
        self.employees = {}

    # ------------------------------------------------------
    # ADD EMPLOYEE
    # ------------------------------------------------------
    def add_employee(self):
        print("\n========== ADD EMPLOYEE ==========")

        employee_id = input("Enter Employee ID (EMP101): ").strip().upper()

        if employee_id in self.employees:
            print("Employee ID already exists.")
            return

        if not Employee.validate_employee_id(employee_id):
            print("Invalid Employee ID. Example: EMP101")
            return

        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip()

        if not Employee.validate_email(email):
            print("Invalid Email.")
            return

        department = input("Enter Department: ").strip()

        print("\nSelect Employee Type")
        print("1. Full-Time Employee")
        print("2. Part-Time Employee")
        print("3. Intern")
        print("4. Manager")

        choice = input("Enter choice: ").strip()

        try:
            basic_salary = float(input("Enter Basic Salary: "))

            if basic_salary <= 0:
                print("Salary must be greater than 0.")
                return

            if choice == "1":
                allowance = float(input("Enter Allowance: "))
                annual_bonus = float(input("Enter Annual Bonus: "))

                employee = FullTimeEmployee(
                    employee_id, name, email, department,
                    basic_salary, allowance, annual_bonus
                )

            elif choice == "2":
                hours_worked = float(input("Enter Hours Worked: "))
                hourly_rate = float(input("Enter Hourly Rate: "))

                employee = PartTimeEmployee(
                    employee_id, name, email, department,
                    basic_salary, hours_worked, hourly_rate
                )

            elif choice == "3":
                internship_duration = int(
                    input("Enter Internship Duration (months): ")
                )
                stipend = float(input("Enter Monthly Stipend: "))

                employee = Intern(
                    employee_id, name, email, department,
                    basic_salary, internship_duration, stipend
                )

            elif choice == "4":
                allowance = float(input("Enter Allowance: "))
                annual_bonus = float(input("Enter Annual Bonus: "))
                team_size = int(input("Enter Team Size: "))
                management_bonus = float(
                    input("Enter Management Bonus: ")
                )

                employee = Manager(
                    employee_id, name, email, department,
                    basic_salary, allowance, annual_bonus,
                    team_size, management_bonus
                )

            else:
                print("Invalid employee type.")
                return

            self.employees[employee_id] = employee
            print("\nEmployee added successfully!")

        except ValueError:
            print("Invalid input. Please enter valid numeric values.")

    # ------------------------------------------------------
    # DISPLAY ALL EMPLOYEES
    # ------------------------------------------------------
    def display_all_employees(self):
        print("\n========== ALL EMPLOYEES ==========")

        if not self.employees:
            print("No employees found.")
            return

        for employee in self.employees.values():
            employee.display_employee()

    # ------------------------------------------------------
    # SEARCH EMPLOYEE
    # ------------------------------------------------------
    def search_employee(self):
        print("\n========== SEARCH EMPLOYEE ==========")

        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id in self.employees:
            self.employees[employee_id].display_employee()
        else:
            print("Employee not found.")

    # ------------------------------------------------------
    # UPDATE SALARY
    # ------------------------------------------------------
    def update_salary(self):
        print("\n========== UPDATE SALARY ==========")

        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id not in self.employees:
            print("Employee not found.")
            return

        try:
            new_salary = float(input("Enter New Basic Salary: "))
            self.employees[employee_id].salary = new_salary
            print("Basic salary updated successfully.")

        except ValueError as error:
            print("Error:", error)

    # ------------------------------------------------------
    # DELETE EMPLOYEE
    # ------------------------------------------------------
    def delete_employee(self):
        print("\n========== DELETE EMPLOYEE ==========")

        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id in self.employees:
            del self.employees[employee_id]
            Employee.total_employee -= 1
            print("Employee deleted successfully.")
        else:
            print("Employee not found.")

    # ------------------------------------------------------
    # SALARY REPORT
    # ------------------------------------------------------
    def salary_report(self):
        print("\n========== EMPLOYEE SALARY REPORT ==========")

        if not self.employees:
            print("No employees found.")
            return

        print(
            f"{'ID':<12}"
            f"{'NAME':<20}"
            f"{'TYPE':<25}"
            f"{'SALARY':>12}"
        )
        print("-" * 69)

        total_salary = 0

        for employee in self.employees.values():
            salary = employee.calculate_salary()
            total_salary += salary

            print(
                f"{employee.employee_id:<12}"
                f"{employee.name:<20}"
                f"{employee.__class__.__name__:<25}"
                f"{salary:>12.2f}"
            )

        print("-" * 69)
        print("Total Employees :", len(self.employees))
        print(f"Total Salary    : {total_salary:.2f}")
        print(f"Average Salary  : {total_salary / len(self.employees):.2f}")

    # ------------------------------------------------------
    # HIGHEST SALARY EMPLOYEE
    # ------------------------------------------------------
    def highest_salary_employee(self):
        print("\n========== HIGHEST SALARY EMPLOYEE ==========")

        if not self.employees:
            print("No employees found.")
            return

        highest_employee = max(
            self.employees.values(),
            key=lambda employee: employee.calculate_salary()
        )

        highest_employee.display_employee()

    # ------------------------------------------------------
    # EMPLOYEE COUNT
    # ------------------------------------------------------
    def employee_count(self):
        print("\nTotal Employees:", len(self.employees))

    # ------------------------------------------------------
    # MAIN MENU
    # ------------------------------------------------------
    def menu(self):
        while True:
            print("\n" + "=" * 45)
            print("       EMPLOYEE MANAGEMENT SYSTEM")
            print("=" * 45)
            print("1. Add Employee")
            print("2. Display All Employees")
            print("3. Search Employee")
            print("4. Update Salary")
            print("5. Delete Employee")
            print("6. Salary Report")
            print("7. Highest Salary Employee")
            print("8. Employee Count")
            print("9. Exit")
            print("=" * 45)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_employee()
            elif choice == "2":
                self.display_all_employees()
            elif choice == "3":
                self.search_employee()
            elif choice == "4":
                self.update_salary()
            elif choice == "5":
                self.delete_employee()
            elif choice == "6":
                self.salary_report()
            elif choice == "7":
                self.highest_salary_employee()
            elif choice == "8":
                self.employee_count()
            elif choice == "9":
                print("Thank you for using Employee Management System!")
                break
            else:
                print("Invalid choice. Please try again.")


# ==========================================================
# PROGRAM START
# ==========================================================
if __name__ == "__main__":
    system = EmployeeManagementSystem()
    system.menu()
