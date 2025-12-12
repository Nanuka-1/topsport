# 3 დავალება
import random

user_input = input("დაწერე ერთი სიტყვა: ")

if len(user_input.split()) != 1:
    print("მხოლოდ ერთი სიტყვა უნდა შეიყვანო!")
    exit()

def generate_scrambled_versions(word):
    letters = list(word)
    generated = set()

    while len(generated) < 5:
        random.shuffle(letters)
        new_word = "".join(letters)

        if new_word not in generated:
            generated.add(new_word)
            yield new_word

scrambles = generate_scrambled_versions(user_input)

for s in scrambles:
    print(s)


# 4 დავალება

user_input = input("შეიყვანე რიცხვები space-ებით: ")

numbers = [int(n) for n in user_input.split()]

# Sorting-ის ვარიანტები
print("\nაირჩიე როგორ დავალაგო რიცხვები:")
print("1 - ზრდადობით")
print("2 - კლებადობით")
print("3 - random-ად არევა")
print("4 - მხოლოდ უნიკალური მნიშვნელობები")

choice = input("შენი არჩევანი: ")

# არჩევანი
if choice == "1":
    result = sorted(numbers)
elif choice == "2":
    result = sorted(numbers, reverse=True)
elif choice == "3":
    import random
    result = numbers[:]      # ვაკოპირებთ, რომ პირვანდელი სია არ შეიცვალოს
    random.shuffle(result)
elif choice == "4":
    result = list(set(numbers))
else:
    result = "არასწორი არჩევანი!"

print("\nშედეგი:", result)


#5 დავალება


sentence = input("შემოიყვანე ტექსტი: ")

# ვტოვებთ მხოლოდ ასოებს და space-ს
filtered_chars = [ch for ch in sentence if ch.isalpha() or ch.isspace()]

# ვაერთიანებთ ასოებად
filtered_sentence = "".join(filtered_chars)

print("გაფილტრული ტექსტი:", filtered_sentence)

