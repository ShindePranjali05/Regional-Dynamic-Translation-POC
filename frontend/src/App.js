import React, { useState } from "react";
import AdviceForm from "./components/AdviceForm";
import TranslationDisplay from "./components/TranslationDisplay";
import { submitAndTranslate, saveTranslations } from "./services/api";

export default function App() {
  const [formData, setFormData] = useState({
    nutrition_advice: "",
    exercise_advice: "",
    injury_care_advice: "",
    target_language: "hi"
  });

  const [translations, setTranslations] = useState({});
  const [entityId, setEntityId] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await submitAndTranslate(formData);
      setEntityId(res.entity_id);
      setTranslations(res.translations || {});
    } catch (err) {
      alert("Translation failed");
    }
    setLoading(false);
  };

  const handleSave = async () => {
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

    await saveTranslations(payload);
    alert("Saved successfully ✅");
  };

  return (
    <div style={{maxWidth: "500px", margin: "auto", padding: "40px", background: "#f5f5f5", minHeight: "100vh" }}>

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
        />
      )}
    </div>
  );
}