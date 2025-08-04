class MovieCollector:
    def __init__(self):
        # Словарь фильмов: {название_фильма: жанр}
        self.movies_genre = {}
        # Список избранных фильмов
        self.favorites = []
        # Доступные жанры фильмов
        self.available_genres = ['Драма', 'Фантастика', 'Комедия', 'Боевик', 'Ужасы']
        # Жанры, не подходящие для детей
        self.adult_genres = ['Ужасы', 'Боевик']

    def add_new_movie(self, name):
        """
        Добавляет новый фильм в коллекцию.
        Условия добавления:
        - Фильма еще нет в коллекции
        - Длина названия от 1 до 100 символов включительно
        """
        if name not in self.movies_genre and 1 <= len(name) <= 100:
            self.movies_genre[name] = ''  # Жанр по умолчанию - пустая строка

    def set_movie_genre(self, name, genre):
        """
        Устанавливает жанр для фильма.
        Условия установки:
        - Фильм существует в коллекции
        - Жанр есть в списке доступных жанров
        """
        if name in self.movies_genre and genre in self.available_genres:
            self.movies_genre[name] = genre

    def get_movie_genre(self, name):
        """
        Возвращает жанр фильма по названию.
        - Возвращает None, если фильма нет в коллекции
        - Возвращает жанр (строку), если фильм есть
        """
        return self.movies_genre.get(name)

    def get_movies_by_genre(self, genre):
        """
        Возвращает список фильмов указанного жанра.
        - Возвращает пустой список, если жанр недопустим
        - Возвращает все фильмы с указанным жанром
        """
        if genre not in self.available_genres:
            return []

        return [movie for movie, movie_genre in self.movies_genre.items()
                if movie_genre == genre]

    def get_movies_for_children(self):
        """
        Возвращает фильмы, подходящие для детей:
        - Жанр установлен (не пустая строка)
        - Жанр не входит в adult_genres
        """
        return [movie for movie, genre in self.movies_genre.items()
                if genre and genre not in self.adult_genres]

    def add_movie_to_favorites(self, name):
        """
        Добавляет фильм в избранное.
        Условия:
        - Фильм существует в коллекции
        - Фильм еще не в избранном
        """
        if name in self.movies_genre and name not in self.favorites:
            self.favorites.append(name)

    def remove_movie_from_favorites(self, name):
        """
        Удаляет фильм из избранного.
        - Если фильма нет в избранном, ничего не происходит
        """
        if name in self.favorites:
            self.favorites.remove(name)

    def get_favorites_movies(self):
        """Возвращает список избранных фильмов."""
        return self.favorites

    def get_all_movies(self):
        """Возвращает полный словарь всех фильмов (название: жанр)."""
        return self.movies_genre