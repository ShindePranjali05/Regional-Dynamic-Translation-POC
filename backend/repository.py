import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="patient_translation_db",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
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

def insert_translation(entity_type, entity_id, field_name, original_text, translated_text, language_code, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO translations 
        (entity_type, entity_id, field_name, original_text, translated_text, language_code, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
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