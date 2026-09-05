# OOP is the programming paradigm that uses "objects" to design applications and computer programs. It utilizes several techniques from previously established paradigms, including modularity, polymorphism, and encapsulation. The main concepts of OOP are:
# 1. Class: A class is a blueprint for creating objects. It defines a set of attributes and methods that the created objects will have.
# 2. Object: An object is an instance of a class. It is a self-contained entity that consists of both data and behavior. Objects are created from classes and can have their own unique values for the attributes defined in the class.     
# 3. Attributes: Attributes are the data stored inside an object. They represent the state or properties of the object. Each object can have its own unique values for the attributes defined in the class.
# 4. Methods: Methods are functions defined inside a class that describe the behaviors of the objects created from that class. They can manipulate the object's attributes and perform actions related to the object.
# 5. Inheritance: Inheritance is a mechanism that allows a class to inherit attributes and methods from another class. The class that inherits is called the subclass or derived class, while the class being inherited from is called the superclass or base class. Inheritance promotes code reusability and establishes a hierarchical relationship between classes.
# 6. Polymorphism: Polymorphism is the ability of different classes to be treated as instances of the same class through a common interface. It allows objects of different classes to be used interchangeably, enabling flexibility and extensibility in code design.
# 7. Encapsulation: Encapsulation is the practice of bundling data (attributes) and methods that operate on that data within a single unit (class). It restricts direct access to the internal state of an object and provides controlled access through methods, ensuring data integrity and security.
# 8. Abstraction: Abstraction is the process of simplifying complex systems by breaking them down into more manageable and understandable components. In OOP, abstraction allows developers to focus on the essential features of an object while hiding unnecessary implementation details. It helps in creating a clear and concise interface for interacting with objects.
# 9. Object-Oriented Design (OOD): OOD is the process of planning and structuring a software system using object-oriented principles. It involves identifying classes, their relationships, and interactions to create a well-organized and maintainable design.
# 10. Object-Oriented Programming Languages: OOP can be implemented using various programming languages that support object-oriented concepts. Some popular OOP languages include Java, C++, Python, C#, Ruby, and Swift. These languages provide features and syntax specifically designed for creating and working with objects and classes.
# 11. Object-Oriented Analysis (OOA): OOA is the process of analyzing a problem domain and identifying the objects, their attributes, and behaviors that are relevant to the system being developed. It focuses on understanding the requirements and designing a solution using object-oriented principles.


# creating a class named Student
class Student:
    pass

# creating an object of the class Student
# student1 is an object of the Student class
student1 = Student()

# giving attributes to the object student1
student1.name = "Alice"
student1.age = 20
student1.course = "Computer Science"


# printing the attributes of the object student1
print(student1.name)
print(student1.age)
print(student1.course)


## 1 Assignment

# creating a class named Car
class Car:
    pass

# creating an object of the class Car
car1 = Car()

# giving attributes to the object car1
car1.brand = "Toyota"
car1.model = "Corolla"
car1.year = 2020
car1.color = "Blue"

# printing the attributes of the object car1
print("\nCar Details")
print(car1.brand)
print(car1.model)
print(car1.year)
print(car1.color)


## 2 Assignment
# creating a class named BankAccount
class BankAccount:
    pass

# creating an object of the class BankAccount
account1 = BankAccount()

# giving attributes to the object account1
account1.account_holder= "John Doe"
account1.account_number = "123456789"
account1.balance = 1000.0

# printing the attributes of the object account1
print("\nBank Account Details")
print("Account Holder:", account1.account_holder)
print("Account Number:", account1.account_number)
print("Balance: ${:.2f}".format(account1.balance))


### 3 Assignment
# creating a class named University
class University:
    pass

# creating three University Objects
university1 = University()
university2 = University()
university3 = University()

# university1
university1.name = "Harvard University"
university1.location = "Cambridge, Massachusetts"
university1.students_enrolled = 20000

# university2
university2.name = "Stanford University"
university2.location = "Stanford, California"
university2.students_enrolled = 17000

# university3
university3.name = "Massachusetts Institute of Technology"
university3.location = "Cambridge, Massachusetts"
university3.students_enrolled = 11000

# printing the attributes of the object university1
print("\nUniversity Details")

print("\University 1:")
print(university1.name)
print(university1.location)
print(university1.students_enrolled)

# printing the attributes of the object university2
print("\nUniversity 2:")
print(university2.name)
print(university2.location)
print(university2.students_enrolled)

# printing the attributes of the object university3
print("\nUniversity 3:")
print(university3.name)
print(university3.location)
print(university3.students_enrolled)
