📘 Project Overview: Dynamic Translation System (POC)

---

🎯 Objective

The goal of this project is to build a Proof of Concept (POC) for a system that can:

1. Accept user-inputted data (patient advice)
2. Dynamically translate the data into a selected regional language
3. Allow the user to review and verify the translation
4. Store both:
   - Original data
   - Verified translated data
     in a structured and traceable way in the database

---

🧠 Why Are We Building This?

In real-world healthcare applications, users (patients/doctors) may prefer different regional languages.

This system ensures:

- Users can input data in one language (e.g., English)
- The system translates it into another language (e.g., Hindi, Marathi)
- The translated content is reviewed before saving
- All translations are properly linked to the original data

---

🧩 Example Use Case

A doctor fills out a form for a patient:

- Nutrition Advice → "Eat more protein and vegetables"
- Exercise Advice → "Walk for 30 minutes daily"
- Injury Care Advice → "Apply ice twice a day"

The system should:

1. Save this original data
2. Translate each field into a selected language (e.g., Hindi)
3. Show translated output to the user
4. Allow user to verify/edit
5. Save translations in database with proper mapping

---

🔄 High-Level Flow

Step 1: User fills form (Frontend)

Step 2: Form is submitted → Backend API

Step 3: Backend saves original data in DB

Step 4: Backend sends text to Translation API (Sarvam AI)

Step 5: Translated text is returned

Step 6: Frontend displays translated output

Step 7: User verifies/edits translation

Step 8: User clicks "Save Translation"

Step 9: Translations are stored in DB with proper references

---

🏗️ What Are We Building in This POC?

✅ Included:

- Simple form UI
- Backend APIs
- Integration with Sarvam AI translation API
- Database to store:
  - Original data
  - Translations
- Verification step before saving translations

---

❌ Not Included (Out of Scope for POC):

- Performance optimization
- Scaling for large traffic
- Caching mechanisms
- Multi-user concurrency handling
- Authentication/authorization

---

🧱 Key Concepts

1. Original Data

The data entered by the user (stored immediately after form submission)

---

2. Translation

The converted version of the original data in another language

---

3. Field-Level Translation

Each field is translated separately:

- nutrition_advice → translated
- exercise_advice → translated
- injury_care_advice → translated

---

4. Verification Step

Translations are not saved immediately
User must:

- Review
- Optionally edit
- Click "Save"

---

5. Traceability (Very Important)

Every translation must:

- Be linked to:
  - Exact record (patient advice)
  - Exact field (nutrition/exercise/etc.)
- Store original text alongside translated text

---

🗃️ Expected Final Output

Frontend:

- Form submission UI
- Translated output displayed clearly
- Save button for translations

---

Backend:

- APIs for:
  - Saving original data
  - Translating data
  - Saving verified translations

---

Database:

- One table for original data
- One table for translations
- Proper mapping between them

---

🧪 Example Output (Simplified)

Original Data:

{
  "nutrition_advice": "Eat more protein",
  "exercise_advice": "Walk daily"
}

Translated Data (Hindi):

{
  "nutrition_advice": "अधिक प्रोटीन खाएं",
  "exercise_advice": "रोज़ चलें"
}

---

✅ Success Criteria

The POC is considered complete when:

- [ ] User can submit form data
- [ ] Original data is saved in DB
- [ ] Translation API is successfully called
- [ ] Translated data is displayed on UI
- [ ] User can verify/edit translation
- [ ] Verified translations are saved in DB
- [ ] Each translation is correctly linked to original data

---

🚀 Summary

This project demonstrates how to build a dynamic, traceable, and user-verified translation system that can be extended in the future for:

- Multiple languages
- Real-time translation
- Large-scale applications

---

👉 
