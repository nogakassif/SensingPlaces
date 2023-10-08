**main.py:**

TO CREATE YOUR MAP USE:

1. `createMyMap(locationsFilePath: str, outputMapPath: str, numOfPlaces: int) -> None`

   Creates a Folium map with markers for the top specified number of places and saves it as an HTML file.

TO GET DIRECTIONS USE:

2. `get_user_directions(locations_file_path:str) -> None`

   Gets user input for origin and destination, and displays the walking route directions. locations_file_path is the csv file of your filtered top locations.

TO CREATE YOUR CSV FILE FROM GOOGLE JSON FILES-

**locationsProcess.py:**

1. `main(output_path, data_folder=None, regex_filter=r'*')`

   Main function that processes JSON files, filters locations, and generates an output CSV file.
   The regex expression is for cases you want to filter your places to a specific city . for example to filter to Jerusalem use:
     regex = r'.+(?:Jerusalem, Israel|ירושלים, ישראל)$'




Please note that API_KEY in `utils.py` should be replaced with your actual Google Maps API key.
