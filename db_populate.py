import requests
from app import app, db
from Db.models import Book

api_key = 'AIzaSyBpiflNK2MZPg-Cux2uqK5CUeR0jcuem2k'
books_data = []

# Функция для загрузки данных о книгах
def load_books(start_index):
    url = f"https://www.googleapis.com/books/v1/volumes?q=subject:fiction&langRestrict=ru&startIndex={start_index}&maxResults=40&key={api_key}"
    response = requests.get(url)
    data = response.json()

    for item in data.get('items', []):
        info = item.get('volumeInfo', {})
        books_data.append({
            "title": info.get('title', 'Нет названия'),
            "author": ', '.join(info.get('authors', ['Неизвестный автор'])),
            "number_of_pages": info.get('pageCount', 0),
            "publisher": info.get('publisher', 'Неизвестное издательство'),
            "cover_photo": info.get('imageLinks', {}).get('thumbnail')
        })

with app.app_context():
    db.create_all()
    for start_index in range(0, 120, 40):
        load_books(start_index)

    books_to_add = [Book(**book_data) for book_data in books_data]
    db.session.bulk_save_objects(books_to_add)
    db.session.commit()

    print(f"{len(books_to_add)} добавлено с API.")

