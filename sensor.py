import time
import random
import mysql.connector
from datetime import datetime

# MySQL setup
db = mysql.connector.connect(
    host="localhost",
    user="iotuser",
    password="iotpass",
    database="iot_data"
)
cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmp280_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    pressure FLOAT,
    timestamp DATETIME
)
""")
db.commit()

def simulate_bmp280():
    # Simulated realistic values
    temperature = round(random.uniform(20.0, 35.0), 2)   # °C
    pressure = round(random.uniform(950.0, 1050.0), 2)   # hPa
    return temperature, pressure

def log_to_db(temperature, pressure):
    timestamp = datetime.now()
    sql = "INSERT INTO bmp280_readings (temperature, pressure, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(sql, (temperature, pressure, timestamp))
    db.commit()

if __name__ == "__main__":
    while True:
        temp, pres = simulate_bmp280()
        log_to_db(temp, pres)
        print(f"[{datetime.now()}] Simulated BMP280 → Temp: {temp}°C | Pressure: {pres} hPa")
        time.sleep(10)  # Log every 10 seconds
