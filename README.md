# Web scraping bot with Python and BeatifulSoup Library.
- Scrap blog articles and related data about lifestyle and things to do in Tokyo from a specific website.
- To prevent a malicious use of this Python app, an environement variable is used to manage the website URL, which doesn't appear on this git-hub repository.
- This web scraping bot may only works with that specific website URL.
- Collected data will be used in a further project

## Usage
```
# import Pandas librairy and the Website_blog class.
import pandas
from scrappackage.scrap_blog_articles import Website_blog

# instantiate the Website_blog class.
wb = Website_blog()

# scrap all the articles and related data.
all_articles_df = wb.scrap_all_blog_articles()

# save the data in all_articles.csv file.
all_articles_df.to_csv("all_articles.csv", mode='w', index=None, header=True)
```

## Package installation
- It is recommended to use a virtual environment to install this project
- If setuptools is already installed, execute the following command line: ```make install```
- If setuptools is not installed, execute the followin command line: ```pip install setuptools``` then ```make install```
- Check out Makefile for more usefull command lines

## Tests
- run the tests with:
```
make tests
```
