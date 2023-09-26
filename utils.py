from typing import List, Optional, Tuple

import requests

API_KEY = "ENTER_YOUR_API_KEY_HERE"
BASE_URL_DIRECTIONS = "https://maps.googleapis.com/maps/api/directions/json?"
BASE_URL_GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json?"


def get_geocode(address: str, api_key: str = API_KEY) -> Tuple[Optional[float], Optional[float]]:
    """
        Retrieves the latitude and longitude coordinates for a given address.

        Args:
            address (str): The address to be geocoded.
            api_key (str): Google Maps API key.

        Returns:
            Tuple[float, float]: A tuple containing the latitude and longitude coordinates.
    """
    url = f"{BASE_URL_GEOCODE}address={address}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Error: {data['status']}")
        return None, None


def get_route_time(start_location: str, end_location: str, waypoints: List[str] = [],
                   api_key: str = API_KEY) -> Optional[int]:
    """
        Calculates the estimated route time between two locations, with optional waypoints.

        Args:
            start_location (str): The starting location.
            end_location (str): The final destination.
            waypoints (List[str], optional): List of waypoints along the route. Default is an empty list.
            api_key (str): Google Maps API key. Default is API_KEY from the script.

        Returns:
            int: Duration of the route in seconds.
    """
    waypoints_str = "|".join(waypoints)
    url = f"{BASE_URL_DIRECTIONS}origin={start_location}&destination={end_location}&waypoints={waypoints_str}&mode=walking&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        duration = 0
        for leg in range(len(waypoints) + 1):
            duration += data['routes'][0]['legs'][leg]['duration']['value']
        return duration  # Duration in seconds
    else:
        print(f"Error: {data['status']}")
        return None


def get_address_from_name(place_name, api_key=API_KEY):
    """
    Retrieves the address for a given place name.

    Args:
        place_name (str): The name of the place.
        api_key (str): Google Maps API key. Default is API_KEY from the script.

    Returns:
        str: The address of the place.
    """
    url = f"{BASE_URL_GEOCODE}address={place_name}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        address = data['results'][0]['formatted_address']
        return address
    else:
        # print(f"Error: {data['status']}")
        return None
