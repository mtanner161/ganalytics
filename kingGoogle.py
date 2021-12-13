## Google API report that pulls all relavent data from King Operating Website
## Developed by Michael Tanner - Sandstone Group

# Google imports classes needed $ pip install google-analytics-data
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

# packages needed for the full project
import pandas as pd
import numpy as np
import os
import json
import requests
import matplotlib.pyplot as plt


# intializes the Google Cloud Client
def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


# runs activeUserReport which gets total number of user-historcal
def activeUserReport(property_id="263279665"):
    property_id = "263279665"  # propertyID from Google Analytics
    client = BetaAnalyticsDataClient()  # calls the authentaction token

    request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="1daysAgo", end_date="today")],
    )
    response = client.run_report(request)

    # prints results
    print("Michael result:")
    for row in response.rows:
        global numViews
        numViews = row.metric_values[0].value
        print(numViews)


# brings in legacy data (if you do not have any, skip this step)
legacyDailyViews = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\ganalytics\cleanUserBetter.csv"
)

# creates an empty DataFrame to hold data
legacyDailyViews.columns = ["Date", "Users"]

# Runs the file
if __name__ == "__main__":
    activeUserReport()

legacyDailyViews = legacyDailyViews.append(
    {"Date": "12/12/2021", "Users": numViews}, ignore_index=True
)

legacyDailyViews.to_csv("./king/ganalytics/cleanUserBetter.csv", index=False)

print(legacyDailyViews)

print("hello")
