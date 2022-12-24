# Atlas to .ics
Export class schedules from atlas.ai.umich.edu as an ics file

# How to use
1. Clone this repo locally
2. Rename secret.json.template to secret.json
3. Update the values in secret.json as necessary. `password` should set as your password to U-M Weblogin.
4. Create a virtual environment inside the root directory and install dependencies in the active virtual environemtn:
```
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```
5. Run `main.py` in your terminal:
```
python main.py
```
6. Import ics file into your gcal

# Limitations
- The scraper won't work if Atlas or Atlas Schedule Builder is down.
- The scraper doesn't take into account breaks or holidays. You'll have to remove classes for fall/spring break.
