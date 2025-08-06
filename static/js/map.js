// static/js/map.js

let map;
let markers = [];
let currentInfoWindow = null;

function initMap() {
    // Initialize the map centered on a default location
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: { lat: 0, lng: 0 }
    });

    // Try to get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                map.setCenter(userLocation);
                
                // Add a marker for user's location
                new google.maps.Marker({
                    position: userLocation,
                    map: map,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 10,
                        fillColor: "#4285F4",
                        fillOpacity: 1,
                        strokeWeight: 2,
                        strokeColor: "#FFFFFF",
                    },
                    title: "Your Location"
                });

                // Add shop markers
                addShopMarkers();
            },
            () => {
                // Handle geolocation error
                handleLocationError(true);
            }
        );
    } else {
        // Browser doesn't support geolocation
        handleLocationError(false);
    }
}

function addShopMarkers() {
    // Clear existing markers
    markers.forEach(marker => marker.setMap(null));
    markers = [];

    // Add markers for each shop
    shopsData.forEach(shop => {
        const marker = new google.maps.Marker({
            position: { lat: shop.lat, lng: shop.lng },
            map: map,
            title: shop.name,
            icon: {
                url: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png'
            }
        });

        const infoWindow = new google.maps.InfoWindow({
            content: createInfoWindowContent(shop)
        });

        marker.addListener('click', () => {
            if (currentInfoWindow) {
                currentInfoWindow.close();
            }
            infoWindow.open(map, marker);
            currentInfoWindow = infoWindow;
            updateShopInfoPanel(shop);
        });

        markers.push(marker);
    });
}

function createInfoWindowContent(shop) {
    return `
        <div class="info-window">
            <h5>${shop.name}</h5>
            <p>${shop.address}</p>
            <p>Phone: ${shop.phone}</p>
        </div>
    `;
}

function updateShopInfoPanel(shop) {
    const shopInfo = document.getElementById('shop-info');
    shopInfo.innerHTML = `
        <div class="shop-details">
            <h3>${shop.name}</h3>
            <p><strong>Address:</strong> ${shop.address}</p>
            <p><strong>Phone:</strong> ${shop.phone}</p>
            <p><strong>Working Hours:</strong> ${shop.working_hours}</p>
            <div class="services">
                <h4>Services:</h4>
                <p>${shop.services}</p>
            </div>
        </div>
    `;
    shopInfo.style.display = 'block';
}

function handleLocationError(browserHasGeolocation) {
    const defaultLocation = { lat: 0, lng: 0 };
    map.setCenter(defaultLocation);
    alert(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
}

// Initialize map when the page loads
window.addEventListener('load', initMap);