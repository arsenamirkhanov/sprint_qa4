import pytest
from movie_collector import MovieCollector


class TestMovieCollector:

    @pytest.fixture
    def collector(self):
        """Фикстура создает новый экземпляр MovieCollector перед каждым тестом"""
        return MovieCollector()

    # Тесты инициализации
    def test_initial_state(self, collector):
        """Проверка начального состояния коллекции"""
        assert collector.movies_genre == {}
        assert collector.favorites == []
        assert collector.available_genres == ['Драма', 'Фантастика', 'Комедия', 'Боевик', 'Ужасы']
        assert collector.adult_genres == ['Ужасы', 'Боевик']

    # Тесты для add_new_movie
    @pytest.mark.parametrize("name", [
        "A",  # минимальная длина
        "Фильм с нормальным названием",
        "   ",  # только пробелы
        "Фильм" * 20,  # 100 символов
    ])
    def test_add_new_movie_valid(self, collector, name):
        """Проверка добавления фильмов с валидными названиями"""
        collector.add_new_movie(name)
        assert name in collector.movies_genre
        assert collector.movies_genre[name] == ""

    @pytest.mark.parametrize("name", [
        "",  # пустая строка
        "A" * 101,  # слишком длинное название
    ])
    def test_add_new_movie_invalid_length(self, collector, name):
        """Проверка обработки невалидной длины названия"""
        collector.add_new_movie(name)
        assert name not in collector.movies_genre

    def test_add_new_movie_duplicate(self, collector):
        """Проверка обработки дубликатов"""
        collector.add_new_movie("Дубликат")
        collector.add_new_movie("Дубликат")
        assert list(collector.movies_genre.keys()) == ["Дубликат"]

    # Тесты для set_movie_genre
    def test_set_movie_genre_valid(self, collector):
        """Установка валидного жанра для существующего фильма"""
        collector.add_new_movie("Матрица")
        collector.set_movie_genre("Матрица", "Фантастика")
        assert collector.get_movie_genre("Матрица") == "Фантастика"

    def test_set_movie_genre_invalid_genre(self, collector):
        """Попытка установить недопустимый жанр"""
        collector.add_new_movie("Неудачник")
        collector.set_movie_genre("Неудачник", "Романтика")
        assert collector.get_movie_genre("Неудачник") == ""

    def test_set_movie_genre_nonexistent_movie(self, collector):
        """Попытка установить жанр для несуществующего фильма"""
        collector.set_movie_genre("Призрак", "Ужасы")
        assert "Призрак" not in collector.movies_genre

    # Тесты для get_movie_genre
    def test_get_movie_genre_exists(self, collector):
        """Получение жанра для фильма с установленным жанром"""
        collector.add_new_movie("Криминальное чтиво")
        collector.set_movie_genre("Криминальное чтиво", "Боевик")
        assert collector.get_movie_genre("Криминальное чтиво") == "Боевик"

    def test_get_movie_genre_unset(self, collector):
        """Получение жанра для фильма без жанра"""
        collector.add_new_movie("Без жанра")
        assert collector.get_movie_genre("Без жанра") == ""

    def test_get_movie_genre_missing(self, collector):
        """Получение жанра для несуществующего фильма"""
        assert collector.get_movie_genre("Неизвестный") is None

    # Тесты для get_movies_by_genre
    def test_get_movies_by_genre_exists(self, collector):
        """Получение фильмов по существующему жанру"""
        # Добавляем и настраиваем фильмы
        collector.add_new_movie("Комедия 1")
        collector.set_movie_genre("Комедия 1", "Комедия")
        collector.add_new_movie("Комедия 2")
        collector.set_movie_genre("Комедия 2", "Комедия")
        collector.add_new_movie("Драма")
        collector.set_movie_genre("Драма", "Драма")

        result = collector.get_movies_by_genre("Комедия")
        assert len(result) == 2
        assert "Комедия 1" in result
        assert "Комедия 2" in result
        assert "Драма" not in result

    def test_get_movies_by_genre_no_matches(self, collector):
        """Получение фильмов по жанру без совпадений"""
        collector.add_new_movie("Фильм")
        collector.set_movie_genre("Фильм", "Фантастика")
        assert collector.get_movies_by_genre("Драма") == []

    def test_get_movies_by_genre_invalid_genre(self, collector):
        """Получение фильмов по недопустимому жанру"""
        collector.add_new_movie("Фильм")
        assert collector.get_movies_by_genre("Мюзикл") == []

    # Тесты для get_movies_for_children
    def test_get_movies_for_children_valid(self, collector):
        """Получение детских фильмов"""
        # Детские фильмы
        collector.add_new_movie("История игрушек")
        collector.set_movie_genre("История игрушек", "Комедия")
        collector.add_new_movie("Звездные войны")
        collector.set_movie_genre("Звездные войны", "Фантастика")

        # Взрослые фильмы
        collector.add_new_movie("Пила")
        collector.set_movie_genre("Пила", "Ужасы")
        collector.add_new_movie("Рэмбо")
        collector.set_movie_genre("Рэмбо", "Боевик")

        # Фильм без жанра
        collector.add_new_movie("Без жанра")

        result = collector.get_movies_for_children()
        assert len(result) == 2
        assert "История игрушек" in result
        assert "Звездные войны" in result
        assert "Пила" not in result
        assert "Рэмбо" not in result
        assert "Без жанра" not in result

    def test_get_movies_for_children_no_valid_movies(self, collector):
        """Проверка случая, когда нет подходящих детских фильмов"""
        collector.add_new_movie("Ужасы")
        collector.set_movie_genre("Ужасы", "Ужасы")
        collector.add_new_movie("Боевик")
        collector.set_movie_genre("Боевик", "Боевик")
        assert collector.get_movies_for_children() == []

    # Тесты для работы с избранным
    def test_add_to_favorites_valid(self, collector):
        """Добавление существующего фильма в избранное"""
        collector.add_new_movie("Избранный")
        collector.add_movie_to_favorites("Избранный")
        assert "Избранный" in collector.get_favorites_movies()

    def test_add_to_favorites_invalid_movie(self, collector):
        """Попытка добавить несуществующий фильм в избранное"""
        collector.add_movie_to_favorites("Призрак")
        assert collector.get_favorites_movies() == []

    def test_add_to_favorites_duplicate(self, collector):
        """Попытка добавить фильм в избранное дважды"""
        collector.add_new_movie("Дубль")
        collector.add_movie_to_favorites("Дубль")
        collector.add_movie_to_favorites("Дубль")
        assert collector.get_favorites_movies() == ["Дубль"]

    def test_remove_from_favorites_exists(self, collector):
        """Удаление фильма из избранного"""
        collector.add_new_movie("Удаляемый")
        collector.add_movie_to_favorites("Удаляемый")
        collector.remove_movie_from_favorites("Удаляемый")
        assert "Удаляемый" not in collector.get_favorites_movies()

    def test_remove_from_favorites_not_exists(self, collector):
        """Попытка удалить несуществующий фильм из избранного"""
        collector.add_new_movie("Остающийся")
        collector.add_movie_to_favorites("Остающийся")
        collector.remove_movie_from_favorites("Несуществующий")
        assert collector.get_favorites_movies() == ["Остающийся"]

    # Тесты для get_all_movies и get_favorites_movies
    def test_get_all_movies(self, collector):
        """Получение полной коллекции фильмов"""
        collector.add_new_movie("Фильм 1")
        collector.add_new_movie("Фильм 2")
        assert collector.get_all_movies() == {"Фильм 1": "", "Фильм 2": ""}

    def test_get_favorites_movies(self, collector):
        """Получение списка избранных фильмов"""
        collector.add_new_movie("Фаворит 1")
        collector.add_movie_to_favorites("Фаворит 1")
        collector.add_new_movie("Фаворит 2")
        collector.add_movie_to_favorites("Фаворит 2")
        assert collector.get_favorites_movies() == ["Фаворит 1", "Фаворит 2"]

    # Дополнительные тесты для граничных случаев
    def test_add_movie_max_length(self, collector):
        """Добавление фильма с названием ровно 100 символов"""
        name = "A" * 100
        collector.add_new_movie(name)
        assert name in collector.movies_genre

    def test_add_movie_min_length(self, collector):
        """Добавление фильма с названием ровно 1 символ"""
        name = "A"
        collector.add_new_movie(name)
        assert name in collector.movies_genre

    def test_set_genre_twice(self, collector):
        """Изменение жанра фильма дважды"""
        collector.add_new_movie("Переключатель")
        collector.set_movie_genre("Переключатель", "Комедия")
        collector.set_movie_genre("Переключатель", "Драма")
        assert collector.get_movie_genre("Переключатель") == "Драма"

    def test_get_movies_for_children_with_unavailable_genre(self, collector):
        """Фильмы с недоступным жанром не должны включаться"""
        collector.add_new_movie("Странный жанр")
        collector.movies_genre["Странный жанр"] = "Мюзикл"  # Прямая установка недопустимого жанра
        assert "Странный жанр" not in collector.get_movies_for_children() # Не работает в коде орига