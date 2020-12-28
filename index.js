const path = require("path");
const spawn = require("child_process").spawn;
const express = require("express");
const app = express();
const server = require("http").createServer(app);
const io = require("socket.io")(server);

app.get("/", (_req, res) => res.sendFile(path.join(__dirname, "index.html")));
app.use("/assets", express.static(path.join(__dirname, "assets")));

const timeout = 300;

let processes = {};
let timer = {};

const closeProcess = (socket, processes, timer) => {
  if (processes[socket.id]) {
    processes[socket.id].kill();
    delete processes[socket.id];
    socket.emit("done");
  }
  if (timer[socket.id]) {
    clearTimeout(timer[socket.id]);
    delete timer[socket.id];
  }
};

io.on("connection", (socket) => {
  socket.on("submit", (code, skipMocks) => {
    if (processes[socket.id]) closeProcess(socket, processes, timer);
    socket.emit("clear");

    socket.emit(
      "result",
      `[Mooshak da Feira] Executing tests... ${
        skipMocks
          ? "(skipping abstraction tests)"
          : `(testing abstraction; might take up to ${timeout / 60} minutes)`
      }\n\n`
    );

    child = spawn("python3.5", [
      "-u",
      path.join(__dirname, "tests", "test.py"),
      skipMocks ? "False" : "True",
    ]);
    processes[socket.id] = child;

    result = (data) => socket.emit("result", data.toString());
    child.stdout.on("data", result);
    child.stderr.on("data", result);

    child.stdin.write(code);
    child.stdin.end();

    child.on("close", () => closeProcess(socket, processes, timer));

    timer[socket.id] = setTimeout(() => {
      socket.emit(
        "result",
        `Program killed because it exceeded timeout (${timeout}s) :(`
      );
      closeProcess(socket, processes, timer);
    }, timeout * 1000);
  });

  socket.on("disconnect", () => {
    if (processes[socket.id]) closeProcess(socket, processes, timer);
  });

  socket.on("kill", () => {
    if (processes[socket.id]) {
      socket.emit("result", "\nProgram killed by user :(");
      closeProcess(socket, processes, timer);
    }
  });
});

server.listen(process.env.PORT || 5000);
console.log(
  `Listening on port ${
    process.env.PORT || 5000
  }. You can change this by passing a value to the PORT environment variable.`
);
