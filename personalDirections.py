import csv
from itertools import islice
from typing import Dict, Tuple, Optional
from urllib.parse import urlencode

import utils


def find_optimal_waypoint(origin: str, destination: str, places: Dict[str, Dict[str, any]],
                          max_favorite_places=20, max_detour_length=120) -> Optional[
    Tuple[str, Dict[str, any]]]:
    """
    Finds an optimal waypoint among a list of places that results in a minor detour in route time.

    Args:
        origin (str): The starting location.
        destination (str): The final destination.
        places (Dict[str, Dict[str, any]]): Dictionary containing place names as keys and information as values.
        max_favorite_places (int, optional): Maximum number of favorite places to consider. Default is 20.
        max_detour_length (int, optional): Maximum acceptable detour time in seconds. Default is 120.

    Returns:
        Optional[Tuple[str, Dict[str, any]]]: A tuple containing the chosen waypoint's name and information,
        or None if no suitable waypoint is found.
    """
    top_places = list(islice(places.items(), 0, max_favorite_places))
    for place, info in top_places:
        distance_to_destination = utils.get_route_time(place, destination)
        info["distance_to_destination"] = distance_to_destination

    places_sorted = sorted(top_places, key=lambda curPlace: curPlace[1]['distance_to_destination'])

    direct_route_duration = utils.get_route_time(origin, destination)
    for place in places_sorted:
        waypoint = place[0]
        waypoint_duration = utils.get_route_time(origin, destination,
                                                 [waypoint])

        if waypoint_duration is not None and direct_route_duration is not None:
            time_difference = waypoint_duration - direct_route_duration
            if time_difference <= max_detour_length:  # Less than 2 minutes longer
                return place

    return None


def get_google_maps_route_link(origin: str, destination: str) -> str:
    """
        Generates a Google Maps link for walking directions between two locations.

        Args:
            origin (str): The starting location.
            destination (str): The final destination.

        Returns:
            str: Google Maps link for walking directions.
        """
    base_url = "https://www.google.com/maps/dir/?api=1"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "walking"
    }
    query_params = urlencode(params)
    route_link = f"{base_url}&{query_params}"
    return route_link


def main(origin: str, destination: str, locationsFilePath: str):
    """
        Main function to find an optimal waypoint and generate a Google Maps walking route link.

        Args:
            origin (str): The starting location.
            destination (str): The final destination.
            locationsFilePath (str): Path to the CSV file containing locations data.

        Returns:
            None
        """
    # Read CSV file with UTF-8 encoding :
    myPlaces = {}
    with open(locationsFilePath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row.pop('address')
            myPlaces[key] = row

    optimal_waypoint = find_optimal_waypoint(origin, destination, myPlaces)

    if optimal_waypoint:
        print(f"Go to {optimal_waypoint[1]['name']}, and then follow the instructions:\n",
              get_google_maps_route_link(optimal_waypoint[0], destination))
    else:
        print(get_google_maps_route_link(origin, destination))


if __name__ == '__main__':
    locationsFilePathExample = "output//new_filtered_locations.csv"

    origin_example = "Betsal'el St 8, Jerusalem, Israel"
    destination_example = "Ben Sira St 8, Jerusalem, Israel"

    main(origin_example, destination_example, locationsFilePathExample)
