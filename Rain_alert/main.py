import requests

# Your API key (replace with your own API key from OpenWeather)
API_KEY = "fbf224bdb685940231210400d5a7b04c"

# The city for which you want to check the weather
city = "Johannesburg"

# Construct the API URL
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract and display the weather information
    weather = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    
    print(f"Current weather in {city}:")
    print(f"Weather: {weather}")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
else:
    print(f"Error: Unable to fetch weather data (status code: {response.status_code})")
