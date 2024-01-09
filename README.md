### Mochi Scraper

Checks Mochizuki's website too see whether his safety information has changed  
If a change has occurred, it sends an email with the updated safety information  
https://www.kurims.kyoto-u.ac.jp/~motizuki/anpi-kakunin-jouhou.html

### Quickstart

First, create the virtual env and install the packages
```python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create an .env file under src/ and put your credentials there  
Use the env_sample as a template to create this file
 
For more information, see https://pypi.org/project/python-dotenv/

Note: When running everything for the first time we need to manually  
put the safety information of today in yesterday.txt in order to  
bootstrap everything

### Usage

Run get_html first to fetch today's website and then scraper.py

