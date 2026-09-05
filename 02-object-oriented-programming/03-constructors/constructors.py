class student:
    def __init__(self):
        print("This is a constructor")

student1 = student()

class Car:
    def __init__(self, brand, model, year, color):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color

car1 = Car("Toyota", "Corolla", 2020, "Blue")

print("\nCar Details")
print("Brand:", car1.brand)
print("Model:", car1.model)
print("Year:", car1.year)
print("Color:", car1.color)



class Student:
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course

student1 = Student("Alice", 20, "Computer Science")
student2 = Student("Bob", 22, "Mathematics")

print("\nStudent Details")
print("Name:", student1.name)
print("Age:", student1.age)
print("Course:", student1.course)

print("\nName:", student2.name)
print("Age:", student2.age)
print("Course:", student2.course)

# Method in Constructor

class BankAccount:
    def __init__(self, account_holder, account_number, balance):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance

    def display_account_details(self):
        print("\nBank Account Details")
        print("Account Holder:", self.account_holder)
        print("Account Number:", self.account_number)
        print("Balance:", self.balance)

account1 = BankAccount("John Doe", "123456789", 1000.0)
account1.display_account_details()


## 1 Assignment

class Car:
    def __init__(self, brand, model, year, color):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color

car1 = Car("Toyota", "Corolla", 2020, "Blue")
car2 = Car("Honda", "Civic", 2021, "Red")

print("\nCar Details")
print("Brand:", car1.brand)
print("Model:", car1.model)
print("Year:", car1.year)
print("Color:", car1.color)

print("\nBrand:", car2.brand)
print("Model:", car2.model)
print("Year:", car2.year)
print("Color:", car2.color)


## 2 Assignment

class Student:
    def __init__(self, name, age,course, year):
        self.name = name
        self.age = age
        self.course = course
        self.year = year

student1 = Student("Alice", 20, "Computer Science", 2)
student2 = Student("Bob", 22, "Mathematics", 3)
student3 = Student("Charlie", 21, "Physics", 1)

print("\nStudent Details")
print("Name:", student1.name)
print("Age:", student1.age)
print("Course:", student1.course)
print("Year:", student1.year)

print("\nName:", student2.name)
print("Age:", student2.age)
print("Course:", student2.course)
print("Year:", student2.year)

print("\nName:", student3.name)
print("Age:", student3.age)
print("Course:", student3.course)
print("Year:", student3.year)


# 3 Assignment

class BankAccount:
    def __init__(self, account_holder, account_number, balance):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance

    def display_account_details(self):
        print("\nBank Account Details")
        print("Account Holder:", self.account_holder)
        print("Account Number:", self.account_number)
        print("Balance:", self.balance)

    def deposit(self, amount):
        if amount > 0:

            self.balance += amount
            print("Deposited: ${:.2f}".format(amount))
            print("New Balance: ${:.2f}".format(self.balance))
        else:
            print("Deposit amount must be positive.")

account1 = BankAccount("John Doe", "123456789", 1000.0)
account1.display_account_details()
account1.deposit(500.0)


class Employee:
    def __init__(self,name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary

    def display_details(self):
        print("\nEmployee Details")
        print("Name:", self.name)
        print("Position:", self.position)
        print("Salary:", self.salary)

    def increase_salary(self, amount):
        if amount > 0:
            self.salary += amount
            print("Salary increased by: ${:.2f}".format(amount))
            print("New Salary: ${:.2f}".format(self.salary))
        else:
            print("Increase amount must be positive.")

employee1 = Employee("Jane Smith", "Manager", 60000.0)
employee1.display_details()
employee1.increase_salary(2000000.0)