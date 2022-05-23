import requests
import random

names = ["Jan", "Kamil", "Marian", "Pawel", "Piotr", "Szymon", "Lukasz", "Sebastian", "Wojciech", "Eryk",
         "Karolina", "Monika", "Katarzyna", "Krystyna", "Kamila", "Kasia", "Kornelia", "Klaudia"]

MAX_USERS = 200
REGISTER_URL = "http://localhost:5001/signup"

if __name__ == '__main__':
    for i in range(MAX_USERS):
        request_body = {
            "name": names[i % len(names)],
            "login": names[i % len(names)].lower()+str(random.randint(10000, 99999)),
            "password1": "pswd",
            "password2": "pswd"
        }

        response = requests.post(REGISTER_URL, json=request_body)



