# spotvibe
Spotivibe is a local script designed to provide Spotify users with a quick and efficient way to access their playlists and automate their organization. By leveraging Spotify's public API tools, Spotivibe allows users to categorize their main playlists into sub-playlists based on specific criteria such as genre, tempo, and more.

## **Technical Workflow**
Spotivibe was created using Python as its main backbone when accessing Spotify's API. Upon initiation, Spotivibe connects to Spotify for its Developer's API using the OAuth 2.0 client credentials flow. It then sends HTTP calls with its own internal values (user inputted when prompted) to Spotify's endpoint to utilize their available playlist manipulation tools.

## **Features**
- *Fast Access*: Spotivibe allows users to easily retrieve their existing Spotify playlists without the need to navigate through the app or website manually.
- *Automated Organization*: Users can take their main playlists and automatically create sub-playlists based on various criteria, making it convenient to manage and quickly enjoy their music collection.
- *Custom Criteria*: Provies flexibility by allowing users to specify their own criteria for organizing sub-playlists, such as genre, tempo, artist, or any other available attributes via Spotify's public API.

**Example Input Page**

![Sample Input Page](tests/assets/example_input_page.jpg?raw=true "Sample Input Page")

**Example Output Page**

![Sample Output Page](tests/assets/example_output_page.jpg?raw=true "Sample Output Page")

## **Local Usage**
- **REQUIREMENT: You must have a Spotify account (free or paid plan)**
### Part 1 - Obtain Spotify API Credentials
- Log into the [Spotify Developer](https://developer.spotify.com/dashboard/) page (anyone with a Spotify account can log in)
- Click on "Create An App" and enter an app name (ex. Spotivibe)
- Save the Client ID and Client Secret on the left side of the page

### Part 2
- Clone the Spotivibe repository to a local IDE
- Set up a virtual environment and run `pip install -r requirements.txt` in your terminal to download required project packages
- Create a duplicate of the `.env.example` file within the repository and rename it `.env`
- Replace the `CLIENT_ID` and `CLIENT_SECRET` values with the saved values from Part 1
- Run the `synestify/src/main.py` file to start up a local Flask app
- Run the React app found in the frontend directory (via 'npm start')
- Select the genre to receive song recommmendations for
- Click submit to view the top 12 song recommendations based on the parameters and image you provided!

## **Creators**
[Lawrence Han](https://github.com/lawrencehhan)
