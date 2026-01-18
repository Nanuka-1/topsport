import unittest
from logic import Calculator, deposit, withdraw, get_status


# ---------- #1 დავალება ----------

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 3), 12)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)


# ---------- #2 დავალება ----------

class TestBankFunctions(unittest.TestCase):

    def test_correct_balance(self):
        self.assertEqual(deposit(1000, 500), 1500)

    def test_negative_deposit_error(self):
        with self.assertRaises(ValueError):
            deposit(1000, -100)

    def test_withdraw_more_than_balance_error(self):
        with self.assertRaises(ValueError):
            withdraw(1000, 2000)


# ---------- #3 დავალება ----------

class TestGetStatus(unittest.TestCase):

    def test_get_status_success(self):
        data = {"status": "სტატუსი მოიძებნა"}
        self.assertEqual(get_status(data), "სტატუსი მოიძებნა")

    def test_get_status_key_error(self):
        with self.assertRaises(KeyError):
            get_status({})


if __name__ == "__main__":
    unittest.main()
