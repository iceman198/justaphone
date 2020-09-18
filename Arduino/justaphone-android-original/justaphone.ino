#include "Keypad.h"
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "SIM7600.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

const byte KP_ROWS = 4; //four rows
const byte KP_COLS = 4; //three columns
char keys[KP_ROWS][KP_COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

String current_number = "";
String current_stats = "";

byte kpRowPins[KP_ROWS] = {12, 11, 10, 9}; //connect to the row pinouts of the keypad
byte kpColPins[KP_COLS] = {8, 7, 6, 5}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad(makeKeymap(keys), kpRowPins, kpColPins, KP_ROWS, KP_COLS);

void setup()
{
  Serial.begin(9600);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    //Serial.println(F("SSD1306 allocation failed"));
  }

  display.display();
  delay(500); // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();

  // Draw a single pixel in white
  display.drawPixel(10, 10, SSD1306_WHITE);

  display.display();
  delay(500);

  current_stats = "100";
  clearDisplay();
}

void loop()
{
  char key = keypad.getKey();

  if (key != NO_KEY) {
    current_number = current_number + key;

    if (key == 'A') {
      startPhoneCall("12076192651");
      current_number = "";
    }
    if (key == 'B') {
      current_number = "";
      hangup();
      getSimVoltage();
    }
    if (key == 'C') {
      current_number = "";
      turnOffSim();
    }
    if (key == 'D') {
      //Serial.println("Delete Key Hit");
      current_number = "";
      clearDisplay();
    }

    delay(100);
    //Serial.println(current_number);
    displayText(current_number);
  }

  /*
    SimSerial.listen();
    if (SimSerial.available()) {
      Serial.print("Data from SimSerial: ");
      while (SimSerial.available() > 0) {
        char inByte = SimSerial.read();
        Serial.write(inByte);
      }
      Serial.println();
    }
  */
}

void clearDisplay() {
  display.clearDisplay();
  displayStats(current_stats);
}

void startPhoneCall(String number) {
  sim7600.PhoneCall(number);
  clearDisplay();
  displayText("Calling");
}

void hangup() {
  sim7600.HangUp();
  clearDisplay();
  displayText("Hangup");
}

void turnOffSim() {
  sim7600.PowerOff();
  clearDisplay();
  displayText("SIM OFF");
}

void getSimVoltage() {
  current_stats = cleansString(sim7600.GetVoltage());
  clearDisplay();
}

void displayStats(String text) {
  display.setTextSize(2);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(0, 0);     // Start at top-left corner
  display.cp437(true);         // Use full 256 char 'Code Page 437' font

  display.println(text);
  display.display();
}

void displayText(String text) {
  display.setTextSize(2);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(0, 20);     // Start at top-left corner
  display.cp437(true);         // Use full 256 char 'Code Page 437' font

  display.println(text);
  display.display();
  //delay(2000);
}

String cleansString(String olddata) {
  String newdata = "";
  for (int i = 0; i < sizeof(olddata); ++i)
  {
    // Ignore carriage returns
    if (olddata[i] != '\r' &&
      olddata[i] != 0x0D &&
      olddata[i] != '\n') {
        newdata[i] << olddata[i];
      }      
  }
}
