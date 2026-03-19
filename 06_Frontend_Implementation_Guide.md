# 🎨 Frontend Implementation Guide: Dynamic Translation System (POC)

---

## 🎯 Objective

This document explains how to build the frontend for:

* Submitting form data
* Displaying translated output
* Allowing user verification
* Saving translations

---

## 🧩 Tech Stack (Flexible)

* React (recommended) / Vanilla JS
* Axios / Fetch for API calls

---

## 📁 Suggested Component Structure

```id="fe-structure"
src/
│
├── components/
│   ├── AdviceForm.jsx
│   ├── TranslationDisplay.jsx
│
├── services/
│   └── api.js
│
└── App.jsx
```

---

## 🧱 Components Overview

---

### 1️⃣ AdviceForm Component

### 📌 Responsibilities:

* Capture user input
* Call submit API

---

### 📌 Fields:

```id="form-fields"
nutrition_advice
exercise_advice
injury_care_advice
target_language
```

---

### 📌 Example UI (Conceptual)

```
Nutrition Advice: [__________]
Exercise Advice:  [__________]
Injury Care:      [__________]

Language: [Hindi ▼]

[Submit]
```

---

### 📌 Submit Logic

```javascript id="submit-logic"
async function handleSubmit() {
    const response = await api.submitAndTranslate(formData);

    setEntityId(response.entity_id);
    setTranslations(response.translations);
}
```

---

---

### 2️⃣ TranslationDisplay Component

---

### 📌 Responsibilities:

* Show translated text
* Allow user to edit
* Save translations

---

### 📌 Example UI

```
Nutrition Advice:
Original: Eat more protein
Translated: [अधिक प्रोटीन खाएं]

Exercise Advice:
Original: Walk daily
Translated: [रोज़ चलें]

[Save Translations]
```

---

## 🧠 State Management

---

### Required State

```javascript id="state"
const [formData, setFormData] = useState({});
const [translations, setTranslations] = useState({});
const [entityId, setEntityId] = useState(null);
const [loading, setLoading] = useState(false);
```

---

## 🔄 API Integration

---

### 📌 API Service

```javascript id="api-service"
export async function submitAndTranslate(data) {
    const res = await fetch("/api/submit-and-translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    return res.json();
}
```

---

### 📌 Save Translations API

```javascript id="save-api"
export async function saveTranslations(payload) {
    const res = await fetch("/api/save-translations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    return res.json();
}
```

---

## 💾 Save Translations Logic

```javascript id="save-logic"
async function handleSave() {
    const payload = {
        entity_type: "patient_advice",
        entity_id: entityId,
        language_code: formData.target_language,
        translations: {}
    };

    for (const field in translations) {
        payload.translations[field] = {
            original_text: formData[field],
            translated_text: translations[field]
        };
    }

    await api.saveTranslations(payload);
    alert("Saved successfully");
}
```

---

## ⏳ Loading State

---

### 📌 During Translation

```javascript id="loading"
setLoading(true);
await submitAndTranslate();
setLoading(false);
```

---

### UI Example

```
[Submit]

Loading translations...
```

---

## ✏️ Editable Translations

---

### Allow user to modify:

```javascript id="edit-translation"
<input
  value={translations.nutrition_advice}
  onChange={(e) =>
    setTranslations({
      ...translations,
      nutrition_advice: e.target.value
    })
  }
/>
```

---

## ⚠️ Important Rules

---

### ✅ 1. Do not auto-save translations

User must click "Save"

---

### ✅ 2. Always store entity_id

Needed for saving translations

---

### ✅ 3. Handle null translations

If API fails for a field, show:

```
Translation failed. Please retry.
```

---

### ✅ 4. Keep UI simple

No need for styling complexity

---

## 🧪 Basic Flow

```id="fe-flow"
User fills form
→ Click Submit
→ API call
→ Show translations
→ User edits (optional)
→ Click Save
→ API call to save
```

---

## 🚀 Summary

Frontend should:

* Collect input
* Call backend
* Display translations
* Allow edits
* Save verified translations

---

