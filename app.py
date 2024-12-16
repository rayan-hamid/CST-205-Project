from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home route (landing page)
@app.route("/")
def home():
    # Render the home page
    return render_template("home.html")

# Carbon footprint calculator route
@app.route("/carbon", methods=["GET", "POST"])
def carbon():
    if request.method == "POST":
        # Retrieve user input from the form
        activity = request.form.get("activity")
        value = request.form.get("value")
        result = None  
        error_message = None  

        headers = {
            "Authorization": "Bearer hZT8jfesuvMXnxSlpvuZbQ",  # API key for authentication
            "Content-Type": "application/json",
        }

        try:
            # Prepare data based on selected activity type
            if activity == "vehicle":
                data = {
                    "type": "vehicle",
                    "distance_unit": "km",
                    "distance_value": float(value),
                    "vehicle_model_id": "7268a9b7-17e8-4c8d-acca-57059252afe9"  # Example vehicle model ID
                }
            elif activity == "electricity":
                data = {
                    "type": "electricity",
                    "electricity_unit": "kwh",
                    "electricity_value": float(value),
                    "country": "us"  # Default country
                }
            elif activity == "flight":
                data = {
                    "type": "flight",
                    "passengers": 1,  # Default passengers count
                    "legs": [{"departure_airport": "SFO", "destination_airport": "LAX"}]  # Example flight path
                }
            elif activity == "shipping":
                data = {
                    "type": "shipping",
                    "weight_unit": "kg",
                    "weight_value": float(value),
                    "distance_unit": "km",
                    "distance_value": float(value),
                    "transport_method": "truck"  # Default shipping method
                }
            else:
                # Handle invalid activity type
                error_message = "Invalid activity type selected."
                return render_template("carbon.html", error=error_message)

            # Send API request to calculate carbon emissions
            response = requests.post("https://www.carboninterface.com/api/v1/estimates", headers=headers, json=data)

            if response.status_code == 201:
                result = response.json()["data"]["attributes"]
            else:
                # Handle API errors
                error_message = f"Error: Unable to fetch data. Status Code: {response.status_code}, Message: {response.json().get('message', 'None')}"

        except Exception as e:
            # Handle exceptions (e.g., invalid input)
            error_message = f"Error: {e}"

        # Render the results or error message
        return render_template("carbon.html", result=result, error=error_message)

    # Render the carbon calculator page
    return render_template("carbon.html")

# Effects page route
@app.route("/effects")
def effects():
    # Render the effects of climate change page
    return render_template("effects.html")

if __name__ == "__main__":
    app.run(debug=True)

