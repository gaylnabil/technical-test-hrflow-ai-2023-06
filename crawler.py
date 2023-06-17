import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from hrflow import Hrflow
import requests


class Crawler:
    """
    selenium Crawler Class
    """

    def __init__(self, settings: dict):
        PATH = 'C:\chromedriver_win32\chromedriver.exe'
        chrome_options = webdriver.ChromeOptions()
# "--headless=new": Compatible in Chrome 109 and above
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280x1696")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--log-level=0")
        chrome_options.add_argument("--v=99")
        chrome_options.add_argument("--ignore-certificate-errors")

        self._driver = webdriver.Chrome(
            service=Service(PATH), options=chrome_options)

        self._settings = settings

        self._client = Hrflow(api_secret=self._settings['X_API_KEY'],
                              api_user=self._settings['X_USER_EMAIL'])

    def get_driver(self):
        return self._driver

    def client(self):
        return self._client

    def format_job(self) -> dict:
        """
        Format the scrapped job according to the HrFlow.ai Job format
        @param driver: Crawler driver
        @return: job in the HrFlow.ai format of skills
        """
        return {
            "name": None,
            "agent_key": None,
            "reference": None,
            "url": None,
            "created_at": None,
            "updated_at": None,
            "summary": "",
            "location": {
                "text": None,
                "lat": None,
                "lng": None,
            },
            "sections": [],
            "skills": [],
            "languages": [],
            "tags": [
            ],
            "ranges_date": [],
            "ranges_float": [],
            "metadatas": [],
        }

    def is_job_exists(self, reference: str) -> bool:
        return self.client().job.indexing.get(
            board_key=self._settings["BOARD_KEY"], reference=reference
        ).get("data") is not None

    def save(self, jon_json: dict) -> int:
        return int(self.client().job.indexing.add_json(
            board_key=self._settings["BOARD_KEY"], job_json=jon_json)['code'])

    def close(self):
        self.get_driver().quit()
