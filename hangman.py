

def play_hangman(secret_word, guesses):

    if not isinstance(secret_word, str):
        raise ValueError("სიტყვა უნდა იყოს სტრინგი")

    secret_word = secret_word.lower()
    guessed_letters = set()
    attempts_left = 6

    for guess in guesses:

        if not isinstance(guess, str):
            continue

        guess = guess.lower()


        if len(guess) != 1:
            continue

        if guess in secret_word:
            guessed_letters.add(guess)
        else:
            attempts_left -= 1


        if all(letter in guessed_letters for letter in secret_word):
            return "თქვენ გამოიცანით სიტყვა"


        if attempts_left == 0:
            return "თქვენ დამარცხდით"

    return "თამაში გრძელდება"




if __name__ == "__main__":
    word = "python"
    guesses = []

    print(" Hangman თამაში დაიწყო!")
    print("გამოიცანი სიტყვა. გაქვს 6 ცდა.")

    while True:
        letter = input("შეიყვანე ასო: ")
        guesses.append(letter)

        result = play_hangman(word, guesses)
        print("სტატუსი:", result)

        if result in ["თქვენ გამოიცანით სიტყვა", "თქვენ დამარცხდით"]:
            break
