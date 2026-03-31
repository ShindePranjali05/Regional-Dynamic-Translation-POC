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
    target_language: "hi-IN"
  });

  const [translations, setTranslations] = useState({});
  const [entityId, setEntityId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState({ type: "", text: "" });

  const isValidPatientId = (id) => {
    return /^[0-9]+$/.test(id);
  };

  const showToast = (type, text, duration = 2500) => {
    setToast({ type, text });
    setTimeout(() => {
      setToast({ type: "", text: "" });
    }, duration);
  };

  const handleSubmit = async () => {
    if (!formData.patient_id) {
      showToast("error", "Patient ID is required");
      return;
    }

    if (!isValidPatientId(formData.patient_id)) {
      showToast("error", "Patient ID should be Integer");
      return;
    }

    if (!formData.target_language) {
      showToast("error", "Please select language");
      return;
    }

    if (
      !formData.nutrition_advice &&
      !formData.exercise_advice &&
      !formData.injury_care_advice
    ) {
      showToast("error", "Please fill at least one advice field");
      return;
    }


    setLoading(true);
    try {
      const res = await submitAndTranslate(formData);

      if (res.error) {
        showToast("error", res.error);
        return;
      }

      setEntityId(res.entity_id);
      setTranslations(res.translations || {});
      showToast("success", "Translations generated successfully ");
    } catch (err) {
      showToast("error", err.message || "Translation failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!entityId) {
      showToast("error", "No translated record found to save");
      return;
    }

    const payload = {
      entity_type: "patient_advice",
      entity_id: entityId,
      language_code: formData.target_language,
      translations: {}
    };

    for (const key in translations) {
      const originalText = formData[key]?.trim();
      const translatedText = translations[key]?.trim();

      if (!originalText || !translatedText) {
        continue;
      }

      payload.translations[key] = {
        original_text: originalText,
        translated_text: translatedText
      };
    }

    setSaving(true);
    try {
      const res = await saveTranslations(payload);

      if (res.error) {
        showToast("error", res.error);
        return;
      }

      showToast("success", "Translations saved successfully ", 2200);

      setTimeout(() => {
        setFormData({
          patient_id: "",
          nutrition_advice: "",
          exercise_advice: "",
          injury_care_advice: "",
          target_language: "hi-IN"
        });
        setTranslations({});
        setEntityId(null);
      }, 2300);
    } catch (err) {
      showToast("error", "Failed to save translations");
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={styles.page}>
      {toast.text && (
        <div
          style={{
            ...styles.toast,
            background: toast.type === "success" ? "#2e7d32" : "#c62828"
          }}
        >
          {toast.text}
        </div>
      )}

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

const styles = {
  page: {
    maxWidth: "500px",
    margin: "auto",
    padding: "40px",
    background: "#f5f5f5",
    minHeight: "100vh",
    position: "relative"
  },
  toast: {
    position: "fixed",
    top: "20px",
    right: "20px",
    color: "#fff",
    padding: "12px 16px",
    borderRadius: "10px",
    boxShadow: "0 6px 20px rgba(0,0,0,0.15)",
    fontSize: "14px",
    fontWeight: "600",
    zIndex: 9999,
    minWidth: "260px"
  }
};