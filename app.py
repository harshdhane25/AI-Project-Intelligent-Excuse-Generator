from flask import Flask, render_template, request, url_for, session
import random
import os
from proof_generator import generate_fake_proof
from datetime import datetime
from googletrans import Translator
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = "your-secret-key"
translator = Translator()

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

translations = {
    'en': {
        'excuse_header': "Excuse Generator",
        'excuse_intro': "Make your absence legendary 💌",
        'choose_scenario': "Choose a scenario:",
        'generate_excuse': "🎲 Generate Excuse",
        'apology_link': "Need to apologize? Generate a guilt-tripping apology 💔",
        'work': "Work",
        'school': "School",
        'social': "Social",
        'family': "Family",
        'history': "History",
        'favorites': "Favorites",
        'your_excuse': "Your Excuse:",
        'fake_proof': "Proof:",
        'top_excuses': "Top Excuses:",
        'prediction': "Prediction: Based on your history, you may need your next excuse on:",
        'play_excuse': "▶️ Play Excuse"
    },
    'es': {
        'excuse_header': "Generador de Excusas",
        'excuse_intro': "Haz que tu ausencia sea legendaria 💌",
        'choose_scenario': "Elige un escenario:",
        'generate_excuse': "🎲 Generar Excusa",
        'apology_link': "¿Necesitas disculparte? Genera una disculpa emocional 💔",
        'work': "Trabajo",
        'school': "Escuela",
        'social': "Social",
        'family': "Familia",
        'history': "Historial",
        'favorites': "Favoritos",
        'your_excuse': "Tu excusa:",
        'fake_proof': "Prueba:",
        'top_excuses': "Principales excusas:",
        'prediction': "Predicción: Según tu historial, podrías necesitar tu próxima excusa el:",
        'play_excuse': "▶️ Reproducir excusa"
    },
    'fr': {
        'excuse_header': "Générateur d'Excuses",
        'excuse_intro': "Rendez votre absence légendaire 💌",
        'choose_scenario': "Choisissez un scénario :",
        'generate_excuse': "🎲 Générer une excuse",
        'apology_link': "Besoin de vous excuser ? Générer une excuse pleine de culpabilité 💔",
        'work': "Travail",
        'school': "École",
        'social': "Social",
        'family': "Famille",
        'history': "Historique",
        'favorites': "Favoris",
        'your_excuse': "Votre excuse:",
        'fake_proof': "Preuve:",
        'top_excuses': "Meilleures excuses:",
        'prediction': "Prévision : Basé sur votre historique, vous pourriez avoir besoin de votre prochaine excuse le:",
        'play_excuse': "▶️ Lire l'excuse"
    },
    'hi': {
        'excuse_header': "बहाना जनरेटर",
        'excuse_intro': "अपनी गैरमौजूदगी को यादगार बनाएं 💌",
        'choose_scenario': "एक स्थिति चुनें:",
        'generate_excuse': "🎲 बहाना जनरेट करें",
        'apology_link': "माफी मांगनी है? एक दिल छू लेने वाली माफी जनरेट करें 💔",
        'work': "काम",
        'school': "स्कूल",
        'social': "सामाजिक",
        'family': "परिवार",
        'history': "इतिहास",
        'favorites': "पसंदीदा",
        'your_excuse': "आपका बहाना:",
        'fake_proof': "सबूत:",
        'top_excuses': "शीर्ष बहाने:",
        'prediction': "भविष्यवाणी: आपके इतिहास के आधार पर, अगला बहाना आपको इस दिन ज़रूरत पड़ सकती है:",
        'play_excuse': "▶️ बहाना सुनें"
    },
    'te': {
        'excuse_header': "నెపం జనరేటర్",
        'excuse_intro': "మీ గైర్హాజరును చరిత్రలో నిలుపుకోండి 💌",
        'choose_scenario': "ఒక పరిస్థిని ఎంచుకోండి:",
        'generate_excuse': "🎲 నెపం తయారు చేయండి",
        'apology_link': "క్షమాపణ చెప్పాలా? మర్మమైన క్షమాపణను రూపొందించండి 💔",
        'work': "పని",
        'school': "పాఠశాల",
        'social': "సామాజిక",
        'family': "కుటుంబం",
        'history': "చరిత్ర",
        'favorites': "ఇష్టమైనవి",
        'your_excuse': "మీ నెపం:",
        'fake_proof': "ఆధారం:",
        'top_excuses': "అగ్ర నెపాలు:",
        'prediction': "అంచనా: మీ చరిత్ర ఆధారంగా, మీకు వచ్చే నెపం అవసరం అయ్యే రోజు:",
        'play_excuse': "▶️ నెపం వినండి"
    }
}

