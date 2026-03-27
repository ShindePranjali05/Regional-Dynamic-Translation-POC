import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from repository import (
    insert_patient_advice,
    insert_translation,
    get_patient_advice_by_id
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
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        patient_id = data.get("patient_id")
        nutrition = data.get("nutrition_advice")
        exercise = data.get("exercise_advice")
        injury_care = data.get("injury_care_advice")
        target_language_code = data.get("target_language_code", "hi-IN")

        if not patient_id:
            return jsonify({
                "success": False,
                "error": "patient_id is required"
            }), 400

        if not any([nutrition, exercise, injury_care]):
            return jsonify({
                "success": False,
                "error": "At least one advice field is required"
            }), 400

        entity_id = insert_patient_advice(
            patient_id,
            nutrition,
            exercise,
            injury_care
        )

        fields_data = {
            "nutrition_advice": nutrition,
            "exercise_advice": exercise,
            "injury_care_advice": injury_care
        }

        translated_fields = translation_service.translate_fields(
            fields_data,
            "en-IN",
            target_language_code
        )

        for field_name, translated_text in translated_fields.items():
            original_text = fields_data.get(field_name)

            if original_text:
                insert_translation(
                    "patient_advice",
                    entity_id,
                    field_name,
                    original_text,
                    translated_text,
                    target_language_code,
                    "verified"
                )

        return jsonify({
            "success": True,
            "message": "Patient advice saved and translated successfully",
            "entity_id": entity_id,
            "translations": translated_fields
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Submit and translate failed: {str(e)}"
        }), 500


@app.route("/save-translations", methods=["POST"])
def save_translations():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        entity_type = data.get("entity_type")
        entity_id = data.get("entity_id")
        language_code = data.get("language_code")
        translations = data.get("translations")

        if not entity_type or not entity_id or not language_code or not translations:
            return jsonify({
                "success": False,
                "error": "entity_type, entity_id, language_code, and translations are required"
            }), 400

        patient_advice = get_patient_advice_by_id(entity_id)

        if not patient_advice:
            return jsonify({
                "success": False,
                "error": "Patient advice not found"
            }), 404

        original_data = {
            "nutrition_advice": patient_advice[2],
            "exercise_advice": patient_advice[3],
            "injury_care_advice": patient_advice[4]
        }

        for field_name, translated_text in translations.items():
            original_text = original_data.get(field_name)

            if original_text:
                insert_translation(
                    entity_type,
                    entity_id,
                    field_name,
                    original_text,
                    translated_text,
                    language_code,
                    "verified"
                )

        return jsonify({
            "success": True,
            "message": "Translations saved successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Save translations failed: {str(e)}"
        }), 500


@app.route("/test-translate", methods=["POST"])
def test_translate():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        input_text = data.get("text")
        source_language_code = data.get("source_language_code", "en-IN")
        target_language_code = data.get("target_language_code", "hi-IN")

        if not input_text:
            return jsonify({
                "success": False,
                "error": "text is required"
            }), 400

        translated_text = translation_service.translate_text(
            input_text,
            source_language_code,
            target_language_code
        )

        return jsonify({
            "success": True,
            "input_text": input_text,
            "translated_text": translated_text,
            "model": "sarvam-translate:v1"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Translation failed: {str(e)}"
        }), 500


@app.route("/test-translate-fields", methods=["POST"])
def test_translate_fields():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400

        source_language_code = data.get("source_language_code", "en-IN")
        target_language_code = data.get("target_language_code", "hi-IN")

        fields_data = {
            "nutrition_advice": data.get("nutrition_advice"),
            "exercise_advice": data.get("exercise_advice"),
            "injury_care_advice": data.get("injury_care_advice")
        }

        if not any(fields_data.values()):
            return jsonify({
                "success": False,
                "error": "At least one advice field is required"
            }), 400

        translated_fields = translation_service.translate_fields(
            fields_data,
            source_language_code,
            target_language_code
        )

        return jsonify({
            "success": True,
            "translated_fields": translated_fields
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Field translation failed: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)