from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class KinopoiskPage:
    """Главная страница сервиса Кинопоиск"""

    URL = "https://www.kinopoisk.ru/"

    def __init__(self, driver: webdriver.Chrome) -> None:
        """
        Инициализация главной страницы

        :param driver: экземпляр Selenium WebDriver.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.implicitly_wait(5)
    @allure.step ('Открываем главную страницу сервиса')
    def open(self) -> None:
             """Открываем главную страницу сервиса Кинопоиск"""
             self.driver.get(self.URL)
   
    @allure.step('Выполняем поиск фильма')
    def search_something(self, query: str)-> None:
        """Вводим запрос в поле поиска и выполняем поиск."""
        search = self.driver.find_element(By.NAME, "kp_query")
        search.send_keys(query)
        search.send_keys(Keys.RETURN)

    @allure.step("Получаем список результатов поиска")
    def get_search_results(self, driver)-> List[str]:
        """Получаем список найденных фильмов (или актеров)."""
        selector = 'a[data-type="film"]'
        wait = WebDriverWait(driver, 10) 
       
        results = self.driver.find_elements(By.CSS_SELECTOR, selector)
        return [r.text for r in results]
    
    @allure.step("Открываем первый результат из полученного списка")
    def open_first_result(self)-> None:
        """Кликаем по первому элементу из полученного списка"""
        selector = 'a[data-type="film"]'
        first = self.driver.find_elements(By.CSS_SELECTOR, selector)
    
    @allure.step ('Проверка сообщения на негативный запрос')
    def bad_request(self) -> bool:
        """Проверяем, что появилось сообщение «Ничего не найдено»."""
        message = self.wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//*[contains(text(), 'К сожалению, по вашему запросу ничего не найдено')]"
                ))
        )
        return message.is_displayed()
        