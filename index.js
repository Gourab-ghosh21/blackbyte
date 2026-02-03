function togglePassword() {
    const input = document.getElementById("passcode");
    input.type = input.type === "password" ? "text" : "password";
}

function checkEnter(event) {
    if (event.key === "Enter") {
        const value = document.getElementById("passcode").value.trim();
        if (value !== "") {
            document.body.innerHTML =
                "<h2 style='color:#4dffff;text-align:center;margin-top:40vh'>System Initialized – Dashboard Placeholder</h2>";
        }
    }
}