# Atlas to .ics
Export class schedules from atlas.ai.umich.edu as an .ics file

# How to use
1. [Clone this GitHub repository locally](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
2. You'll also need [Python](https://www.python.org/) on your computer in order to run this program.
3. Rename `secret.json.template` to `secret.json`
4. Update the values in `secret.json` as necessary. `password` should set as your password to U-M Weblogin.
5. Create a virtual Python environment inside the root directory and install dependencies in the active virtual environment: 
```
\\For Windows PowerShell:
python3 -m venv venv/
venv\Scripts\activate
python -m pip install -r requirements.txt
```
```
\\For Linux or MacOS:
python3 -m venv venv/
source venv/bin/activate
python -m pip install -r requirements.txt
```
6. Run `main.py` in your terminal. Be sure to have your phone nearby so that you will be able to verify the Duo Push request.
```
python main.py
```
7. An .ics file should have been created in the same directory as `main.py`
8. Import .ics file into your calendar

# Limitations
- The scraper won't work if Atlas or Atlas Schedule Builder is down.
- The scraper doesn't take into account breaks, holidays, or other edge cases. You'll have to remove classes for fall/spring break.

If you're interested, I also wrote a [Medium Post](https://www.python.org/downloads/) about how I built this webscraper.
