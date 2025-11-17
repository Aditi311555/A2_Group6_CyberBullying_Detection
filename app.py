from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import pickle
import os
import traceback
from werkzeug.security import generate_password_hash, check_password_hash
import speech_recognition as sr
from googletrans import Translator

# ===== OCR imports =====
import pytesseract
from PIL import Image

# ===== Apriori Imports =====
import pandas as pd
import emoji
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# ===== Additional Imports =====
import re
from symspellpy import SymSpell, Verbosity  # SymSpell for obfuscated text correction

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret_in_production"

DB_PATH = "cyberbully.db"
VECT_PATH = "vectorizer.pkl"
MODEL_PATH = "LinearSVCTuned.pkl"
BULLY_LIMIT = 10

# ====== Load ML classifier ======
if not os.path.exists(VECT_PATH) or not os.path.exists(MODEL_PATH):
    print("ERROR: Model/vectorizer missing!")
    raise SystemExit(1)

try:
    with open(VECT_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception:
    traceback.print_exc()
    raise SystemExit(1)

# ====== Leetspeak Normalize Map ======
LEET_MAP = str.maketrans({
    "1": "i",
    "!": "i",
    "@": "a",
    "$": "s",
    "5": "s",
    "0": "o",
    "3": "e",
    "7": "t"
})

# ====== SymSpell Setup for Obfuscated Word Correction ======
sym_spell = SymSpell(max_dictionary_edit_distance=2)
PROFANITY_ROOTS = ["fuck", "shit", "kill", "bitch", "stupid", "dumb", "ugly", "idiot", "die", "asshole", "slut"]
for word in PROFANITY_ROOTS:
    sym_spell.create_dictionary_entry(word, 10000)  # Add common abusive root words

def normalize_word(word):
    cleaned = re.sub(r"[^a-zA-Z]", "", word)  # Remove *, #, @, etc.
    suggestions = sym_spell.lookup(cleaned, Verbosity.CLOSEST, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term
    return word

def normalize_text(text):
    t = text.lower()
    t = t.translate(LEET_MAP)
    words = t.split()
    normalized = [normalize_word(w) for w in words]
    return " ".join(normalized)

# ====== ML Model Prediction ======
def predict_is_bullying(text: str) -> bool:
    t = (text or "").strip()
    if t == "":
        return False
    t = normalize_text(t)
    X = vectorizer.transform([t])
    return bool(model.predict(X)[0] == 1)

# ===== Database Connection =====
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ======== APRIORI EMOJI DETECTION =========
emoji_training_data = [
    ["lol you look stupid 🖕🏻💀", "bullying"],
    ["haha you failed 💀💀🖕🏻", "bullying"],
    ["you are useless 🤬😡", "bullying"],
    ["shut up 🤬🤬", "bullying"],
    ["nice photo 😊", "not_bullying"],
    ["great work 👏🔥", "not_bullying"],
    ["happy birthday 🎉🥳", "not_bullying"]
]

def extract_emojis(text):
    return [ch for ch in text if ch in emoji.EMOJI_DATA]

df = pd.DataFrame(emoji_training_data, columns=["comment", "label"])
df["emojis"] = df["comment"].apply(extract_emojis)

bully_emoji_lists = df[df["label"] == "bullying"]["emojis"].tolist()
te = TransactionEncoder()
te_data = te.fit(bully_emoji_lists).transform(bully_emoji_lists)
df_encoded = pd.DataFrame(te_data, columns=te.columns_)

frequent_sets = apriori(df_encoded, min_support=0.3, use_colnames=True)
rules = association_rules(frequent_sets, metric="confidence", min_threshold=0.6)
blocked_emoji_sets = [frozenset(row["antecedents"]) for _, row in rules.iterrows()]

def apriori_detect(comment):
    emojis_found = set(extract_emojis(comment))
    for pattern in blocked_emoji_sets:
        if pattern.issubset(emojis_found):
            return True, emojis_found, pattern
    return False, emojis_found, None

# ==========================
# ======== ROUTES ==========
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():
    """Create new user."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return render_template(
                "register.html",
                error="Provide username and password."
            )

        pw_hash = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, pw_hash),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username already taken.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login + session creation."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid credentials.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/clear_comments")
def clear_comments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM comments")
    conn.commit()
    conn.close()
    return "All comments cleared!"


@app.route("/", methods=["GET", "POST"])
def index():
    """Main page: comment posting + bullying detection."""
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()

    # Load current user
    cur.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
    user = cur.fetchone()

    if not user:
        conn.close()
        session.clear()
        return redirect(url_for("login"))

    if user["is_blocked"]:
        conn.close()
        return render_template("blocked.html", username=user["username"])

    message = None
    prediction = None

    # Handle POST
    if request.method == "POST":
        text = request.form.get("text", "").strip()

        # =========== AUDIO PROCESSING ===========
        audio_file = request.files.get("audio")
        if audio_file and audio_file.filename != "":
            temp_path = "temp_upload.wav"
            audio_file.save(temp_path)
            recognizer = sr.Recognizer()
            try:
                with sr.AudioFile(temp_path) as source:
                    audio_data = recognizer.record(source)
                    transcript = recognizer.recognize_google(audio_data)
                    text = (text + " " + transcript).strip()
            except Exception:
                pass
            os.remove(temp_path)

        # =========== IMAGE OCR PROCESSING ===========
        image_file = request.files.get("image")
        if image_file and image_file.filename != "":
            temp_img_path = "temp_upload.png"
            image_file.save(temp_img_path)
            try:
                img = Image.open(temp_img_path)
                extracted_text = pytesseract.image_to_string(img)
                text = (text + " " + extracted_text).strip()
            except Exception:
                pass
            finally:
                os.remove(temp_img_path)

        # ======== TRANSLATION FOR BULLYING DETECTION ONLY ========
        original_text = text  # Preserve Marathi/raw input
        english_text = text  # By default, assume already in English

        if text:
            try:
                translator = Translator()
                detected = translator.detect(text)
                if detected.lang == "mr":  # If Marathi detected
                    english_text = translator.translate(text, src="mr", dest="en").text
            except Exception as e:
                print("Translation error:", e)

        # ======== BULLYING DETECTION LOGIC ========
        if english_text:
            is_bully_ml = predict_is_bullying(english_text)
            apriori_bully, emojis_found, pattern = apriori_detect(english_text)

            is_bully = is_bully_ml or apriori_bully

            if not is_bully:
                cur.execute(
                    "INSERT INTO comments (user_id, comment, prediction) VALUES (?, ?, 0)",
                    (user["id"], original_text),
                )
                conn.commit()
                message = "✅ Comment posted successfully!"
                prediction = 0
            else:
                new_cnt = user["bullying_count"] + 1
                cur.execute(
                    "UPDATE users SET bullying_count=? WHERE id=?",
                    (new_cnt, user["id"])
                )
                conn.commit()

                if apriori_bully:
                    message = f"⚠ Bullying emoji detected"
                else:
                    message = f"⚠ Bullying detected! Warning {new_cnt}/{BULLY_LIMIT}"

                prediction = 1

                if new_cnt >= BULLY_LIMIT:
                    cur.execute(
                        "UPDATE users SET is_blocked=1 WHERE id=?",
                        (user["id"],)
                    )
                    conn.commit()
                    conn.close()
                    return render_template("blocked.html", username=user["username"])

                cur.execute("SELECT * FROM users WHERE id=?", (user["id"],))
                user = cur.fetchone()

    # Load clean comments for display
    cur.execute(
        "SELECT comment, created_at FROM comments WHERE prediction=0 ORDER BY created_at DESC"
    )
    comments = cur.fetchall()
    conn.close()

    return render_template(
        "index.html",
        username=user["username"],
        message=message,
        prediction=prediction,
        bullying_count=user["bullying_count"],
        comments=comments
    )


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("Database not found. Run: python create_db.py")
        raise SystemExit(1)

    print("Starting Flask app...")
    app.run(debug=True, host="127.0.0.1", port=5003)
