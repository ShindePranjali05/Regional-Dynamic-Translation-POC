from flask import Flask, request, jsonify
from flask_cors import CORS
from repository import insert_patient_advice, insert_translation, get_patient_advice_by_id

app = Flask(__name__)
CORS(app)

@app.route("/health")
def health():
    return {"status": "OK"}

@app.route("/")
def home():
    return "Server is running"

@app.route('/submit-and-translate', methods=['POST'])
def submit_and_translate():
    data = request.json

    patient_id = data.get("patient_id")
    nutrition = data.get("nutrition_advice")
    exercise = data.get("exercise_advice")
    injury_care = data.get("injury_care_advice")

    entity_id = insert_patient_advice(
        patient_id, nutrition, exercise, injury_care
    )

    return jsonify({
        "entity_id": entity_id,
        "translations": {
            "nutrition_advice": "dummy",
            "exercise_advice": "dummy",
            "injury_care_advice": "dummy"
        }
    })

@app.route('/save-translations', methods=['POST'])
def save_translations():
    data = request.json

    entity_type = data.get("entity_type")
    entity_id = data.get("entity_id")
    language_code = data.get("language_code")
    translations = data.get("translations")

    patient_advice = get_patient_advice_by_id(entity_id)

    if not patient_advice:
        return jsonify({"error": "Patient advice not found"}), 404

    original_data = {
        "nutrition_advice": patient_advice[2],
        "exercise_advice": patient_advice[3],
        "injury_care_advice": patient_advice[4]
    }

    for field_name, translated_text in translations.items():
        original_text = original_data.get(field_name)

        insert_translation(
            entity_type,
            entity_id,
            field_name,
            original_text,
            translated_text,
            language_code,
            "draft"
        )

    return jsonify({
        "message": "Translations saved successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)