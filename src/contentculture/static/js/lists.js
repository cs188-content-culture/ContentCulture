// Find the Create List form
const createListForm = document.getElementById("createListForm");

// Run when the user submits the form
createListForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    // Get the information entered by the user
    const name = document.getElementById("listName").value.trim();
    const description = document.getElementById("listDescription").value.trim();

    if (!name) {
        return;
    }

    try {
        // Send the list information to Flask
        const response = await fetch("/api/lists", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                description: description
            })
        });

        const result = await response.json();

        // Check whether Flask saved the list
        if (!response.ok) {
            alert(result.message || "Could not create list.");
            return;
        }

        // Create a card using the saved list information
        const newCard = document.createElement("div");
        newCard.className = "col-md-4";

        newCard.innerHTML = `
            <a href="/lists/${result.id}" class="text-decoration-none">
                <div class="media-card">
                    <span class="media-category">Empty List</span>
                    <h5></h5>
                    <p></p>
                    <p>0 items</p>
                </div>
            </a>
        `;

        // Add the list information safely
        newCard.querySelector("h5").textContent = result.name;
        newCard.querySelector("p").textContent = result.description;

        document.getElementById("listsContainer").appendChild(newCard);

        // Clear the form
        createListForm.reset();

        // Show the success message
        document.getElementById("listSuccess").classList.remove("d-none");

        // Close the modal
        const modalElement = document.getElementById("createListModal");
        const modal = bootstrap.Modal.getInstance(modalElement);

        if (modal) {
            modal.hide();
        }

    } catch (error) {
        console.error(error);
        alert("Could not connect to the server.");
    }
});