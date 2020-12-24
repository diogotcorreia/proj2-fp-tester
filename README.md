# Mooshak da Feira (v2)

This small NodeJs app is aimed at unit testing the code for IST FP Project 2 (2020-2021).  
The app turns on a web server which allows the students to paste their code and run the tests,
without any knowledge on unit testing.

## How to setup

1. Make sure you have NodeJS, Yarn and Python 3.5 (edit version in `index.js` if you want to use another version).
2. Install dependencies with `yarn install` (or just `yarn`).
3. Run the server with `yarn start` (production) or `yarn dev` (development).
4. Go to `localhost:5000` (or the port you specified in the `PORT` env variable).
5. Paste your code and see the tests running.

## Contributing

### Tests

Tests are located at `tests/test.py`.
Additional test files (big outputs, for example), might be in their own `.txt` files.

To contribute, just submit a pull request. Make sure the test is correct before submitting a PR.

### Application

Improvements to the web interface or NodeJS backend are also appreciated.

As above, submit a pull request or open an issue if you want to discuss the changes before implementing them.
