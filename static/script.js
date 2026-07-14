document.getElementById("addBtn").addEventListener("click", async () => {
    const note = document.getElementById("note").value.trim();
    if (!note) return alert("Please enter a note!");

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("successCard").classList.add("hidden");

    try {
        const response = await fetch("/add_event", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ note })
        });

        const data = await response.json();
        document.getElementById("loading").classList.add("hidden");

        if (data.status === "success") {
            document.getElementById("successCard").classList.remove("hidden");
            document.getElementById("calendarLink").href = data.eventLink;
        } else {
            alert("Error: " + data.message);
        }
    } catch (err) {
        document.getElementById("loading").classList.add("hidden");
        alert("Something went wrong: " + err.message);
    }
});
