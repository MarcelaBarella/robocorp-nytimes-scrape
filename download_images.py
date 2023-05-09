from datetime import datetime
from RPA.Robocorp.WorkItems import WorkItems
import urllib.request
from urllib.parse import urlparse, unquote

# Download article image from web


def main():

    work_items = WorkItems()
    work_items.get_input_work_item()
    payload = work_items.get_work_item_payload()
    articles = payload["articles"]
    files = []

    def download_image(article):
        filename_from_url = unquote(
            urlparse(article["picture_url"]).path.split("/")[-1])
        (filename, _) = urllib.request.urlretrieve(
            article["picture_url"], f"./output/{filename_from_url}")
        article["picture_filename"] = filename
        files.append(filename)
        return article

    articles = list(map(download_image, articles))

    # Outputs articles and pictures
    work_items.create_output_work_item({"articles": articles}, files, True)


# Call the main() function, checking that
# we are running as a stand-alone script:
if __name__ == "__main__":
    main()
