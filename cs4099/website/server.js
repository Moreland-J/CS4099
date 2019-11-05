const http = require('http');
var fs = require('fs');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
//   res.statusCode = 200;
  res.writeHead(200, {'Content-Type': 'text/html'});
  fs.readFile('./main/', null, function(error, data) {
      if (error) {
        res.writeHead(404);
        res.write('File not Found');
      }
      else {
        res.write(data);
      }
      res.end();
  });
//   res.end();
});

// server.listen(port, hostname, () => {
//   console.log(`Server running at http://${hostname}:${port}/`);
// });

http = createServer(onRequest).listen(3000);