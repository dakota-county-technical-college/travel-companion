// Our html document that's loading this script
let doc;

// Add an event listener to ensure nothing happens until we've loaded the page
window.addEventListener("DOMContentLoaded", (event) => init());

// Initialize the page
function init() {
    // Add a click event listener to the places button 
    doc = document.getElementById("placesBtn");
    if (doc) {
        doc.addEventListener("click", requestPlacesData);
    }
}

// Execute when the user clicks the places button
function requestPlacesData() {

    console.log("yep");
    // The URL of our place data view that resides in views.py
    const url = "http://127.0.0.1:8000/itineraries/loadPlaceData/";

    // Perform a simple get request to the view
    const promise = fetch(url);
    promise.then(response => {
        console.log(response.json());
    });
    
    /**
     * TODO: ADD ERROR HANDLING JUST IN CASE
     */
}