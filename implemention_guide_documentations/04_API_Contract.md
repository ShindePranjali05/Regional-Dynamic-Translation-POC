# 🔌 API Contracts: Dynamic Translation System (POC)

---

## 🎯 Objective

This document defines all backend APIs required for the system.

For each API, we will specify:

* Endpoint
* Method
* Request format
* Response format
* Example payloads

---

## 🧩 API Overview

We will implement **3 main APIs**:

```
1. Submit Form + Get Translation
2. Save Verified Translations
3. Get Translations (Optional - for testing)
```

---

# 1️⃣ Submit Form + Get Translation

---

## 📌 Endpoint

```
POST /api/submit-and-translate
```

---

## 📥 Request Body

```json
{
  "patient_id": 101,
  "nutrition_advice": "Eat more protein",
  "exercise_advice": "Walk daily",
  "injury_care_advice": "Apply ice",
  "target_language": "hi"
}
```

---

## ⚙️ Backend Responsibilities

* Validate input
* Save original data in `patient_advice`
* Call translation service for each field
* Return translated output

---

## 📤 Response Body

```json
{
  "entity_id": 1,
  "translations": {
    "nutrition_advice": "अधिक प्रोटीन खाएं",
    "exercise_advice": "रोज़ चलें",
    "injury_care_advice": "बर्फ लगाएं"
  }
}
```

---

## ⚠️ Error Response

```json
{
  "error": "Translation failed for some fields",
  "details": {
    "exercise_advice": "API timeout"
  }
}
```

---

# 2️⃣ Save Verified Translations

---

## 📌 Endpoint

```
POST /api/save-translations
```

---

## 📥 Request Body

```json
{
  "entity_type": "patient_advice",
  "entity_id": 1,
  "language_code": "hi",
  "translations": {
    "nutrition_advice": {
      "original_text": "Eat more protein",
      "translated_text": "अधिक प्रोटीन खाएं"
    },
    "exercise_advice": {
      "original_text": "Walk daily",
      "translated_text": "रोज़ चलें"
    }
  }
}
```

---

## ⚙️ Backend Responsibilities

* Validate entity exists
* Loop through each field
* Insert into `translations` table
* Ensure no duplicates (use unique constraint)

---

## 📤 Response Body

```json
{
  "message": "Translations saved successfully"
}
```

---

## ⚠️ Error Response

```json
{
  "error": "Duplicate translation exists"
}
```

---

# 3️⃣ Get Translations (Optional)

---

## 📌 Endpoint

```
GET /api/translations?entity_id=1&language=hi
```

---

## 📤 Response Body

```json
{
  "entity_id": 1,
  "language": "hi",
  "translations": {
    "nutrition_advice": "अधिक प्रोटीन खाएं",
    "exercise_advice": "रोज़ चलें"
  }
}
```

---

## 🧠 Notes

* This API is useful for testing and debugging
* Not mandatory for POC

---

# 🔁 API Flow Summary

```
Frontend → /submit-and-translate
        → Backend saves original data
        → Backend calls translation API
        → Returns translations

Frontend → /save-translations
        → Backend stores verified translations
```

---

# ⚠️ Important Implementation Rules

---

## 1. Field Names Must Match DB Columns

```
nutrition_advice
exercise_advice
injury_care_advice
```

---

## 2. Do NOT send entire JSON for translation

Instead:

* Translate each field separately

---

## 3. Always return entity_id

Frontend needs it to save translations later

---

## 4. Handle Partial Failures

If one field fails:

* Return others
* Include error details

---

# 🚀 Summary

These APIs enable:

* End-to-end flow from input → translation → verification → storage
* Clean separation of responsibilities
* Easy frontend integration

---


