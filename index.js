var exec = require('child_process').exec;
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

const express = require('express');
//const url = require('url');
const app = express();
const port = 8088;

var myIp = "";

var lineSelected = 0;
var lines = [ "", "", "", "" ];

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
      console.log('sending command: ' + cmd);
      response.sendStatus(`Shutdown initiated`);
      shutdown();
    } else if (cmd == "cursorUp") {
      console.log('sending command: ' + cmd);
      response.sendStatus("cursorUp");
      selectUp();
    } else if (cmd == "cursorDown") {
      console.log('sending command: ' + cmd);
      response.sendStatus("cursorDown");
      selectDown();
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

function selectDown() {
  lineSelected++;
  if (lineSelected > lines.length) {
    lineSelected = 1;
  }
  writeOled();
}

function selectUp() {
  lineSelected--;
  if (lineSelected <= 0) {
    lineSelected = lines.length;
  }
  writeOled();
}

function shutdown() {
  lineSelected = 0;
  lines = ["Shutting down"];
  writeOled();
  dir = exec(`shutdown now`, function (err, stdout, stderr) {
    if (err) {
      console.log('error sending command: ', err);
    }
    console.log(stdout);
  });

  dir.on('exit', function (code) {
    console.log('exit complete with code ', code);
  });
}

function startup() {
  getIP();
  // dir = exec(`python /home/pi/Documents/justaphone/python/stats.py > /dev/null 2>&1`, function (err, stdout, stderr) {
  //   if (err) {
  //     console.log('error sending command: ', err);
  //   }
  // });
  oled.turnOnDisplay();
  lineSelected = 1;
  lines = ["IP: " + myIp, "two line", "three line", "line four"];
  writeOled();
}

function writeOled() {
  clearDisplay();
  for (i = 0; i < lines.length; i++) {
    var cursorInt = (i*8);
    console.log("Set cursorInt to " + cursorInt);
    oled.setCursor(1, 1 + cursorInt);
    var linetxt = lines[i];
    if (i+1 == lineSelected) {
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

function clearDisplay() {
  oled.clearDisplay();
}

function getIP() {
  var os = require('os');
  var ifaces = os.networkInterfaces();
  
  Object.keys(ifaces).forEach(function (ifname) {
    if (ifname.indexOf("wlan") > -1) {
      var alias = 0;
  
      ifaces[ifname].forEach(function (iface) {
        if ('IPv4' !== iface.family || iface.internal !== false) {
          // skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
          return;
        }
    
        if (alias >= 1) {
          // this single interface has multiple ipv4 addresses
          console.log(ifname + ':' + alias, iface.address);
          myIp = iface.address;
        } else {
          // this interface has only one ipv4 adress
          console.log(ifname, iface.address);
          myIp = iface.address;
        }
        ++alias;
      });
    }
  });
}

startup();
