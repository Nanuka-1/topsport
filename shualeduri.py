#==================1 დავალება =================

library = [
    {"title": "1984", "author": "George Orwell", "year": 1949},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937},
    {"title": "Harry Potter", "author": "J.K. Rowling", "year": 1997},
    {"title": "The Alchemist", "author": "Paulo Coelho", "year": 1988},
    {"title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "year": 1943},
    {"title": "Animal Farm", "author": "George Orwell", "year": 1945},
    {"title": "Dune", "author": "Frank Herbert", "year": 1965},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953},
    {"title": "Brave New World", "author": "Aldous Huxley", "year": 1932},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951}
]



def show_books():
    print("\n ბიბლიოთეკაში არსებული წიგნები:")
    for index, book in enumerate(library, start=1):
        print(f"{index}. {book['title']} - {book['author']} ({book['year']})")


def add_book():
    title = input("შეიყვანე წიგნის სათაური: ")
    author = input("შეიყვანე ავტორი: ")
    year = input("შეიყვანე გამოცემის წელი: ")

    new_book = {
        "title": title,
        "author": author,
        "year": year
    }

    library.append(new_book)
    print("წიგნი დაემატა ბიბლიოთეკას")


def search_book():
    search_title = input("შეიყვანე საძიებელი სათაური: ")

    for book in library:
        if book["title"] == search_title:
            print(f"🔍 ნაპოვნია: {book['title']} - {book['author']} ({book['year']})")
            return

    print("წიგნი ვერ მოიძებნა")


def take_book():
    show_books()
    choice = int(input("აირჩიე წიგნის ნომერი წასაკითხად: "))

    if 1 <= choice <= len(library):
        taken_book = library.pop(choice - 1)
        print(f"შენ აიღე: {taken_book['title']}")
    else:
        print("არასწორი ნომერი")




while True:
    print("\n------ მინი ბიბლიოთეკა ------")
    print("1. ყველა წიგნის ნახვა")
    print("2. წიგნის დამატება")
    print("3. წიგნის ძებნა სათაურით")
    print("4. წიგნის წაღება ბიბლიოთეკიდან")
    print("5. გამოსვლა")

    choice = input("აირჩიე მოქმედება (1-5): ")

    if choice == "1":
        show_books()
    elif choice == "2":
        add_book()
    elif choice == "3":
        search_book()
    elif choice == "4":
        take_book()
    elif choice == "5":
        print(" ნახვამდის!")
        break
    else:
        print("არასწორი არჩევანი")


#==================2 დავალება =====================

import random

suits = ["ყვავი", "ჯვარი", "გული", "აგური"]
values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

deck = []

for suit in suits:
    for value in values:
        deck.append((value, suit))


def card_value(card):
    value = card[0]

    if value in ["J", "Q", "K"]:
        return 10
    elif value == "A":
        return 11
    else:
        return int(value)


def calculate_score(cards):
    score = 0
    for card in cards:
        score += card_value(card)
    return score


def play_game():
    random.shuffle(deck)

    player_cards = [deck.pop(), deck.pop()]
    computer_cards = [deck.pop(), deck.pop()]

    while True:
        player_score = calculate_score(player_cards)
        computer_score = calculate_score(computer_cards)

        print("\nთქვენი კარტები:", player_cards, "ქულა:", player_score)
        print("კომპიუტერის პირველი კარტა:", computer_cards[0])

        if player_score > 21:
            print("თქვენ წააგეთ (გადააჭარბეთ 21-ს)")
            return

        choice = input("აირჩიე add ან stop: ")

        if choice == "add":
            player_cards.append(deck.pop())
        elif choice == "stop":
            break

    while calculate_score(computer_cards) < 17:
        computer_cards.append(deck.pop())

    player_score = calculate_score(player_cards)
    computer_score = calculate_score(computer_cards)

    print("\nთქვენი კარტები:", player_cards, "ქულა:", player_score)
    print("კომპიუტერის კარტები:", computer_cards, "ქულა:", computer_score)

    if computer_score > 21 or player_score > computer_score:
        print("თქვენ მოიგეთ!")
    elif computer_score > player_score:
        print("თქვენ წააგეთ!")
    else:
        print("ფრე — თავიდან ვითამაშოთ!")


play_game()


#=============3 დავალება =================

import logging



