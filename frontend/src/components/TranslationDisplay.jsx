import React from "react";

export default function TranslationDisplay({
  translations,
  setTranslations,
  formData,
  onSave,
  saving
}) {
  const fieldOrder = [
    "nutrition_advice",
    "exercise_advice",
    "injury_care_advice"
  ];

  const formatLabel = (key) => {
    return key
      .replaceAll("_", " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
  };

  const handleChange = (key, value) => {
    setTranslations({
      ...translations,
      [key]: value
    });
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Translated Output</h3>

      {fieldOrder
        .filter((key) => key in translations)
        .map((key) => (
          <div key={key} style={styles.card}>
            <p style={styles.label}>{formatLabel(key)}</p>

            <p style={styles.original}>
              <span style={styles.subLabel}>Original:</span>{" "}
              {formData[key] || ""}
            </p>

            <p style={styles.subLabel}>Translated:</p>

            <input
              type="text"
              value={translations[key] || ""}
              onChange={(e) => handleChange(key, e.target.value)}
              style={styles.input}
              placeholder={`Edit ${formatLabel(key)} translation`}
              disabled={saving}
            />
          </div>
        ))}

      <button
        onClick={onSave}
        style={{
          ...styles.button,
          opacity: saving ? 0.7 : 1,
          cursor: saving ? "not-allowed" : "pointer"
        }}
        disabled={saving}
      >
        {saving ? "Saving..." : "Save Translations"}
      </button>
    </div>
  );
}

const styles = {
  container: {
    marginTop: "20px",
    padding: "12px",
    background: "#ebf5e8",
    borderRadius: "10px",
    border: "1px solid #c8e6c9"
  },
  title: {
    marginBottom: "12px",
    color: "#2e7d32",
    fontSize: "16px",
    fontWeight: "600"
  },
  card: {
    background: "#ffffff",
    padding: "8px 10px",
    borderRadius: "6px",
    marginBottom: "8px",
    border: "1px solid #e0e0e0",
    boxShadow: "0 1px 3px rgba(0,0,0,0.06)"
  },
  label: {
    fontWeight: "600",
    marginBottom: "2px",
    fontSize: "12px",
    color: "#2f2f2f"
  },
  subLabel: {
    fontWeight: "500",
    fontSize: "12px",
    color: "#444"
  },
  original: {
    marginBottom: "6px",
    color: "#666",
    fontSize: "11px"
  },
  input: {
    width: "100%",
    padding: "6px 8px",
    borderRadius: "6px",
    border: "1px solid #d0d0d0",
    boxSizing: "border-box",
    background: "#f9fbf9",
    fontSize: "13px",
    transition: "all 0.2s ease"
  },
  button: {
    marginTop: "10px",
    padding: "10px",
    background: "linear-gradient(135deg, #2e7d32, #43a047)",
    color: "white",
    border: "none",
    borderRadius: "6px",
    fontSize: "13px",
    fontWeight: "500"
  }
};