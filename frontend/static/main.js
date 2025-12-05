const API_BASE = "http://localhost:5000/api";

async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

async function deleteJSON(url) {
  const res = await fetch(url, { method: "DELETE" });
  return res.json();
}

document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const email = document.getElementById("email").value;
      const phone = document.getElementById("phone").value;
      const resp = await postJSON(`${API_BASE}/patients`, { name, email, phone });
      document.getElementById("message").innerText = JSON.stringify(resp);
    });
  }

  const scheduleForm = document.getElementById("scheduleForm");
  if (scheduleForm) {
    fetch(`${API_BASE}/doctors`).then(r => r.json()).then(list => {
      const sel = document.getElementById("doctorSelect");
      list.forEach(d => {
        const o = document.createElement("option");
        o.value = d.id;
        o.text = `${d.name} — ${d.specialty || ""}`;
        sel.appendChild(o);
      });
    });

    scheduleForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const start = document.getElementById("start").value;
      const doctor_id = parseInt(document.getElementById("doctorSelect").value, 10);
      const resp = await fetch(`${API_BASE}/patients`);
      document.getElementById("msg").innerText = "En el frontend de ejemplo asumimos patient_id en tests.";
    });
  }

  const loadBtn = document.getElementById("load");
  if (loadBtn) {
    loadBtn.addEventListener("click", async () => {
      const email = document.getElementById("email").value;
+      alert("En esta demo, use las pruebas E2E para validar la lista de citas. Frontend simplificado.");
    });
  }
});
