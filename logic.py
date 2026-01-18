# ---------- #1 დავალება ----------

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("0-ზე გაყოფა არ შეიძლება")
        return a / b


# ---------- #2 დავალება ----------

def deposit(balance, amount):
    if amount < 0:
        raise ValueError("უარყოფითი თანხის შეტანა არ შეიძლება")
    return balance + amount


def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("არასაკმარისი ბალანსი")
    return balance - amount


# ---------- #3 დავალება ----------

def get_status(response):
    if "status" in response:
        return response["status"]
    else:
        raise KeyError("შეცდომა, სტატუსი ვერ მოიძებნა")
