// Initialize and add the map
let map;

async function initMap() {
  try {
    // Center the map on the requested city.
    const defaultLocation = JSON.parse(document.getElementById('map-default-location').textContent);
    const position = { lat: defaultLocation[0], lng: defaultLocation[1] };

    // Request needed libraries.
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

    // Import and set up our custom map type
    const customMapTypeID = '522b64fa57f21058';

    // The map, centered at the default location
    map = new Map(document.getElementById("map"), {
      zoom: 12,
      center: position,
      mapId: "DEMO_MAP_ID",
      mapId: customMapTypeID,
    });

    // Create markers for each location in mapData
    const mapData = JSON.parse(document.getElementById('map-data').textContent);
    for (const location of mapData) {
      // Check if location exists and has a valid location property
      if (location && location.location) {
        const [lat, lng] = location.location.trim().split(',').map(parseFloat);
        // Check if lat and lng are valid numbers
        if (!isNaN(lat) && !isNaN(lng)) {

          // Define the activity tag that will mark each place on the map
          const activityTag = document.createElement("div");
          activityTag.className = "activity-tag";
          activityTag.textContent = location.title;

          // Create the marker
          const marker = new AdvancedMarkerElement({
            position: { lat, lng },
            map: map,
            title: location.title,
            content: activityTag,
          });

          // Add a listener to scroll to the activity when the marker is clicked
          marker.addListener("click", ({ domEvent, latLng }) => {
            const { target } = domEvent;
      
            let element = document.getElementById(location.title);
            let y = element.getBoundingClientRect().top + window.scrollY;
            window.scroll({
              top: y,
              behavior: 'smooth'
            }); 
          });

        } else {
          console.error("Invalid latitude or longitude:", location.location);
        }
      } else {
        console.error("Invalid location:", location);
      }
    }
  } catch (error) {
    console.error("An error occurred while initializing the map:", error);
  }
}

initMap();
