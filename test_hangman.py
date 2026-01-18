from hangman import play_hangman


def test_win_game():
    result = play_hangman("python", ["p", "y", "t", "h", "o", "n"])
    assert result == "თქვენ გამოიცანით სიტყვა"


def test_lose_game():
    result = play_hangman("python", ["a", "b", "c", "d", "e", "f"])
    assert result == "თქვენ დამარცხდით"
