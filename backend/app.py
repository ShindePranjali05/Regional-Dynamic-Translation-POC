import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from repository import (
    insert_patient_advice,
    upsert_translation,
    get_patient_advice_by_id,
    find_existing_patient_advice
)
from services.translation_service import TranslationService

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("SARVAM_API_KEY")
translation_service = TranslationService(api_key)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"}), 200


@app.route("/", methods=["GET"])
def home():
    return "Server is running", 200


@app.route("/submit-and-translate", methods=["POST"])
def submit_and_translate():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        patient_id = data.get("patient_id")
        nutrition = data.get("nutrition_advice")
        exercise = data.get("exercise_advice")
        injury_care = data.get("injury_care_advice")
        target_language = data.get("target_language")

        if not patient_id:
            return jsonify({"error": "patient_id is required"}), 400

        if not target_language:
            return jsonify({"error": "target_language is required"}), 400

        fields_data = {
            "nutrition_advice": nutrition,
            "exercise_advice": exercise,
            "injury_care_advice": injury_care
        }

        existing_record = find_existing_patient_advice(
            patient_id,
            nutrition,
            exercise,
            injury_care
        )

        if existing_record:
            entity_id = existing_record[0]
        else:
            entity_id = insert_patient_advice(
                patient_id,
                nutrition,
                exercise,
                injury_care
            )

        translations = translation_service.translate_fields(
            fields_data,
            source_lang="en-IN",
            target_lang=target_language
        )

        return jsonify({
            "message": "Submitted and translated successfully",
            "entity_id": entity_id,
            "translations": translations
        }), 200

    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500


@app.route("/save-translations", methods=["POST"])
def save_translations():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        entity_type = data.get("entity_type")
        entity_id = data.get("entity_id")
        language_code = data.get("language_code")
        translations = data.get("translations")

        if not entity_type or not entity_id or not language_code or not translations:
            return jsonify({
                "error": "entity_type, entity_id, language_code, and translations are required"
            }), 400

        saved_count = 0

        for field_name, value in translations.items():
            original_text = value.get("original_text")
            translated_text = value.get("translated_text")

            if original_text is None or translated_text is None:
                continue

            upsert_translation(
                entity_type=entity_type,
                entity_id=entity_id,
                field_name=field_name,
                original_text=original_text,
                translated_text=translated_text,
                language_code=language_code,
                status="verified"
            )

            saved_count += 1

        return jsonify({
            "message": "Translations saved successfully",
            "saved_count": saved_count
        }), 200

    except Exception as e:
        return jsonify({"error": f"Save failed: {str(e)}"}), 500


@app.route("/patient-advice/<int:entity_id>", methods=["GET"])
def get_patient_advice(entity_id):
    try:
        row = get_patient_advice_by_id(entity_id)

        if not row:
            return jsonify({"error": "Patient advice not found"}), 404

        return jsonify({
            "id": row[0],
            "patient_id": row[1],
            "nutrition_advice": row[2],
            "exercise_advice": row[3],
            "injury_care_advice": row[4]
        }), 200

    except Exception as e:
        return jsonify({"error": f"Fetch failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)