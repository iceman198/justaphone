var exec = require('child_process').exec;
var oled = require('oled-ssd1306-i2c');
var font = require('oled-font-5x7');

var oled_opts = {
  width: 128, // screen width
  height: 32, // screen height
  address: 0x3C, // Pass I2C address of screen if it is not the default of 0x3C
  device: '/dev/i2c-1', // Pass your i2c device here if it is not /dev/i2c-1
  microview: true, // set to true if you have a microview display
};

var oled = new oled(oled_opts);

const express = require('express');
//const url = require('url');
const app = express();
const port = 8088;

app.use(express.static('public'));
app.get('/', function (req, res) {
  res.sendFile(__dirname + "/" + "index.html");
})

app.get('/service/', (request, response) => {
  //var url_parts = url.parse(request.url, true);
  //var query = url_parts.query;
  var cmd = request.query.cmd;
  console.log(`cmd is ${cmd}`);
  if (cmd) {
    if (cmd == "shutdown") {
      console.log('sending command');
      response.sendStatus(`Shutdown initiated`);
      dir = exec(`shutdown now`, function (err, stdout, stderr) {
        if (err) {
          console.log('error sending command: ', err);
        }
        console.log(stdout);
      });

      dir.on('exit', function (code) {
        console.log('exit complete with code ', code);
      });
    } else {
      response.sendStatus(`Command not recognized`);
    }
  }
});

app.listen(port, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log(`server is listening on ${port}`)
});

function startup() {
  // dir = exec(`python /home/pi/Documents/justaphone/python/stats.py > /dev/null 2>&1`, function (err, stdout, stderr) {
  //   if (err) {
  //     console.log('error sending command: ', err);
  //   }
  // });
  oled.turnOnDisplay();
  oled.clearDisplay();
  oled.setCursor(1, 1);
  oled.writeString(font, 1, 'Cats and dogs are really cool animals, you know.', 1, true);
  oled.update();
}

startup();
