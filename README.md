California Megan's Law Web Scraper
==================================

A web scraper project to pull data from the California Megan's Law
sex offender website at meganslaw.ca.gov.

The scraper utilized the python Scrapy project to search and retrieve
data from the site. Objects are returned to Scrapy's control where
the user can specify the output format.


Getting Setup
-------------

```bash
mkvirtualenv project_name
git clone this-repo
cd repo-folder
pip install -r requirements.txt
scrapy runspider sexoff_scraper/spiders/sexoff.py -o output.json -a county=ORANGE
```


County Choices
--------------

```
ALAMEDA
ALPINE
AMADOR
BUTTE
CALAVERAS
COLUSA
CONTRA%20COSTA
DEL%20NORTE
EL%20DORADO
FRESNO
GLENN
HUMBOLDT
IMPERIAL
INYO
KERN
KINGS
LAKE
LASSEN
LOS%20ANGELES
MADERA
MARIN
MARIPOSA
MENDOCINO
MERCED
MODOC
MONO
MONTEREY
NAPA
NEVADA
ORANGE
PLACER
PLUMAS
RIVERSIDE
SACRAMENTO
SAN%20BENITO
SAN%20BERNARDINO
SAN%20DIEGO
SAN%20FRANCISCO
SAN%20JOAQUIN
SAN%20LUIS%20OBISPO
SAN%20MATEO
SANTA%20BARBARA
SANTA%20CLARA
SANTA%20CRUZ
SHASTA
SIERRA
SISKIYOU
SOLANO
SONOMA
STANISLAUS
SUTTER
TEHAMA
TRINITY
TULARE
TUOLUMNE
VENTURA
YOLO
YUBA
```