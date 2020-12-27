const fs = require('fs');
const path = require('path');
const spawn = require('child_process').spawn;
const express = require('express');
const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server);

app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));
app.use("/assets", express.static(path.join(__dirname, "assets")));

const timeout = 60;

let processes = {};
let timer = undefined;

const closeProcess = (socket, processes, timer) => {
    processes[socket.id].kill();
    if(timer) clearTimeout(timer)
    socket.emit('done')
}

io.on('connection', socket => {

    socket.on('submit', code => {

        if(processes[socket.id]) closeProcess(socket, processes, timer);
        socket.emit('clear');

        child = spawn('python3.5', ['-u', path.join(__dirname, 'tests', 'test.py')]);
        processes[socket.id] = child;

        result = (data) => socket.emit('result', data.toString());
        child.stdout.on('data', result);
        child.stderr.on('data', result);

        child.stdin.write(code)
        child.stdin.end()

        child.on('close', () => closeProcess(socket, processes, timer));

        timer = setTimeout(() => {
            child.kill();
            socket.emit('result', 'timeout :(');
        }, timeout*1000);
    })

    socket.on('disconnect', () => {
        if(processes[socket.id]) closeProcess(socket, processes, timer);
    });

});

server.listen(process.env.PORT || 5000);
console.log(
  `Listening on port ${
    process.env.PORT || 5000
  }. You can change this by passing a value to the PORT environment variable.`
);
