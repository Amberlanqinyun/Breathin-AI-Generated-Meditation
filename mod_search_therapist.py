import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def search_nearby_therapists(location):
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': location,
        'radius': 5000,
        'type': 'therapist',
        'key': api_key
    }
    response = requests.get(search_url, params=params)
    results = response.json().get('results', [])
    therapists = [{'name': result['name'], 'address': result['vicinity']} for result in results]
    return therapists
