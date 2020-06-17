#include "Keypad.h"
#include "Adafruit_FONA.h"
#include <SPI.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "Waveshare_SIM7600.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define SIM_RX 2
#define SIM_TX 3
#define SIM_RST 40 // Dummy
#define SIM_BAUD 115200

#define ARDUINO_BAUD 9600

//SoftwareSerial SimSerial(SIM_RX, SIM_TX);
//SoftwareSerial SIM7600SS = SoftwareSerial(SIM_RX, SIM_TX);
//SoftwareSerial *SIM7600Serial = &SIM7600SS;

//Adafruit_FONA SIM7600 = Adafruit_FONA(SIM_RST);

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

bool serialDebug = false;
char phone_number[] = "12076192651";

const int defaultTextSize = 2;

const byte KP_ROWS = 4; //four rows
const byte KP_COLS = 4; //three columns
char keys[KP_ROWS][KP_COLS] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}};

String current_number = "";
String current_stats = "";
String current_voltage = "0";

byte kpRowPins[KP_ROWS] = {12, 11, 10, 9}; //connect to the row pinouts of the keypad
byte kpColPins[KP_COLS] = {8, 7, 6, 5};    //connect to the column pinouts of the keypad

Keypad keypad = Keypad(makeKeymap(keys), kpRowPins, kpColPins, KP_ROWS, KP_COLS);

void displayStats(String text)
{
  display.setTextSize(defaultTextSize); // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);  // Draw white text
  display.setCursor(0, 0);              // Start at top-left corner
  display.cp437(true);                  // Use full 256 char 'Code Page 437' font

  display.println(text);
  display.display();
}

void clearDisplay()
{
  display.clearDisplay();
  //current_stats = current_voltage;
  displayStats(current_stats);
}

void getSimVoltage()
{
  //if (SimSerial.available()) {
  //  SimSerial.write("AT+CBC\n");
  //} else {
  //  Serial.write("SimSerial is not available");
  //}

  //if (!serialDebug) { Serial.println("AT+CBC"); }
  if (!serialDebug)
  {
    sim7600.PhoneCall(phone_number);
  }
}

void displayText(String text)
{
  display.setTextSize(defaultTextSize); // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);  // Draw white text
  display.setCursor(0, 20);             // Start at top-left corner
  display.cp437(true);                  // Use full 256 char 'Code Page 437' font

  display.println(text);
  display.display();
  //delay(2000);
}

void testdrawchar(void)
{
  display.clearDisplay();

  display.setTextSize(defaultTextSize); // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);  // Draw white text
  display.setCursor(10, 0);             // Start at top-left corner
  display.cp437(true);                  // Use full 256 char 'Code Page 437' font

  display.println(F("scroll"));
  // Not all the characters will fit on the display. This is normal.
  // Library will draw what it can and the rest will be clipped.
  //for(int16_t i=0; i<256; i++) {
  //  if(i == '\n') display.write(' ');
  //  else          display.write(i);
  //}

  display.display();
  delay(2000);
}

void checkSimStatus()
{
  current_stats = "checking";
  clearDisplay();

  uint8_t answer = 0;
  int timeout = 10;
  int mycount = 0;
  while (answer == 0 && mycount < timeout)
  { // Send AT every two seconds and wait for the answer
    answer = sim7600.sendATcommand("AT", "OK", 1000);
    //delay(1000);
    mycount++;
  }

  if (answer == 1) {
    current_stats = "SIM GOOD!";
  } else {
    current_stats = "NO SIM";
  }
  clearDisplay();
}

void setup()
{
  Serial.begin(ARDUINO_BAUD);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
  {
    if (serialDebug)
    {
      Serial.println(F("SSD1306 allocation failed"));
    }
  }

  display.display();
  delay(500); // Pause for 2 seconds
  display.clearDisplay();

  current_stats = "100% - >>>";
  clearDisplay();

  // Let's setup the SIM chip
  checkSimStatus();
  //SimSerial.begin(SIM_BAUD);

  //Serial.println("Interfacing SIM7600 GSM GPS Module with Maker UNO");
  //Serial.println("Initializing... (May take a minute)");

  //SIM7600Serial->begin(SIM_BAUD);
  //if (!SIM7600.begin(*SIM7600Serial)) {
  //  Serial.println("Couldn't find SIM7600");
  //  //while (1);
  //}
  //Serial.println(F("SIM7600 is OK"));

  // Print SIM card IMEI number.
  //char imei[16] = {0}; // MUST use a 16 character buffer for IMEI!
  //uint8_t imeiLen = SIM7600.getIMEI(imei);
  //if (imeiLen > 0) {
  //  Serial.print("SIM card IMEI: "); Serial.println(imei);
  //}

  //SIM7600Serial->print("AT+CNMI=2,1\r\n");  // Set up the SIM800L to send a +CMTI notification when an SMS is received
  //Serial.println("GSM is ready!");
}

void loop()
{
  char key = keypad.getKey();

  if (key != NO_KEY)
  {
    current_number = current_number + key;
    if (key == 'D')
    {
      if (serialDebug)
      {
        Serial.println("Delete Key Hit");
      }
      current_number = "";
      clearDisplay();
    }
    if (key == 'B')
    {
      //getSimVoltage();
      checkSimStatus();
    }
    if (serialDebug)
    {
      Serial.println(current_number);
    }
    displayText(current_number);
  }

  //SimSerial.listen();
  //if (SimSerial.available()) {
  //  Serial.print("Data from SimSerial: ");
  //  while (SimSerial.available() > 0) {
  //    char inByte = SimSerial.read();
  //    Serial.write(inByte);
  //  }
  //  Serial.println();
  //}

  //if (Serial.available()) {
  //  current_voltage = "";
  //  while (Serial.available() > 0) {
  //    char inByte = Serial.read();
  //    current_voltage = current_voltage + inByte;
  //  }
  //}
}
