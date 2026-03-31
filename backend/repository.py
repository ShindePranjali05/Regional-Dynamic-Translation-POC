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
    conn = None
    cursor = None

    try:
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
        return entity_id

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error inserting patient advice:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def upsert_translation(entity_type, entity_id, field_name, original_text, translated_text, language_code, status):
    conn = None
    cursor = None

    try:
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
        return True

    except Exception as e:
        if conn:
            conn.rollback()
        print("Error upserting translation:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_patient_advice_by_id(entity_id):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, patient_id, nutrition_advice, exercise_advice, injury_care_advice
            FROM patient_advice
            WHERE id = %s;
        """, (entity_id,))

        row = cursor.fetchone()
        return row

    except Exception as e:
        print("Error fetching patient advice by id:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def find_existing_patient_advice(patient_id, nutrition, exercise, injury_care):
    conn = None
    cursor = None

    try:
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
        return row

    except Exception as e:
        print("Error finding existing patient advice:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()