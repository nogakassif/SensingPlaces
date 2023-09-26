import csv
import json
import os
import re
from typing import Dict

import utils


def process_files(path_to_json_files: str, output_name: str, regex_filter: str = r'*') -> None:
    """
        Processes JSON files in the specified directory, filters data based on a regex pattern,
        and creates a CSV file containing filtered and aggregated location information.

        Args:
            path_to_json_files (str): Path to the directory containing JSON files.
            output_name (str): Path to the output CSV file.
            regex_filter (str, optional): Regular expression pattern to filter locations. Defaults to r'*'.
        """
    visited = dict()

    # get all JSON file names as a list
    json_file_names = [filename for filename in os.listdir(path_to_json_files) if
                       filename.endswith('.json')]
    for json_file_name in json_file_names:
        with open(os.path.join(path_to_json_files, json_file_name), encoding="utf8") as json_file:
            data = json.load(json_file)

            for activity in data['timelineObjects']:
                if 'placeVisit' in activity and 'location' in activity[
                    'placeVisit'] and "address" in activity['placeVisit']["location"]:
                    location = activity['placeVisit']["location"]["address"]
                    match = re.search(regex_filter, location)  # filters to the wanted area
                    if match:
                        insert_place(visited, location, activity['placeVisit']["location"])
    visited = {key: value for key, value in visited.items() if value["visits"] > 1}
    visited = dict(sorted(visited.items(), key=lambda item: item[1]["visits"], reverse=True))

    # Convert to CSV file
    with open(output_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['address', 'name', 'visits']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in visited.items():
            row = {'address': key, **value}
            writer.writerow(row)


def insert_place(visited: Dict[str, Dict[str, any]], location: str, info: Dict):
    """
        Inserts a location into the visited dictionary or updates its visit count.

        Args:
            visited (dict): Dictionary to store visited locations.
            location (str): Address of the location.
            info (dict): Location information.
        """
    if location not in visited:
        name = info["name"] if "name" in info else None
        visited[location] = {"name": name, "visits": 0}
    visited[location]["visits"] += 1


def get_favorite_places(output_file: str) -> None:
    """
    Asks the user for 20 favorite places and creates a CSV file mapping place names to their addresses.

    Args:
        output_file (str): Path to the output CSV file.
    """
    favorite_places = []
    for i in range(1, 21):
        place = input(f"Enter favorite place #{i} in Jerusalem (or type 'q' to finish): ")
        if place.lower() == 'q':
            break
        favorite_places.append(place)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['address', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for place_name in favorite_places:
            address = utils.get_address_from_name(place_name)
            if not address:
                address = input(f"Please write the address of {place_name}: ")
            writer.writerow({'address': address, 'name': place_name})


def main(output_path, data_folder=None, regex_filter=r'*'):
    """
        Main function that processes JSON files, filters locations, and generates an output CSV file.
    """
    if not data_folder:
        get_favorite_places(output_path)
        return
    process_files(data_folder, output_path, regex_filter)


if __name__ == '__main__':
    # regex = r'.+(?:Jerusalem, Israel|ירושלים, ישראל)$'
    # data_folder = "data"
    # output_path = "output/new_filtered_locations.csv"
    # main(output_path, data_folder, regex)

    output_path = "output/picked_locations.csv"
    main(output_path)