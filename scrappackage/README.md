# Web scraping bot - scrappackage

## scrap_blog_articles.py
Contains the '''Website_blog''' class, which have the following methods:

### sleep_random_time()
  - Sleep method to avoid the website server to be overloaded with too many requests in a short time.

### get_website_blog_url()
  - get the environement variable which contains the website's blog url.

### convert_date(date)
  - Convert a date from 'MMMM DDth, YYYY' format to "YYYY-MM-DD" format.

### scrap_one_article_page(url)
  - Scrap data from one article's page from the given url.

### scrap_blog_page_one_only()
  - Scrap the first page only of the website's blog.
  - Page one has a different layout than other pages.
  - It contains informations and links to several articles.

### scrap_blog_one_page_for_page_two_and_more(page)
  - Scrap one page of the website's blog, for page two and more, from the given URL.
  - Page layout is different than page one.
  - It contains informations and links to several articles.

### scrap_all_blog_articles()
  - Scrap all the pages of the website's blog, return a Pandas DataFrame
