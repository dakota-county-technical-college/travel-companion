// Initialize and add the map
let map;

async function initMap() {
  // The location of DCTC
  const position = { lat: 44.737, lng: -93.079 };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  map = new Map(document.getElementById("map"), {
    zoom: 4,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  // The marker, positioned at DCTC
  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: "DCTC",
  });
}

initMap();