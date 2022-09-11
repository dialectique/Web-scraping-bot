import re
import os
import requests
import random
import time
import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime



class Website_blog:
    """
    A class for scrap a particular website's blog articles.
    The environment variable BLOG_URL contains the website URL.
    I use an environement variable to prevent malicious use of my script.
    """

    def sleep_random_time(self):
        """
        Sleep method to avoid the website server to be overloaded
        with too many requests in a short time.
        :return: None
        :rtype: NoneType
        """
        # Program execution will be stopped for a period of time
        # ranging from 5 to 16 seconds.
        wait_time = random.randint(5, 25)
        time.sleep(wait_time)


    def get_website_blog_url(self):
        """
        Get the the absolute path of the root directory
        and read the .env file to get the environement variable
        which contains the website's blog url.
        '.env' file must contain only one environment variable.
        :return: website's blog url
        :rtype: string
        """
        # Get and return the absolute path of the root directory.
        root_abs_path = os.path.dirname(
            os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
            )

        # get the environment variables
        with open(os.path.join(root_abs_path, ".env")) as f:
            env_var_dict = {}
            for line in f:
                var_name, value = line.split("=")
                env_var_dict[var_name] = value

        # get and return the website URL
        return env_var_dict["WEBSITE_BLOG_URL_TEST"].strip()


    def convert_date(self, date: str = "") -> str:
        """
        Convert a date to "YYYY-MM-DD" format.
        Example: "June 17th, 2020" returns "2020-06-17"
        :param date: date with "month DDth, YYYY" format
        :type date: str
        :raise TypeError: if date is not a string with the required format
        :return: date with "YYYY-MM-DD" format
        :rtype: str
        """
        pattern = re.compile(
            r"^(January|February|March|April|May|June|July|August|September|October|November|December)"
            r" ([1-9]|[12][0-9]|3[01])(st|nd|rd|th), [0-9]{4}$"
            )
        if re.search(pattern, date):
            date_list = date.split()
            date_list[1] = date_list[1][:-3]
            try:
                return datetime.strptime(" ".join(date_list), "%B %d %Y") \
                    .strftime("%Y-%m-%d")
            except Exception as e:
                raise e
        raise ValueError(
            "Date doesn't have the required format. Examples of correct date format:\n"
            "February 1st, 2017'  'May 2nd, 1997'  'June 3rd, 2008'  'March 4th, 2015'"
            )


    def scrap_one_article_page(self, url):
        """
        Scrap data from one article's page of the website's blog:
        date, author, tags, text(leads + article)
        :param url: url of the article's page
        :type date: str
        :raise ConnectionError: if page not found
        :return: a dict with article's date | author | tags | text
        :rtype: dict
        """

        # Setup the request and soup setup.
        data = requests.get(url)
        soup = BeautifulSoup(data.text, "html.parser")

        # Articles' page can maybe have different layout
        # so let's use try/except to avoid interupting the script.

        # Article's date
        try:
            date = soup.find("div", "hero__meta") \
                    .span.string.split("|")[0].strip()
        except:
            date=""

        # Article's author
        try:
            author = soup.find("div", "hero__meta") \
                    .span.string.split("|")[1].strip()
        except:
            author=""

        # List of article's tags
        try:
            tags = ", ".join(
                [tag.a.string.strip() for tag in soup.find_all("li", "tags__tag")]
                )
        except:
            tags = ""

        # List of article's' leads and text
        try:
            text = " ".join(
                    [p.get_text().strip().replace("\n", " ") for p in soup \
                        .find("div", "entry-content__content") \
                        .find_all(["h2", "h3", "p"])]
                    )
        except:
            text = ""

        return {
            'date': date,
            'author': author,
            'tags': tags,
            'text': text
        }


    def scrap_blog_page_one_only(self) -> pd.core.frame.DataFrame:
        """
        Scrap the first page only of the website's blog.
        Page one has a different layout than other pages.
        For other pages, see the method: self.scrap_blog_one_page_for_page_two_and_more()
        :return: a dataframe with articles' url | title | date | author |
            category | tags | text
        :rtype: pandas.core.frame.DataFrame
        """

        # Setup the url, request, soup setup and scrap.
        page_url = f"{self.get_website_blog_url()}1/"
        data = requests.get(page_url)
        soup = BeautifulSoup(data.text, "html.parser")

        # Display the page URL
        print(f"Scrap articles from URL page: {page_url}")

        # Top article title
        top_title = soup.find("h1", "hero__title").a.string.strip()

        # Top article url
        top_url = soup.find("h1", "hero__title").a["href"]

        # Top article categories.
        # We need to go on the article page, and get the categories.
        # "home" is excluded as it is just a link to the home page.
        # Categories are stored as a string
        data_top_article = requests.get(top_url)
        soup_top_article = BeautifulSoup(data_top_article.text, "html.parser")
        top_categories = ", ".join(
            [cat.string for cat in soup_top_article.find("nav", "breadcrumbs", "ul") \
                .find_all("a") if cat.string != "Home"]
            )

        # List of titles and urls
        # for the top picks featured articles only (the two following articles).
        titles_soup = soup.find_all("h3", "card__title")
        pick_titles = [titles_soup[i].span.string.strip() for i in range(2)]
        url_soup = soup.find_all("div", "card__image")
        picks_urls = [url_soup[i].a["href"] for i in range(2)]

        # List of titles and urls
        # for the other articles (15).
        other_titles = []
        other_urls = []
        other_titles_soup = soup.find_all("ul", "grid")
        for titles_soup in [other_titles_soup[1], other_titles_soup[2]]:
            other_titles.append([title.a.string.strip() for title in titles_soup.find_all("h3", "card__title")])
            other_urls.append([title.a["href"] for title in titles_soup.find_all("h3", "card__title")])
        # flatten those nested lists
        other_titles = sum(other_titles, [])
        other_urls = sum(other_urls, [])

        # Categories of articles except the top one:
        # 1- soup setup for categories scrapping
        # 2- for each article, store a string of categories
        # (for 2+15=17 articles)
        categories_soup = soup.find_all("div", "card__category label")
        other_articles_categories = [", ".join(
            [category.string for category in categories_soup[i].find_all("a")]
            ) for i in range(17)]

        # Lists of titles, urls and categories for all the articles
        # of the first page.
        df_titles = pd.DataFrame(
            {"title": [top_title] + pick_titles + other_titles})
        df_urls = pd.DataFrame({"url": [top_url] + picks_urls + other_urls})
        df_categories = pd.DataFrame(
            {"categories": [top_categories] + other_articles_categories})

        # Create:
        # - a list of articles' date,
        # - a list of articles' author,
        # - a list of articles' tags,
        # - a list of articles' leads.
        # For each articles: scrap data and append those 4 lists.
        date_for_each_article = []
        author_for_each_article = []
        tags_for_each_article = []
        text_for_each_article = []

        for url in df_urls["url"]:
            article_data = self.scrap_one_article_page(url)
            date_for_each_article.append(article_data['date'])
            author_for_each_article.append(article_data['author'])
            tags_for_each_article.append(article_data['tags'])
            text_for_each_article.append(article_data['text'])
            print("*", end="", flush=True) # simple progression bar
            self.sleep_random_time()

        # Display the number of articles scrapped right after
        # the simple progression bar.
        print(f" {len(df_urls)} articles scrapped on this page.\n")

        # Create pandas dataframe for articles' date,
        # articles' author, articles' tags, and articles' text.
        df_dates = pd.DataFrame({'date': date_for_each_article})
        df_authors = pd.DataFrame({'author': author_for_each_article})
        df_tags = pd.DataFrame({'tags': tags_for_each_article})
        df_texts = pd.DataFrame({'text': text_for_each_article})

        # Concatenate the previous df and return the final df
        return pd.concat(
            [df_urls, df_titles, df_dates, df_authors, df_categories,
             df_tags, df_texts], axis=1
            )


    def scrap_blog_one_page_for_page_two_and_more(self, page: int = 2) -> pd.core.frame.DataFrame:
        """
        Scrap 1 page of the website's blog, for page two and more.
        Page one has a different layout than other pagers.
        For page one, see the method: self.scrap_blog_page_one_only()
        :param page: page number, minimum value: 2
        :type date: int
        :raise ConnectionError: if page not found
        :return: a dataframe with articles' url | title | date | author |
            category | tags | text
        :rtype: pandas.core.frame.DataFrame
        """

        # Check if the argument is valid (int >= 2)
        try:
            if int(page) <= 1:
                raise ValueError("argument must be integer >= 2")
        except ValueError:
            raise ValueError("argument must be integer >= 2")

        # Setup the url, request, soup setup and scrap.
        # Raise exception if page not found
        page_url = f"{self.get_website_blog_url()}{int(page)}/"
        data = requests.get(page_url)
        soup = BeautifulSoup(data.text, "html.parser")
        if soup.h1.string == 'Page not found':
            raise ConnectionError('Page not found')

        # Display the page URL
        print(f"Scrap articles from URL page: {page_url}")

        # Create pandas dataframes for all the titles
        # and all the articles' urls.
        titles_soup = soup.find_all("h3", "card__title")
        df_titles = pd.DataFrame(
            {'title': [title.a["title"] for title in titles_soup]}
            )
        df_urls = pd.DataFrame(
            {'url': [title.a["href"] for title in titles_soup]}
            )

        # Create a pandas dataframe to store the categories of all the articles of the page:
        # 1- soup setup for categories scrapping,
        # 2- for each article, store a string of categories.
        categories_soup = soup.find_all("div", "card__category label")
        categories_for_each_article = [", ".join(
            [category.string for category in categories.find_all("a")]
            ) for categories in categories_soup]
        df_categories = pd.DataFrame({'categories': categories_for_each_article})

        # Create:
        # - a list of articles' date,
        # - a list of articles' author,
        # - a list of articles' tags,
        # - a list of articles' leads
        # For each articles: scrap data and append those 4 lists.
        date_for_each_article = []
        author_for_each_article = []
        tags_for_each_article = []
        text_for_each_article = []

        for url in df_urls["url"]:
            article_data = self.scrap_one_article_page(url)
            date_for_each_article.append(article_data['date'])
            author_for_each_article.append(article_data['author'])
            tags_for_each_article.append(article_data['tags'])
            text_for_each_article.append(article_data['text'])
            print("*", end="", flush=True) # simple progression bar
            self.sleep_random_time()

        # Display the number of articles scrapped right after
        # the simple progression bar.
        print(f" {len(df_urls)} articles scrapped on this page.\n")

        # Create pandas dataframe for articles' date,
        # articles' author, articles' tags, and articles' text
        df_dates = pd.DataFrame({'date': date_for_each_article})
        df_authors = pd.DataFrame({'author': author_for_each_article})
        df_tags = pd.DataFrame({'tags': tags_for_each_article})
        df_texts = pd.DataFrame({'text': text_for_each_article})

        # Concatenate the previous df and return the final df
        return pd.concat(
            [df_urls, df_titles, df_dates, df_authors, df_categories,
             df_tags, df_texts], axis=1
            )


    def scrap_all_blog_articles(self):
        """
        Scrap all the pages of the website's blog
        :return: a dataframe with articles' url | title | date | author |
            category | tags | text
        :rtype: pandas.core.frame.DataFrame
        """

        # Scrap first articles' page.
        df_all_articles = self.scrap_blog_page_one_only()

        # Scrap the following articles' pages and concat the df
        # until the method scrap_blog_one_page_for_page_two_and_more()
        # returns an empty df or raise an exception.
        page = 2
        while True:
            try:
                df_page = self.scrap_blog_one_page_for_page_two_and_more(page)
            except:
                print(f"Error on page {page}. Please check it.")
                break
            if len(df_page) == 0:
                break
            df_all_articles = pd.concat([df_all_articles, df_page])
            if page >= 75:
                break
            page += 1
        return df_all_articles


    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")


def main():
    print("The library scrape_one_page.py has been ran directly.")


if __name__ == "__main__":
    main()
