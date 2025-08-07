#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Wed Aug 6 2025
    
    @author: Yaning
"""

from bs4 import BeautifulSoup
import csv
import os
from datetime import date
import pandas as pd


today = date.today().strftime("%Y_%m_%d")


HTML_DIR = "/home/yaning/Documents/Job_Escort/htmls/zeit/new"
# keep a record of crawled lists in csv (good for revisit)
OUTPUT_CSV = f"/home/yaning/Documents/Job_Escort/csv_records/zeit/zeit_{today}.csv"

all_jobs = []
def safe_get_text(soup_element):
    return soup_element.get_text(strip=True) if soup_element else None

def extract_jobs_from_html(html_content, file_name):

    soup = BeautifulSoup(html_content, "lxml")
    begin = file_name.find('_')
    end = file_name.rfind('_')
    keyword = file_name[begin+1:end]

    jobs = []
    
    ul = soup.find("ul", class_="flex flex-col gap-2", id="job-teasers-job-teasers")
    if ul != None:
        job_list = ul.find_all("li", recursive=False)
        
        for job in job_list:
            institute = safe_get_text(job.find("p", class_="text-style-paragraph-sm line-clamp-2 overflow-ellipsis text-left text-text-55"))
            title = safe_get_text(job.find("h2", class_="inline break-words"))
            location = safe_get_text(job.find("div", class_="inline-flex min-w-0 max-w-min items-center text-center font-medium text-white-0 bg-primary-60 rounded-[4px] py-[2px] px-[6px] [print-color-adjust:exact] text-sm tracking-[0.035px] leading-4 md:leading-5"))
            posted_on = safe_get_text(job.find("div", class_="inline-flex min-w-0 max-w-min items-center text-center font-medium text-text-70 bg-neutral-20 rounded-[4px] py-[2px] px-[6px] [print-color-adjust:exact] text-sm tracking-[0.035px] leading-4 md:leading-5"))

            dict = {
                "title": title,
                "location": location,
                "posted_on": posted_on,
                "institute": institute,
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
old_df = pd.read_csv("/home/yaning/Documents/Job_Escort/htmls/zeit/old.csv")
new_df = pd.read_csv(OUTPUT_CSV)


# update the old.csv add the new jobs into the old csv
combined_df = pd.concat([old_df, new_df], ignore_index=True)
# drop the duplication job that got from different keywords
subset_cols = [col for col in combined_df.columns if col != 'keyword']
combined_df = combined_df.drop_duplicates(subset=subset_cols)
combined_df.to_csv("/home/yaning/Documents/Job_Escort/htmls/zeit/old.csv", index=False)



# combine the posted_time and the link to make sure they are the same
old_df['comb'] = old_df['posted_on'].astype(str) + '|' + old_df['location'].astype(str)
new_df['comb'] = new_df['posted_on'].astype(str) + '|' + new_df['location'].astype(str)

new_df['exist'] = new_df['comb'].isin(old_df['comb'])
filtered_df = new_df[~new_df['exist']]
# also need to get rid of the same job different keywords
subset_cols = [col for col in filtered_df.columns if col != 'keyword']
filtered_df = filtered_df.drop_duplicates(subset=subset_cols)

filtered_df.to_csv(f"/home/yaning/Documents/Job_Escort/new_jobs/zeit/zeit_{today}.csv")

