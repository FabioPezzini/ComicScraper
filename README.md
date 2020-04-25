![logo ComicScraper](comicscraper/ComicScraper.png)
ComicScraper is a scraper that allow you to create your personal DB containing all the informations
about the comics (from 1946 to now) and some manga.
It includes also the covers of each comic.

##### To use it you need:
- Python3
- MongoDB

##### To run it, install in the venv:
- Scrapy: https://scrapy.org/
- PyMongo: https://pymongo.readthedocs.io/en/stable/

### How use the script:
1. Move in the dir comicscraper/comicscraper
2. If it is the first execution of the script type:  
    `scrapy crawl comicsITA`   
3. Every week you can update the status of the DB (i suggest to use it on Sunday), type:  
    `scrapy crawl comicsWeekly`    
    
###### TODO:
- Add ALL american comics (now it adds only some american comics, but if someone will ask me to add also the american version I will do it)




N.B= The purpose of the scraper is absolutely non-commercial and has been designed for educational and learning purposes only (Python & Scrapy).
However, if the owner of the sites does not want the project up just tell me and the project will be taken down.
The author of ComicScraper doesn't take the fault for improper use by the user.
