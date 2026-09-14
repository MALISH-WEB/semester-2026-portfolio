######### CLASSES AND OBJECTS ######### 

class Student:
    pass

student1 = Student()  

student1.name = "Alice"
student1.age = 20
student1.grade = "A"

print(student1.name)
print(student1.age) 
print(student1.grade)

class Car:
    pass

car1 = Car()

car1.color = "Red"
car1.make = "Toyota"
car1.model = "Camry"

print(car1.color)
print(car1.make)
print(car1.model)


####### CONSTRUCTORSAND SELF #########
class Student:
    def __init__(self,name,age,course):
        self.name = name
        self.age = age
        self.course = course

student1 = Student("Alice", 20, "Computer Science")
student2 = Student("Bob", 22, "Mathematics")

print(student1.name, student1.age, student1.course)
print(student2.name, student2.age, student2.course)



######## METHODS #########

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            return "Error: Division by zero is not allowed."
        return a / b

a = 10
b = 5

print("Addition:", Calculator().add(a, b))
print("Subtraction:", Calculator().subtract(a, b))
print("Multiplication:", Calculator().multiply(a, b))
print("Division:", Calculator().divide(a, b))



######## ENCAPSULATION #########
class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: {amount}. New balance: {self.__balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew: {amount}. New balance: {self.__balance}")
        else:
            print("Invalid withdrawal amount.")

    def get_balance(self):
        return self.__balance

account = BankAccount("John Doe", 1000)
account.deposit(500)
account.withdraw(200)
print("Current balance:", account.get_balance())


######### GETTERS AND SETTERS #########
class Person:
    def __init__(self, name, age):
        self.__name = name  # Private attribute
        self.__age = age    # Private attribute

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if age >= 0:
            self.__age = age
        else:
            print("Age cannot be negative.")


person = Person("Alice", 30)
print("Age:", person.get_age())
person.set_age(35)
print("New Age:", person.get_age())




########## INHERITANCE #########
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

   def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


class Student(Person):
    def __init__(self, name, age, course):
        super().__init__(name, age)  # Call the constructor of the parent class
        self.course = course

student = Student("Alice", 20, "Computer Science")
student.display_info()
print(f"Name: {student.name}, Age: {student.age}, Course: {student.course}")


##### POLYMORPHISM #########
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

class Cat(Animal):
    def speak(self):
        print("Cat meows")

Animal =[Dog(), Cat()]

# Call the speak method on each instance
for animal in Animal:
    animal.speak()



#### COMPLETE QUESTION #####

class Person:
    def __init__(self, name, age):
        self.name = name
        self.__age = age # private attribute


class Student(Person):
    def __init__(self, name, age, student_id, course, tuition):
        super().__init__(name, age)  # Call the constructor of the parent class
        self.course = course
        self.student_id = student_id
        self.__tuition = tuition

    def get_tuition(self):
        return self.__tuition

    def set_tuition(self, tuition):
        if tuition >=0:
            self.__tuition = tuition
        else:
            print("Tuition cannot be negative.")

    # pay tuition method
    def pay_tuition(self, amount):
        if amount > 0:
            print("Payment must be graeter than 0")
        elif amount > self.__tuition:
            print("Payment exceeds tuition amount")
        else:
            self.__tuition -= amount
            print(f"Payment of {amount} made. Remaining tuition: {self.__tuition}")

    # Display student details method

    def display_student_details(self):
        self.display_student_details()
        print("Student ID:", self.student_id)
        print("Course:", self.course)
        print("Tuition:", self.__tuition)

    # Creating Objects
student1 = Student(
    "John Doe", 
    20, 
    "S12345", 
    "Computer Science", 
    5000
)
student2 = Student(
    "Jane Smith",
    22,
    "S67890",
    "Mathematics",
    4000
)

# Displaying student details
print("............. STUDENT 1 ............")
student1.display_student_details()

print("\n............. STUDENT 2 ............")
student2.display_student_details()


# Paying tuition
print("\n............. PAYING TUITION ............")
student1.pay_tuition(1000)

print("\n............. UPDATED STUDENT 1 DETAILS ............")
student1.display_student_details()

# Using Setter
print("\n............. UPDATING TUITION ............")
student1.set_tuition(4000)
