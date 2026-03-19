# 🗃️ Database Design: Dynamic Translation System (POC)

---

## 🎯 Objective

This document defines:

* Database tables
* Field structures
* Relationships
* Constraints

The goal is to ensure:

* Every translation is **traceable**
* Every translation is linked to:

  * The correct record
  * The correct field
  * The original text

---

## 🧩 Overview of Tables

We will use **2 main tables**:

```id="tables-overview"
1. patient_advice   → stores original data
2. translations     → stores translated data
```

---

## 🧱 Table 1: `patient_advice`

### 📌 Purpose:

Stores the **original user input**

---

### 🧾 Schema

```sql id="patient-advice-schema"
CREATE TABLE patient_advice (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER,

    nutrition_advice TEXT,
    exercise_advice TEXT,
    injury_care_advice TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 🧠 Field Explanation

| Field              | Description                 |
| ------------------ | --------------------------- |
| id                 | Unique record ID            |
| patient_id         | Identifier for patient      |
| nutrition_advice   | Original nutrition advice   |
| exercise_advice    | Original exercise advice    |
| injury_care_advice | Original injury care advice |
| created_at         | Record creation time        |
| updated_at         | Last update time            |

---

## 🧱 Table 2: `translations`

### 📌 Purpose:

Stores **translated text** with full traceability

---

### 🧾 Schema

```sql id="translations-schema"
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,

    entity_type VARCHAR(50),     -- e.g. 'patient_advice'
    entity_id INTEGER,           -- FK to patient_advice.id

    field_name VARCHAR(100),     -- e.g. 'nutrition_advice'

    original_text TEXT,
    translated_text TEXT,

    language_code VARCHAR(10),   -- e.g. 'hi', 'mr', 'ta'

    status VARCHAR(20),          -- 'draft', 'verified'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔗 Relationships

```id="relationship"
patient_advice.id  →  translations.entity_id
```

---

### Example Mapping

```id="mapping-example"
patient_advice:
id = 1

translations:
entity_id = 1
field_name = 'nutrition_advice'
```

---

## 🧠 Why This Design?

### ✅ 1. Field-Level Mapping

Each translation is stored separately:

```id="field-mapping"
nutrition_advice → one row
exercise_advice → one row
```

---

### ✅ 2. Supports Multiple Languages

```id="multi-language"
Same field → multiple language entries
```

Example:

* nutrition_advice → Hindi
* nutrition_advice → Marathi

---

### ✅ 3. Full Traceability

Each row stores:

* original_text
* translated_text
* field_name
* entity reference

---

### ✅ 4. Extensible

Later you can add:

* more fields
* more entities (not just patient_advice)

---

## 🔐 Constraints (VERY IMPORTANT)

Add this unique constraint:

```sql id="unique-constraint"
UNIQUE (entity_type, entity_id, field_name, language_code)
```

---

### 🧠 Why?

Prevents duplicate translations like:

❌ Same field translated twice for same language

---

## 🧪 Sample Data

---

### 🧾 patient_advice

```json id="sample-patient"
{
  "id": 1,
  "patient_id": 101,
  "nutrition_advice": "Eat more protein",
  "exercise_advice": "Walk daily",
  "injury_care_advice": "Apply ice"
}
```

---

### 🌐 translations

```json id="sample-translation"
[
  {
    "entity_type": "patient_advice",
    "entity_id": 1,
    "field_name": "nutrition_advice",
    "original_text": "Eat more protein",
    "translated_text": "अधिक प्रोटीन खाएं",
    "language_code": "hi",
    "status": "verified"
  },
  {
    "entity_type": "patient_advice",
    "entity_id": 1,
    "field_name": "exercise_advice",
    "original_text": "Walk daily",
    "translated_text": "रोज़ चलें",
    "language_code": "hi",
    "status": "verified"
  }
]
```

---

## 🔄 Data Lifecycle

```id="lifecycle"
1. User submits form
2. Data stored in patient_advice
3. Translation generated
4. User verifies
5. Data stored in translations
```

---

## ⚠️ Important Rules

### 1. NEVER overwrite original data

* Always keep original intact

---

### 2. ALWAYS store original_text in translations

* Even though it's in parent table

---

### 3. One row per field per language

* Do NOT store JSON blobs

---

### 4. Use consistent field_name values

* Must match column names exactly

---

## 🚀 Summary

This database design ensures:

* Clean separation of original vs translated data
* Easy querying and debugging
* Support for multiple languages
* Strong data traceability

---

👉 Move to next document: **04_API_Contracts.md**
