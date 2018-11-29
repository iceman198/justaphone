var exec = require('child_process').exec;
var display = require('./modules/display.js');

const express = require('express');
//const url = require('url');
const app = express();
const port = 8088;

var myIp = "";

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
      display.selectUp();
    } else if (cmd == "cursorDown") {
      console.log('sending command: ' + cmd);
      response.sendStatus("cursorDown");
      display.selectDown();
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

function shutdown() {
  lineSelected = 0;
  lines = ["Shutting down"];
  display.write(1, lines);
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

  display.loadMenu("stats");
  //lines = ["IP: " + myIp, "two line", "three line", "line four"];
  //display.write(1, lines);
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
