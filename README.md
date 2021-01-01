# Mooshak da Feira (v2)

This small NodeJs app is aimed at unit testing the code for IST FP Project 2 (2020-2021).  
The app turns on a web server which allows the students to paste their code and run the tests,
without any knowledge on unit testing.

## How to setup

(if using Windows, execute the following commands through Git Bash)

1. Make sure you have Git, NodeJS, Yarn (optional) and Python (v3.5 is recommended for this project).
2. Clone the repository with `git clone https://github.com/diogotcorreia/proj2-fp-tester.git`
3. Install dependencies with `yarn install` (or just `yarn`). If you don't have yarn, you can also do `npm i`.
4. Run the server with `yarn start` (production) or `yarn dev` (development). If you don't have yarn, you can also do `npm run start` or `npm run dev`.
5. Navigate to `localhost:5000` on your browser (or the port you specified in the `PORT` env variable).
6. If you want to use another Python version, set the `PYTHON_PATH` env variable, like `PYTHON_PATH=python3.5 yarn dev`.
7. Paste your code and see the tests running.

## Contributing

### Tests

Tests are located at `tests/test.py`.
Additional test files (big outputs, for example), might be in their own `.txt` files.

To contribute, just submit a pull request. Make sure the test is correct before submitting a PR.

### Application

Improvements to the web interface or NodeJS backend are also appreciated.

As above, submit a pull request or open an issue if you want to discuss the changes before implementing them.
