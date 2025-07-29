from flask import Flask, render_template, request, session
import warnings

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Needed for session support
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Web route
@app.route("/", methods=["GET", "POST"])
def chat():
    global mood
    if request.method == "GET":
        session.clear()
        session["history"] = []
        session["step"] = 1
        session["name"] = ""
        bot_msg = "I am your emotional support guide, what is your name?"
        session["history"].append(("bot", bot_msg))


    if request.method == "POST":
        name_input = request.form.get("name", "").strip()
        message_input = request.form.get("message", "").strip()

        if session["step"] == 1 and name_input:
            session["name"] = name_input
            bot_msg = f"How are you feeling today?"
            session["history"].append(("user", name_input))
            session["history"].append(("bot", bot_msg))
            session["step"] = 2

        elif session["step"] == 2 and message_input:
            session["history"].append(("user", message_input))
            bot_msg = "What has made you feel this way?"
            session["history"].append(("bot", bot_msg))
            session["step"] = 3

        elif session["step"] == 3 and message_input:
            session["history"].append(("user", message_input))
            bot_msg = "Have you got anything planned today?"
            session["history"].append(("bot", bot_msg))
            session["step"] = 4

        elif session["step"] == 4 and message_input:
            session["history"].append(("user", message_input))
            bot_msg = "Got it"
            session["history"].append(("bot", bot_msg))
            bot_msg = "Your daily check in has concluded."
            session["history"].append(("bot", bot_msg))
            session["step"] = 5

    return render_template("index.html", history=session["history"], step=session["step"], name=session["name"])

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
