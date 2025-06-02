from flask import Flask, request, render_template_string
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from sheet_handler import add_user_to_sheet, remove_user_from_sheet

app = Flask(__name__)
geolocator = Nominatim(user_agent="mcp_weather_signup")
tz_finder = TimezoneFinder()

# HTML form for signup/unsubscribe
form_html = '''
<h2>🌤️ MCP Weather Bot Sign-Up</h2>
<form method="POST" action="/signup">
  Name: <input name="name" required><br><br>
  Email: <input name="email" required><br><br>
  City: <input name="city" required><br><br>
  <button type="submit">Subscribe</button>
</form>

<h2>❌ Unsubscribe</h2>
<form method="POST" action="/unsubscribe">
  Email: <input name="email" required><br><br>
  <button type="submit">Unsubscribe</button>
</form>
'''

@app.route("/")
def index():
    return render_template_string(form_html)

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    city = request.form["city"]

    location = geolocator.geocode(city)
    if not location:
        return "❌ City not found. Try again."

    lat, lon = location.latitude, location.longitude
    timezone = tz_finder.timezone_at(lng=lon, lat=lat)
    location_str = f"{lat},{lon}"

    added = add_user_to_sheet(name, email, city, location_str, timezone)
    if not added:
        return "⚠️ You're already subscribed."

    return f"✅ Thanks {name}, you're subscribed for {city}!"

@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    email = request.form["email"]
    removed = remove_user_from_sheet(email)

    if removed:
        return "✅ You have been unsubscribed."
    else:
        return "⚠️ Email not found in subscription list."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