logging.basicConfig(
    filename="atm.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)




balance = 500  # ლარი



def show_balance():
    print(f"თქვენი ბალანსია: {balance} ლარი")


def deposit(amount):
    global balance

    if amount > 1000:
        print("ერთჯერადად 1000 ლარზე მეტის შეტანა არ შეიძლება ")
        return

    balance += amount
    logging.info(f"შეტანა: {amount} ლარი")
    print(f"შეტანილია {amount} ლარი")


def withdraw(amount):
    global balance

    if amount > balance:
        print("ანგარიშზე არ არის საკმარისი თანხა ")
        return

    balance -= amount
    logging.info(f"გატანა: {amount} ლარი")
    print(f"გატანილია {amount} ლარი")



while True:
    print("\n--- ATM Machine ---")
    print("1. ბალანსის ნახვა")
    print("2. თანხის შეტანა")
    print("3. თანხის გატანა")
    print("4. გამოსვლა")

    choice = input("აირჩიე ოპერაცია (1-4): ")

    if choice == "1":
        show_balance()

    elif choice == "2":
        amount = int(input("შეიყვანე შესატანი თანხა (ლარი): "))
        deposit(amount)

    elif choice == "3":
        amount = int(input("შეიყვანე გასატანი თანხა (ლარი): "))
        withdraw(amount)

    elif choice == "4":
        print("მადლობა სარგებლობისთვის 👋")
        break


#===============4 დავალება ========================

import random
import logging



JACKPOT = 100_000

PRIZES = {
    6: 1.0,
    5: 0.6,
    4: 0.4,
    3: 0.2
}



logging.basicConfig(
    filename="lottery.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8"
)



def generate_computer_numbers():

    return random.sample(range(1, 50), 6)


def get_player_numbers():

    numbers = set()

    while len(numbers) < 6:
        n = int(input(f"შეიყვანე რიცხვი #{len(numbers) + 1} (1-49): "))
        numbers.add(n)

    return list(numbers)



def count_matches(computer, player):

    return len(set(computer) & set(player))


def calculate_prize(matches):

    multiplier = PRIZES.get(matches, 0)
    return int(JACKPOT * multiplier)


def show_result(computer, player, matches, prize):

    print("\n  ლატარიის შედეგი ")
    print("კომპიუტერის რიცხვები:", sorted(computer))
    print("შენი რიცხვები:", sorted(player))
    print("დამთხვევები:", matches)
    print("მოგება:", prize)


def log_result(computer, player, matches, prize):

    logging.info(
        f"computer={sorted(computer)} | "
        f"player={sorted(player)} | "
        f"matches={matches} | "
        f"jackpot={JACKPOT} | "
        f"prize={prize}"
    )



def main():
    print(" კეთილი იყოს შენი მობრძანება ლატარიაში ")

    computer_numbers = generate_computer_numbers()
    player_numbers = get_player_numbers()

    matches = count_matches(computer_numbers, player_numbers)
    prize = calculate_prize(matches)

    show_result(computer_numbers, player_numbers, matches, prize)
    log_result(computer_numbers, player_numbers, matches, prize)


if __name__ == "__main__":
    main()

#=======================5 დავალება ======================

import re



EMAIL = "user@mail.com"
NICKNAME = "george777"
PASSWORD = "password123"


NAME_PATTERN = re.compile(r"^[a-z]+$")


def validate_name(name: str) -> list[str]:

    errors: list[str] = []
    s = (name or "").strip()


    if not s:
        return ["სახელი ცარიელია — შეიყვანე მინიმუმ 1 ლათინური პატარა ასო (a-z)."]

    has_digit = any(ch.isdigit() for ch in s)
    has_upper = any("A" <= ch <= "Z" for ch in s)
    has_space = any(ch.isspace() for ch in s)
    has_symbol = any((not ch.isalnum()) and (not ch.isspace()) for ch in s)


    has_non_latin_letter = any(
        ch.isalpha() and not (("a" <= ch <= "z") or ("A" <= ch <= "Z"))
        for ch in s
    )


    if s.isdigit():
        errors.append("შემოყვანილია რიცხვითი მნიშვნელობა — შემოიტანე მხოლოდ string პატარა რეგისტრში (a-z).")

    only_symbols = all((not ch.isalnum()) and (not ch.isspace()) for ch in s)
    if only_symbols:
        errors.append("შემოყვანილია სიმბოლოები — შემოიტანე მხოლოდ string პატარა რეგისტრში (a-z).")

    if has_space:
        errors.append("სახელი არ უნდა შეიცავდეს გამოტოვებებს (space/tab).")

    if has_upper:
        errors.append("შემოყვანილია დიდი ასო(ები) — გამოიყენე მხოლოდ პატარა ასოები (a-z).")

    if has_digit and not s.isdigit():
        errors.append("შემოყვანილია ციფრი(ები) — სახელში დაშვებულია მხოლოდ ასოები (a-z).")

    if has_symbol and not only_symbols:
        errors.append("შემოყვანილია სპეციალური სიმბოლო(ები) — დაშვებულია მხოლოდ ასოები (a-z).")

    if has_non_latin_letter:
        errors.append("შემოყვანილია ლათინურისგან განსხვავებული ასოები — გამოიყენე მხოლოდ ინგლისური ლათინური (a-z).")

    if not NAME_PATTERN.match(s):

        if not errors:
            errors.append("არასწორი ფორმატი — სახელში დაშვებულია მხოლოდ ლათინური პატარა ასოები (a-z).")

    return errors


def main():
    print("=== რეგისტრაცია ===")
    print(f"ელ-ფოსტა: {EMAIL}")
    print(f"ზედმეტსახელი: {NICKNAME}")
    print(f"პაროლი: {PASSWORD}")
    print("შეიყვანე მხოლოდ სახელი (ლათინური პატარა ასოები a-z)\n")

    while True:
        name = input("სახელი: ")

        errors = validate_name(name)
        if not errors:

            name = name.strip()

            print("\n✅ წარმატებით დარეგისტრირდი! შენახული მონაცემები:")
            print(f"ელ-ფოსტა: {EMAIL}")
            print(f"სახელი: {name}")
            print(f"ზედმეტსახელი: {NICKNAME}")
            print(f"პაროლი: {PASSWORD}")
            break


        print("\n შეყვანა არასწორია. დაფიქსირდა:")
        for i, msg in enumerate(errors, 1):
            print(f"{i}) {msg}")
        print("სცადე კიდევ ერთხელ.\n")


if __name__ == "__main__":
    main()

