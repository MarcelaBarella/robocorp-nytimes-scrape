from datetime import datetime
from dateutil.relativedelta import relativedelta
from pages.nytimes.nytimes import NYTimes
from RPA.Excel.Files import Files
from RPA.Robocorp.WorkItems import WorkItems
import urllib.request
from urllib.parse import urlparse, unquote
import re
import os

# Transforms the data including new fields
def main():

    work_items = WorkItems()
    work_items.get_input_work_item()
    payload = work_items.get_work_item_payload()
    files = work_items.get_work_item_files("*")

    articles = payload["articles"]
    
    lib = Files()
    filename = "./output/articles.xlsx"
    lib.create_workbook(filename)
    lib.append_rows_to_worksheet(articles, None, True)
    lib.save_workbook()
    files.append(filename)

    work_items.create_output_work_item({ "articles": articles }, files, True)

# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
