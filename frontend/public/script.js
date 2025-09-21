let full_document_text = "";

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const res = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            body: formData,
        });
        const data = await res.json();
        if (res.ok && data.status === "success") {
            document.getElementById("login-box").style.display = "none";
            document.getElementById("main-box").style.display = "block";
        } else {
            document.getElementById("login-msg").innerText = data.message || "Login failed";
        }
    } catch (error) {
        document.getElementById("login-msg").innerText = "Error connecting to server";
        console.error(error);
    }
}

async function upload() {
    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData,
        });
        const data = await res.json();

        if (data.text) {
            // Save extracted text
            full_document_text = data.text;

            // Now call /summarize with that text
            const sumForm = new FormData();
            sumForm.append("text", full_document_text);

            const sumRes = await fetch("http://127.0.0.1:8000/summarize", {
                method: "POST",
                body: sumForm,
            });
            const sumData = await sumRes.json();

            if (sumData.summary) {
                document.getElementById("summary-box").innerText = sumData.summary;
            } else {
                alert("Error: " + (sumData.error || "Unknown error while summarizing"));
            }
        } else {
            alert("Error: " + (data.error || "Unknown error while uploading"));
        }
    } catch (error) {
        alert("Error connecting to server");
        console.error(error);
    }
}

async function askQuestion() {
    const question = document.getElementById("question").value;
    if (!question) return alert("Enter a question");

    const formData = new FormData();
    formData.append("question", question);
    formData.append("document", full_document_text);

    try {
        const res = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            body: formData,
        });
        const data = await res.json();
        document.getElementById("answer-box").innerText =
            data.answer ? data.answer : (data.error || "Error occurred");
    } catch (error) {
        alert("Error connecting to server");
        console.error(error);
    }
}
