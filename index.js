const path = require('path');
const spawn = require('child_process').spawn;
const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);

app.get('/', (_req, res) => res.sendFile(path.join(__dirname, 'index.html')));
app.use('/assets', express.static(path.join(__dirname, 'assets')));

const timeout = 300;

let queue = [];
let sockets = {};
let processing;

const enqueue = (q, s, code, skipMocks) => {
  sockets[s.id] = { code: code, skipMocks: skipMocks };
  p = q.push(s) - (processing ? 0 : 1);
  if (p > 0) {
    s.emit(
      'result',
      `[Mooshak da Feira] Your test is in the queue. There ${
        p == 1 ? 'is 1 test' : `are ${p} tests`
      } before yours.\n`
    );
  } else {
    s.emit('result', '[Mooshak da Feira] ');
  }
};

const notifyNewPos = (q) => {
  q.forEach((s, i) => {
    s.emit('result', `There ${i == 0 ? 'is 1 test' : `are ${i + 1} tests`} before yours.\n`);
  });
};

const next = (q) => {
  s = q.shift();
  notifyNewPos(q);
  return s;
};

const leaveQueue = (q, s) => {
  i = q.indexOf(s);
  if (i == -1) {
    console.log('socket tried to leave queue but was not in it');
    return;
  }
  delete sockets[s.id];
  q.splice(i, 1);
  notifyNewPos(q.slice(i));
  s.emit('done');
};

const killProcess = (s) => {
  if (!sockets[s.id]) return;   // already killed
  if (sockets[s.id]['timer']) clearTimeout(sockets[s.id]['timer']);
  if (sockets[s.id]['process']) sockets[s.id]['process'].kill();
  delete sockets[s.id];
  s.emit('done');
  processing = undefined;
};

const processTests = (s) => {
  s.emit(
    'result',
    `Executing tests... ${
      sockets[s.id]['skipMocks']
        ? '(skipping abstraction tests)'
        : `(testing abstraction; might take up to ${timeout / 60} minutes)`
    }\n\n`
  );

  child = spawn('python3.5', [
    '-u',
    path.join(__dirname, 'tests', 'test.py'),
    sockets[s.id]['skipMocks'] ? 'False' : 'True',
  ]);
  sockets[s.id]['process'] = child;

  sockets[s.id]['timer'] = setTimeout(() => {
    s.emit('result', `Program killed because it exceeded timeout (${timeout}s) :(`);
    killProcess(s);
  }, timeout * 1000);

  result = (data) => s.emit('result', data.toString());
  child.stdout.on('data', result);
  child.stderr.on('data', result);

  child.stdin.write(sockets[s.id]['code']);
  child.stdin.end();

  child.on('close', () => killProcess(s));
};

io.on('connection', (socket) => {
  socket.on('submit', (code, skipMocks) => {
    socket.emit('clear');
    enqueue(queue, socket, code, skipMocks);
  });

  socket.on('disconnect', () => {
    if (processing == socket.id) {
      killProcess(socket);
    } else if (queue.indexOf(socket) != -1) {
      leaveQueue(queue, socket);
    }
  });

  socket.on('kill', () => {
    if (processing == socket.id) {
      socket.emit('result', '\nProgram killed by user :(');
      killProcess(socket);
    } else if (queue.indexOf(socket) != -1) {
      socket.emit('result', '\nLeft queue.');
      leaveQueue(queue, socket);
    }
  });
});

server.listen(process.env.PORT || 5000);
console.log(
  `Listening on port ${
    process.env.PORT || 5000
  }. You can change this by passing a value to the PORT environment variable.`
);

setInterval(() => {
  if (!processing && queue.length != 0) {
    socket = next(queue);
    processing = socket.id;
    processTests(socket);
  }
}, 10);
