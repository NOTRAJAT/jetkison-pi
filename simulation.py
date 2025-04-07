#simulation
import time
import mysql.connector
from datetime import datetime
import signal
import board
import busio
import adafruit_bmp280

# Global flag
running = True

def stop_handler(signum, frame):
    global running
    print("Stopping script...")
    running = False

# Register signal handlers
signal.signal(signal.SIGTERM, stop_handler)
signal.signal(signal.SIGINT, stop_handler)

# BMP280 setup
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Optional: set sea-level pressure for accurate altitude
bmp280.sea_level_pressure = 1013.25

# MySQL setup
db = mysql.connector.connect(
    host="localhost",
    user="newuser",
    password="newpass",
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

def log_to_db(temperature, pressure):
    timestamp = datetime.now()
    sql = "INSERT INTO bmp280_readings (temperature, pressure, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(sql, (temperature, pressure, timestamp))
    db.commit()

if __name__ == "__main__":
    while running:
        temp = round(bmp280.temperature, 2)
        pres = round(bmp280.pressure, 2)
        log_to_db(temp, pres)
        print(f"[{datetime.now()}] BMP280 → Temp: {temp}°C | Pressure: {pres} hPa")
        time.sleep(10)
