🏗️ System Architecture: Dynamic Translation System (POC)

---

🎯 Objective

This document explains how different parts of the system interact:

- Frontend (UI)
- Backend (API server)
- Translation Service (Sarvam AI)
- Database

The goal is to clearly understand the end-to-end data flow.

---

🧩 High-Level Components

[Frontend]  →  [Backend API]  →  [Database]
                         ↓
                 [Translation Service]
                         ↓
                    [Sarvam AI API]

---

🔹 Component Breakdown

1. Frontend (UI)

Responsible for:

- Taking user input (form)
- Displaying translated output
- Allowing user to verify/edit
- Sending API requests to backend

---

2. Backend (API Server)

Responsible for:

- Receiving form data
- Saving original data
- Calling translation service
- Returning translated data
- Saving verified translations

---

3. Translation Service (Internal Layer)

This is a wrapper layer inside backend.

Responsible for:

- Sending text to Sarvam API
- Receiving translated text
- Handling errors/retries

---

4. Sarvam AI API (External Service)

Responsible for:

- Translating text from one language to another

---

5. Database

Responsible for storing:

- Original data (patient advice)
- Translations (linked to original data)

---

🔄 End-to-End Flow (Detailed)

Step 1: User fills the form on frontend

Step 2: Frontend sends POST request to backend
        → /submit-form

Step 3: Backend:
        - Validates input
        - Saves original data in DB

Step 4: Backend triggers translation:
        - Calls Translation Service
        - Sends each field separately to Sarvam API

Step 5: Sarvam API returns translated text

Step 6: Backend sends translated data back to frontend

Step 7: Frontend displays translated fields

Step 8: User reviews and optionally edits translations

Step 9: User clicks "Save Translation"

Step 10: Frontend sends POST request:
         → /save-translation

Step 11: Backend saves translations in DB

---

⚙️ Sync vs Async Behavior

Current POC Approach (Simple Sync Flow)

Submit Form → Backend → Call Translation API → Return Response

- Translation happens immediately after submission
- User waits for response

---

Why This Is OK for POC

- Simpler to implement
- Easier to debug
- No need for queues/background jobs

---

Future (Not in Scope)

In production, this could become async:

- Background jobs
- Message queues
- Retry systems

---

🧠 Field-Level Translation Flow

We DO NOT send the entire form as one block.

Instead:

For each field:
   send text → translation API → get result

Example:

nutrition_advice → translate
exercise_advice → translate
injury_care_advice → translate

---

✅ Why This Approach?

- Easier debugging
- Better control
- Prevents mapping issues
- Allows partial retries

---

🔌 API Interaction Overview

1. Submit Form API

Frontend → Backend:

`{
  "nutrition_advice": "...",
  "exercise_advice": "...",
  "injury_care_advice": "...",
  "target_language": "hi"
}`

---

2. Translation Happens Internally

Backend:

TranslationService.translate(text, target_language)

---

3. Response to Frontend

`{
  "translations": {
    "nutrition_advice": "...",
    "exercise_advice": "...",
    "injury_care_advice": "..."
  }
}`

---

4. Save Translation API

Frontend → Backend:

`{
  "entity_id": "123",
  "translations": {
    "nutrition_advice": "...",
    "exercise_advice": "..."
  },
  "language": "hi"
}`

---

🗃️ Data Flow Summary

User Input
   ↓
Frontend
   ↓
Backend API
   ↓
Database (Original Data Saved)
   ↓
Translation Service
   ↓
Sarvam API
   ↓
Backend
   ↓
Frontend (Display Translation)
   ↓
User Verification
   ↓
Backend API
   ↓
Database (Translations Saved)
---

⚠️ Important Design Decisions

1. Original Data is Always Saved First

- Never depend on translation API to store data

---

2. Translation is NOT Auto-Saved

- Requires user verification

---

3. Translations are Stored Separately

- Keeps data clean and scalable

---

4. Field-Level Mapping is Mandatory

- Avoids ambiguity in data

---

🧱 Error Handling (High-Level)

Possible Failures:

- Translation API fails
- Partial translation fails
- Invalid input

---

Expected Behavior:

- Original data should still be saved
- Failed translations should be shown as errors
- User should be able to retry

---

🚀 Summary

This architecture ensures:

- Clean separation of concerns
- Easy debugging and maintenance
- Clear data traceability
- Simple implementation for POC

---

