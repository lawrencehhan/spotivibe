from flask import Flask, request, Response
from uuid import uuid4
from dotenv import load_dotenv
import os
import threading
import webbrowser
import time
# from task_connect_api import requestUserAuthorization

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
auth_code = None
bearer_token = None
app = Flask(__name__)
app.config["SECRET_KEY"] = uuid4().bytes

@app.route("/")
def starting_url():
	status_code = Response(status=200)
	return status_code

@app.route("/callback")
def handle_auth_callback():
    global auth_code
    auth_code = request.args.get("code")
    return f"Authorization code received: {auth_code}"

def start_app():
     app.run(host="localhost", port=8888)

def requestUserAuthorization():
    auth_url = "https://accounts.spotify.com/authorize"
    redirect_uri = 'http://localhost:8888/callback'
    auth_scope = ["playlist-read-private", "playlist-read-collaborative", "playlist-modify-private", "playlist-modify-public", "user-read-email", "user-read-private"]
    personal_auth_url = f"{auth_url}?client_id={CLIENT_ID}&response_type=code&redirect_uri={redirect_uri}&scope={'+'.join(auth_scope)}"

    webbrowser.open(personal_auth_url)

    thread = threading.Thread(target=start_app)
    thread.daemon = True
    thread.start()

    timeout = 30
    start_time = time.time()
    while auth_code is None:
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            raise TimeoutError("Authorization code retrieval timed out.")
        time.sleep(0.1)

    return


if __name__ == "__main__":
    try:
        print('Requesting authorization from Spotify user.')
        requestUserAuthorization()
        print('Authorization code returned:')
        print(auth_code)
    except TimeoutError:
         print("Timeout: Failed to get authorization code within 30 seconds.")
    except Exception as e:
        print("Failed to get authorization code:", e)