excuse_proofs = {
    "Work": [
        ("I'm feeling unwell and didn’t want to risk spreading anything.", "proof6.jpg"),
        ("There was an unexpected power outage at my place.", "proof5.jpg"),
        ("My internet went down just before the meeting.", "proof4.jpg"),
        ("I had to handle a family emergency this morning.", "proof13.jpg")
    ],
    "School": [
        ("I had a doctor's appointment that ran longer than expected.", "proof6.jpg"),
        ("My younger sibling was sick and I had to take care of them.", "proof9.jpg"),
        ("There was a transportation strike in my area.", "proof2.jpg"),
        ("I lost track of time while working on another assignment.", "proof12.jpg")
    ],
    "Social": [
        ("I wasn't feeling mentally up to socializing today.", "proof1.jpg"),
        ("My pet had a small emergency and needed my attention.", "proof3.jpg"),
        ("I got caught up in work and lost track of time.", "proof4.jpg"),
        ("There was a last-minute family gathering I couldn’t skip.", "proof8.jpg")
    ],
    "Family": [
        ("I was helping a relative with a medical emergency.", "proof13.jpg"),
        ("There was an issue at home that needed my immediate attention.", "proof9.jpg"),
        ("I was caught up in an important family conversation.", "proof9.jpg"),
        ("We had an unexpected visitor I couldn’t leave unattended.", "proof10.jpg")
    ]
}

apology_templates = {
    "Work": [
        "I'm truly sorry for missing work. It wasn’t my intention to let anyone down.",
        "I know how important today was — please believe that I deeply regret not being there.",
        "Work matters to me, and I feel awful that I couldn’t show up when it mattered most."
    ],
    "School": [
        "I take full responsibility for not being present. I'm deeply sorry to my classmates and teachers.",
        "I hate that I let this happen — I’ll do everything I can to make it right.",
        "It’s not an excuse, just a sincere apology. I hope I can earn back your trust."
    ],
    "Family": [
        "I never meant to let the family down. I hope you know how bad I feel.",
        "Please forgive me — I value our time together and hate that I missed it.",
        "Family means the world to me. I’m genuinely sorry for my absence."
    ],
    "Social": [
        "I was really looking forward to it. I’m so sorry I couldn’t make it.",
        "I feel like I let everyone down — I hope you can understand.",
        "Please know I regret not showing up — it wasn’t intentional."
    ]
}

def rank_excuses(excuse_proof_list):
    ranked = []
    for excuse, proof in excuse_proof_list:
        score = 0
        if "emergency" in excuse.lower():
            score += 5
        if "doctor" in excuse.lower() or "medical" in excuse.lower():
            score += 4
        if "internet" in excuse.lower():
            score += 3
        if "transport" in excuse.lower() or "power outage" in excuse.lower():
            score += 2
        if "family" in excuse.lower():
            score += 1
        ranked.append((score, (excuse, proof)))
    ranked.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in ranked]

