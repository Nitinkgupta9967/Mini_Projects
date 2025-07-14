import html
import json
import random
import requests
from dotenv import load_dotenv

load_dotenv()

while True:
    try:
        parameters = {
            "amount": 10,
            "type": "boolean"
        }
        response = requests.get("https://opentdb.com/api.php", params=parameters)
        response.raise_for_status()
        data = response.json()

        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

        question_no = random.randint(0, 9)
        question_data = data["results"][question_no]
        question = html.unescape(question_data["question"])
        correct_answer = question_data["correct_answer"].upper()

        print("\nQuestion:", question)
        ans = input("Answer (True/False or 'exit' to quit): ").strip().upper()

        if ans == "EXIT":
            print("Exiting quiz. Goodbye!")
            break

        if ans == correct_answer:
            print("✅ Correct!\n")
        else:
            print(f"❌ Incorrect. The correct answer was: {correct_answer}\n")

    except Exception as e:
        print("An error occurred:", e)
        break