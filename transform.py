from RPA.Robocorp.WorkItems import WorkItems
import re

# Transforms the data including new fields
def main():

    work_items = WorkItems()
    work_items.get_input_work_item()
    payload = work_items.get_work_item_payload()

    articles = payload["articles"]
    search_phrase = payload["config"]["search_phrase"]

    def calculate_extra_columns(article):
        article["search_phrase_count"] = count_search_phrases(article, search_phrase)
        article["contains_amount_of_money"] = contains_amount_of_money(article)
        return article
    
    articles = list(map(calculate_extra_columns, articles))

    work_items.create_output_work_item({ "articles": articles }, None, True)


def count_search_phrases(article, search_phrase):
    return article["title"].count(search_phrase) + article["description"].count(search_phrase)

# Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
def contains_amount_of_money(article):
    title_and_description = " ".join([article["title"], article["description"]])

    # Format $111,111.1 | $11.1 (also accepting $11)
    if re.search(r'\$(?:[0-9]{1,3})(?:,[0-9]{3})*(?:\.[0-9]{1,2})?', title_and_description) != None: return True

    # Format 11 dollars | 11 USD
    if re.search(r'[0-9]+ (?:dollars|dollar|USD)', title_and_description) != None: return True

    return False


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()
