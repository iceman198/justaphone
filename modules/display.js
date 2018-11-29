var oled = require('oled-ssd1306-i2c'); // https://github.com/perjg/oled_ssd1306_i2c
var font = require('oled-font-5x7');

var oled_opts = {
    width: 128, // screen width
    height: 32, // screen height
    address: 0x3C, // Pass I2C address of screen if it is not the default of 0x3C
    device: '/dev/i2c-1', // Pass your i2c device here if it is not /dev/i2c-1
    microview: true, // set to true if you have a microview display
};

var oled = new oled(oled_opts);
oled.turnOnDisplay();

var lineSelected = 0;
var lines = ["", "", "", ""];

function getMenu(name) {
    var fs = require("fs");
    var fileJson = fs.readFileSync('./modules/menus/' + name + '.json');
    lines = JSON.parse(fileJson).lines;
    console.log("lines = " + JSON.stringify(lines));
}

function writeOled() {
    oled.clearDisplay();
    for (i = 0; i < lines.length; i++) {
        var cursorInt = (i * 8);
        console.log("Set cursorInt to " + cursorInt);
        oled.setCursor(1, 1 + cursorInt);
        var linetxt = lines[i].getMenutext;
        if (i + 1 == lineSelected) {
            linetxt = "-" + linetxt;
            console.log("Set linetxt to " + linetxt);
        } else {
            linetxt = " " + linetxt;
            console.log("Set linetxt to " + linetxt);
        }
        oled.writeString(font, 1, linetxt, 1, false);
    }

    oled.update();
}

exports.write = function(linenum, mylines) {
    lineSelected = linenum;
    lines = mylines;
    writeOled();
}

exports.loadMenu = function(menuname) {
    getMenu(menuname);
    writeOled();
}

exports.selectDown = function() {
    lineSelected++;
    if (lineSelected > lines.length) {
        lineSelected = 1;
    }
    writeOled();
}

exports.selectUp = function() {
    lineSelected--;
    if (lineSelected <= 0) {
        lineSelected = lines.length;
    }
    writeOled();
}

exports.clearDisplay = function() {
    oled.clearDisplay();
}

exports.setLineSelection = function (num) {
    lineSelected = num;
}
