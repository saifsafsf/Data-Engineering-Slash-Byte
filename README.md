# Scraping-Real-Estate-Information
This project scrapes information from a website with real estate listings and then saves the data in `.csv` format.
The project is immune to the pop-up ads on the subject website i.e. `https://www.zameen.com/`.

### How to Run:
- Make sure the Chrome Driver is placed in the same directory as the file accessing it.
- OR it can be placed in the `PATH` environment variable.
- Run the `main.py` file.
- Enter the city name.
- Once the program is running, do NOT switch the windows until the dropdown menu is accessed.
- After that, the script will keep running in the back, the user can safely navigate through the open windows.

You can also scrape multiple webpages from the same location. (see comments in `__main__` function).
Two scraped datasets have been provided.
