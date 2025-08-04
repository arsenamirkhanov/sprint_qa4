import pytest  # Импортируем pytest для написания и запуска тестов
from books_collector import BooksCollector  # Импортируем тестируемый класс


class TestBooksCollector:

    # Фикстура создает новый экземпляр BooksCollector перед каждым тестом
    @pytest.fixture
    def collector(self):
        return BooksCollector()  # Возвращаем новый объект для теста

    # Тест конструктора __init__
    def test_init_initial_state(self, collector):
        # Проверяем начальное состояние объекта
        assert collector.books_genre == {}  # Словарь книг должен быть пустым
        assert collector.favorites == []  # Список избранного должен быть пустым
        # Проверяем предопределенные жанры
        assert collector.genre == ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        # Проверяем возрастные жанры
        assert collector.genre_age_rating == ['Ужасы', 'Детективы']

    # Тесты метода add_new_book
    @pytest.mark.parametrize('name', ['Нормальная книга', 'О' * 40])  # Параметризация: два валидных имени
    def test_add_new_book_valid_name(self, collector, name):
        collector.add_new_book(name)  # Вызываем метод добавления книги
        assert name in collector.books_genre  # Проверяем, что книга появилась в словаре
        assert collector.books_genre[name] == ''  # Проверяем, что жанр не установлен

    @pytest.mark.parametrize('name', ['', 'О' * 41])  # Невалидные имена: пустое, длинное
    def test_add_new_book_invalid_name_length(self, collector, name):
        collector.add_new_book(name)  # Пытаемся добавить книгу
        assert name not in collector.books_genre  # Проверяем, что книга НЕ добавилась

    def test_add_new_book_whitespace_name(self, collector):
        """Проверяем, что строки из пробелов не добавляются ОНИ ДОБАВЛЯЮТСЯ"""
        name = '   '  # 3 пробела
        collector.add_new_book(name)
        assert name not in collector.books_genre  # Должно быть не добавлено

    def test_add_new_book_duplicate(self, collector):
        collector.add_new_book('Дубль')  # Первое добавление
        collector.add_new_book('Дубль')  # Попытка добавить дубликат
        assert list(collector.books_genre.keys()) == ['Дубль']  # Проверяем только одну книгу в словаре

    # Тесты метода set_book_genre
    def test_set_book_genre_valid(self, collector):
        # Подготовка: напрямую добавляем книгу в словарь
        collector.books_genre = {'Книга': ''}
        collector.set_book_genre('Книга', 'Фантастика')  # Устанавливаем валидный жанр
        assert collector.books_genre['Книга'] == 'Фантастика'  # Проверяем установку жанра

    def test_set_book_genre_invalid_book(self, collector):
        # Попытка установить жанр для несуществующей книги
        collector.set_book_genre('Несуществующая', 'Фантастика')
        # Проверяем, что книга не появилась в словаре
        assert 'Несуществующая' not in collector.books_genre

    def test_set_book_genre_invalid_genre(self, collector):
        # Подготовка: напрямую добавляем книгу
        collector.books_genre = {'Книга': ''}
        # Пытаемся установить недопустимый жанр
        collector.set_book_genre('Книга', 'Недопустимый')
        assert collector.books_genre['Книга'] == ''  # Жанр должен остаться пустым

    # Тесты метода get_book_genre
    def test_get_book_genre_exists(self, collector):
        # Подготовка: напрямую задаем книгу с жанром
        collector.books_genre = {'Книга': 'Комедии'}
        # Проверяем получение жанра
        assert collector.get_book_genre('Книга') == 'Комедии'

    def test_get_book_genre_unset(self, collector):
        # Подготовка: книга без жанра
        collector.books_genre = {'Книга': ''}
        # Проверяем, что возвращается пустая строка
        assert collector.get_book_genre('Книга') == ''

    def test_get_book_genre_missing(self, collector):
        # Пытаемся получить жанр несуществующей книги
        assert collector.get_book_genre('Призрак') is None  # Должно вернуть None

    # Тесты метода get_books_with_specific_genre
    def test_get_books_with_specific_genre_exists(self, collector):
        # Подготовка: создаем несколько книг с разными жанрами
        collector.books_genre = {
            'Книга1': 'Мультфильмы',
            'Книга2': 'Мультфильмы',
            'Книга3': 'Детективы'
        }
        # Запрашиваем книги определенного жанра
        result = collector.get_books_with_specific_genre('Мультфильмы')
        # Проверяем, что вернулись только книги с нужным жанром
        assert result == ['Книга1', 'Книга2']

    def test_get_books_with_specific_genre_no_matches(self, collector):
        # Подготовка: книга с другим жанром
        collector.books_genre = {'Книга': 'Фантастика'}
        # Запрашиваем книги с жанром, которого нет
        result = collector.get_books_with_specific_genre('Ужасы')
        assert result == []  # Должен вернуться пустой список

    def test_get_books_with_specific_genre_invalid_genre(self, collector):
        # Подготовка: книга с валидным жанром
        collector.books_genre = {'Книга': 'Фантастика'}
        # Запрашиваем несуществующий жанр
        result = collector.get_books_with_specific_genre('Боевик')
        assert result == []  # Должен вернуться пустой список

    # Тест метода get_books_genre
    def test_get_books_genre(self, collector):
        # Подготовка: напрямую задаем словарь книг
        collector.books_genre = {'Книга1': '', 'Книга2': 'Фантастика'}
        # Проверяем, что метод возвращает полный словарь
        assert collector.get_books_genre() == {'Книга1': '', 'Книга2': 'Фантастика'}

    # Тесты метода get_books_for_children
    def test_get_books_for_children_valid(self, collector):
        # Подготовка: книги разных категорий
        collector.books_genre = {
            'Мультик': 'Мультфильмы',  # Детский
            'Комедия': 'Комедии',  # Детский
            'Ужастик': 'Ужасы',  # Возрастной
            'Детектив': 'Детективы'  # Возрастной
        }
        # Получаем детские книги
        result = collector.get_books_for_children()
        # Проверяем, что вернулись только безопасные жанры
        assert result == ['Мультик', 'Комедия']

    def test_get_books_for_children_no_genre(self, collector):
        # Подготовка: книга без жанра
        collector.books_genre = {'Книга': ''}
        # Должны получить пустой список
        assert collector.get_books_for_children() == []

    def test_get_books_for_children_invalid_genre(self, collector):
        # Подготовка: книга с неразрешенным жанром
        collector.books_genre = {'Книга': 'Боевик'}
        # Не должен включать книги с неразрешенными жанрами
        assert collector.get_books_for_children() == []

    # Тесты метода add_book_in_favorites
    def test_add_book_in_favorites_valid(self, collector):
        # Подготовка: добавляем книгу в коллекцию
        collector.books_genre = {'Книга': 'Фантастика'}
        # Добавляем в избранное
        collector.add_book_in_favorites('Книга')
        assert 'Книга' in collector.favorites  # Проверяем наличие в избранном

    def test_add_book_in_favorites_invalid_book(self, collector):
        # Пытаемся добавить несуществующую книгу
        collector.add_book_in_favorites('Призрак')
        assert collector.favorites == []  # Список должен остаться пустым

    def test_add_book_in_favorites_duplicate(self, collector):
        # Подготовка: книга уже в избранном
        collector.books_genre = {'Книга': 'Фантастика'}
        collector.favorites = ['Книга']  # Начальное состояние
        # Пытаемся добавить дубликат
        collector.add_book_in_favorites('Книга')
        # Проверяем, что дубликата нет
        assert collector.favorites == ['Книга']

    # Тесты метода delete_book_from_favorites
    def test_delete_book_from_favorites_exists(self, collector):
        # Подготовка: добавляем книгу в избранное
        collector.favorites = ['Книга']  # Прямая установка
        # Удаляем книгу
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.favorites  # Книга должна исчезнуть

    def test_delete_book_from_favorites_not_exists(self, collector):
        # Подготовка: в избранном есть другие книги
        collector.favorites = ['Другая книга']
        # Пытаемся удалить несуществующую в избранном книгу
        collector.delete_book_from_favorites('Книга')
        # Проверяем, что исходный список не изменился
        assert collector.favorites == ['Другая книга']

    # Тест метода get_list_of_favorites_books
    def test_get_list_of_favorites_books(self, collector):
        # Подготовка: задаем список избранного
        collector.favorites = ['Избранная1', 'Избранная2']
        # Проверяем, что метод возвращает полный список
        assert collector.get_list_of_favorites_books() == ['Избранная1', 'Избранная2']