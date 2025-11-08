from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Create Flask app
app = Flask(__name__)

# ✅ Properly load and use API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")

        if not user_input:
            return jsonify({"reply": "Please type something!"})

        # 💬 Custom personality for your bot
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """
                You are Rynex AI — a friendly, cool, and smart chatbot built by Rynex Edits.
                You specialize in cars, editing, and technology.
                Talk like a confident, helpful assistant who sometimes uses emojis 😎🔥
                Keep your replies short and engaging.
                """},
                {"role": "user", "content": user_input},
            ]
        )

        bot_reply = completion.choices[0].message.content.strip()
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("🔥 Error:", e)
        return jsonify({"reply": f"⚠️ Server Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
