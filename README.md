# DNA Survey
### Guide user through questionnaire of predefined questions and compiles answers into a responses excel sheet.

## Release Installation (Windows)
1. Download latest release for Windows -> [v1.01](https://github.com/madanmukundan/dnasurvey/releases/tag/v1.01) and unzip.

2. Run by double-clicking from DNASurvey\DNASurvey.exe
    - Please do not move DNASurvey.exe from its parent folder (lib requirements for gui)

## Python installation
1. Create virtual environment (venv example given) in a local directory created for this app.
    - `python -m venv <C:\path\to\new\virtual\environment>`
    - `python3 -m venv </path/to/new/virtual/environment>`
    - `conda create -n <name of environment>`

3. Activate environment
    - in Windows cmd: `<path to venv>\.venv\bin\activate.bat`
    - in bash/zsh: `source <path to venv>/bin/activate`
    - using conda: `conda activate <name of environment>`

4. Install dependencies from requirements.txt
    - `pip install -r requirements.txt`
5. Run DNASurvey.py
    - `python dnasurvey/DNASurvey.py`

## Use of DNASurvey
1. Enter First and Last Name
2. Load questions either by "Browse", Drag-N-Drop, or use the default question set.
3. Start Survey

## Notes on Survey
- Survey can be saved interim so answers are not lost.

## Updating Questions
- Questions are meant to be formatted in column B as a single string per question.

## Viewing Responses
- Responses are saved under the Responses/ folder and can be viewed directly or loaded into DNASurvey for viewing answered questions.
- For dev, all questions have a response field initialized. Missing responses have this field labeled "\<missing\>"

## Linux notes for customtkinter
- On linux, python needs to use an xft-enabled version of tkinter, which cannot be installed via pip. Within directory:
    - `conda install -c conda-forge tk=*=xft_*`

