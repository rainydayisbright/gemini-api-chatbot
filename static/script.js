document.getElementById("promptForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const prompt = document.getElementById("prompt").value;
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "⏳ Generating...";

  const formData = new FormData();
  formData.append("prompt", prompt);

  const res = await fetch("/generate", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();

  if (data.error) {
    resultDiv.innerHTML = `<p style="color:red;">❌ ${data.error}</p>`;
    return;
  }

  resultDiv.innerHTML = "";
  data.results.forEach((r) => {
    if (r.endsWith(".png") || r.endsWith(".jpg")) {
      const img = document.createElement("img");
      img.src = "/" + r;
      img.style.width = "300px";
      img.style.display = "block";
      img.style.margin = "10px 0";
      resultDiv.appendChild(img);
    } else {
      resultDiv.innerHTML += `<p>${r}</p>`;
    }
  });
});
