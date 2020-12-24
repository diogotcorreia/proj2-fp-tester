const express = require("express");
const fs = require("fs").promises;
const bodyParser = require("body-parser");
const { v4: uuidv4 } = require("uuid");
const app = express();
const path = require("path");
const spawn = require("child_process").spawn;

app.use(bodyParser.text());

app.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.use("/assets", express.static(path.join(__dirname, "assets")));

app.post("/run", async (req, res) => {
  const uuid = uuidv4();
  const filePath = path.join(__dirname, "tests", `runner-${uuid}.py`);
  await fs.writeFile(filePath, req.body);

  const pythonProcess = spawn("python3.5", [
    path.join(__dirname, "tests", "test.py"),
    `runner-${uuid}`,
  ]);

  let result = "";

  const handleData = (data) => {
    str = data.toString();
    if (/\.+/.test(str)) result += str;
    else result += str + "\n";
  };

  pythonProcess.stdout.on("data", handleData);

  pythonProcess.stderr.on("data", handleData);

  pythonProcess.on("close", async () => {
    await fs.unlink(filePath);
    res.send(result);
  });

  setTimeout(() => {
    result += "Max timeout exceeded (3s). Program killed.";
    pythonProcess.kill();
  }, 3000);
});

app.listen(process.env.PORT || 5000);
console.log(
  `Listening on port ${
    process.env.PORT || 5000
  }. You can change this by passing a value to the PORT environment variable.`
);
