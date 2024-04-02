from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import datetime, csv, re, time

current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%d.%m %H_%M")
file_name = f"drushim {formatted_time}.csv"

driver_path = "/opt/homebrew/bin/chromedriver"
opt = webdriver.ChromeOptions()
# opt.add_argument("--headless")
web = webdriver.Chrome(service=Service(driver_path), options=opt)
web.implicitly_wait(10)


header = ["Title", "Company", "Job description", "Requirements", "Categories", "Link"]
jobs_rows = []


def write_csv(file, rows):
    with open(file, "w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)

page = 0
url = f"https://il.indeed.com/jobs?q=it&rbl=תל+אביב+-יפו,+מחוז+תל+אביב&jlid=fd347958ce788d3b&start={page}"
web.get(url)
job_listing_num = 1
counter = 0
# total_listings_text = web.find_element(
#     By.CSS_SELECTOR, "jobsearch-JobCountAndSortPane-jobCount>span"
# ).text
# total_listings = re.findall(r"\d+", total_listings_text)[0]


def next_page_btn():
    page += 10
    web.get(url)


# print(f"\n started scraping {total_listings} listings \n")

while True:
    try:
        lis = web.find_elements(
            By.CSS_SELECTOR,
            "#mosaic-jobResults ul>li",
        )
        for li in lis:
            print(f"Scrape job {job_listing_num}")
            print(li.text)
            time.sleep(1)
            job_listing_num += 1
            counter += 1
            if counter == 10:
                counter = 0
                next_page_btn()

        # divs = box.find_elements(By.TAG_NAME, "div")

        # find the div corresponding to the info you want to scrape
        # for div in divs:
        #     print(f'{div.get_attribute("innerHTML")}\n\n')

        # title = divs[2].text
        # company = divs[15].text

        # gather all the divs again in the updated html after clicking the + button

        # updated_divs = web.find_element(
        #     By.CSS_SELECTOR,
        #     f"div.jobList_vacancy:nth-child({num}) > div:nth-child(1) > div",
        # ).find_elements(By.TAG_NAME, "div")
        # for description in updated_divs:
        #     text = description.text
        #     if "תיאור משרה" in text:
        #         job_desc = text.replace("\n", " ")
        #     if "דרישות התפקיד" in text:
        #         req = text.replace("\n", " ")
        # box1 = box.find_elements(By.TAG_NAME, "a")
        # box2 = box.find_elements(By.TAG_NAME, "tbody")
        # box2 = [b.text for b in box2]
        # categories = box2[0].replace("\n", " & ")
        # link = box1[3].get_attribute("href")
        # jobs_rows.append((title, company, job_desc, req, categories, link))
        # if want to limit results
        # if job_listing_num == 10:
        #     break

        # only 10 pages avilable onjobmaster currently
        if job_listing_num == 102:
            break
    except Exception as e:
        if "element click intercepted" in str(e):
            print("no more items - clickling on next page")
            page += 1
            next_page_btn()
            continue
        # elif "stale element not found in the current frame" in str(e):
        #     print("advertisement div - skipping 1 div")
        #     # job_listing_num += 1
        #     continue
        else:
            print(e)
            break

# print(f"\nFinished scraping successfully {job_listing_num-1} out of {total_listings} listings \n")

# write_csv(file_name, jobs_rows)
