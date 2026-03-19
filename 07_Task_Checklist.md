# ✅ Task Checklist

---

## 🎯 Objective

This checklist provides a **step-by-step plan (3 weeks)** to complete the Dynamic Translation System POC.

Follow this sequentially. Do NOT skip steps.

---

## 🗓️ Overall Timeline

* Week 1 → Setup + Database + Basic APIs
* Week 2 → Translation Integration + Backend Completion
* Week 3 → Frontend + End-to-End Integration

---

# 📅 WEEK 1: Foundation (Setup + Database + Basic Backend)

---

## ✅ Day 1: Project Setup

### Tasks:

* Setup backend project (Node.js / Python)
* Setup frontend project (React or simple HTML)
* Setup database (PostgreSQL / MySQL)

---

### Deliverables:

* Backend server running
* Frontend app running
* Database connected

---

### How to Verify:

* Backend: `GET /health` returns OK
* Frontend loads in browser
* DB connection successful

---

---

## ✅ Day 2: Database Implementation

### Tasks:

* Create `patient_advice` table
* Create `translations` table
* Add unique constraint

---

### Deliverables:

* Tables created successfully

---

### How to Verify:

* Run SQL queries
* Insert dummy data manually

---

---

## ✅ Day 3: Basic Backend API (No Translation Yet)

### Tasks:

* Create API: `POST /submit-and-translate`
* Save data into `patient_advice`
* Return dummy response

---

### Example Dummy Response:

```json
{
  "entity_id": 1,
  "translations": {
    "nutrition_advice": "dummy",
    "exercise_advice": "dummy"
  }
}
```

---

### Deliverables:

* API saves data correctly

---

### How to Verify:

* Use Postman
* Check DB entries

---

---

## ✅ Day 4: Repository Layer

### Tasks:

* Implement DB functions:

  * insert patient advice
  * insert translation

---

### Deliverables:

* Clean DB abstraction layer

---

### How to Verify:

* Call functions directly
* Check DB

---

---

## ✅ Day 5: Save Translations API (Basic)

### Tasks:

* Create API: `/save-translations`
* Insert into `translations` table

---

### Deliverables:

* API working with static data

---

### How to Verify:

* Send sample payload
* Check DB

---

---

# 📅 WEEK 2: Translation Integration + Backend Completion

---

## ✅ Day 6: Sarvam API Setup

### Tasks:

* Get API key
* Test API using Postman

---

### Deliverables:

* Able to translate a single string

---

### How to Verify:

* Input → output translation works

---

---

## ✅ Day 7: Translation Service

### Tasks:

* Create `translationService`
* Create `sarvamService`

---

### Deliverables:

* Function: `translate(text, language)`

---

### How to Verify:

* Call function manually
* Check output

---

---

## ✅ Day 8: Field-Level Translation

### Tasks:

* Implement loop for translating each field

---

### Deliverables:

* Function returns translated object

---

### Example:

```json
{
  "nutrition_advice": "...",
  "exercise_advice": "..."
}
```

---

---

## ✅ Day 9: Integrate Translation in API

### Tasks:

* Connect translation service to `/submit-and-translate`

---

### Deliverables:

* API returns real translations

---

### How to Verify:

* Test with Postman

---

---

## ✅ Day 10: Error Handling

### Tasks:

* Handle API failures
* Handle empty fields
* Handle partial failures

---

### Deliverables:

* API does not crash on errors

---

---

## ✅ Day 11: Save Translations (Final)

### Tasks:

* Integrate real translation data
* Add status = verified

---

### Deliverables:

* Proper DB entries

---

---

# 📅 WEEK 3: Frontend + Integration

---

## ✅ Day 12: Basic Form UI

### Tasks:

* Create form inputs
* Add submit button

---

### Deliverables:

* UI renders correctly

---

---

## ✅ Day 13: Submit API Integration

### Tasks:

* Call `/submit-and-translate`
* Store response in state

---

### Deliverables:

* Translations received in frontend

---

---

## ✅ Day 14: Display Translations

### Tasks:

* Show translated fields below form

---

### Deliverables:

* Clear UI display

---

---

## ✅ Day 15: Editable Translations

### Tasks:

* Allow user to edit translated text

---

### Deliverables:

* Editable input fields

---

---

## ✅ Day 16: Save Translations API Integration

### Tasks:

* Call `/save-translations`

---

### Deliverables:

* Data saved from frontend

---

---

## ✅ Day 17: Loading + UX Improvements

### Tasks:

* Add loading states
* Handle errors in UI

---

---

## ✅ Day 18: End-to-End Testing

### Tasks:

* Full flow test:

  * Submit
  * Translate
  * Edit
  * Save

---

---

## ✅ Day 19–21: Buffer + Debugging

### Tasks:

* Fix bugs
* Clean code
* Improve readability

---

---

# ⚠️ Common Mistakes (Read Carefully)

---

### ❌ Sending full JSON for translation

✔️ Always translate field-by-field

---

### ❌ Not storing original_text

✔️ Always store it

---

### ❌ Duplicate translations

✔️ Respect unique constraint

---

### ❌ Skipping error handling

✔️ Handle API failures

---

# 🧠 When to Ask for Help

Ask for help if:

* API not working at all
* DB errors unclear

---

# 🚀 Final Deliverable

By end of Week 3, system should:

* Accept form input
* Translate data
* Display translations
* Allow edits
* Save verified translations
* Store everything correctly in DB

---

## ✅ Completion Checklist

* [ ] Backend APIs working
* [ ] Translation API integrated
* [ ] Frontend working
* [ ] End-to-end flow complete
* [ ] No major bugs

---

