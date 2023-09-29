# Survey Analysis and Text-to-Audio Conversion

This repository contains two Python programs for survey analysis and text-to-audio conversion. The first program allows you to convert video and audio files to MP3 format and optimize MP3 audio files. The second program utilizes GPT-4 for text generation tasks.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Program 1: Survey Analysis](#program-1-survey-analysis)
- [Program 2: Text Generation](#program-2-text-generation)

## Installation

To run these programs, you'll need Python 3.x installed on your system. You can follow these steps to set up your environment:

1. Clone this repository to your local machine using Git:

   ```bash
   git clone https://github.com/Cha0smagick/Transcript_tools
   cd Transcript_tools

    Install the required Python packages using pip. Create a virtual environment first (optional but recommended) and activate it:

    bash

python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

Then, install the dependencies:

bash

    pip install -r requirements.txt

Usage
Program 1: Survey Analysis

This program offers the following features:

    Convert video and audio files to MP3 format.
    Optimize MP3 audio files by increasing volume and enhancing vocal frequencies.
    Convert audio to text using the Whisper ASR model.

To run the program, execute the following command:

bash

python Interview_analysis_tools_BASE.py

Follow the on-screen menu to choose from the available options.
Program 2: Text Generation

This program utilizes the GPT-4 model for text generation tasks. It reads a large text file, splits it into chunks, and generates responses for each chunk.

To use this program, follow these steps:

    Provide a text file (UTF-8 encoded) that you want to analyze. The program will split the text into manageable chunks automatically.

    Run the program with the following command:

    python Procesar_textos_largos.py

    The program will interactively generate responses for each chunk and save them in a formatted text file named entrevistas_completa_formateada.txt.

License

This project is licensed under the MIT License - see the LICENSE file for details.
