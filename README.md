# rock-paper-scissors

A simple Rock, Paper, Scissors game you play in the command line, plus a stocks dashboard that shows stock prices in a chart.

## What You Need

- Python 3 (the easiest way to get it is [Anaconda](https://www.anaconda.com/download))
- Git or GitHub Desktop

## Setup

1. Download (clone) [this repo](https://github.com/Cami1111/rock-paper-scissors) from GitHub and save it somewhere on your computer.

2. Open your command line and go into the repo folder:

```sh
cd path/to/rock-paper-scissors
```

3. Create a virtual environment called "rps-env". You only need to do this the first time:

```sh
conda create -n rps-env python=3.11
```

4. Turn on the virtual environment. Do this every time you come back to the project:

```sh
conda activate rps-env
```

5. Install the packages this project needs. They are listed in the "requirements.txt" file:

```sh
pip install -r requirements.txt
```

## API Key (only for the stocks dashboard)

The stocks dashboard gets its data from AlphaVantage, so it needs an API key. You can get one using [this form](https://www.alphavantage.co/support/#api-key), or use one shared by the professor.

Create a file called ".env" in the main folder of the repo, and put your key in it like this:

```sh
# this is the ".env" file...

ALPHAVANTAGE_API_KEY="______________"
```

The ".env" file stays on your computer only. It is never uploaded to GitHub, so your key stays private.

## How to Run

Run the example script:

```sh
python -m app.my_script
```

Play Rock, Paper, Scissors:

```sh
python -m app.rps
```

Open the stocks dashboard:

```sh
python -m app.stocks
```

## How to Test

Run all the automated tests to check that the code works:

```sh
pytest
```

The same tests also run automatically on GitHub every time new code is added to the main branch or a pull request is opened.
