//#include "Adafruit_FONA.h"
#include <ESP8266WiFi.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
//#include <Adafruit_SSD1306.h> // for OLED display
#include <Adafruit_PCD8544.h>  // include adafruit PCD8544 (Nokia 5110) library
#include "SIM7600.h"

#define ARDUINO_BAUD 9600

//#define SCREEN_WIDTH 128 // OLED display
//#define SCREEN_HEIGHT 64 // OLED display
//#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
//Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET); // OLED display

Adafruit_PCD8544 display = Adafruit_PCD8544(D4, D3, D2, D1, D0); // Nokia 5110 display

const static int powerpin = 14;

int loopCount = 0;

bool simReady = false;
bool isRinging = false;

const int textSize = 1;
const int statsSize = 1;
const int statMax = 10;
const int displayMax = 24;
const int displayContrast = 60;

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
  display.setCursor(0, 0);              // Start at top-left corner
  display.println(currentStats);
  display.display();

  //Serial.print("displayStats() ~ ");
  //Serial.println(currentStats);
}

void displayText()
{
  display.setTextSize(textSize); // Normal 1:1 pixel scale
  display.setCursor(0, 20);             // Start at top-left corner

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

bool prepDisplay() {

  /* OLED start
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64 // for OLED screen
    Serial.println(F("SSD1306 allocation failed"));
  }
  display.setTextColor(SSD1306_WHITE);  // Draw white text
  display.cp437(true);                  // Use full 256 char 'Code Page 437' font
  */ /* OLED finish */

  /* Nokia start */
  display.begin(); // for Nokia screen
  display.setTextColor(BLACK);
  display.setContrast(displayContrast);
  display.setRotation(2);
  /* Nokia finish */
  
  currentStats = "Initializing";
  clearDisplay();
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

void answer() {
  sim7600.Answer();
  currentText = "Talking";
  clearDisplay();
}

void turnOffSim() {
  Serial.print("turnOffSim() ~ turning off SIM");
  sim7600.PowerOff();
  currentStats = "SIM OFF";
  clearDisplay();
}

void turnOnSim() {
  Serial.print("turnOnSim() ~ Starting SIM");
  sim7600.PowerOn(powerpin);
  currentStats = "SIM INIT";
  clearDisplay();
}

void getSimSignal() {
  char* mysignal = cleanChar(sim7600.GetSignal());
  char* newsignal = "";
  for (int i = 0; mysignal[i] != '\0'; i++) {
    if (mysignal[i] == ':') {
      mysignal[0] = mysignal[i+2];
      newvoltage[1] = mysignal[i+3];
      newvoltage[2] = mysignal[i+4];
      newvoltage[3] = mysignal[i+5];
      newvoltage[4] = mysignal[i+6];
      newvoltage[5] = mysignal[i+7];
    }
  }

  Serial.print("getSimSignal() ~ mysignal: ");
  Serial.println(mysignal);
  currentStats = currentStats + " S:" + mysignal;
  //clearDisplay();
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
  Serial.print("getSimVoltage() ~ newvoltage: ");
  Serial.println(newvoltage);
  currentStats = newvoltage;
  //clearDisplay();
}

void setup()
{
  Serial.begin(ARDUINO_BAUD);
  Serial.setTimeout(100);

  WiFi.mode(WIFI_OFF);

  delay(500);
  prepDisplay();
  delay(5000);
  turnOffSim();
  delay(5000);
  turnOnSim();
}

void loop()
{
  loopCount++;
  //Serial.print("loopCount: ");
  //Serial.println(loopCount);

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
      currentText = "Ready";
      clearDisplay();
    }
    
    if (mystring.indexOf("RING") != -1) {
      clearDisplay();
      currentText = "RING";
      isRinging = true;
      displayText();
    } 

    if (mystring.indexOf("MISSED") != -1) {
      clearDisplay();
      currentText = mystring;
      isRinging = false;
      displayText();
    }
  }

  if (keypad == "C") {
    //startPhoneCall("12076192651");
    char* mynumber = strdup(currentNumber.c_str());
    startPhoneCall(mynumber);
  }

  if (keypad == "O") {
    answer();
    currentNumber = "";
  }

  if (keypad == "H") {
    hangup();
    currentNumber = "";
    clearDisplay();
  }

  //if (keypad == "C") {
    //turnOffSim();
    //getSimVoltage();
  //}

  if (simReady) {
    if (loopCount > 10) {
      getSimVoltage();
      getSimSignal();
      clearDisplay();
      loopCount = 0;
    }
  }
  //Serial.println("loop() ~ STOP");
}
