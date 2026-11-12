
// Find the Create List form
const createListForm = document.getElementById("createListForm");

// Run this code when the form is submitted
createListForm.addEventListener("submit", function (event) {

    // Stop the page from refreshing
    event.preventDefault();

    // Get the user's input
    const name = document.getElementById("listName").value.trim();
    const description = document.getElementById("listDescription").value.trim();

    // Make sure the list has a name
    if (name === "") {
        return;
    }

    // Create a new list card
    const newCard = document.createElement("div");
    newCard.className = "col-md-4";

    newCard.innerHTML = `
        <div class="media-card">
            <h5></h5>
            <p></p>
            <p>0 items</p>
        </div>
    `;

    // Add the user's text safely
    newCard.querySelector("h5").textContent = name;
    newCard.querySelector("p").textContent = description;

    // Add the card to the page
    document.getElementById("listsContainer").appendChild(newCard);

    // Close the modal
    const modalElement = document.getElementById("createListModal");
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();

    // Clear the form
    createListForm.reset();
});
