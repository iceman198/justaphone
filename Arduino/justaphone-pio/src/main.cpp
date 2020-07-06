#include "Keypad.h"
//#include "Adafruit_FONA.h"
#include <SPI.h>
#include <Wire.h>
//#include <SoftwareSerial.h>
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

//SoftwareSerial SimSerial(13, 15);
//SoftwareSerial SimSerial(SIM_RX, SIM_TX);
//SoftwareSerial SIM7600SS = SoftwareSerial(SIM_RX, SIM_TX);
//SoftwareSerial *SIM7600Serial = &SIM7600SS;

//Adafruit_FONA SIM7600 = Adafruit_FONA(SIM_RST);

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET 40 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

char phone_number[] = "12076192651";

const int defaultTextSize = 2;

int buttonY = 0;
int buttonB = 0;
int buttonG = 0;
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

//byte kpRowPins[KP_ROWS] = {12, 11, 10, 9}; //connect to the row pinouts of the keypad
//byte kpColPins[KP_COLS] = {8, 7, 6, 5};    //connect to the column pinouts of the keypad

//Keypad keypad = Keypad(makeKeymap(keys), kpRowPins, kpColPins, KP_ROWS, KP_COLS);

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
  Serial.println("cleansString() ~ OUT");
  return newdata;
}

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
  String myvoltage = cleansString(sim7600.GetVoltage());
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

  pinMode(D5, INPUT_PULLUP);
  pinMode(D3, INPUT_PULLUP);
  pinMode(D4, INPUT_PULLUP);

  current_stats = "Ready";
  clearDisplay();
}

void loop()
{
  bool keychange = false;

  buttonY = digitalRead(D5);
  buttonB = digitalRead(D3);
  buttonG = digitalRead(D4);
  if (buttonY == LOW) {
    if (current_number != "Y") {
      startPhoneCall("12076192651");
      keychange = true;
    }
    current_number = "Y";
  } else if (buttonB == LOW) {
    if (current_number != "B") {
      hangup();
      keychange = true;
    }
    current_number = "B";
  } else if (buttonG == LOW) {
    if (current_number != "G") {
      //turnOffSim();
      getSimVoltage();
      keychange = true;
    }
    current_number = "G";
  } else {
    current_number = "*";
  }

  //char key = keypad.getKey();

  //if (key != NO_KEY) {
    //current_number = current_number + key;

    //if (key == 'A') {
    //  startPhoneCall("12076192651");
    //  current_number = "";
    //}
    //if (key == 'B') {
    //  current_number = "";
    //  hangup();
    //  getSimVoltage();
    //}
    //if (key == 'C') {
    //  current_number = "";
    //  turnOffSim();
    //}
    //if (key == 'D') {
      //Serial.println("Delete Key Hit");
    //  current_number = "";
    //  clearDisplay();
    //}

    //delay(100);
    //Serial.println(current_number);
    
  //}

  //if (keychange) {
  //  clearDisplay();
  //  displayText(current_number);
  //  delay(500);
  //}
}
