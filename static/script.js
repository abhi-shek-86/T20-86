document.addEventListener("DOMContentLoaded", function() {
    updateTargetLanguages();
});

function updateTargetLanguages() {
    const srcLang = document.getElementById("src_lang").value;
    const tgtLangSelect = document.getElementById("tgt_lang");

    // Clear previous target options
    tgtLangSelect.innerHTML = '<option value="" disabled selected>Select Target Language</option>';

    if (srcLang in supportedPairs) {
        supportedPairs[srcLang].forEach(lang => {
            let option = document.createElement("option");
            option.value = lang;
            option.textContent = lang.toUpperCase();
            tgtLangSelect.appendChild(option);
        });
    }
}

function translateText() {
    const text = document.getElementById("text").value;
    const srcLang = document.getElementById("src_lang").value;
    const tgtLang = document.getElementById("tgt_lang").value;
    const resultArea = document.getElementById("translation");

    if (!text || !srcLang || !tgtLang) {
        resultArea.textContent = "⚠ Please fill all fields!";
        return;
    }

    fetch("/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, src_lang: srcLang, tgt_lang: tgtLang })
    })
    .then(response => response.json())
    .then(data => { resultArea.textContent = data.translation; })
    .catch(error => { resultArea.textContent = "⚠ Error translating text."; });
}
