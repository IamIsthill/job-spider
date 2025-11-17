import asyncio
from typing import TypedDict

from playwright.async_api import async_playwright
from playwright_stealth import Stealth

import constants
from parse_html import parseHtml, findContent
from gsheet import getSpreadSheet

async def visit_url(url: str) -> str:
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        return await page.content()

class JobInfo(TypedDict):
    title: str
    company: str
    location: str
    work_type: str
    salary: str
    description: str
    job_link: str

async def get_job_links(base: str, starting_url:str,  selector: dict) -> list[str]:
    doc = parseHtml(await visit_url(starting_url))

    elements = doc.find_all(attrs=selector)

    links: list[str] = []

    if(len(elements) > 0):
        for link in elements:
            if link.get('href'):
                full_link = constants.BASE_URL + link.get('href')
                links.append(full_link)
    
    return links

async def get_job_detail(link:str) -> JobInfo:    
    job: JobInfo = {}
        
    doc = parseHtml(await visit_url(link))

    for key, value in constants.JOB_INFO.items():
        info = findContent(doc, {constants.SELECTOR:value})
        job[key] = info

    job['job_link'] = link
    return job

async def main():
    links = await get_job_links(constants.BASE_URL, constants.STARTING_URL, {constants.SELECTOR: constants.JOB_LINKS})

    if not links:
        print('No job fetched')
        return
    
    jobs: list[JobInfo] = []

    for link in links:
        job = await get_job_detail(link)
        jobs.append(job)

    sheet = getSpreadSheet()

    # Add header
    header = list(constants.JOB_INFO.keys())
    header.append('job_link')
    sheet.update("A1", [header])

    # Save jobs
    for job in jobs:
        row = list(job.values())
        sheet.append_row(row)


asyncio.run(main())