def predict_next_excuse_time(history):
    from collections import Counter
    from datetime import timedelta

    if not history:
        return "No data to predict."
    
    valid_entries = [entry for entry in history if isinstance(entry, dict) and "timestamp" in entry]
    if not valid_entries:
        return "No valid history entries."

    times = [datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S") for entry in valid_entries]
    days_of_week = [time.weekday() for time in times]
    common_day = Counter(days_of_week).most_common(1)[0][0]
    today = datetime.now()
    days_until_next = (common_day - today.weekday()) % 7
    predicted_date = today + timedelta(days=days_until_next)
    avg_hour = sum(time.hour for time in times) / len(times)
    predicted_time = predicted_date.replace(hour=int(avg_hour), minute=0, second=0, microsecond=0)
    return predicted_time.strftime("%A, %Y-%m-%d at %I:%M %p")

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_language = request.form.get('language') or request.args.get('lang') or 'en-US'
    lang_code = selected_language.split('-')[0]
    language_dict = translations.get(lang_code, translations['en'])

    if "history" not in session:
        session["history"] = []
    if "favorites" not in session:
        session["favorites"] = []

    excuse = None
    proof = None
    proof_label = ""
    top_3_excuses = []

    if request.method == 'POST':
        scenario = request.form.get('scenario')
        urgency = request.form.get('urgency')
        selected_language = request.form.get('language', 'en-US')

        if scenario in excuse_proofs:
            all_excuses_proofs = excuse_proofs[scenario]
            ranked_excuses_proofs = rank_excuses(all_excuses_proofs)
            top_3_excuses_proofs = ranked_excuses_proofs[:3]
            if top_3_excuses_proofs:
                selected_excuse, selected_proof_filename = random.choice(top_3_excuses_proofs)
            else:
                selected_excuse, selected_proof_filename = ranked_excuses_proofs[0]
            excuse = selected_excuse
            top_3_excuses = [exc for exc, proof in ranked_excuses_proofs[:3]]

            # Handle proof upload
            if 'proof_image' in request.files and request.files['proof_image'].filename != '':
                file = request.files['proof_image']
                ext = os.path.splitext(file.filename)[1]
                filename = str(uuid.uuid4()) + ext
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                proof = url_for('static', filename=f'uploads/{filename}')
                is_fake = random.choice(["fake", "real"])
                proof_label = f"This proof is likely {is_fake}"
            else:
                proof = url_for('static', filename=f'proofs/{selected_proof_filename}')
                proof_label = ""

            # Translate excuse if not English
            target_lang = selected_language.split('-')[0]
            if target_lang != 'en':
                try:
                    translation = translator.translate(excuse, dest=target_lang)
                    excuse = translation.text
                except Exception as e:
                    print("Translation error:", e)

            # Save to history
            session["history"].append({
                "excuse": excuse,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            session.modified = True

    predicted_schedule = predict_next_excuse_time(session.get("history", []))
    return render_template('index.html', excuse=excuse, proof=proof, proof_label=proof_label,
                           selected_language=selected_language, language_dict=language_dict,
                           top_excuses=top_3_excuses, predicted_schedule=predicted_schedule)

@app.route("/history")
def history():
    lang = request.args.get('lang', 'en')
    language_dict = translations.get(lang, translations['en'])
    return render_template("history.html", history=session.get("history", []),
                           favorites=session.get("favorites", []), language_dict=language_dict)

@app.route("/favorite", methods=["POST"])
def favorite():
    excuse = request.form.get("excuse")
    if excuse and excuse not in session["favorites"]:
        session["favorites"].append(excuse)
        session.modified = True
    return url_for("history")

@app.route('/apology', methods=['GET', 'POST'])
def apology():
    apology_message = None
    proof = None
    lang = request.args.get('lang', 'en')
    language_dict = translations.get(lang, translations['en'])

    if request.method == 'POST':
        scenario = request.form.get('scenario')
        urgency = request.form.get("urgency")
        tone = request.form.get('tone')
        if scenario in apology_templates:
            apology_message = random.choice(apology_templates[scenario])
            proof = generate_fake_proof(urgency)

    return render_template('apology.html', apology=apology_message, proof=proof, language_dict=language_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)