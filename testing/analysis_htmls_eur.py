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

today = date.today().strftime("%Y_%m_%d")

HTML_DIR = "/home/yaning/Documents/Job_Escort/htmls/08_01"
OUTPUT_CSV = f"euraxess_{today}.csv"


all_jobs = []

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
            location = job.find("span", class_="ecl-label ecl-label--highlight").get_text(strip=True)
            temp = job.find_all("li", class_="ecl-content-block__primary-meta-item")
            institute = temp[0].get_text(strip=True)
            posted_on = temp[1].get_text(strip=True).replace("Posted on: ", "")
            ddl = job.find("time").get_text(strip=True)
            link = job.find("h3", class_="ecl-content-block__title").find("a").get("href")
            title = job.find("h3", class_="ecl-content-block__title").get_text(strip=True)
            details = job.find("div", class_="ecl-content-block__description").get_text(strip=True)

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

