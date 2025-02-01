import pytest

from main import BooksCollector

class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def setup_method(self):
        self.collector = BooksCollector()

    @pytest.mark.parametrize("book_name", ["Властелин колец", "Гарри Поттер", "1984"])
    def test_add_new_book_valid(self, book_name):
        self.collector.add_new_book(book_name)
        assert book_name in self.collector.get_books_genre()

    def test_add_new_book_duplicate(self):
        self.collector.add_new_book("Властелин колец")
        self.collector.add_new_book("Властелин колец")
        assert len(self.collector.get_books_genre()) == 1

    @pytest.mark.parametrize("invalid_book_name", [
        "",
        "Очень длинное название книги, которое превышает допустимую длину в 40 символов"
    ])
    def test_add_new_book_invalid(self, invalid_book_name):
        self.collector.add_new_book(invalid_book_name)
        assert invalid_book_name not in self.collector.get_books_genre()

    @pytest.mark.parametrize(
        "book_name, genre",
        [
            ("Игра престолов", "Фантастика"),
            ("Хоббит", "Фантастика"),
            ("Сияние", "Ужасы"),
            ("Убийство в Восточном экспрессе", "Детективы"),
        ]
    )
    def test_set_book_genre_valid(self, book_name, genre):
        self.collector.add_new_book(book_name)
        self.collector.set_book_genre(book_name, genre)
        assert self.collector.get_book_genre(book_name) == genre

    def test_set_book_genre_invalid_genre(self):
        self.collector.add_new_book("Игра престолов")
        self.collector.set_book_genre("Игра престолов", "Научная фантастика")
        assert self.collector.get_book_genre("Игра престолов") == ""

    def test_set_book_genre_book_not_exists(self):
        self.collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert self.collector.get_book_genre("Несуществующая книга") is None

    @pytest.mark.parametrize(
        "book_name, genre",
        [
            ("Гарри Поттер", "Фантастика"),
            ("Ведьмак", "Фантастика"),
        ]
    )
    def test_get_book_genre_valid(self, book_name, genre):
        self.collector.add_new_book(book_name)
        self.collector.set_book_genre(book_name, genre)
        assert self.collector.get_book_genre(book_name) == genre

    def test_get_book_genre_invalid(self):
        assert self.collector.get_book_genre("Несуществующая книга") is None

    def test_get_books_with_specific_genre(self):
        self.collector.add_new_book("Книга 1")
        self.collector.add_new_book("Книга 2")
        self.collector.set_book_genre("Книга 1", "Фантастика")
        self.collector.set_book_genre("Книга 2", "Фантастика")
        assert self.collector.get_books_with_specific_genre("Фантастика") == ["Книга 1", "Книга 2"]

    def test_get_books_with_specific_genre_empty(self):
        assert self.collector.get_books_with_specific_genre("Фантастика") == []

    def test_get_books_genre(self):
        self.collector.add_new_book("книга1")
        self.collector.set_book_genre("книга1", "Фантастика")
        assert self.collector.get_books_genre() == {"книга1": "Фантастика"}

    def test_get_books_for_children(self):
        self.collector.add_new_book("Книга 1")
        self.collector.add_new_book("Книга 2")
        self.collector.set_book_genre("Книга 1", "Мультфильмы")
        self.collector.set_book_genre("Книга 2", "Ужасы")
        assert self.collector.get_books_for_children() == ["Книга 1"]

    def test_get_books_for_children_empty(self):
        assert self.collector.get_books_for_children() == []

    def test_add_book_in_favorites(self):
        self.collector.add_new_book("Алхимик")
        self.collector.add_book_in_favorites("Алхимик")
        assert self.collector.get_list_of_favorites_books() == ["Алхимик"]

    def test_add_book_in_favorites_already_exists(self):
        self.collector.add_new_book("Алхимик")
        self.collector.add_book_in_favorites("Алхимик")
        self.collector.add_book_in_favorites("Алхимик")
        assert self.collector.get_list_of_favorites_books() == ["Алхимик"]

    def test_add_book_in_favorites_not_exists(self):
        self.collector.add_book_in_favorites("Несуществующая книга")
        assert self.collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites(self):
        self.collector.add_new_book("Мастер и Маргарита")
        self.collector.add_book_in_favorites("Мастер и Маргарита")
        self.collector.delete_book_from_favorites("Мастер и Маргарита")
        assert self.collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_not_exists(self):
        self.collector.delete_book_from_favorites("Несуществующая книга")
        assert self.collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books(self):
        self.collector.add_new_book("1984")
        self.collector.add_book_in_favorites("1984")
        assert self.collector.get_list_of_favorites_books() == ["1984"]

    def test_get_list_of_favorites_books_empty(self):
        assert self.collector.get_list_of_favorites_books() == []