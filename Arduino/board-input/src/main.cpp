#include "Keypad.h"

const byte KP_ROWS = 4; //four rows
const byte KP_COLS = 4; //three columns
char keys[KP_ROWS][KP_COLS] = {
  {'H', '3', '2', '1'},
  {'S', '6', '5', '4'},
  {'O', '9', '8', '7'},
  {'C', '#', '0', '*'}
};

byte kpRowPins[KP_ROWS] = {2, 11, 10, 9}; //rows top to bottom
byte kpColPins[KP_COLS] = {7, 6, 5, 4}; //columns right to left (when looking at it from the back)

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
