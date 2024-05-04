// Initialize and add the map
let map;

async function initMap() {
  try {
    // Center the map on the requested city.
    const defaultLocation = JSON.parse(document.getElementById('map-default-location').textContent);
    const position = { lat: defaultLocation[0], lng: defaultLocation[1] };

    // Request needed libraries.
    const { Map, Marker } = await google.maps.importLibrary("maps");

    // The map, centered at the default location
    map = new Map(document.getElementById("map"), {
      zoom: 12,
      center: position,
      mapId: "DEMO_MAP_ID",
    });

    // Create markers for each location in mapData
    const mapData = JSON.parse(document.getElementById('map-data').textContent);
    console.log("************mapData");
    console.log(mapData);
    console.log(googleMapsApiKey);
    console.log("************mapdatadone");
    for (const location of mapData) {
      console.log("************location");
      console.log(location);
      console.log("************locationdone");
      // Check if location exists and has a valid location property
      if (location && location.location) {
        const [lat, lng] = location.location.trim().split(',').map(parseFloat);
        // Check if lat and lng are valid numbers
        if (!isNaN(lat) && !isNaN(lng)) {
          const marker = new Marker({
            position: { lat, lng },
            map: map,
            title: location.title,
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
