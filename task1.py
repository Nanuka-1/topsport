# 1 დავალება

import random
import string   # ყველა ასო სიმბოლო სტრინგში მზადაა

# ინპუტები
length = input("შეიყვანე პაროლის სიგრძე: ")

if not length.isdigit():    #isdigit ამოწმებს ციფრები შეიყვანე თუ არა
    print("გთხოვ, შეიყვანე რიცხვი!")
    exit()

length = int(length)

use_digits = input("გინდა რიცხვები? (yes/no): ").lower()
use_letters = input("გინდა ლათინური ასოები? (yes/no): ").lower()
use_symbols = input("გინდა სიმბოლოები? (yes/no): ").lower()

# ქართული ასოების შემოწმება
if any("ა" <= ch <= "ჰ" for ch in use_letters):
    print("შეიყვანე მხოლოდ ლათინური ასოები!")
    exit()

#სიმბოლოების ლისტები
characters_list = []

if use_digits == "yes":
    characters_list.extend(list(string.digits))

if use_letters == "yes":
    characters_list.extend(list(string.ascii_letters))

if use_symbols == "yes":
    characters_list.extend(list(string.punctuation))

if not characters_list:   # თუ ცარიელია ჩემი ჩარაქტერი ამას დაუწერს
    print("ამოირჩიე მაინც ერთი ვარიანტი!")
    exit()

# PAROLEBIS GENERIREBA (FOR ციკლი)
password_list = []   # list რომელშიც პაროლის ასოები დაგროვდება

for _ in range(length):
    random_char = random.choice(characters_list)
    password_list.append(random_char)   # list.append REQUIRED

# list → string (join REQUIRED)
password = "".join(password_list)

# პრინტი ფორმატირებით
print(f"შენი გენერირებული პაროლია: {password}")


 # 2 დავალება

import string

#  მომხმარებლის შეყვანის შემოწმება
user_input = input("შეიყვანე ფიბონაჩის რიცხვი: ")

#  ცარიელი ველი
if user_input.strip() == "":
    print("შენ არაფერი შეიყვანე! მხოლოდ რიცხვი უნდა შეიყვანო!")
    exit()

# თუ არის ასო
if any(ch.isalpha() for ch in user_input):
    print(f'შენ შეიყვანე ასო(ები): "{user_input}" — არასწორია! მხოლოდ რიცხვი შეიყვანე!')
    exit()

# თუ არის სიმბოლო
if any(ch in string.punctuation for ch in user_input):
    print(f'შენ შეიყვანე სიმბოლო(ები): "{user_input}" — არასწორია! მხოლოდ რიცხვი შეიყვანე!')
    exit()

# თუ არის space
if any(ch.isspace() for ch in user_input):
    print(f'შენ შეიყვანე დაშორება/space: "{user_input}" — არასწორია! მხოლოდ რიცხვი შეიყვანე!')
    exit()

# საბოლოო შემოწმება — არის თუ არა საერთოდ რიცხვი
if not user_input.isdigit():
    print(f'შენ შეიყვანე უცნაური ტექსტი: "{user_input}" — საჭიროა მხოლოდ მთელი რიცხვი!')
    exit()



n = int(user_input)

# ფიბონაჩის დასაწყისი
f1 = 1
f2 = 1

# თუ მომხმარებელმა მიუთითა 1
if n == 1:
    print(f1)
    exit()

# თუ მიუთითა 2
print(f1, f2, end=" ")

# while ციკლი
while n > 2:
    f1, f2 = f2, f1 + f2
    print(f2, end=" ")
    n -= 1

