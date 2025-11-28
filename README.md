Real-Time Weather Information & Data Logger
------------------------------------------------------------------------------------------
 A Python weather application that provides real-time weather information and data logging capabilities. The project is organized with a clear folder structure and uses SQLite for data storage.
 
General / Positive Qualities
 -----------------------------------------------------------------------------------------
* Real-time Weather Data: Fetches current weather information

* Data Logging: Stores weather data in SQLite database
 
* Local Storage: Uses weather_data.db for persistent data storage

* Python Implementation: Organized as a Python project

  Project Structure
  -----------------------------------------------------------------------------------------
  weather_app/
├── weather_app/       
├── weather_data.db
     
 Repository
------------------------------------------------------------------------------------------
* SQLite Database used for lightweight, file-based storage

* Single-table design with weather_data table

* Automatic table creation on application initialization

* Local file storage (weather_data.db) for portability

 Database Architecture 
 ----------------------------------------------------------------------------------------
  ```sql
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
            )```

data base:example of output
--------------------------------------------------------------------------------------------
Main Menu:
1. Check weather
2. View history
3. Exit
Enter your choice (1-3): 2

== Recent Weather Queries ==

Paris: 32.21°C, 25.0% humidity, 2.4 m/s wind
Condition: overcast clouds
Time: 2025-11-27 23:48:11

London: 13.08°C, 90.0% humidity, 3.68 m/s wind
Condition: overcast clouds
Time: 2025-11-27 23:47:40

Vancouver: 30.21°C, 86.0% humidity, 1.2 m/s wind
Condition: broken clouds
Time: 2025-11-27 23:37:55

Tokyo: 32.72°C, 75.0% humidity, 3.68 m/s wind
Conditions: broken clouds
Time: 2025-11-27 23:22:09

Mumbai: 20.00°C, 80.0% humidity, 2.23 m/s wind
Conditions: broken clouds
Time: 2025-11-27 23:20:15


User Encounter
-----------------------------------------------------------------------------------------
* Persistent History: Maintains complete query history across application sessions

* Instant Feedback: Real-time weather data retrieval with loading indicators

* Zero Setup: Automatic configuration and database initialization on first run

* Error Resilience: Graceful handling of network issues and invalid inputs without crashes

Error Management 
------------------------------------------------------------------------------------------
* Invalid API keys: Provides clear error messages

* Network issues: Handles connection timeouts and failures

* Invalid city names: Validates input and provides suggestions

* Database errors: Manages database connection issues

* User input validation: Ensures proper input format

 Support
----------------------------------------------------------------------------------------- 
Active internet connection

Valid OpenWeatherMap API key

Python 3.6+ installed

Write permissions for database creation 


 
