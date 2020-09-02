from library import db
from library.Common.util import ConvertModelListToDictList


class Accounts(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    account_name = db.Column(db.String(50), nullable=False, unique=True)
    account_password = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(50))
    delete_at = db.Column(db.DateTime, default=None)
    customers = db.relationship('Customers', backref='account', lazy='subquery')
    employees = db.relationship('Employees', backref='account', lazy='subquery')

    def serialize(self):
        return {"account_id": self.account_id, "account_name": self.account_name, "note": self.note,
                "delete_at": self.delete_at, "role": self.role.serialize()}

    def __repr__(self):
        return f"Account('{self.account_id}','{self.account_name}','{self.note}', '{self.delete_at}', " \
               f"'{self.role.serialize()}')"


class Books(db.Model):
    book_id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True, unique=True)
    book_name = db.Column(db.String(50), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    old_amount = db.Column(db.Integer)
    new_amount = db.Column(db.Integer)
    image = db.Column(db.String(50))
    page_number = db.Column(db.Integer)
    description = db.Column(db.String(1500))
    cost_price = db.Column(db.Float)
    retail_price = db.Column(db.Float)
    discount = db.Column(db.Float)
    ranking = db.Column(db.String(50))
    delete_at = db.Column(db.DateTime, default=None)
    note = db.Column(db.String(1500))
    borrow_ticket_details = db.relationship('Borrowticketdetails', backref='book', lazy=True)
    stocktaketicketdetails = db.relationship('Stocktaketicketdetails', backref="book", lazy=True)

    def serialize(self):
        return {"book_id": self.book_id, "book_name": self.book_name, "note": self.note,
                "supplier": self.supplier.serialize(), "category": self.category.serialize(),
                "author": self.author.serialize(),
                "old_amount": self.old_amount, "new_amount": self.new_amount, "image": self.image,
                "page_number": self.page_number, "description": self.description, "cost_price": self.cost_price,
                "retail_price": self.retail_price, "discount": self.discount, "ranking": self.ranking,
                "delete_at": self.delete_at}

    def __repr__(self):
        return f"('book_id':{self.book_id},'book_name': {self.book_name},'note : {self.note},'supplier': {self.supplier.serialize()},'category': {self.category.serialize()}, " \
               f"'author': {self.author.serialize()},'old_amount': {self.old_amount},'new_amount': {self.new_amount},'image': {self.image},'page_number': {self.page_number}, " \
               f"'description ':{self.description},'cost_price': {self.cost_price},'retail_price': {self.retail_price},'discount': {self.discount},'ranking': {self.ranking})"


class Borrowticketdetails(db.Model):
    borrow_ticket_id = db.Column(db.Integer, db.ForeignKey('borrowtickets.borrow_ticket_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    delete_at = db.Column(db.DateTime, default=None)

    def serialize(self):
        return {"borrow_ticket_id": self.borrow_ticket_id, "book_id": self.book_id, "delete_at": self.delete_at}

    def __repr__(self):
        return f"('book_id':{self.book_id}, 'borrow_ticket_id': {self.borrow_ticket_id})"


class Borrowtickets(db.Model):
    borrow_ticket_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    quantity = db.Column(db.Integer)
    borrow_date = db.Column(db.DateTime)
    appointment_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    delete_at = db.Column(db.DateTime, default=None)
    note = db.Column(db.String(1500))
    borrow_ticket_detail = db.relationship('Borrowticketdetails', backref='borrowticket', lazy=True)

    def serialize(self):
        return {"borrow_ticket_id": self.borrow_ticket_id, "customer": self.customer.serialize(), "note": self.note,
                "employee": self.employee.serialize(), "quantity": self.quantity, "borrow_date": self.borrow_date,
                "appointment_date": self.appointment_date, "return_date": self.return_date, "status": self.status,
                "delete_at": self.delete_at, "borrow_ticket_detail": ConvertModelListToDictList(self.borrow_ticket_detail)}

    def __repr__(self):
        return f"Borrowticket('{self.borrow_ticket_id}','{self.customer.serialize()}','{self.note}','{self.employee.serialize()}'," \
               f"'{self.quantity}','{self.borrow_date}','{self.appointment_date}','{self.return_date}','{self.status}', '{self.delete_at}')"


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    category_name = db.Column(db.String(50))
    description = db.Column(db.String(1500))
    note = db.Column(db.String(1500))
    delete_at = db.Column(db.DateTime, default=None)
    books = db.relationship('Books', backref="category", lazy=True)

    def serialize(self):
        return {"category_id": self.category_id, "category_name": self.category_name, "note": self.note,
                "description": self.description, "delete_at": self.delete_at}

    def __repr__(self):
        return f"Category('{self.category_id}','{self.category_name}','{self.note}','{self.description}', '{self.delete_at}')"


class Customers(db.Model):
    customer_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    identity_id = db.Column(db.String(50), nullable=False, unique=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), unique=True)
    student_code = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(50))
    birth_date = db.Column(db.DateTime)
    address = db.Column(db.String(1500))
    gender = db.Column(db.Boolean)
    note = db.Column(db.String(1500))
    delete_at = db.Column(db.DateTime, default=None)
    borrow_tickets = db.relationship('Borrowtickets', backref='customer', lazy=True)
    orders = db.relationship('Orders', backref='customer', lazy=True)

    def serialize(self):
        return {"customer_id": self.customer_id, "identity_id": self.identity_id, "note": self.note,
                "account": self.account.serialize(), "student_code": self.student_code, "last_name": self.last_name,
                "first_name": self.first_name, "email": self.email, "phone": self.phone, "birth_day": self.birth_date,
                "address": self.address, "gender": self.gender, "delete_at": self.delete_at}

    def __repr__(self):
        return f"Customer('{self.customer_id}','{self.identity_id}','{self.note}','{self.account.serialize()}'," \
               f"'{self.student_code}','{self.first_name}','{self.last_name}','{self.email}','{self.birth_date}','{self.address}'," \
               f"'{self.gender}','{self.phone}', '{self.delete_at}')"


class Employees(db.Model):
    employee_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    identity_id = db.Column(db.String(50), nullable=False, unique=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), unique=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    birth_date = db.Column(db.DateTime)
    hire_date = db.Column(db.DateTime)
    address = db.Column(db.String(1500))
    gender = db.Column(db.Boolean)
    image = db.Column(db.String(50))
    basic_rate = db.Column(db.Float)
    note = db.Column(db.String(1500))
    delete_at = db.Column(db.DateTime, default=None)
    schedules = db.relationship('Schedules', backref='employee', lazy=True)
    orders = db.relationship('Orders', backref='employee', lazy=True)
    borrow_tickets = db.relationship('Borrowtickets', backref='employee', lazy=True)
    stocktake_tickets = db.relationship('Stocktaketickets', backref='employee', lazy=True)

    def serialize(self):
        return {"employee_id": self.employee_id, "identity_id": self.identity_id, "note": self.note,
                "account": self.account.serialize(), "last_name": self.last_name, "first_name": self.first_name,
                "phone": self.phone, "birth_day": self.birth_date, "address": self.address, "gender": self.gender,
                "image": self.image, "basic_rate": self.basic_rate, "delete_at": self.delete_at, "email": self.email,
                "hire_date": self.hire_date}

    def __repr__(self):
        return f"Employee('{self.employee_id}','{self.identity_id}','{self.note}','{self.account.serialize()}','{self.first_name}'" \
               f",'{self.last_name}','{self.phone}','{self.birth_date}','{self.address}','{self.gender}','{self.image}'" \
               f",'{self.basic_rate}', '{self.delete_at}', '{self.hire_date}', '{self.email}')"


class Orderdetails(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    retail_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    discount = db.Column(db.Float)
    total = db.Column(db.Float)
    note = db.Column(db.String(1500))
    delete_at = db.Column(db.DateTime, default=None)

    def serialize(self):
        return {"order_id": self.order.serialize(), "book_id": self.book.serialize(), "note": self.note,
                "retail_price": self.retail_price, "quantity": self.quantity, "discount": self.discount,
                "total": self.note, "delete_at": self.delete_at}

    def __repr__(self):
        return f"Orderdetail('{self.order.serialize()}','{self.book.serialize()}','{self.note}','{self.retail_price}','{self.quantity}'," \
               f"'{self.discount}','{self.note}', {self.delete_at})"


class Orders(db.Model):
    order_id = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    order_date = db.Column(db.DateTime)
    total = db.Column(db.Float)
    type = db.Column(db.String(50))
    note = db.Column(db.String(1500))
    delete_at = db.Column(db.DateTime, default=None)
    orderdetails = db.relationship('Orderdetails', backref="order", lazy=True)

    def serialize(self):
        return {"order_id": self.order_id, "customer": self.customer.serialize(), "note": self.note,
                "employee": self.employee.serialize(),
                "order_date": self.order_date, "total": self.order_date, "type": self.type, "delete_at": self.delete_at}

    def __repr__(self):
        return f"Order('{self.order_id}', '{self.customer.serialize()}', '{self.employee.serialize()}','{self.note}', '{self.order_date}', '{self.total}', " \
               f"'{self.type}', '{self.delete_at}')"


class Roles(db.Model):
    role_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    role_name = db.Column(db.String(50))
    note = db.Column(db.String(1500))
    delete_at = db.Column(db.DateTime, default=None)
    accounts = db.relationship('Accounts', backref="role", lazy=True)

    def serialize(self):
        return {"role_id": self.role_id, "role_name": self.role_name, "note": self.note, "delete_at": self.delete_at}

    def __repr__(self):
        return f"Role('{self.role_id}','{self.role_name}','{self.note}', '{self.delete_at}')"


class Schedules(db.Model):
    schedule_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    date = db.Column(db.DateTime)
    time_from = db.Column(db.DateTime)
    time_to = db.Column(db.DateTime)
    actual_hours = db.Column(db.Float)
    expected_hours = db.Column(db.Float)
    salary = db.Column(db.Float)
    delete_at = db.Column(db.DateTime, default=None)
    note = db.Column(db.String(1500))

    def serialize(self):
        return {"id": self.schedule_id, "employee": self.employee.serialize(), "date": self.date,
                "time_from": self.time_from, "time_to": self.time_to, "note": self.note,
                "actual_hours": self.actual_hours, "expected_hours": self.expected_hours, "salary": self.salary,
                "delete_at": self.delete_at}

    def __repr__(self):
        return f"Schedule('{self.schedule_id}','{self.employee.serialize()}','{self.date}','{self.time_from}','{self.time_to}'," \
               f"'{self.note}','{self.actual_hours}','{self.expected_hours}','{self.salary}', '{self.delete_at}')"


class Stocktaketicketdetails(db.Model):
    Stocktake_ticket_id = db.Column(db.Integer, db.ForeignKey('stocktaketickets.stocktake_ticket_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    new_quantity = db.Column(db.Integer)
    old_quantity = db.Column(db.Integer)

    def serialize(self):
        return {"stocktake_ticket": self.stocktaketicket.serialize(), "book": self.book.serialize(),
                "new_quantity": self.new_quantity, "old_quantity": self.old_quantity}

    def __repr__(self):
        return f"Stocktaketicketdetail('{self.stocktaketicket.serialize()}','{self.book.serialize()}','{self.new_quantity}'," \
               f"'{self.old_quantity}')"


class Stocktaketickets(db.Model):
    stocktake_ticket_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    total_quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    delete_at = db.Column(db.DateTime, default=None)
    stocktaketicketdetails = db.relationship('Stocktaketicketdetails', backref="stocktaketicket", lazy=True)

    def serialize(self):
        return {"stocktake_ticket_id": self.stocktake_ticket_id, "employee": self.employee.serialize(),
                "total_quantity": self.total_quantity, "date": self.date}

    def __repr__(self):
        return f"Stocktaketicket('{self.stocktake_ticket_id}','{self.employee.serialize()}','{self.total_quantity}','{self.date}', '{self.delete_at}')"


class Suppliers(db.Model):
    supplier_id = db.Column(db.Integer, unique=True, autoincrement=True, primary_key=True, nullable=False)
    contact_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(1500))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(1500))
    delete_at = db.Column(db.DateTime, default=None)
    books = db.relationship('Books', backref='supplier', lazy=True)

    def serialize(self):
        return {"supplier_id": self.supplier_id, "contact_name": self.contact_name, "note": self.note,
                "address": self.address, "phone": self.phone, "email": self.email, "delete_at": self.delete_at}

    def __repr__(self):
        return f"Supplier('{self.supplier_id}','{self.contact_name}','{self.note}','{self.address}','{self.phone}'," \
               f"'{self.email}', '{self.delete_at}')"


class Authors(db.Model):
    author_id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False, autoincrement=True)
    author_name = db.Column(db.String(50))

    books = db.relationship('Books', backref='author', lazy=True)
    delete_at = db.Column(db.DateTime, default=None)

    def serialize(self):
        return {"author_id": self.author_id, "author_name": self.author_name}

    def __repr__(self):
        return f"Author('{self.author_id}','{self.author_name}')"
