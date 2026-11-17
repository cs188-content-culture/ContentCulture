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

    // Update the number of items
    const count = mediaContainer.children.length;
    document.getElementById("mediaCount").textContent = count + " items";

    // Clear the form
    addMediaForm.reset();

    // Close the popup
    const modalElement = document.getElementById("addMediaModal");
    const modal = bootstrap.Modal.getInstance(modalElement);
    modal.hide();
});