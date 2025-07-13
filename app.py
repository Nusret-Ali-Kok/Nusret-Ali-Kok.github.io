from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def load_experiences():
    experience_folder = "experiences"
    experiences = []

    for filename in os.listdir(experience_folder):
        if filename.endswith(".json"):
            with open(os.path.join(experience_folder, filename), "r") as f:
                experience = json.load(f)
                experiences.append(experience)

    return experiences

@app.route("/")
def home():
    query = request.args.get("q", "").lower()
    experiences = load_experiences()

    if query:
        experiences = [
            exp for exp in experiences
            if query in exp["title"].lower()
            or query in exp["description"].lower()
            or any(query in tag.lower() for tag in exp["tags"])
        ]

    return render_template("index.html", experiences=experiences, query=query)

if __name__ == "__main__":
    app.run(debug=True)