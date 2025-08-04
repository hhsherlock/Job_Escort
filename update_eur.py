#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Tue Jul 29 2025
    
    @author: Yaning
"""

from bs4 import BeautifulSoup
import csv
import os
from datetime import date
import pandas as pd


today = date.today().strftime("%Y_%m_%d")


HTML_DIR = "/home/yaning/Documents/Job_Escort/htmls/eur/new"
# keep a record of crawled lists in csv (good for revisit)
OUTPUT_CSV = f"/home/yaning/Documents/Job_Escort/csv_records/eur/euraxess_{today}.csv"

all_jobs = []
def safe_get_text(soup_element):
    return soup_element.get_text(strip=True) if soup_element else None

def extract_jobs_from_html(html_content, file_name):

    soup = BeautifulSoup(html_content, "lxml")
    begin = file_name.find('_')
    end = file_name.rfind('_')
    keyword = file_name[begin+1:end]

    jobs = []
    
    ul = soup.find("ul", class_="unformatted-list")
    if ul != None:
        job_list = ul.find_all("li", recursive=False)
        
        for job in job_list:
            location = safe_get_text(job.find("span", class_="ecl-label ecl-label--highlight"))
            temp = job.find_all("li", class_="ecl-content-block__primary-meta-item")
            institute = safe_get_text(temp[0])
            posted_on = safe_get_text(temp[1]).replace("Posted on: ", "")
            ddl = safe_get_text(job.find("time"))
            link = job.find("h3", class_="ecl-content-block__title").find("a").get("href")
            title = safe_get_text(job.find("h3", class_="ecl-content-block__title"))
            details = safe_get_text(job.find("div", class_="ecl-content-block__description"))

            dict = {
                "title": title,
                "location": location,
                "posted_on": posted_on,
                "deadline": ddl,
                "details": details,
                "institute": institute,
                "link": link,
                "keyword": keyword
            }

            jobs.append(dict)

    return jobs

# Loop through HTML files
for filename in os.listdir(HTML_DIR):
    if filename.endswith(".html"):
        filepath = os.path.join(HTML_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            html = file.read()
            jobs_in_file = extract_jobs_from_html(html, filename)
            all_jobs.extend(jobs_in_file)

# Save to CSV
if all_jobs:
    fieldnames = all_jobs[0].keys()
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"✅ Saved {len(all_jobs)} jobs to {OUTPUT_CSV}")
else:
    print("⚠️ No jobs found.")



# filtering and get the new jobs
old_df = pd.read_csv("/home/yaning/Documents/Job_Escort/htmls/eur/old.csv")
new_df = pd.read_csv(OUTPUT_CSV)


# update the old.csv add the new jobs into the old csv
combined_df = pd.concat([old_df, new_df], ignore_index=True)
# drop the duplication job that got from different keywords
subset_cols = [col for col in combined_df.columns if col != 'keyword']
combined_df = combined_df.drop_duplicates(subset=subset_cols)
combined_df.to_csv("/home/yaning/Documents/Job_Escort/htmls/eur/old.csv", index=False)



# combine the posted_time and the link to make sure they are the same
old_df['comb'] = old_df['posted_on'].astype(str) + '|' + old_df['link'].astype(str)
new_df['comb'] = new_df['posted_on'].astype(str) + '|' + new_df['link'].astype(str)

new_df['exist'] = new_df['comb'].isin(old_df['comb'])
filtered_df = new_df[~new_df['exist']]
# also need to get rid of the same job different keywords
subset_cols = [col for col in filtered_df.columns if col != 'keyword']
filtered_df = filtered_df.drop_duplicates(subset=subset_cols)

filtered_df.to_csv(f"/home/yaning/Documents/Job_Escort/new_jobs/eur/euraxess_{today}.csv")

