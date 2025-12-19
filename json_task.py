# 1 დავალება


import json

json_data = """
[
    {"id": 1, "price": 50},
    {"id": 2, "price": 200},
    {"id": 3, "price": 150}
]
"""


products = json.loads(json_data)

expensive_products = [product for product in products if product["price"] > 100]


print("ძვირი პროდუქტები (ფასი > 100):")
for item in expensive_products:
    print(f"ID: {item['id']}, ფასი: {item['price']}")


# 2 დავალება

import json

json_data = """
{
  "company": {
    "departments": [
      {
        "name": "IT",
        "employees": [
          {"name": "Ana"},
          {"name": "Beka"}
        ]
      },
      {
        "name": "HR",
        "employees": [
          {"name": "Nino"}
        ]
      }
    ]
  }
}
"""

data = json.loads(json_data)

names = []

for department in data["company"]["departments"]:

    for employee in department["employees"]:
        names.append(employee["name"])

print(names)


#3 დავალება

import json


json_data = """
[
  {"name": "Ana", "grades": [90, 80, 95]},
  {"name": "Beka", "grades": [70, 85, 88]},
  {"name": "Nino", "grades": [100, 95, 99]}
]
"""


students = json.loads(json_data)

best_student = None
best_average = 0

for student in students:
    grades = student["grades"]
    average = sum(grades) / len(grades)

    if average > best_average:
        best_average = average
        best_student = student["name"]

print(f"საუკეთესო სტუდენტია: {best_student}")
print(f"საშუალო ქულა: {best_average}")

# 4 დავალება

import json

json_data = """
{
  "companies": [
    {
      "name": "TechCorp",
      "employees": [
        {"name": "Ana", "salary": 3000},
        {"name": "Beka", "salary": 4500}
      ]
    },
    {
      "name": "SoftPlus",
      "employees": [
        {"name": "Nino", "salary": 5000},
        {"name": "Giorgi", "salary": 2500}
      ]
    }
  ]
}
"""
data = json.loads(json_data)


for company in data["companies"]:
    company_name = company["name"]

    for employee in company["employees"]:
        if employee["salary"] > 4000:
            print(f"{employee['name']} - {company_name}")



# 5 დავალება


import requests

response = requests.get("https://jsonplaceholder.typicode.com/users")

data = response.json()

print(data[0]["name"])

# 6 დავალება

import requests

url = "https://jsonplaceholder.typicode.com/posts"

new_post = {
    "title": "Test",
    "body": "Hello World",
    "userId": 5
}

response = requests.post(url, json=new_post)

if response.status_code == 201:
    print("პოსტი წარმატებით შეიქმნა!")
    print(response.json())
else:
    print("შეცდომა:", response.status_code)


# 7 დავალება

import requests

url = "https://jsonplaceholder.typicode.com/todos"

try:

    response = requests.get(url)
    response.raise_for_status()

    todos = response.json()

    print(" შეუსრულებელი TODO ამოცანები:")
    for task in todos:
        if task["completed"] is False:
            print(f"ID: {task['id']} | {task['title']}")

except Exception as e:
    print("შეცდომა:", e)




# 8 დავალება
import requests


POSTS_URL = "https://jsonplaceholder.typicode.com/posts"
USERS_URL = "https://jsonplaceholder.typicode.com/users"

try:
    #GET posts and users
    posts_response = requests.get(POSTS_URL)
    users_response = requests.get(USERS_URL)

    posts_response.raise_for_status()
    users_response.raise_for_status()

    posts = posts_response.json()
    users = users_response.json()

    # Create dict: userId -> user name
    users_dict = {user["id"]: user["name"] for user in users}

    # 3. Print first 5 posts
    print(" პირველი 5 პოსტი და მათი ავტორები:\n")
    for post in posts[:5]:
        title = post["title"]
        author_id = post["userId"]
        author_name = users_dict.get(author_id, "Unknown Author")

        print(f"{title} – {author_name}")

except requests.exceptions.RequestException as e:
    print("შეცდომა მონაცემების წამოღებისას:", e)

