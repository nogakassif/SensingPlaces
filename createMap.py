from typing import Dict

import folium

import utils

COLORS = ['darkred', 'red', 'orange', 'beige']


def create_map(addresses: Dict[str, any], top: int) -> folium.Map:
    """
        Creates a Folium map with markers for specified addresses.

        Args:
            addresses (Dict[str, any]): Dictionary of addresses as keys and information as values.
            top (int): Number of top addresses to consider for mapping.

        Returns:
            folium.Map: A Folium map object with markers for the specified addresses.
    """
    addresses = list(addresses.keys())[:top]
    # Importing the required libraries

    # Create a map centered at the first address in the list
    map_center = utils.get_geocode(addresses[0])
    map_obj = folium.Map(location=map_center, zoom_start=14)

    # Add markers for each address on the map with different colors
    for i, address in enumerate(addresses):
        lat, lng = utils.get_geocode(address)
        if lat is not None and lng is not None:
            # Assign a color based on the index
            color_index = i // len(COLORS)
            color = COLORS[color_index]

            folium.Marker([lat, lng], popup=address, icon=folium.Icon(color=color)).add_to(map_obj)

    return map_obj

