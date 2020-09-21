//#include "Adafruit_FONA.h"
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "SIM7600.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define SIM_RX 2
#define SIM_TX 3
#define SIM_RST 40 // Dummy
#define SIM_BAUD 9600

#define ARDUINO_BAUD 9600

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

char phone_number[] = "12076192651";

bool simReady = false;

const int textSize = 2;
const int statsSize = 1;
const int statMax = 10;
const int displayMax = 10;

String currentNumber = "";
String currentStats = "";
String currentText = "";
String currentVoltage = "0";

bool isNumeric(String str) {
   for (int i = 0; i < str.length(); i++)
      if (isdigit(str[i]) == false)
         return false; //when one non numeric value is found, return false
      return true;
}

String charToString(char* olddata) {
  String newdata = "";
  for (int i = 0; olddata[i] != '\0'; i++) {
    newdata += olddata[i];
  }
  return newdata;
}

char* cleanChar(char* olddata) {
  //Serial.print("cleanChar() ~ IN: ");
  //Serial.println(olddata);
  char* newdata = (char*) malloc( 100 );
  int n = 0;
  for (int i = 0; olddata[i] != '\0'; i++) {
    if (olddata[i] != '\n' && olddata[i] != '\r') {
        newdata[n] = olddata[i];
        //Serial.print(n);
        //Serial.print(" - ");
        //Serial.print(newdata[n]);
        //Serial.println("");
        n++;
      }
  }
  //Serial.print("cleanChar() ~ OUT: ");
  //Serial.println(newdata);
  return newdata;
}

void displayStats()
{
  String newtext = "";

  display.setTextSize(statsSize); // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);  // Draw white text
  display.setCursor(0, 0);              // Start at top-left corner
  display.cp437(true);                  // Use full 256 char 'Code Page 437' font
  display.println(currentStats);
  display.display();

  //Serial.print("displayStats() ~ ");
  //Serial.println(currentStats);
}

void displayText()
{
  display.setTextSize(textSize); // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);  // Draw white text
  display.setCursor(0, 20);             // Start at top-left corner
  display.cp437(true);                  // Use full 256 char 'Code Page 437' font

  display.println(currentText);
  display.display();
  //delay(2000);

  //Serial.print("displayText() ~ ");
  //Serial.println(currentText);
}

void clearDisplay()
{
  display.clearDisplay();
  display.display();
  //current_stats = current_voltage;
  displayStats();
  displayText();
}

void checkSimStatus()
{
  currentStats = "checking";
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
    currentStats = "SIM GOOD!";
  } else {
    currentStats = "NO SIM";
  }
  clearDisplay();
}

void startPhoneCall(char* number) {
  sim7600.PhoneCall(number);
  currentText = "Calling";
  clearDisplay();
}

void hangup() {
  sim7600.HangUp();
  currentText = "Hangup";
  clearDisplay();
}

void turnOffSim() {
  sim7600.PowerOff();
  currentStats = "SIM OFF";
  clearDisplay();
}

void turnOnSim() {
  sim7600.PowerOn();
  currentStats = "SIM INIT";
  clearDisplay();
}

void getSimVoltage() {
  char* myvoltage = cleanChar(sim7600.GetVoltage());
  char* newvoltage = (char*) malloc(6);
  for (int i = 0; myvoltage[i] != '\0'; i++) {
    if (myvoltage[i] == ':') {
      newvoltage[0] = myvoltage[i+2];
      newvoltage[1] = myvoltage[i+3];
      newvoltage[2] = myvoltage[i+4];
      newvoltage[3] = myvoltage[i+5];
      newvoltage[4] = myvoltage[i+6];
      newvoltage[5] = myvoltage[i+7];
    }
  }
  //Serial.print("getSimVoltage() ~ newvoltage: ");
  //Serial.println(newvoltage);
  currentStats = newvoltage;
  clearDisplay();
}

void setup()
{
  Serial.begin(ARDUINO_BAUD);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    //Serial.println(F("SSD1306 allocation failed"));
  }
  delay(500); // Pause for 2 seconds
  currentStats = "Initializing";
  clearDisplay();

  turnOnSim();
}

void loop()
{
  //Serial.println("loop() ~ START");
  String keypad; // for incoming serial data

  if (Serial.available() > 0) {
    // read the incoming byte:
    keypad = Serial.readString();

    // say what you got:
    Serial.print("Numpad: ");
    Serial.println(keypad);
    if (isNumeric(keypad)) {
      currentNumber += keypad;
      currentText = currentNumber;
      clearDisplay();
      displayText();
    }
  }

  char* mybuff = sim7600.checkBuffer(500, 10);

  //String mybuff = sim7600.checkBufferString(100);

  if (mybuff[0] != '\0') {
  //if (mybuff.length() > 0) {
    //mybuff = cleanString(mybuff);
    mybuff = cleanChar(mybuff);
    //char* buffchar = cleanChar(strdup(mybuff.c_str()));
    Serial.print("SIM notification: ");
    Serial.println(mybuff);
    String mystring = charToString(mybuff);
    
    if (mystring.indexOf("PB DONE") != -1) {
      simReady = true;
      currentStats = "Ready";
      clearDisplay();
    }
    
    if (mystring.indexOf("RING") != -1) {
      clearDisplay();
      currentText = "RING";
      displayText();
    } 
    if (mystring.indexOf("MISSED") != -1) {
      clearDisplay();
      currentText = "MISSED CALL";
      displayText();
    }
  }

  if (keypad == "A") {
    //startPhoneCall("12076192651");
    char* mynumber = strdup(currentNumber.c_str());
    startPhoneCall(mynumber);
  }

  if (keypad == "B") {
    hangup();
    currentNumber = "";
    clearDisplay();
  }

  if (keypad == "C") {
    //turnOffSim();
    getSimVoltage();
  }

  if (simReady) {
    getSimVoltage();
  }

  //Serial.println("loop() ~ STOP");
}
