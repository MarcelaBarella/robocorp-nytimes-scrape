from datetime import datetime
from dateutil.relativedelta import relativedelta
from pages.nytimes.nytimes import NYTimes
from RPA.Robocorp.WorkItems import WorkItems
from SeleniumLibrary.errors import ElementNotFound


def main():
    # Read input config
    work_items = WorkItems()
    work_items.get_input_work_item()
    config = work_items.get_work_item_payload()

    nytimes = NYTimes()

    try:
        nytimes.open()

        # Need to accept GDPR otherwise the overlay
        # can interfere with interactions
        try:
            nytimes.accept_gdpr()
        except ElementNotFound:
            # GDPR terms might not appear depending on the session and locale
            # and does not represent an error
            pass

        search_results = nytimes.search(config["search_phrase"])
        search_results.sort_by("newest")
        search_results.filter_sections(config["sections"])

        cut_date = calculate_cut_date(config["months"])

        # Loads enough pages as to guarantee we get all data
        # for the considered months
        while datetime.strptime(search_results.articles[-1]["date"],
                                "%Y-%m-%d").date() > cut_date:
            if not search_results.load_more_articles():
                break

        # Filters only articles from the cut date onwards
        articles = list(filter(lambda article: datetime.strptime(
            article["date"],
            "%Y-%m-%d").date() >= cut_date,
            search_results.articles))

        # Output articles to a WorkItem for next task
        work_items.create_output_work_item(
            {"articles": articles, "config": config}, None, True)

    finally:
        # Always close the browser
        nytimes.close_browser()


def calculate_cut_date(months):
    now = datetime.now()

    # Calculates how many months ago we need to fetch
    # from the configuration variable using the rule:
    #
    # 0 or 1: only current month (0 months ago)
    # 2: 1 month ago
    # 3: 2 months ago
    # ...
    months_ago = months - 1
    if months_ago < 0:
        months_ago = 0

        # Calculates the minimum date we're going to consider
        #
        # subtracts months_ago months from the date
        # sets the day of the month to 1
    cut_date = (now + relativedelta(months=(-1) * months_ago, day=1)).date()
    return cut_date


# Call the scrape() function, checking that
# we are running as a stand-alone script:
if __name__ == "__main__":
    main()
