import asyncio
from typing import Any, TypedDict

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

import constants
from parse_html import parseHtml, findContent

async def visit_url(url: str) -> str:
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
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
    job: JobInfo = {'job_link': link}
        
    doc = parseHtml(await visit_url(link))

    for key, value in constants.JOB_INFO.items():
        info = findContent(doc, {constants.SELECTOR:value})
        job[key] = info
    
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

asyncio.run(main())
