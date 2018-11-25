import pandas as pd
from bs4 import BeautifulSoup
import csv


# Removes htlm tags from a review
def review_remove_html(review):
    return BeautifulSoup(review, 'lxml').get_text()
