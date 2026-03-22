# Sarvam AI Translation API Integration Guide

## 🎯 Objective

This document explains how to integrate the **Sarvam AI Translation API** into our backend system to translate patient advice fields dynamically.

---

## 🧠 Overview

We need to:

1. Take original text (nutrition, exercise, injury care)
2. Send it to Sarvam AI API
3. Receive translated text
4. Store it in the `translations` table

---

## 🔗 Step 1: Get API Access

* Visit official docs:
  https://docs.sarvam.ai/api-reference-docs/getting-started/quickstart

* Sign up on Sarvam AI platform

* Generate an **API Key**

👉 This key will be used for authentication

---

## ⚙️ Step 2: Install Required Library

In backend (Flask project):

```bash
pip install requests
```

---

## 🌐 Step 3: API Endpoint

Refer official API reference:
https://docs.sarvam.ai/api-reference-docs

Example translation endpoint:

```text
POST https://api.sarvam.ai/translate
```

---

## 📥 Step 4: Request Format

```json
{
  "input": "Eat fruits",
  "source_language": "en",
  "target_language": "hi"
}
```

---

## 🔐 Headers

```json
{
  "Authorization": "Bearer YOUR_API_KEY",
  "Content-Type": "application/json"
}
```

---

## 📤 Step 5: Response Format

```json
{
  "translated_text": "फल खाओ"
}
```

---

## 🧩 Step 6: Python Integration (Flask)

```python
import requests

API_KEY = "your_api_key"

def translate_text(text, target_lang):
    url = "https://api.sarvam.ai/translate"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": text,
        "source_language": "en",
        "target_language": target_lang
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("translated_text")
    else:
        return None
```

---

## 🔄 Step 7: Integrate with Backend Flow

```python
fields = {
    "nutrition_advice": data["nutrition_advice"],
    "exercise_advice": data["exercise_advice"],
    "injury_care_advice": data["injury_care_advice"]
}

for field_name, text in fields.items():
    translated = translate_text(text, "hi")

    # Insert into translations table
```

---

## 🗄️ Step 8: Store in Database

For each field:

* entity_type → "patient_advice"
* entity_id → record ID
* field_name → field name
* original_text → original text
* translated_text → API output
* language_code → "hi"
* status → "draft"

---

## ⚠️ Error Handling

Handle cases where:

* API fails
* No response
* Rate limits

Example:

```python
if not translated:
    translated = "Translation failed"
```

---

## 🔐 Best Practices

* Do NOT hardcode API key → use `.env`
* Refer auth docs:
  https://docs.sarvam.ai/api-reference-docs/authentication
* Add logging for API calls
* Retry API if it fails
* Validate input before sending

---

## 🚀 Final Flow

1. User submits form
2. Save data in `patient_advice`
3. Call Sarvam API for each field
4. Store results in `translations`
5. Mark status as `draft` or `verified`

---

## 🎯 Summary

* Sarvam API handles translation
* Backend sends request and receives response
* Data stored field-by-field in DB
* System supports multiple languages

---

## 📌 Notes

* Always follow official docs:
  https://docs.sarvam.ai
* Keep API key secure
* Ensure proper error handling in production

---
