var exec = require('child_process').exec;

const express = require('express');
//const url = require('url');
const app = express();
const port = 8088;

app.use(express.static('public'));
app.get('/', function (req, res) {
   res.sendFile( __dirname + "/" + "index.html" );
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
      dir = exec(`shutdown now`, function(err, stdout, stderr) {
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
  dir = exec(`python /home/pi/Documents/JustAphone/python/stats.py > /dev/null 2>&1`, function(err, stdout, stderr) {
    if (err) {
      console.log('error sending command: ', err);
    }
  });
}

startup();
