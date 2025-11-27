import requests
import json
import sqlite3
from datetime import datetime
import os

class WeatherDataLogger:
    """Handles database operations for logging weather data"""
    
    def __init__(self, db_name="weather_data.db"):
        self.db_name = db_name
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with required table"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Drop existing table to recreate with new structure
        cursor.execute('DROP TABLE IF EXISTS weather_logs')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity INTEGER NOT NULL,
                pressure INTEGER NOT NULL,
                wind_speed REAL NOT NULL,
                weather_condition TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                api_response TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(" Database initialized with new structure!")
    
    def log_weather_data(self, city_name, temperature, humidity, pressure, wind_speed, weather_condition, api_response):
        """Log weather data to database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO weather_logs 
            (city_name, temperature, humidity, pressure, wind_speed, weather_condition, timestamp, api_response)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (city_name, temperature, humidity, pressure, wind_speed, weather_condition, timestamp, json.dumps(api_response)))
        
        conn.commit()
        conn.close()
        print(f" Weather data for {city_name} logged successfully!")
    
    def get_logs(self, limit=10):
        """Retrieve recent weather logs"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM weather_logs 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        logs = cursor.fetchall()
        conn.close()
        return logs

class WeatherAPI:
    """Handles API interactions with OpenWeatherMap"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_data(self, city_name):
        """Fetch weather data for a given city"""
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric'  # For Celsius temperature
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            data = response.json()
            
            # Validate API response
            if data.get('cod') != 200:
                raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to weather API: {str(e)}")
        except ValueError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}")

class WeatherProcessor:
    """Processes and extracts relevant weather information"""
    
    @staticmethod
    def extract_weather_info(api_response):
        """Extract relevant weather information from API response"""
        try:
            city_name = api_response['name']
            temperature = api_response['main']['temp']
            humidity = api_response['main']['humidity']
            pressure = api_response['main']['pressure']
            wind_speed = api_response.get('wind', {}).get('speed', 0)  # Handle missing wind data
            weather_condition = api_response['weather'][0]['description']
            
            # Convert timestamp to readable format
            timestamp = api_response.get('dt', None)
            if timestamp:
                local_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            else:
                local_time = "N/A"
            
            return {
                'city_name': city_name,
                'temperature': temperature,
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'weather_condition': weather_condition,
                'local_time': local_time,
                'full_response': api_response
            }
        except KeyError as e:
            raise ValueError(f"Invalid API response format: Missing key {str(e)}")

class WeatherApplication:
    """Main application class that orchestrates the weather app"""
    
    def __init__(self, api_key):
        self.weather_api = WeatherAPI(api_key)
        self.data_logger = WeatherDataLogger()
        self.weather_processor = WeatherProcessor()
    
    def get_weather_for_city(self, city_name):
        """Get weather data for a single city and log it"""
        try:
            # Validate input
            if not city_name or not city_name.strip():
                raise ValueError("City name cannot be empty")
            
            city_name = city_name.strip()
            
            print(f"\n  Fetching weather data for: {city_name}")
            
            # Get data from API
            api_response = self.weather_api.get_weather_data(city_name)
            
            # Process the data
            weather_info = self.weather_processor.extract_weather_info(api_response)
            
            # Display results
            self._display_weather_info(weather_info)
            
            # Log to database
            self.data_logger.log_weather_data(
                weather_info['city_name'],
                weather_info['temperature'],
                weather_info['humidity'],
                weather_info['pressure'],
                weather_info['wind_speed'],
                weather_info['weather_condition'],
                weather_info['full_response']
            )
            
            return weather_info
            
        except Exception as e:
            print(f" Error: {str(e)}")
            return None
    
    def _display_weather_info(self, weather_info):
        """Display weather information in a user-friendly format"""
        print("\n" + "="*50)
        print(f" CITY: {weather_info['city_name']}")
        print("="*50)
        print(f" Local Time: {weather_info['local_time']}")
        print(f"  Temperature: {weather_info['temperature']}°C")
        print(f" Humidity: {weather_info['humidity']}%")
        print(f" Pressure: {weather_info['pressure']} hPa")
        print(f" Wind Speed: {weather_info['wind_speed']} m/s")
        print(f" Condition: {weather_info['weather_condition'].title()}")
        print("="*50)
    
    def show_recent_logs(self):
        """Display recent weather logs"""
        print("\n RECENT WEATHER LOGS")
        print("="*80)
        
        logs = self.data_logger.get_logs(limit=5)
        
        if not logs:
            print("No logs found.")
            return
        
        for log in logs:
            # Safely unpack with proper error handling
            if len(log) == 9:  # New format with pressure and wind_speed
                log_id, city, temp, humidity, pressure, wind_speed, condition, timestamp, _ = log
                timestamp = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                print(f"{log_id}. {city} | {temp}°C | {humidity}% | {pressure}hPa | {wind_speed}m/s | {condition} | {timestamp}")
            else:
                # Handle old format logs gracefully
                print(f"Log format: {len(log)} columns - Data: {log}")

def main():
    """Main function to run the weather application"""
    
    # API Key - You need to get this from OpenWeatherMap
    API_KEY = "dd10d23bf3e0104bd4e939edbcb06ea9"  # Replace with your actual API key
    
    # Check if API key is set
    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        print(" Please get a free API key from OpenWeatherMap and replace the API_KEY variable")
        print(" Visit: https://openweathermap.org/api")
        return
    
    # Initialize application
    app = WeatherApplication(API_KEY)
    
    print(" WELCOME TO REAL-TIME WEATHER INFORMATION & DATA LOGGER ")
    print("="*60)
    
    while True:
        print("\nOptions:")
        print("1. Get weather for a city")
        print("2. View recent logs")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            city_name = input("Enter city name: ").strip()
            if city_name:
                app.get_weather_for_city(city_name)
            else:
                print(" Please enter a valid city name.")
        
        elif choice == '2':
            app.show_recent_logs()
        
        elif choice == '3':
            print("👋 Thank you for using the Weather App! Goodbye!")
            break
        
        else:
            print(" Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()