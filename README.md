# DrumLogs

DrumLogs is a simple Python utility project for managing and playing drum audio samples. It includes tools for loading samples, sequencing patterns, randomizing drum steps, and basic audio playback.

## Features

* Simple step sequencer
* Random drum pattern generator
* Basic DSP utilities

## Project Structure

```bash
.
├── configs/
├── src/
│   ├── audio_tools/
│   └── dsp/
├── main.py
├── pre_main.py
├── requirements.txt
└── pyproject.toml
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yanas-logs/drumlogs.git
cd drumlogs
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main application:

```bash
python main.py
```

Make sure your drum samples are placed inside the `audio_data/` directory.

Example category structure:

```bash
audio_data/
├── kick/
├── snare/
└── hihat/
```

## Requirements

* Python 3.8+

## Author

Created by Yana Suryana (yanas-logs)

## License

MIT License.
