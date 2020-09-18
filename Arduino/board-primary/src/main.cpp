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

const int defaultTextSize = 2;
const int statmax = 10;
const int displaymax = 10;

String current_number = "";
String current_stats = "";
String current_voltage = "0";

bool isNumeric(String str) {
   for (int i = 0; i < str.length(); i++)
      if (isdigit(str[i]) == false)
         return false; //when one non numeric value is found, return false
      return true;
}

char* cleanChar(char* olddata) {
  char* newdata = (char*) malloc( 100 );
  int n = 0;
  for (int i = 0; olddata[i] != '\0'; i++) {
    if (olddata[i] != '\n') {
        newdata[n] = olddata[i];
        Serial.print(n);
        Serial.print(" - ");
        Serial.print(newdata[n]);
        Serial.println("");
        n++;
      }
  }
  Serial.print("cleanChar() ~ OUT: ");
  Serial.println(newdata);
  return newdata;
}

void displayStats(String text)
{

  String newtext = "";

  for(int i = 0; i < text.length() && i <= statmax; i++) {
    newtext = newtext + text[i]; //get character at position i
  }

  display.setTextSize(defaultTextSize); // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);  // Draw white text
  display.setCursor(0, 0);              // Start at top-left corner
  display.cp437(true);                  // Use full 256 char 'Code Page 437' font

  display.println(text);
  display.display();

  Serial.print("displayStats() ~ ");
  Serial.println(text);
}

void clearDisplay()
{
  display.clearDisplay();
  //current_stats = current_voltage;
  displayStats(current_stats);
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

  Serial.print("displayText() ~ ");
  Serial.println(text);
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

void startPhoneCall(char* number) {
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

void turnOnSim() {
  sim7600.PowerOn();
  clearDisplay();
  displayText("Serial Ready");
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
  current_stats = newvoltage;
  clearDisplay();
}

void setup()
{
  Serial.begin(ARDUINO_BAUD);

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

  current_stats = "Ready";
  clearDisplay();

  turnOnSim();
}

void loop()
{
  String keypad; // for incoming serial data

  if (Serial.available() > 0) {
    // read the incoming byte:
    keypad = Serial.readString();

    // say what you got:
    Serial.print("Numpad: ");
    Serial.println(keypad);
    if (isNumeric(keypad)) {
      current_number = current_number + keypad;
      clearDisplay();
      displayText(current_number);
    }
  }

  char* mybuff;
  mybuff = sim7600.checkBuffer(500);
  if (mybuff[0] != '\0') {
    mybuff = cleanChar(mybuff);
    Serial.print("SIM notification: ");
    Serial.println(mybuff);
  }

  if (keypad == "A") {
    //startPhoneCall("12076192651");
    char* mynumber = strdup(current_number.c_str());
    startPhoneCall(mynumber);
  }

  if (keypad == "B") {
    hangup();
    current_number = "";
    clearDisplay();
  }

  if (keypad == "C") {
    //turnOffSim();
    getSimVoltage();
  }
}
