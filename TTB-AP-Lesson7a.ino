// Using an Arduino with Python LESSON 7: Measuring Temperature and Humidity With the DHT11.
// https://www.youtube.com/watch?v=kF6biceKwFY
// https://toptechboy.com/using-an-arduino-with-python-lesson-7-measuring-temperature-and-humidity-with-the-dht11/

#include <DHT.h>              // DHT11/22 sensor library.

// DHT11/22 sensor defines.
#define DHTTYPE11 DHT11       // Blue module, DHT11 defined as 11 in <DHT.h>.
#define DHTTYPE22 DHT22       // White module, DHT22 defined as 22 in <DHT.h>.

// Arduino analog I/O pin defines.
#define POT1PIN A0             // Also known as IO pin 21.

// Arduino digital I/O pin defines.
#define DHT11PIN 3
#define DHT22PIN 4

//Code loop job defines.
#define JOB1CYCLE 100         // Job 1 execution cycle: 0.1s - Get the data: Read the potentiometers.
#define JOB2CYCLE 1000        // Job 2 execution cycle: 1s   - Get the data: Read the DHT11 sensor.
#define JOB3CYCLE 2000        // Job 3 execution cycle: 2s   - Get the data: Read the DHT22 sensor..
#define JOB4CYCLE 100         // Job 4 execution cycle: 0.1s - Share the results: Output data to the serial console.

//Sensor object initialisations.
DHT myDHT11(DHT11PIN, DHTTYPE11);     // Initialize the DHT11 sensor for normal 16mhz Arduino (default delay = 6).
DHT myDHT22(DHT22PIN, DHTTYPE22);     // Initialize the DHT22 sensor for normal 16mhz Arduino (default delay = 6).

void setup() {
  // Initialise the potentiometer pins.
  pinMode(POT1PIN, INPUT);
  // Start the DHT11 sensor.
  myDHT11.begin();
  // Start the DHT22 sensor.
  myDHT22.begin();
  // Start the serial port.
  Serial.begin(115200);
  while(!Serial); // Wait for the serial I/O to start.
}

void loop() {
  // Initialise the potentiometer variable to something that indicates an invalid reading.
  static int pot1Value = -1;
  // Initialise the DHT variables to something that indicates an invalid reading.
  static float temperatureDHT11 = NAN;
  static float humidityDHT11    = NAN;
  static float temperatureDHT22 = NAN;
  static float humidityDHT22    = NAN;
  // Record the current time. Used for all jobs and ensures they are synchronised.
  unsigned long timeNow = millis();
  // Job variables. Set to timeNow to allow the sensors to settle.
  static unsigned long timeMark1 = timeNow; // Last time Job 1 was executed.
  static unsigned long timeMark2 = timeNow; // Last time Job 2 was executed.
  static unsigned long timeMark3 = timeNow; // Last time Job 3 was executed.
  static unsigned long timeMark4 = timeNow; // Last time Job 4 was executed.
  // Job 1 - Get the data: Read the potentiometers.
  if (timeNow - timeMark1 >= JOB1CYCLE) {
    timeMark1 = timeNow;
    // Do something...
    pot1Value = analogRead(POT1PIN);
  }
  // Job 2 - Get the data: Read the DHT11 sensor.
  if (timeNow - timeMark2 >= JOB2CYCLE) {
    timeMark2 = timeNow;
    // Do something...   
    temperatureDHT11 = myDHT11.readTemperature();
    humidityDHT11 = myDHT11.readHumidity();
  }
  // Job 3 - Get the data: Read the DHT22 sensor.
  if (timeNow - timeMark3 >= JOB3CYCLE) {
    timeMark3 = timeNow;
    // Do something...
    temperatureDHT22 = myDHT22.readTemperature();
    humidityDHT22 = myDHT22.readHumidity();
  }
  // Job 4 - Share the results: Output CSV data to the serial console.
  if (timeNow - timeMark4 >= JOB4CYCLE) {
    timeMark4 = timeNow;
    // Do something...
    Serial.print(pot1Value);
    Serial.print(",");
    Serial.print(temperatureDHT11);
    Serial.print(",");
    Serial.print(humidityDHT11);
    Serial.print(",");
    Serial.print(temperatureDHT22);
    Serial.print(",");
    Serial.print(humidityDHT22);
    Serial.println();
  }
}

// EOF
