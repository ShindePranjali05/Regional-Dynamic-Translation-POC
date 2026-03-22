export async function submitAndTranslate(data) {
  const res = await fetch("http://127.0.0.1:5000/submit-and-translate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  return res.json();
}

export async function saveTranslations(payload) {
  const res = await fetch("http://127.0.0.1:5000/save-translations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  return res.json();
}