class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

Book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 10.99)
Book2 = Book("To Kill a Mockingbird", "Harper Lee", 7.99)
Book3 = Book("Atomic Habits", "James Clear", 11.99)

print(Book1.title, Book1.author, Book1.price)
print(Book2.title, Book2.author, Book2.price)
print(Book3.title, Book3.author, Book3.price)


class Laptop:
    def __init__(self, brand, model, ram, storage, price):
        self.brand = brand
        self.model = model
        self.ram = ram
        self.storage = storage
        self.price = price
Laptop1 = Laptop("Dell", "XPS 13", "16GB", "512GB SSD", 999.99)
Laptop2 = Laptop("Apple", "MacBook Pro", "16GB", "1TB SSD", 1299.99)

print(Laptop1.brand, Laptop1.model, Laptop1.ram, Laptop1.storage, Laptop1.price)
print(Laptop2.brand, Laptop2.model, Laptop2.ram, Laptop2.storage, Laptop2.price)


class BankAccount:
    def __init__(self, account_holder, account_number, balance):
        self.account_holder = account_holder
        self.account_number = account_number
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount
        print(f"Deposited {amount}")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("sufficient funds")
        else:
            self.__balance -= amount
            print(f"Withdrew {amount}")

    def get_balance(self):
        return self.__balance

account1 = BankAccount("John Doe", "123456789", 1000.0)
account1.deposit(500)
account1.withdraw(200)
print(account1.get_balance())


class Vehicle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def __init__(self, brand, model, year, number_of_doors):
        super().__init__(brand, model, year)
        self.number_of_doors = number_of_doors


car1 = Vehicle("Toyota", "Camry", 2020, 4)
print(car1.brand, car1.model, car1.year, car1.number_of_doors)

