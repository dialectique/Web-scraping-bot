"""
tests scrape_one_page.py
"""
import os
from scrappackage.scrap_blog_articles import Website_blog


wb = Website_blog()


def test_scrap_blog_page_one_only():
    db = wb.scrap_blog_page_one_only()
    file_name = f"websiteblog_first_page.csv"
    db.to_csv(file_name, mode='w', index=None, header=True)
    assert os.path.exists(file_name)


def test_scrap_blog_one_page_for_page_two_and_more():
    page = 8
    db = wb.scrap_blog_one_page_for_page_two_and_more(page)
    file_name = f"websiteblog_onepage_page_{page}.csv"
    db.to_csv(file_name, mode='w', index=None, header=True)
    assert os.path.exists(file_name)


# other tests to write
