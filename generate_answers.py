import csv
import requests
import time

API_URL = "http://localhost:8000/generate"

with open("test_questions.csv", newline="", encoding="utf-8") as infile, \
     open("wonderbot_outputs.csv", "w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=["question", "answer"])
    writer.writeheader()
    for row in reader:
        topic = row["question"]
        try:
            resp = requests.post(API_URL, data={"topic": topic, "age": 7})
            resp.raise_for_status()
            answer = resp.json().get("outputs", {}).get("text", "")
        except Exception as e:
            answer = f"[ERROR] {e}"
        writer.writerow({"question": topic, "answer": answer})
        time.sleep(1)  # avoid rate limits 