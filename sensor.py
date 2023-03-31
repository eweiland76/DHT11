import time
import Adafruit_DHT
from Adafruit_IO import Client, Feed, RequestError

# Set up Adafruit IO credentials
ADAFRUIT_IO_USERNAME = 'your_username'
ADAFRUIT_IO_KEY = 'your_key'

# Set up DHT11 sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin where the DHT11 sensor is connected

# Set up Adafruit IO feeds
TEMPERATURE_FEED_NAME = 'temperature'
HUMIDITY_FEED_NAME = 'humidity'

# Create an instance of the Adafruit IO client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create temperature feed if it doesn't exist
try:
    temperature_feed = aio.feeds(TEMPERATURE_FEED_NAME)
except RequestError:
    temperature_feed = Feed(name=TEMPERATURE_FEED_NAME)
    temperature_feed = aio.create_feed(temperature_feed)

# Create humidity feed if it doesn't exist
try:
    humidity_feed = aio.feeds(HUMIDITY_FEED_NAME)
except RequestError:
    humidity_feed = Feed(name=HUMIDITY_FEED_NAME)
    humidity_feed = aio.create_feed(humidity_feed)

# Main loop
while True:
    # Read data from DHT11 sensor
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    # If data is valid, send it to Adafruit IO
    if humidity is not None and temperature is not None:
        aio.send_data(temperature_feed.key, temperature)
        aio.send_data(humidity_feed.key, humidity)
        print("Data sent to Adafruit IO: Temperature = {} C, Humidity = {} %".format(temperature, humidity))

    # Wait for 5 minutes before reading again
    time.sleep(300)
