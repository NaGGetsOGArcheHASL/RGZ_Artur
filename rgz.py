from flask import Blueprint, render_template, request, make_response, redirect, session, url_for
from Db import db
from Db.models import User, Book
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user

rgz = Blueprint('rgz', __name__) 


@rgz.route("/", methods=['GET'])
def main():
    page = request.args.get('page', 1, type=int)
    title_filter = request.args.get('title', '', type=str)
    author_filter = request.args.get('author', '', type=str)
    pages_from = request.args.get('pages_from', type=int)
    pages_to = request.args.get('pages_to', type=int)
    publisher_filter = request.args.get('publisher', '', type=str)
    query = Book.query

    if title_filter:
        query = query.filter(Book.title.like(f"%{title_filter}%"))
    if author_filter:
        query = query.filter(Book.author.like(f"%{author_filter}%"))
    if pages_from is not None and pages_to is not None:
        query = query.filter(Book.number_of_pages.between(pages_from, pages_to))
    if publisher_filter:
        query = query.filter(Book.publisher.like(f"%{publisher_filter}%"))

    books = query.paginate(page=page, per_page=20)

    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Guest"

    return render_template('main.html', books=books, username=username)


@rgz.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username_form = request.form.get("username").strip()
    password_form = request.form.get("password")

    if not username_form:
        return render_template("register.html", errors='Пустое имя пользователя')

    if User.query.filter_by(username=username_form).first():
        return render_template("register.html", errors='Пользователь с таким именем уже существует')

    if len(password_form) < 5:
        return render_template("register.html", errors='Пароль должен быть длиннее 5 символов')

    hashed_password = generate_password_hash(password_form, method='pbkdf2:sha256')
    new_user = User(username=username_form, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/login")


@rgz.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username_form = request.form.get("username").strip()
    password_form = request.form.get("password")

    if not username_form or not password_form:
        return render_template("login.html", errors='Заполните поля пользователя и пароля')

    user = User.query.filter_by(username=username_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=False)
        return redirect(url_for('rgz.main'))
    else:
        return render_template("login.html", errors='Неверное имя пользователя или пароль')


@rgz.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        # Извлекаем данные из формы
        title = request.form.get('title')
        author = request.form.get('author')
        number_of_pages = request.form.get('number_of_pages')
        publisher = request.form.get('publisher')
        cover_photo = request.form.get('cover_photo')

        # Обновляем данные книги
        book.title = title
        book.author = author
        book.number_of_pages = number_of_pages
        book.publisher = publisher
        book.cover_photo = cover_photo

        # Сохраняем изменения в базе данных
        db.session.commit()

        return redirect(url_for('rgz.main'))

    return render_template('edit_book.html', book=book)

@rgz.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required  
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not current_user.is_admin:
        abort(403)
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('rgz.main'))


@rgz.route('/books/add', methods=['GET', 'POST'])
@login_required 
def add_book():
    if not current_user.is_admin:
        return "Access denied", 403  

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        number_of_pages = request.form.get('number_of_pages')
        publisher = request.form.get('publisher')
        cover_photo = request.form.get('cover_photo')
        new_book = Book(title=title, author=author, number_of_pages=number_of_pages, publisher=publisher, cover_photo=cover_photo)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('rgz.main'))
    
    return render_template('add_book.html')

    
@rgz.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('rgz.login'))
