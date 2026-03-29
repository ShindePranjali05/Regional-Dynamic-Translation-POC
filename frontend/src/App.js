import React, { useState } from "react";
import AdviceForm from "./components/AdviceForm";
import TranslationDisplay from "./components/TranslationDisplay";
import { submitAndTranslate, saveTranslations } from "./services/api";

export default function App() {
  const [formData, setFormData] = useState({
    patient_id: "",
    nutrition_advice: "",
    exercise_advice: "",
    injury_care_advice: "",
    target_language: "hi"
  });

  const [translations, setTranslations] = useState({});
  const [entityId, setEntityId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleSubmit = async () => {
    if (
      !formData.patient_id ||
      !formData.nutrition_advice ||
      !formData.exercise_advice ||
      !formData.injury_care_advice
    ) {
      alert("Please fill all fields");
      return;
    }

    setLoading(true);
    try {
      const res = await submitAndTranslate(formData);

      if (res.error) {
        alert(res.error);
        return;
      }

      setEntityId(res.entity_id);
      setTranslations(res.translations || {});
    } catch (err) {
      alert("Translation failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!entityId) {
      alert("No translated record found to save");
      return;
    }

    const payload = {
      entity_type: "patient_advice",
      entity_id: entityId,
      language_code: formData.target_language,
      translations: {}
    };

    for (const key in translations) {
      payload.translations[key] = {
        original_text: formData[key],
        translated_text: translations[key]
      };
    }

    setSaving(true);
    try {
      const res = await saveTranslations(payload);

      if (res.error) {
        alert(res.error);
        return;
      }

      alert("Saved successfully.");
    } catch (err) {
      alert("Save failed");
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "500px",
        margin: "auto",
        padding: "40px",
        background: "#f5f5f5",
        minHeight: "100vh"
      }}
    >
      <AdviceForm
        formData={formData}
        setFormData={setFormData}
        onSubmit={handleSubmit}
        loading={loading}
      />

      {Object.keys(translations).length > 0 && (
        <TranslationDisplay
          translations={translations}
          setTranslations={setTranslations}
          formData={formData}
          onSave={handleSave}
          saving={saving}
        />
      )}
    </div>
  );
}