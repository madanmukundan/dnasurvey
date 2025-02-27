### DNA Survey
## Guide user through questionnaire of predefined questions and compiles answers into a responses excel sheet.

# Installation
1. Create virtual environment (venv example given) in a local directory created for this app
    '''python -m venv <C:\path\to\new\virtual\environment>'''
2. Install dependencies from requirements.txt
    '''pip install -r requirements.txt'''
3. Run DNASurvey.py
    '''python -m dnasurvey/DNASurvey.py'''

# Use of DNASurvey
1. Enter First and Last Name
2. Load questions either by "Browse", Drag-N-Drop, or use the default question set.
3. Start Survey

# Notes on Survey
- Survey can be saved interim so answers are not lost.

# Updating Questions
- Questions are meant to be formatted in column B as a single string per question.

# Viewing Responses
- Responses are saved under the Responses/ folder and can be viewed directly or loaded into DNASurvey for viewing answered questions.
- For dev, all questions have a response field initialized. Missing responses have this field labeled "<missing>"
