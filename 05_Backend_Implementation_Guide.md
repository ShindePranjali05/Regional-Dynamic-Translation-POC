# ⚙️ Backend Implementation Guide: Dynamic Translation System (POC)

---

## 🎯 Objective

This document provides a **step-by-step guide** to implement the backend.

It includes:

* Folder structure
* Core logic
* Translation integration
* Pseudocode for all major flows

---

## 🧩 Recommended Tech Stack (Flexible)

* Language: Node.js / Python (either is fine)
* Framework: Express (Node) / FastAPI (Python)
* Database: PostgreSQL / MySQL

---

## 📁 Suggested Folder Structure

```id="structure"
backend/
│
├── controllers/
│   └── translationController.js
│
├── services/
│   ├── translationService.js
│   └── sarvamService.js
│
├── repositories/
│   ├── patientAdviceRepo.js
│   └── translationRepo.js
│
├── routes/
│   └── translationRoutes.js
│
├── utils/
│   └── logger.js
│
└── app.js
```

---

## 🧠 High-Level Flow

```id="flow"
Controller → Service → External API → Service → Controller → Response
```

---

# 1️⃣ Submit + Translate Flow

---

## 📌 Controller Logic

```javascript id="controller-submit"
async function submitAndTranslate(req, res) {
    const {
        patient_id,
        nutrition_advice,
        exercise_advice,
        injury_care_advice,
        target_language
    } = req.body;

    // Step 1: Save original data
    const entityId = await patientAdviceRepo.create({
        patient_id,
        nutrition_advice,
        exercise_advice,
        injury_care_advice
    });

    // Step 2: Call translation service
    const translations = await translationService.translateFields({
        nutrition_advice,
        exercise_advice,
        injury_care_advice
    }, target_language);

    // Step 3: Return response
    return res.json({
        entity_id: entityId,
        translations
    });
}
```

---

# 2️⃣ Translation Service

---

## 📌 Core Logic

```javascript id="translation-service"
async function translateFields(fields, targetLanguage) {
    const result = {};

    for (const key in fields) {
        const text = fields[key];

        if (!text) continue;

        try {
            const translated = await sarvamService.translate(text, targetLanguage);
            result[key] = translated;
        } catch (error) {
            result[key] = null;
        }
    }

    return result;
}
```

---

## 🧠 Key Points

* Loop through each field
* Call API per field
* Handle failures gracefully

---

# 3️⃣ Sarvam API Integration

---

## 📌 Example Wrapper

```javascript id="sarvam-service"
async function translate(text, targetLanguage) {
    const response = await fetch("SARVAM_API_URL", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_API_KEY"
        },
        body: JSON.stringify({
            input: text,
            target_language: targetLanguage
        })
    });

    const data = await response.json();

    return data.translated_text;
}
```

---

## ⚠️ Important

* Do NOT call Sarvam directly from controller
* Always go through service layer

---

# 4️⃣ Save Translations Flow

---

## 📌 Controller Logic

```javascript id="save-controller"
async function saveTranslations(req, res) {
    const { entity_type, entity_id, language_code, translations } = req.body;

    for (const field in translations) {
        const { original_text, translated_text } = translations[field];

        await translationRepo.create({
            entity_type,
            entity_id,
            field_name: field,
            original_text,
            translated_text,
            language_code,
            status: "verified"
        });
    }

    return res.json({ message: "Translations saved successfully" });
}
```

---

# 5️⃣ Repository Layer

---

## 📌 Example: Insert Translation

```javascript id="repo-code"
async function createTranslation(data) {
    // Insert into translations table
    // Use parameterized query or ORM
}
```

---

## 🧠 Responsibility

* Only DB operations
* No business logic

---

# 6️⃣ Error Handling

---

## ⚠️ Cases to Handle

### 1. Translation API fails

* Return partial data
* Do not crash API

---

### 2. Empty fields

* Skip translation

---

### 3. Duplicate entries

* Handle DB unique constraint error

---

## 📌 Example

```javascript id="error-handling"
try {
    // DB insert
} catch (err) {
    if (err.code === "UNIQUE_CONSTRAINT") {
        throw new Error("Duplicate translation");
    }
}
```

---

# 7️⃣ Logging (Basic)

---

## 📌 Log These

* API request received
* Translation API response
* Errors

---

```javascript id="logging"
console.log("Translating:", text);
console.error("Translation failed:", error);
```

---

# 8️⃣ Important Rules

---

### ✅ 1. Always save original data first

---

### ✅ 2. Never block on full failure

* Return partial translations if needed

---

### ✅ 3. One API call per field

---

### ✅ 4. Keep services reusable

---

# 🚀 Summary

Backend should:

* Save original data
* Translate field-by-field
* Return results
* Save verified translations

---

