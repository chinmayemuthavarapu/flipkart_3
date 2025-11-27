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
