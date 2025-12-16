# 1 დავალება

def char_generators(word):
    for char in word:
        yield char

word = "CODE"

for char in char_generators(word):
    print(char)


# 2 დავალება
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]

while True:
    user_input = input("შემოიყვანეთ ინდექსი (გამოსასვლელად 'exit'): ")

    if user_input.lower() == "exit":
        print("გასვლა პროგრამიდან")
        break

    try:
        index = int(user_input)
        print(f"მნიშვნელობა ინდექსზე {index} არის: {arr[index]}")

    except ValueError:
        print("გთხოვთ შეიყვანოთ მხოლოდ ციფრი")

    except IndexError:
        print("ასეთი ინდექსი ლისტში არ არსებობს")


# 3 დავალება

import logging
import json

logging.basicConfig(
    filename="game.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_score(name, points):
    log_entry = {"player": name, "points": points}
    logging.info(json.dumps(log_entry, ensure_ascii=False))


questions = [
    ("5 + 5", 10),
    ("10 - 3", 7),
    ("4 * 2", 8),
    ("20 / 4", 5),
    ("3 + 7", 10)
]


while True:
    name = input("შეიყვანეთ თქვენი სახელი: ").strip()
    if name:
        break
    print("სახელი სავალდებულოა, სცადეთ კიდევ ერთხელ.")

score = 0

for question, correct_answer in questions:
    answer = input(f"{question} = ")

    try:
        if int(answer) == correct_answer:
            score += 10
    except ValueError:
        pass

log_score(name, score)
print(f"{name}, თქვენ დააგროვეთ {score} ქულა")

# 4 davaleba


import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("quiz.log", mode="a", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


 #  გენერატორი შეკითხვებისთვის
def question_generator():
    questions = [
        "რომელია საფრანგეთის დედაქალაქი?",
        "5 + 5 = ?",
        "რომელია დედამიწის თანამგზავრი?",
        "10 - 3 = ?",
        "რამდენი დღეა ერთ კვირაში?"
    ]

    for question in questions:
        yield question


 #  შეკითხვების კითხვა და ლოგირება
for question in question_generator():
    print(question)
    answer = input("თქვენი პასუხი: ")

    logger.info(f"კითხვა: {question}")
    logger.info(f"პასუხი: {answer}")
    logger.info("-" * 30)

print("ყველა პასუხი შენახულია quiz.log ფაილში")

  # 5 დავალება

choices = ["ქვა", "ბადე", "მაკრატელი"]

user_score = 0
computer_score = 0

while user_score < 3 and computer_score < 3:
    user_choice = input("აირჩიე ქვა / ბადე / მაკრატელი: ").strip()
    computer_choice = random.choice(choices)

    print(f"კომპიუტერმა აირჩია: {computer_choice}")

    if user_choice not in choices:
        print("არასწორი არჩევანი, სცადე კიდევ\n")
        continue

    if user_choice == computer_choice:
        print("ფრეა!\n")
        continue

    if (
        (user_choice == "ქვა" and computer_choice == "მაკრატელი") or
        (user_choice == "მაკრატელი" and computer_choice == "ბადე") or
        (user_choice == "ბადე" and computer_choice == "ქვა")
    ):
        print("რაუნდი მოიგე ")
        user_score += 1
    else:
        print("რაუნდი მოიგო კომპიუტერმა ")
        computer_score += 1

    print(f"ქულა: მომხმარებელი {user_score} - {computer_score} კომპიუტერი\n")

if user_score == 3:
    print(" მომხმარებელმა გაიმარჯვა!")
else:
    print(" კომპიუტერმა გაიმარჯვა!")


    #6 დავალება


import random

while True:
    gamer1 = random.randint(1, 6)
    gamer2 = random.randint(1, 6)

    print(f"Gamer 1 გააგორა: {gamer1}")
    print(f"Gamer 2 გააგორა: {gamer2}")

    if gamer1 == gamer2:
        print("ფრეა! ვიმეორებთ...\n")
        continue
    elif gamer1 > gamer2:
        print(" Gamer 1 მოიგო!")
        break
    else:
        print(" Gamer 2 მოიგო!")
        break


