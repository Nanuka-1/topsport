#-----------1 დავალება ------------



class BankAccount:
    def __init__(self, owner, balance=0):
        self.__owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("შესატანი თანხა უნდა იყოს დადებითი")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("გამოსატანი თანხა უნდა იყოს დადებითი")
        if amount > self.__balance:
            raise ValueError("არასაკმარისი ბალანსი")
        self.__balance -= amount
        return self.__balance

    def get_balance(self):
        return self.__balance

    def get_owner(self):
        return self.__owner



#--------------2 დავალება --------------

class ShoppingCart:
    def __init__(self, items):
        # items არის სია
        self.items = items

    def __len__(self):
        #  რაოდენობა
        return len(self.items)

    def __eq__(self, other):
        # საშუალებას გვაძლევს შევადაროთ ორი კალათა == ოპერატორით
        if isinstance(other, ShoppingCart):
            return len(self.items) == len(other.items)
        return False

#  კალათები სხვადასხვა რაოდენობის პროდუქტებით

cart1 = ShoppingCart(["ვაშლი", "რძე", "პური"])
cart2 = ShoppingCart(["წიგნი", "კალამი", "რვეული"])
cart3 = ShoppingCart(["ყავა", "შაქარი"])
cart4 = ShoppingCart(["წყალი", "წვენი"])

#  კალათის შედარება (ტოლია)
print(f"კალათა 1 == კალათა 2: {cart1 == cart2}")

#  კალათის შედარება (1 და 2 ტოლია, მაგრამ 3 - არა)
print(f"კალათა 1, 2 და 3 ტოლია? {cart1 == cart2 == cart3}")

#  კალათის შედარება (წყვილებში შედარება)
print(f"კალათა 3 == კალათა 4: {cart3 == cart4}")
print(f"ყველა კალათა ერთმანეთის ტოლია? {cart1 == cart2 == cart3 == cart4}")

#--------------3 დავალება ------------------------

from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    year: int

    def is_classic(self):
        # აბრუნებს True-ს, თუ წელი ნაკლებია 1970-ზე
        return self.year < 1970


book1 = Book("ვეფხისტყაოსანი", "შოთა რუსთაველი", 1200)
book2 = Book("ჰარი პოტერი", "ჯ.კ. როულინგი", 1997)
book3 = Book("დიდოსტატის მარჯვენა", "კონსტანტინე გამსახურდია", 1939)


print(f"'{book1.title}' არის კლასიკა? {book1.is_classic()}")
print(f"'{book2.title}' არის კლასიკა? {book2.is_classic()}")
print(f"'{book3.title}' არის კლასიკა? {book3.is_classic()}")


#------------------------4 დავალება --------------------
class Person:
    def __del__(self):
        print("Person removed")

# ობიექტის შექმნა
p1 = Person()

# ობიექტის წაშლა
del p1


#--------------5 დავალება ------------------------------
class CustomList:
    def __init__(self, data):
        # მონაცემებს ვინახავთ შიდა სიაში
        self.data = data

    def __getitem__(self, index):
        #  მივწვდეთ: my_list[0]
        return self.data[index]

    def __setitem__(self, index, value):
        # შევცვალოთ: my_list[0] = 10
        self.data[index] = value

    def __iter__(self):
        # აბრუნებს იტერატორს, რომ ციკლმა იმუშაოს
        return iter(self.data)

# --- გამოყენება ---

# შევქმნათ ობიექტი
my_list = CustomList([10, 20, 30, 40])

#  __getitem__ - ელემენტის წაკითხვა
print(f"მეორე ელემენტია: {my_list[1]}")

#  __setitem__ - ელემენტის შეცვლა
my_list[1] = 99
print(f"შეცვლილი ელემენტი: {my_list[1]}")

#  __iter__ - for ციკლში გამოყენება
print("სიის ყველა ელემენტი:")
for item in my_list:
    print(item)


#--------------6 დავალება --------------------

class Refrigerator:
    def __init__(self, items):
        self.items = items

    def __contains__(self, item):
        #ამოწმებს პროდუქტებს სიაში
        return item in self.items

    def __str__(self):
        # აბრუნებს ობიექტის ტექსტურ აღწერას
        return f"Fridge with {len(self.items)} items"

    def __del__(self):
        # წაშლა
        print("Fridge unplugged!")

# --- გამოყენება ---

fridge = Refrigerator(["milk", "cheese", "apple"])


if "milk" in fridge:
    print("Yes, milk is in the fridge.")
else:
    print("No milk found.")

print(fridge)

del fridge


#-----------------------7 დავალება -------------------

class FunnyCalculator:
    def __str__(self):
        return "I’m the funniest calculator in Python!"

    def __add__(self, other):
        return "Why are you adding numbers? Just buy a calculator"

    def __mul__(self, other):
        return "Multiplication is too mainstream..."

    def __truediv__(self, other):
        if other == 0:
            return "ZeroDivisionError? Nah, let’s just say infinity"
        return f"Okay, I'll divide it: {10 / other}"

# --- გამოყენება ---

calc = FunnyCalculator()

print(calc)

print(calc + 5)

print(calc * 2)

print(calc / 0)

print(calc /2)

