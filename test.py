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




