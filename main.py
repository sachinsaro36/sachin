from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        interest TEXT,
        skill TEXT,
        subject TEXT,
        career TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()



@app.route("/")
def home():
    return render_template("index.html")



def predict_career(interest, skill, subject):

    # Priority: SKILL > SUBJECT > INTEREST

    if subject == "computer science":
        if skill == "design":
            return "UI/UX Designer"
        elif skill == "programming":
            return "Software Developer"
        else:
            return "IT Specialist"

    elif subject == "arts":
        if skill == "design":
            return "Graphic Designer"
        return "Creative Artist"

    elif subject == "math":
        if skill == "programming":
            return "Data Scientist"
        return "Statistician"

    elif subject == "biology":
        return "Doctor"

    elif subject == "commerce":
        if skill == "communication":
            return "Marketing Manager"
        return "Business Analyst"

    return "Career Counselor"



@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        interest = data.get("interest", "").lower()
        skill = data.get("skill", "").lower()
        subject = data.get("subject", "").lower()

        if not interest or not skill or not subject:
            return jsonify({"career": "Please provide complete details"})

        # 🔥 Prediction
        career = predict_career(interest, skill, subject)

        # 🔥 SAVE TO DATABASE
        conn = sqlite3.connect("career.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users (interest, skill, subject, career)
        VALUES (?, ?, ?, ?)
        """, (interest, skill, subject, career))

        conn.commit()
        conn.close()

        return jsonify({"career": career})

    except Exception as e:
        print("Error:", e)
        return jsonify({"career": "Something went wrong"})



if __name__ == "__main__":
    app.run(debug=True)