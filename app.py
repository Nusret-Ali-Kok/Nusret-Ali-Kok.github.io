from flask import Flask, render_template, request
import json
import os
from llm import API_call_chat
from dotenv import load_dotenv
load_dotenv()
from linkify import linkify_response
from flask import session

app = Flask(__name__)
app.secret_key = "supersupersupersecretkey"  # replace with a random secure string

def load_experiences():
    experience_folder = "experiences"
    experiences = []

    for filename in os.listdir(experience_folder):
        if filename.endswith(".json"):
            with open(os.path.join(experience_folder, filename), "r") as f:
                experience = json.load(f)
                # Create a URL-safe slug from title
                slug = experience["title"].lower().replace(" ", "-")
                experience["slug"] = slug
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



@app.route("/experience/<exp_id>")
def experience_detail(exp_id):
    experiences = load_experiences()
    for exp in experiences:
        if exp["id"] == exp_id:
            return render_template("experience.html", exp=exp)
    return "Experience not found", 404



from flask import session, request, render_template

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "chat_history" not in session:
        session["chat_history"] = []

    user_input = ""
    bot_response = ""

    if request.method == "POST":
        user_input = request.form.get("message")
        api_key = os.environ.get("OPENROUTER_API_KEY")

        if not api_key:
            bot_response = "API key is missing. Please set OPENROUTER_API_KEY."
        else:
            # Load experiences and format them
            experiences = load_experiences()
            experience_texts = "\n\n".join(
                f"Title: {exp['title']}\nDescription: {exp['description']}\nTags: {', '.join(exp['tags'])}\nURL: /experience/{exp['id']}"
                for exp in experiences
            )

            # Append user's message to history
            session["chat_history"].append({"role": "user", "content": user_input})

            # Prepare messages for the LLM API: add system prompt + chat history
            messages = [
                {
                    "role": "system",
                    "content": f"""
                    You are an intelligent chatbot that helps potential employers learn about a candidate through interactive conversation.

                    Below is a list of the candidate's actual experiences, with titles, descriptions, and tags. Your job is to:
                    - Understand the employer's questions
                    - Identify the most relevant experiences based on content and tags
                    - Present them in a friendly, clear way
                    - Link to the relevant experience pages if helpful

                    Only use the experiences provided below to answer. Don’t make up new details.

                    Candidate's experiences:
                    {experience_texts}

                    Respond in a conversational tone. Don't write a formal letter — just talk like a helpful assistant who's very familiar with the candidate's past work.
                    """
                }
            ] + session["chat_history"]  # add full conversation history

            try:
                # Call API with chat messages instead of just a single prompt
                bot_response = API_call_chat(messages, api_key)  # You will create this function next
            except Exception as e:
                bot_response = str(e)

            bot_response = linkify_response(bot_response)

            # Append bot's response to chat history
            session["chat_history"].append({"role": "assistant", "content": bot_response})

            # Save session changes
            session.modified = True

    return render_template("chat.html", user_input=user_input, bot_response=bot_response, chat_history=session.get("chat_history", []))

if __name__ == "__main__":
    app.run(debug=True)