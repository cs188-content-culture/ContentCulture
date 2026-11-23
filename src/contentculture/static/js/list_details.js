// Find the Add Media form
const addMediaForm = document.getElementById("addMediaForm");

// Run this function when the form is submitted
addMediaForm.addEventListener("submit", function (event) {
    event.preventDefault();

    // Get the information entered by the user
    const title = document.getElementById("mediaTitle").value;
    const medium = document.getElementById("mediaMedium").value;
    const rating = document.getElementById("mediaRating").value;
    const commentary = document.getElementById("mediaCommentary").value;

    // Find where the media cards are displayed
    const mediaContainer = document.getElementById("mediaContainer");

    // Create a new column for the media card
    const column = document.createElement("div");
    column.className = "col-md-4";
    // Store the media category for filtering
    column.dataset.medium = medium;

    // Create the card
    const card = document.createElement("div");
    card.className = "media-card";

    // Add the media information
    const titleElement = document.createElement("h5");
    titleElement.textContent = title;

    const mediumElement = document.createElement("p");
    mediumElement.textContent = medium;

    const ratingElement = document.createElement("p");
    ratingElement.textContent = "Rating: " + rating + "/5";

    const commentaryElement = document.createElement("p");
    commentaryElement.textContent = "Commentary: " + commentary;

    // Put everything inside the card
    card.appendChild(titleElement);
    card.appendChild(mediumElement);
    card.appendChild(ratingElement);
    card.appendChild(commentaryElement);

    // Add the card to the page
    column.appendChild(card);
    mediaContainer.appendChild(column);

    // Apply the selected filter to the new card
    const selectedCategory = document.getElementById("mediaFilter").value;

    if (selectedCategory !== "All" && medium !== selectedCategory) {
        column.classList.add("d-none");
    }

    // Update the number of items
    const count = mediaContainer.children.length;
    document.getElementById("mediaCount").textContent = count + " items";

    // Clear the form
    addMediaForm.reset();

    // Show a success message
    document.getElementById("mediaSuccess").classList.remove("d-none");

    // Close the popup
    const modalElement = document.getElementById("addMediaModal");
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();
});

// Find the media category filter
const mediaFilter = document.getElementById("mediaFilter");

// Filter the media cards when the user selects a category
mediaFilter.addEventListener("change", function () {

    // Get the selected category
    const selectedCategory = mediaFilter.value;

    // Find all media cards
    const mediaCards = document.querySelectorAll("#mediaContainer > div");

    // Check the category of each card
    mediaCards.forEach(function (card) {

        const medium = card.dataset.medium;

        if (selectedCategory === "All" || medium === selectedCategory) {
            card.classList.remove("d-none");
        } else {
            card.classList.add("d-none");
        }
    });
});