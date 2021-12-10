from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import httplib2
import pandas as pd
import os
import json

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\google\clients_secrets.json",
    ["https://www.googleapis.com/auth/analytics.readonly"],
)

http = credentials.authorize(httplib2.Http())
service = build(
    "analytics",
    "v4",
    http=http,
    discoveryServiceUrl="https://analyticsreporting.googleapis.com/$discovery/rest",
)

regex = "~^/4-ways-to-take-your-business-into-the-future/.*"

response = (
    service.reports()
    .batchGet(
        body={
            "reportRequests": [
                {
                    "viewId": "172173820",
                    "dateRanges": [{"startDate": "90daysAgo", "endDate": "today"}],
                    "metrics": [{"ga:7dayUsers"}],
                    "dimensions": [{"ga:userType"}],
                    "filtersExpression": f"ga:pagePath={regex}",
                    "orderBys": [
                        {"fieldName": "ga:7dayUsers", "sortOrder": "DESCENDING"}
                    ],
                    "pageSize": 10000,
                }
            ]
        }
    )
    .execute()
)


dim = []
val = []


# Extract Data
for report in response.get("reports", []):

    columnHeader = report.get("columnHeader", {})
    dimensionHeaders = columnHeader.get("dimensions", [])
    metricHeaders = columnHeader.get("metricHeader", {}).get("metricHeaderEntries", [])
    rows = report.get("data", {}).get("rows", [])

    for row in rows:

        dimensions = row.get("dimensions", [])
        dateRangeValues = row.get("metrics", [])

        for header, dimension in zip(dimensionHeaders, dimensions):
            dim.append(dimension)

        for i, values in enumerate(dateRangeValues):
            for metricHeader, value in zip(metricHeaders, values.get("values")):
                val.append(int(value))

df = pd.DataFrame()
df["Sessions"] = val
df["pagePath"] = dim
df = df[["pagePath", "Sessions"]]

print(df)

df.to_csv("page_by_session.csv")
