import re
import os
import requests

import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime



class Website_blog:
    """
    a class for scrap a particular website's blog articles
    environment variable BLOG_URL contains the website URL
    """


    def get_website_blog_url(self):
        """
        get the the absolute path of the root directory
        and read the .env file to get the environement variable
        which contains the website's blog url
        .env file must contain only one environment variable
        :return: website's blog url
        :rtype: string
        """
        root_abs_path = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
        with open(os.path.join(root_abs_path, ".env")) as f:
            _, text = f
        return text.split("=")[1].strip()

    def scrap_blog_one_page(self, page: int = 2) -> pd.core.frame.DataFrame:
        """
        Scrap 1 page of the website blog
        :param page: page number, minimum value: 2
        :type date: int
        :raise ConnectionError: if page not found
        :return: a dataframe with articles name | url | dates | categories
        :rtype: pandas.core.frame.DataFrame
        """

        # check if the argument is valid (int >= 2)
        try:
            if int(page) <= 1:
                raise ValueError("argument must be interger >= 2")
        except ValueError:
            raise ValueError("argument must be interger >= 2")

        # setup the url, request, soup setup and scrap.
        # Raise exception if page not found
        page_url = f"{self.get_website_blog_url()}{int(page)}/"
        data = requests.get(page_url)
        soup = BeautifulSoup(data.text, "html.parser")
        if soup.h1.string == 'Page not found':
            raise ConnectionError('Page not found')

        # create pandas dataframes for all the titles
        # and all the articles' urls of the page
        titles_soup = soup.find_all("h3", "card__title")
        df_titles = pd.DataFrame(
            {'titles': [title.a["title"] for title in titles_soup]}
            )
        df_urls = pd.DataFrame(
            {'urls': [title.a["href"] for title in titles_soup]}
            )

        # create a pandas dataframe to store the categories of all the articles of the page:
        # 1- soup setup for categories scrapping
        # 2- for each article, store a list of categories in a list
        # 3- create a list of all the unique categories of all the page's articles
        # 4- create a dict: for each category, store a list of 0 and 1
        # where 1: the article has the category, else 0
        categories_soup = soup.find_all("div", "card__category label")
        categories_for_each_article = [
            [category.string for category in categories.find_all("a")]
            for categories in categories_soup]
        categories_keys = sorted(list(set(sum(categories_for_each_article, []))))
        categories_dict = {}
        for key in categories_keys:
            categories_dict[key] = [
                1 if key in cats else 0 for cats in categories_for_each_article
                ]
        df_categories = pd.DataFrame(categories_dict)

        # for each article, create:
        # a list of articles' date,
        # a list of articles' author,
        # a list of articles' tags,
        # a list of articles' leads
        # for each articles: request the article url, scrap and append the two lists
        date_for_each_article = []
        author_for_each_article = []
        tags_for_each_article = []
        text_for_each_article = []
        for url in df_urls['urls']:
            data = requests.get(url)
            soup = BeautifulSoup(data.text, "html.parser")
            article_date = soup.find("div", "hero__meta") \
                .span.string.split("|")[0].strip()
            date_for_each_article.append(self.convert_date(article_date))
            article_author = soup.find("div", "hero__meta") \
                .span.string.split("|")[1].strip()
            author_for_each_article.append(article_author)
            article_tags = soup.find_all("li", "tags__tag")
            tags_for_each_article.append([tag.a.string for tag in article_tags])
            article_text = " ".join(
                [p.get_text() for p in soup \
                    .find("div", "entry-content__content") \
                    .find_all(["h2", "h3", "p"])]
                )
            text_for_each_article.append(article_text)

        # create pandas dataframes for the tags (similary to the categories df)
        tags_keys = sorted(list(set(sum(tags_for_each_article, []))))
        tags_dict = {}
        for key in tags_keys:
            tags_dict[key] = [
                1 if key in tags else 0 for tags in tags_for_each_article
                ]
        df_tags = pd.DataFrame(tags_dict)

        # create pandas dataframe for articles' date,
        # articles' author and articles' text
        df_dates = pd.DataFrame({'dates': date_for_each_article})
        df_authors = pd.DataFrame({'dates': author_for_each_article})
        df_texts = pd.DataFrame({'leads': text_for_each_article})

        return pd.concat(
            [df_titles, df_dates, df_authors,
             df_texts, df_tags], axis=1
            )


    def convert_date(self, date: str = "") -> str:
        """
        Convert a date to "YYYY-MM-DD" format
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
            "Date doesn't have the required format. For example:\n"
            "February 1st, 2017'  'May 2nd, 1997'  'June 3rd, 2008'  'March 4th, 2015'"
            )


    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")


def main():
    print("The library scrape_one_page.py has been ran directly.")

if __name__ == "__main__":
    main()
