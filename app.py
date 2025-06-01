from flask import Flask, request, jsonify
import json, os
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

app = Flask(__name__)
geolocator = Nominatim(user_agent="weather_signup")
tz_finder = TimezoneFinder()
USER_FILE = "users.json"

# Ensure file exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump([], f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

@app.route("/")
def home():
    return "🌤️ MCP Weather Bot is running."

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    city = data.get("city")

    location = geolocator.geocode(city)
    if not location:
        return jsonify({"error": "City not found"}), 400

    lat, lon = location.latitude, location.longitude
    timezone = tz_finder.timezone_at(lng=lon, lat=lat)

    users = load_users()
    if any(u["email"] == email for u in users):
        return jsonify({"message": "Already subscribed"}), 200

    users.append({
        "name": name,
        "email": email,
        "location": f"{lat},{lon}",
        "city": city,
        "timezone": timezone
    })
    save_users(users)
    return jsonify({"message": f"Subscribed {name}!"})

@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    data = request.get_json()
    email = data.get("email")
    users = load_users()
    new_users = [u for u in users if u["email"] != email]
    save_users(new_users)
    return jsonify({"message": f"Unsubscribed {email}!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
