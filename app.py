from flask import Flask, render_template
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
    experiences = load_experiences()
    return render_template("index.html", experiences=experiences)

if __name__ == "__main__":
    app.run(debug=True)
