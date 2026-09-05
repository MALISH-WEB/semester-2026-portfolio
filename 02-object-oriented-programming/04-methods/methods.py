# Mehods are functions that are defined inside a class
# Object State

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
P1 = Student("Alice", 20)
P1.introduce()


class BankAccount:
    def __init__(self, owner_name, starting_balance):
        self.owner_name = owner_name
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance is {self.balance}.")


    def display_balance(self):
        print(f"Current balance is {self.balance}.")

Bank1 = BankAccount("Malish", 5000)
Bank1.deposit(50000) 
Bank1.deposit(70000)
Bank1.display_balance()
