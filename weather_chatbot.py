import requests #for HTTP requets to web server (both hugging face and open weather)
import datetime
from API_key import weather_key

#model set up: mistralai/Mistral-7B-Instruct for instructions
HF_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
HEADERS = {"Authorization": f"Bearer {weather_key}"}

#function to get weather for a city
def get_weather(city):
    api_key = weather_key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url).json() #sending a request to the API and getting the response and convert it to json
    
    #extracting weather data from response
    if response.get("main"):
        current_temperature = response["main"]["temp"]
        current_pressure = response["main"]["pressure"]
        current_humidiy = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]
        weather = response["weather"][0]["description"]
        visibility = response["visibility"] / 1000 
        
         # Checking for rain (OpenWeather API returns rain data as "1h" for the last hour)
        rain_chance = "No rain expected"
        if "rain" in response:
            rain_chance = f"Rain: {response['rain'].get('1h', 0)} mm in the last hour"
        
        #getting sunset/sunrise based on current day:
        sunrise = datetime.datetime.fromtimestamp(response["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(response["sys"]["sunset"])
        current_time = datetime.datetime.now()
        
        #converting to 12-hour format
        sunrise = sunrise.strftime("%Y-%m-%d %H:%M:%S")
        sunset = sunset.strftime("%Y-%m-%d %H:%M:%S")
        current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        #displaying weather data
        return f"""Weather Report for {city}, {response['sys']['country']}:
        Temperature: {current_temperature}°C
        Pressure: {current_pressure} hPa
        Humidity: {current_humidiy}%
        Weather: {weather}
        Wind Speed: {wind_speed} m/s
        Visibility: {visibility} km
        {rain_chance}
        Sunrise: {sunrise}
        Sunset: {sunset}
        Current Time: {current_time}"""   
    #if data not found, return message:
    return "Data not found for that city"

def get_user_ip_address_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        location_data = response.json()
        city, country = location_data["city"], location_data["country"]
        return city, country
    except requests.RequestException as e:
        print(f"Error getting location: {e}")
        return None, None

def chat_bot(user_input):
    if "weather" in user_input.lower(): #cheking for the word weather in user input, case insensitive
        if "today" in user_input or "how is the weather" in user_input:
            city, country = get_user_ip_address_location()
            if city:
                return get_weather(city)
            else:
                return "Sorry, I couldn't determine your location. Please specify a city."
        # parse city from user input
        if "in" in user_input.lower(): #if in found in input:
            city = user_input.lower().split("in")[-1].strip() #split the input on "in" and take the last part as city
        else:
            city = user_input.strip()
        return get_weather(city)
    
      # Check for common greetings or simple responses
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if any(greeting in user_input for greeting in greetings):
        return "Hello! How can I assist you today?"

    # Check for thank you messages
    gratitude = ["thank you", "thanks", "appreciate", "appreciated", "okay", "ok", "great"]
    if any(gratitude in user_input for gratitude in gratitude):
        return "You're welcome! 😊"

    # Check for asking about the bot's status
    if "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"

    # Check for exit command
    if "exit" in user_input:
        return "Goodbye! Have a great day!"

    else: #if no weather in input, general chat bot response using hugging face model.
        payload = {"inputs": user_input}
        response = requests.post(HF_URL, headers=HEADERS, json=payload).json()
        if isinstance(response, list):
            return response[0]['generated_text']
        return "I didn't understand that." #if no response from hugging face, return default message


"""#main loop for interacting with user
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    print("Weather_Bot:", chat_bot(user_input)) """