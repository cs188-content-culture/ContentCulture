// Find the movie search elements
const searchMovieButton = document.getElementById("searchMovieButton");
const movieSearchResults = document.getElementById("movieSearchResults");
const movieSearchSection = document.getElementById("movieSearchSection");
const mediaMedium = document.getElementById("mediaMedium");
const mediaTitle = document.getElementById("mediaTitle");

// Clear the selected result when the title changes
mediaTitle.addEventListener("input", function () {
    selectedMovie = null;
    movieSearchResults.replaceChildren();
});

// Remember which TMDB movie was selected
let selectedMovie = null;

// Update the search button when the category changes
mediaMedium.addEventListener("change", function () {
    selectedMovie = null;
    movieSearchResults.replaceChildren();
    mediaTitle.value = "";

    // Update the button label
    searchMovieButton.textContent = "Search " + {
        "Movie": "Movies",
        "TV Show": "TV Shows",
        "Book": "Books",
        "Game": "Games"
    }[mediaMedium.value];

    // All four categories now support searching
    movieSearchSection.classList.remove("d-none");
});

// Search TMDB for movies or TV shows
searchMovieButton.addEventListener("click", async function () {
    const query = mediaTitle.value.trim();
    const medium = mediaMedium.value;

    if (!query) {
        movieSearchResults.textContent = "Please enter a title.";
        return;
    }

    // Choose the API based on media category
    const endpoints = {
        "Movie": "/api/search/movies",
        "TV Show": "/api/search/tv",
        "Book": "/api/search/books",
        "Game": "/api/search/games"
    };

    const url = endpoints[medium];

    movieSearchResults.textContent = "Searching...";
    selectedMovie = null;

    try {
        const response = await fetch(
            url + "?query=" + encodeURIComponent(query)
        );

        if (!response.ok) {
            throw new Error("Search failed");
        }

        const results = await response.json();
        movieSearchResults.replaceChildren();

        if (results.length === 0) {
            movieSearchResults.textContent = "No results found.";
            return;
        }

        // Display the first five matching results
        results.slice(0, 5).forEach(function (item) {
            const button = document.createElement("button");
            button.type = "button";
            button.className =
                "btn btn-outline-secondary d-block w-100 mb-2 text-start";

            // Get the title and year based on the API
            let title;
            let year;

            if (medium === "Book") {
                title = item.title;
                year = item.first_publish_year || "Unknown year";
            } else if (medium === "Game") {
                title = item.name;
                year = item.released ? item.released.slice(0, 4) : "Unknown year";
            } else if (medium === "TV Show") {
                title = item.name;
                year = item.first_air_date
                    ? item.first_air_date.slice(0, 4)
                    : "Unknown year";
            } else {
                title = item.title;
                year = item.release_date
                    ? item.release_date.slice(0, 4)
                    : "Unknown year";
            }

            button.textContent = title + " (" + year + ")";

            button.addEventListener("click", function () {
                selectedMovie = item;
                mediaTitle.value = title;
                movieSearchResults.textContent =
                    "Selected: " + title + " (" + year + ")";
            });

            movieSearchResults.appendChild(button);
        });

    } catch (error) {
        movieSearchResults.textContent =
            "Could not search for media. Please try again.";
        console.error(error);
    }
});


// Find the Add Media form
const addMediaForm = document.getElementById("addMediaForm");

// Run this function when the form is submitted
addMediaForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    // Get the information entered by the user
    const title = document.getElementById("mediaTitle").value;
    const medium = document.getElementById("mediaMedium").value;
    const rating = document.getElementById("mediaRating").value;
    const commentary = document.getElementById("mediaCommentary").value;

    // Require TMDB selection for movies and TV shows
    if (!selectedMovie) {
        movieSearchResults.textContent =
            "Please search for and select a title first.";
        return;
    }

    // Find where the media cards are displayed
    const mediaContainer = document.getElementById("mediaContainer");

    // Get the ID of the current list
    const listId = mediaContainer.dataset.listId;

    // Open Library uses "key"; the other APIs use "id"
    const externalId = selectedMovie
        ? String(
            medium === "Book"
                ? selectedMovie.key
                : selectedMovie.id
        )
        : null;

    // Send the media information to Flask
    try {
        const response = await fetch(`/api/lists/${listId}/media`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                medium: medium,
                external_id: externalId,
                rating: Number(rating),
                commentary: commentary
            })
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.message || "Could not add media.");
            return;
        }

    } catch (error) {
        console.error(error);
        alert("Could not connect to the server.");
        return;
    }

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
    selectedMovie = null;
    movieSearchResults.replaceChildren();
    movieSearchSection.classList.remove("d-none");


    // Show a success message
    document.getElementById("mediaSuccess").classList.remove("d-none");

    searchMovieButton.textContent = "Search Movies";

    // Close the popup
    const modalElement = document.getElementById("addMediaModal");
    const modal = bootstrap.Modal.getInstance(modalElement);

    if (modal) {
        modal.hide();
    } else {
        console.log("Bootstrap modal instance not found");
    }
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