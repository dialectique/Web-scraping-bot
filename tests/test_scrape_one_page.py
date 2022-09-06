"""
tests scrape_one_page.py
"""
import os
from scrappackage.scrape_one_page import Website_blog


wb = Website_blog()

def test_scrap_blog_one_page_with_existing_page():
    page = 8
    db = wb.scrap_blog_one_page(page)
    file_name = f"websiteblog_onepage_page_{page}.csv"
    db.to_csv(file_name, mode='w', index=None, header=True)
    assert os.path.exists(file_name)

# other tests to write
