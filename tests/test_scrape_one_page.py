"""
tests scrape_one_page.py
"""
import pytest
import os
from scrappackage.scrap_blog_articles import Website_blog, main


wb = Website_blog()

def test_sleep_random_time():
    assert wb.sleep_random_time() == None


def test_get_website_blog_url():
    # Get and return the absolute path of the root directory.
    root_abs_path = os.path.dirname(
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    )
    # read the .env file to get the url for testing purpose.
    with open(os.path.join(root_abs_path, ".env")) as f:
        env_var_dict = {}
        for line in f:
            var_name, value = line.split("=")
            env_var_dict[var_name] = value
    WEBSITE_BLOG_URL_TEST = env_var_dict["WEBSITE_BLOG_URL_TEST"].strip()
    assert WEBSITE_BLOG_URL_TEST == wb.get_website_blog_url()


def test_convert_date_correct_date_format():
    assert wb.convert_date("June 17th, 2020") == "2020-06-17"


def test_convert_date_correct_date_wrong_format_1():
    with pytest.raises(Exception):
        wb.convert_date("June 17th 2020")


def test_convert_date_correct_date_wrong_format_2():
    with pytest.raises(Exception):
        wb.convert_date("August, 3rd 2021")


def test_convert_date_correct_date_wrong_format_3():
    with pytest.raises(Exception):
        wb.convert_date("2019 September 3")


def test_scrap_one_article_page():
    # Get and return the absolute path of the root directory.
    root_abs_path = os.path.dirname(
    os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    )
    # read the .env file to get an article's url for testing purpose.
    with open(os.path.join(root_abs_path, ".env")) as f:
        env_var_dict = {}
        for line in f:
            var_name, value = line.split("=")
            env_var_dict[var_name] = value
    WEBSITE_ARTICLE_PAGE_TEST = env_var_dict["WEBSITE_ARTICLE_PAGE_TEST"].strip()
    returned_data = wb.scrap_one_article_page(WEBSITE_ARTICLE_PAGE_TEST)
    assert len(returned_data) == 4


def test_scrap_blog_page_one_only():
    df = wb.scrap_blog_page_one_only()
    assert len(df) == 18
    assert len(df.columns) == 7


def test_scrap_blog_one_page_for_page_two_and_more():
    page = 8
    df = wb.scrap_blog_one_page_for_page_two_and_more(page)
    assert len(df) == 24
    assert len(df.columns) == 7


def test_scrap_all_blog_articles():
    df = wb.scrap_all_blog_articles()
    file_name = f"all_articles.csv"
    df.to_csv(file_name, mode='w', index=None, header=True)


def test_ping():
    assert wb.ping() == "pong"

def test_main():
    assert main() == None
