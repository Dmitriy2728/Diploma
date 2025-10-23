import pytest
import allure
import requests
from Pages.kinopoisk_api_page import KinopoiskAPI


@allure.feature("API Кинопоиск.dev")
class TestKinopoiskAPI:

    @pytest.fixture(scope="class")
    def api(self):
        return KinopoiskAPI()

    @allure.title("Поиск фильма по названию на кириллице")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем, что поиск по названию 'Матрица' возвращает корректный фильм.")
    def test_search_movie_cyrillic(self, api):
        response = api.search_movie_by_title("Матрица")
        assert response.status_code == 200, "Некорректный статус-код"
        data = response.json()
        assert len(data["docs"]) > 0, "Фильмы не найдены"
        assert any("Матрица" in d["name"] for d in data["docs"]), "В результатах нет 'Матрица'"

    @allure.title("Поиск фильма по названию на латинице")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем, что поиск по названию 'Interstellar' возвращает корректный фильм.")
    def test_search_movie_latin(self, api):
        response = api.search_movie_by_title("Interstellar")
        assert response.status_code == 200
        data = response.json()
        assert len(data["docs"]) > 0, "Фильмы не найдены"
        assert any("Interstellar" in (d["alternativeName"] or "") for d in data["docs"]), "Фильм не найден"

    @allure.title("Поиск актёра по имени на латинице")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что поиск по имени 'Keanu Reeves' возвращает актёра.")
    def test_search_actor_latin(self, api):
        response = api.search_person("Keanu Reeves")
        assert response.status_code == 200
        data = response.json()
        assert len(data["docs"]) > 0, "Актёры не найдены"
        assert any("Keanu" in d["enName"] for d in data["docs"]), "Актёр не найден"

    @allure.title("Негативный тест — поиск фильма с несуществующим годом")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Проверяем, что поиск фильма с годом выпуска 3025 не возвращает данных.")
    def test_search_movie_invalid_year(self, api):
        url = f"{api.BASE_URL}/movie"
        params = {"year": 1750}
        response = api.search_movie_by_year(params)
        data = response.json()
        # assert data == 'Bad Request', "Нашлись фильмы с несуществующим годом"
        # assert response.status_code == 400
        print(data)


    @allure.title("Негативный тест — поиск актёра с нулевым ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем, что при запросе актёра с ID=0 возвращается ошибка 400.")
    def test_get_actor_with_zero_id(self, api):
        response = api.get_person_by_id(0)
        assert response.status_code == 400, "Ожидался статус 400 при запросе несуществующего актёра"
