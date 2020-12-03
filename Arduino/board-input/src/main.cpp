#include "Keypad.h"

const byte KP_ROWS = 5; //four rows
const byte KP_COLS = 5; //three columns
char keys[KP_ROWS][KP_COLS] = {
  {'1', '2', '3', '4', '5'},
  {'6', '7', '8', '9', 'A'},
  {'B', 'C', 'D', 'E', 'F'},
  {'G', 'H', 'I', 'J', 'K'},
  {'L', 'M', 'N', 'O', 'P'}
};

byte kpRowPins[KP_ROWS] = {12, 11, 10, 9, 8}; //rows top to bottom
byte kpColPins[KP_COLS] = {6, 5, 4, 3, 2}; //columns right to left (when looking at it from the back)

Keypad keypad = Keypad(makeKeymap(keys), kpRowPins, kpColPins, KP_ROWS, KP_COLS);

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  char key = keypad.getKey();

  if (key != NO_KEY) {
    Serial.print(key);
    delay(100);
  }
}
