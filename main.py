import csv

import createMap
import personalDirections


def createMyMap(locationsFilePath: str, outputMapPath: str, numOfPlaces: int) -> None:
    """
        Creates a Folium map with markers for the top specified number of places and saves it as an
        HTML file.

        Args:
            locationsFilePath (str): Path to the CSV file containing location data.
            outputMapPath (str): Directory where the generated map HTML file will be saved.
            numOfPlaces (int): Number of top places to consider for mapping.

        Returns:
            None
    """
    # Read CSV file with UTF-8 encoding :
    addresses_dict = {}
    with open(locationsFilePath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row.pop('address')
            addresses_dict[key] = row
    my_map = createMap.create_map(addresses_dict, numOfPlaces)
    # Save the map to an HTML file
    my_map.save(f"{outputMapPath}//MyMapTop{numOfPlaces}.html")


def get_user_directions(locationsFilePath:str) -> None:
    """
        Gets user input for origin and destination, and displays the walking route directions.

        Args:
            locationsFilePath (str): Path to the CSV file containing location data.
    """
    origin = input("Enter your origin: ")
    destination = input("Enter the destination: ")
    personalDirections.main(origin, destination, locationsFilePath)


if __name__ == '__main__':
    locationsFilePath = "output//new_filtered_locations.csv"
    outputMapPath = "output"
    createMyMap(locationsFilePath, outputMapPath, 16)

    # get directions:
    # get_user_directions(locationsFilePath)
