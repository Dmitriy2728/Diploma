from Pages.kinopoisk_page import KinopoiskPage
from selenium import webdriver
import pytest
import allure

@pytest.mark.ui
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

class TestKinopoiskSearch:

    @allure.feature("Поисковая строка на Кинопоиске")
    @allure.title("Открытие главной страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем, что главная страница Кинопоиска успешно открывается")
    def test_open_homepage(self, driver):
        page = KinopoiskPage(driver)
        page.open()
        assert "Кинопоиск" in driver.title, "Главная страница не открылась"

    @allure.title("Поиск фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем, что поиск по названию фильма 'Матрица' возвращает корректные результаты.")
    def test_search_movie_by_name(self, driver):
        page = KinopoiskPage(driver)
        page.open()
        page.search_something("Матрица")
        results = page.get_search_results(driver)
        assert any("Матрица" in r for r in results), "Фильм не найден в результатах поиска"

    @allure.title("Поиск актёра по имени")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что поиск по имени актёра 'Киану Ривз' возвращает список релевантных результатов.")
    def test_search_actor_by_name(self, driver):
        page = KinopoiskPage(driver)
        page.open()
        page.search_something("Киану Ривз")
        results = page.get_search_results(driver)
        assert any("Киану Ривз" in r for r in results), "Актёр не найден в результатах поиска"
    
    @allure.title("Поиск по пустому запросу")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Проверяем, что сайт переводит нас страницу случайного фильма и не падает.")
    def test_search_empty_query(self, driver):
        page = KinopoiskPage(driver)
        page.open()
        page.search_something("")
        assert "Случайный фильм!" in driver.title, "Не должно быть ошибки"

    @allure.title("Поиск по негативному запросу")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Проверяем, что сайт выдает нам сообщение.")
    def test_search_bad_query(self, driver):
        page = KinopoiskPage(driver)
        page.open()
        page.search_something("1п4 562р22прй4е")
        assert page.bad_request(), (
            "Не появилось сообщение «К сожалению, по вашему запросу ничего не найдено»"
        )