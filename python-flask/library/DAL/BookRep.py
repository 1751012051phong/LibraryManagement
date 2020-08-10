from library import db
from library.Common.util import ConvertModelListToDictList
from library.DAL import models
from flask import jsonify, json
from library.Common.util import ConvertModelListToDictList


def GetBooksByPage(req):
    book_pagination = models.Books.query.paginate(page=req.page, per_page=req.per_page)
    has_next = book_pagination.has_next
    has_prev = book_pagination.has_prev
    books = ConvertModelListToDictList(book_pagination.items)
    print(type(books))
    return has_next, has_prev, books


def CreateBook(req):
    book = models.Books(book_name=req.book_name,
                        supplier_id=req.supplier_id,
                        category_id=req.category_id,
                        author_id=req.author_id,
                        old_amount=req.old_amount,
                        new_amount=req.new_amount,
                        image=req.image,
                        page_number=req.page_number,
                        description=req.description,
                        cost_price=req.cost_price,
                        retail_price=req.retail_price,
                        discount=req.discount,
                        ranking=req.ranking)

    db.session.add(book)
    db.session.commit()
    return req


def DeleteBookById(req):
    book = models.Books.query.get(req.book_id)
    db.session.delete(book)
    db.session.commit()
    return req


def UpdateBook(req):
    book = models.Books.query.get(req.book_id)
    book.book_name = req.book_name
    book.supplier_id = req.supplier_id
    book.category_id = req.category_id
    book.author_id = req.author_id
    book.old_amount = req.old_amount
    book.new_amount = req.new_amount
    book.image = req.image
    book.page_number = req.page_number
    book.description = req.description
    book.cost_price = req.cost_price
    book.retail_price = req.retail_price
    book.discount = req.discount
    book.ranking = req.ranking
    db.session.add(book)
    db.session.commit()
    return req


def SearchBookById(req):
    book = models.Books.query.get(req.book_id)
    db.session.commit()
    return book


def SearchBookByName(req):
    model_books = models.Books.query.filter(models.Books.book_name.contains(req.book_name)).all()
    books = ConvertModelListToDictList(model_books)
    return books
