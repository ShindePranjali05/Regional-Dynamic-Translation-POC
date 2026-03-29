import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


def insert_patient_advice(patient_id, nutrition, exercise, injury_care):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patient_advice
        (patient_id, nutrition_advice, exercise_advice, injury_care_advice)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """, (patient_id, nutrition, exercise, injury_care))

    entity_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return entity_id


def upsert_translation(entity_type, entity_id, field_name, original_text, translated_text, language_code, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO translations
        (entity_type, entity_id, field_name, original_text, translated_text, language_code, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (entity_type, entity_id, field_name, language_code)
        DO UPDATE SET
            original_text = EXCLUDED.original_text,
            translated_text = EXCLUDED.translated_text,
            status = EXCLUDED.status;
    """, (
        entity_type,
        entity_id,
        field_name,
        original_text,
        translated_text,
        language_code,
        status
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_patient_advice_by_id(entity_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, patient_id, nutrition_advice, exercise_advice, injury_care_advice
        FROM patient_advice
        WHERE id = %s;
    """, (entity_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row

def find_existing_patient_advice(patient_id, nutrition, exercise, injury_care):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, patient_id, nutrition_advice, exercise_advice, injury_care_advice
        FROM patient_advice
        WHERE patient_id = %s
          AND nutrition_advice = %s
          AND exercise_advice = %s
          AND injury_care_advice = %s
        ORDER BY id DESC
        LIMIT 1;
    """, (patient_id, nutrition, exercise, injury_care))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row