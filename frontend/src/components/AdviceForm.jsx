export default function AdviceForm({ formData, setFormData, onSubmit, loading }) {

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFocus = (e) => {
    e.target.style.border = "1px solid #2e7d32";
    e.target.style.boxShadow = "0 0 0 2px rgba(46,125,50,0.1)";
  };

  const handleBlur = (e) => {
    e.target.style.border = "1px solid #cfd8dc";
    e.target.style.boxShadow = "none";
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Dynamic Translation Form</h2>

      <label style={styles.label}>Patient ID</label>
      <input
        name="patient_id"
        value={formData.patient_id}
        onChange={handleChange}
        style={styles.input}
        onFocus={handleFocus}
        onBlur={handleBlur}
        placeholder="Enter patient ID..."
      />

      <label style={styles.label}>Nutrition Advice</label>
      <input
        name="nutrition_advice"
        value={formData.nutrition_advice}
        onChange={handleChange}
        style={styles.input}
        onFocus={handleFocus}
        onBlur={handleBlur}
        placeholder="Enter nutrition advice..."
      />

      <label style={styles.label}>Exercise Advice</label>
      <input
        name="exercise_advice"
        value={formData.exercise_advice}
        onChange={handleChange}
        style={styles.input}
        onFocus={handleFocus}
        onBlur={handleBlur}
        placeholder="Enter exercise advice..."
      />

      <label style={styles.label}>Injury Care Advice</label>
      <input
        name="injury_care_advice"
        value={formData.injury_care_advice}
        onChange={handleChange}
        style={styles.input}
        onFocus={handleFocus}
        onBlur={handleBlur}
        placeholder="Enter injury care advice..."
      />

      <label style={styles.label}>Language</label>
      <select
        name="target_language"
        value={formData.target_language}
        onChange={handleChange}
        style={styles.input}
        onFocus={handleFocus}
        onBlur={handleBlur}
      >
        <option value="hi-IN">Hindi</option>
        <option value="bn-IN">Bengali</option>
        <option value="gu-IN">Gujarati</option>
        <option value="kn-IN">Kannada</option>
        <option value="ml-IN">Malayalam</option>
        <option value="mr-IN">Marathi</option>
        <option value="od-IN">Odia</option>
        <option value="pa-IN">Punjabi</option>
        <option value="ta-IN">Tamil</option>
        <option value="te-IN">Telugu</option>

      </select>

      <button
        onClick={onSubmit}
        style={{
          ...styles.button,
          opacity: loading ? 0.7 : 1,
          cursor: loading ? "not-allowed" : "pointer"
        }}
        disabled={loading}
      >
        {loading ? "Translating..." : "Submit & Translate"}
      </button>

      {loading && <p style={styles.loading}>Loading translations...</p>}
    </div>
  );
}

const styles = {
  container: {
    background: "#ffffff",
    padding: "25px",
    borderRadius: "12px",
    boxShadow: "0 4px 20px rgba(0,0,0,0.08)"
  },
  title: {
    marginBottom: "15px",
    color: "#2e7d32",
    textAlign: "center"
  },
  label: {
    fontSize: "13px",
    color: "#555",
    marginBottom: "4px",
    display: "block"
  },
  input: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #cfd8dc",
    outline: "none",
    fontSize: "14px",
    marginBottom: "12px",
    transition: "all 0.2s ease",
    background: "#fafafa",
    boxSizing: "border-box"
  },
  button: {
    marginTop: "10px",
    width: "100%",
    padding: "12px",
    background: "linear-gradient(135deg, #2e7d32, #43a047)",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontWeight: "600",
    fontSize: "14px"
  },
  loading: {
    marginTop: "10px",
    fontSize: "13px",
    color: "#777"
  }
};