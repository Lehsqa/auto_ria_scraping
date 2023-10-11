import asyncio
import re
from asyncio.exceptions import TimeoutError
from datetime import datetime
from typing import Any

import aiohttp
from aiohttp.client_exceptions import ClientPayloadError, ServerDisconnectedError
from bs4 import BeautifulSoup

from domain.car_details import CarDetailsRepository, CarDetailsUncommited


class Scraper:
    start_url: str = f'https://auto.ria.com/uk/search/?lang_id=4&page=0&countpage=100&indexName=auto&custom=1&abroad=2'

    def __int__(self):
        self._ERRORS = (ClientPayloadError, ServerDisconnectedError, TimeoutError)

    @staticmethod
    def parse_last_page(html: str) -> int:
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find_all('span', id_='page-item mhide')
        pages_list = [element.get('data-page') for element in pages if element.get('data-page')]
        if pages_list:
            return int(pages_list[-1])
        return 2000

    @staticmethod
    def parse_cars_urls(html: str) -> list[str]:
        soup = BeautifulSoup(html, 'html.parser')
        address_elements = soup.find_all('a', class_='address')
        urls = [element.get('href') for element in address_elements if element.get('href')]

        return urls

    @staticmethod
    def parse_car_details(html: str) -> dict[str, Any]:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h1', class_='head')
        price_usd = soup.find('div', class_='price_value').find('strong')
        odometer = soup.find('div', class_='base-information bold').find('span', class_='size18')
        username = soup.find('div', class_='seller_info_name bold')
        phone_number = ''
        image_url = soup.find('img', class_='outline m-auto')
        images_count = soup.find('a', class_='show-all link-dotted')
        car_number = soup.find('span', class_='state-num ua')
        car_vin = soup.find('span', class_='label-vin')

        return {
            'title': title.get('title') if title is not None else 'None',
            'price_usd': price_usd.get_text() if price_usd is not None else '0 $',
            'odometer': int(re.search(r'\d+', odometer.get_text()).group() + '000') if odometer is not None else 0,
            'username': username.get_text().replace(' ', '') if username is not None else 'None',
            'phone_number': phone_number,
            'image_url': image_url.get('src') if image_url is not None else 'None',
            'images_count': int(re.search(r'\d+', images_count.get_text()).group()) if images_count is not None else 0,
            'car_number': car_number.get_text() if car_number is not None else 'None',
            'car_vin': car_vin.get_text() if car_vin is not None else 'None',
            'datetime_found': datetime.now()
        }

    @staticmethod
    async def fetch(session: aiohttp.ClientSession, url: str) -> str:
        async with session.get(url) as response:
            assert response.status == 200
            await asyncio.sleep(0)
            print(url)
            return await response.text()

    async def get_cars_details(self, session: aiohttp.ClientSession, page_id: int) -> list[str] or None:
        main_url: str = f'https://auto.ria.com/uk/search/?lang_id=4&page={page_id}&countpage=100&indexName=auto&custom=1&abroad=2'

        try:
            html_cars_urls: str = await self.fetch(session=session, url=main_url)
            loop = asyncio.get_event_loop()
            urls: list[str] = await loop.run_in_executor(None, self.parse_cars_urls, html_cars_urls)
            for url in urls:
                html_car_details: str = await self.fetch(session=session, url=url)
                payload: dict[str, Any] = await loop.run_in_executor(None, self.parse_car_details, html_car_details)
                await CarDetailsRepository().create(
                    CarDetailsUncommited(url=url, **payload)
                )
        except self._ERRORS:
            return None

    async def aiohttp_event_loop(self):
        connector = aiohttp.TCPConnector(limit=25)
        timeout = aiohttp.ClientTimeout(total=1800)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = []

            html_last_page = await self.fetch(session=session, url=self.start_url)
            last_page = self.parse_last_page(html=html_last_page)

            for page_id in range(last_page):
                task = asyncio.create_task(self.get_cars_details(session=session, page_id=page_id))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.aiohttp_event_loop())
