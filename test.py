
sentence = input("შემოიყვანე წინადადება: ").strip()

# სიტყვებად გაყოფა
words = sentence.split()

# ფუნქცია: წმენდა — ვაძლევთ მხოლოდ ასოებს
def clean_word(word):
    # შეგროვდება მხოლოდ ის სიმბოლოები, რომელთა isalpha() == True
    return "".join(ch for ch in word if ch.isalpha())

# ქმნით შედეგის dictionary-ს:
result = {}
for w in words:
    cw = clean_word(w)
    if cw:
        result[cw] = len(cw)

print("\nResult:", result)



