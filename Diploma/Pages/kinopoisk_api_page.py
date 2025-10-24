from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import requests
from dotenv import load_dotenv
import os



class KinopoiskAPI:
    """Page Object для работы с API Кинопоиск.dev"""

    load_dotenv()
    token = os.getenv("Token")
    BASE_URL = "https://api.kinopoisk.dev/v1.4"
    
    def __init__(self)-> None:
        self.headers = {"X-API-KEY": self.token}

    @allure.step("Поиск фильма по названию: {title}")
    def search_movie_by_title(self, title: str)-> None:
        """Ищет фильм по названию."""
        url = f"{self.BASE_URL}/movie/search"
        params = {"query": title}
        response = requests.get(url, headers=self.headers, params=params, timeout=60)
        return response

    @allure.step("Поиск фильма по году: {year}")
    def search_movie_by_year(self, year: str)-> None:
        """Ищет фильм по году."""
        url = f"{self.BASE_URL}/movie"
        params = {'page': 1,
                   'limit': 10,
                    'year': year
                  }
        response = requests.get(url, headers=self.headers, params=params, timeout=60)
        return response

    @allure.step("Поиск актёра по имени: {name}")
    def search_person(self, name: str)-> None:
        """Ищет актёра по имени."""
        url = f"{self.BASE_URL}/person/search"
        params = {"query": name}
        response = requests.get(url, headers=self.headers, params=params, timeout=60)
        return response

    @allure.step("Получение информации о фильме по ID: {movie_id}")
    def get_movie_by_id(self, movie_id: int)-> None:
        """Возвращает данные о фильме по ID."""
        url = f"{self.BASE_URL}/movie/{movie_id}"
        response = requests.get(url, headers=self.headers)
        return response

    @allure.step("Получение информации об актёре по ID: {person_id}")
    def get_person_by_id(self, person_id: int)-> None:
        """Возвращает данные об актёре по ID."""
        url = f"{self.BASE_URL}/person/{person_id}"
        response = requests.get(url, headers=self.headers, timeout=60)
        return response