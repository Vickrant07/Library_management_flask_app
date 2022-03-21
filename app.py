#Author: Vickrant Bawankule
#Web Development ca1
"""
My system has two kinds of user: customer ones, and administrators.
Choose Register on the main page in order to register as a regular/customer user and choose any password (min 6 char).
But to login as an administrator you must got to admin login page, if you don't have an admin account then please register there.
    here is a secret, the admin id must start with # for e.g #vickrant and choose any password (min 6 char)
"""
# I feel that the manage stock route, checkout routes, and previous orders route are quite good

from flask import Flask, render_template, redirect, url_for, session, g, request
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import ManageStock, RegistrationForm, LoginForm, AdminLoginForm, AdminRegistrationForm
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "this_is_my_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def load_logged_in_customers():
    g.customer = session.get("customer_id", None)

@app.before_request
def load_logged_in_admin():
    g.admin = session.get("admin_id", None)

def login_required(view):  
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.customer is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

def admin_login_required(view):  
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for("admin_login", next=request.url))
        return view(**kwargs)
    return wrapped_view

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/base")
def base():
    return render_template("base.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        customer_id = form.customer_id.data
        password = form.password.data
        db = get_db()
        matching_customer = db.execute("""SELECT * FROM customers
                                        WHERE customer_id = ?;""", (customer_id,)).fetchone()
        if matching_customer is None:
            form.customer_id.errors.append("Unknown customer id!")
        elif not check_password_hash(matching_customer["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()     
            session["admin_id"] = {}                       
            session["customer_id"] = customer_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        password = form.password.data
        db = get_db()
        matching_admin = db.execute("""SELECT * FROM admins
                                        WHERE admin_id = ?;""", (admin_id,)).fetchone()
        if matching_admin is None:
            form.admin_id.errors.append("Unknown admin id!")
        elif not check_password_hash(matching_admin["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()    
            session["customer_id"] = {}                        
            session["admin_id"] = admin_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("base")
            return redirect(next_page)   
    return render_template("admin_login.html", form=form)

@app.route("/logout")
def logout():
    session.clear() 
    return redirect( url_for("index") )

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        customer_id = form.customer_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        possible_clashing_customer = db.execute("""SELECT * FROM customers
                                        WHERE customer_id = ?;""", (customer_id,)).fetchone()
        if possible_clashing_customer is not None:
            form.customer_id.errors.append("Customer id already taken!")
        else:
            db.execute("""INSERT INTO customers (customer_id, password)
                          VALUES (?,?)""", (customer_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )   
    return render_template("register.html", form=form)

@app.route("/register_admin", methods=["GET", "POST"])
def register_admin():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        password = form.password.data
        password2 = form.password2.data
        if admin_id[0] != "#":
            form.admin_id.errors.append("Admin id must start with '#'!")
        else:
            db = get_db()
            possible_clashing_admin = db.execute("""SELECT * FROM admins
                                            WHERE admin_id = ?;""", (admin_id,)).fetchone()
            if possible_clashing_admin is not None:
                form.admin_id.errors.append("Admin id already taken!")
            else:
                db.execute("""INSERT INTO admins (admin_id, password)
                            VALUES (?,?)""", (admin_id, generate_password_hash(password)))
                db.commit()
                return redirect( url_for("admin_login") )   
    return render_template("register_admin.html", form=form)

@app.route("/books", methods=["GET", "POST"])
def books():
    db = get_db()
    books = db.execute("""SELECT * FROM books;""").fetchall()
    return render_template("books.html", books=books)

@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    db = get_db()
    book = db.execute("""SELECT * FROM books
                        WHERE book_id = ?;""", (book_id,)).fetchone()
    return render_template("book.html", book=book)

@app.route("/add_to_cart/<int:book_id>", methods=["GET", "POST"])
@login_required  
def add_to_cart(book_id):
    if "cart" not in session:
        session["cart"] = {}
    if book_id not in session["cart"]:
        session["cart"][book_id] = 0
    session["cart"][book_id]= session["cart"][book_id] + 1
    return redirect(url_for("cart"))

@app.route("/cart", methods=["GET", "POST"])
@login_required 
def cart():
    if "cart" not in session:
        session["cart"] = {}
    names = {}
    prices = {}
    rents = {}
    quantities = {}
    total_rent : float = 0.0
    total_price : float = 0.0
    db = get_db()
    for book_id in session["cart"]:
        book = db.execute("""SELECT * FROM books 
                            WHERE book_id = ?;""", (book_id,)).fetchone()
        name = book["name"]
        names[book_id] = name
        quantity = session["cart"][book_id]
        quantities[book_id] = quantity
        price = book["price"]
        prices[book_id] = price
        total_price = total_price + (prices[book_id]*quantities[book_id])
        rent = book["rent"]
        rents[book_id] = rent
        total_rent = total_rent + (rents[book_id]*quantities[book_id])
    return render_template("cart.html", cart=session["cart"], names=names, prices=prices, rents=rents, total_rent=total_rent, total_price=total_price)

@app.route("/remove_item/<int:book_id>", methods=["GET", "POST"])
@login_required
def remove_item(book_id):
    session["cart"].pop(book_id)
    return redirect(url_for("cart"))

@app.route("/empty_cart", methods=["GET", "POST"])
@login_required
def empty_cart():
    session["cart"] = {}
    return redirect(url_for("cart"))
    
@app.route("/checkout_rent", methods=["GET", "POST"])
@login_required
def checkout_rent():
    customer_id = g.customer
    names = {}
    rents = {}
    quantities = {}
    name_str = ""
    books_id_str = ""    
    quantity_str = ""
    total_rent : float = 0.0
    db = get_db()
    for book_id in session["cart"]:
        book = db.execute("""SELECT * FROM books 
                            WHERE book_id = ?;""", (book_id,)).fetchone()
        name = book["name"]
        names[book_id] = name
        quantity = session["cart"][book_id] 
        quantities[book_id] = quantity
        name_str += str(name) + ", "
        books_id_str += str(book_id) + " "
        quantity_str += str(quantities[book_id]) + " "
        rent = book["rent"]
        rents[book_id] = rent
        total_rent = total_rent + (rents[book_id]*quantities[book_id])
    db.execute("""INSERT INTO orders (customer_id, books_id_str, name_str, quantity_str, total_rent)
               VALUES (?,?,?,?,?)""",(customer_id, books_id_str, name_str, quantity_str, total_rent))
    db.commit()
    return render_template("checkout_rent.html", cart=session["cart"], names=names, rents=rents, total_rent=total_rent)

@app.route("/checkout_buy", methods=["GET", "POST"])
@login_required
def checkout_buy():
    customer_id = g.customer
    names = {}
    prices = {}
    quantities = {}
    name_str = ""
    books_id_str = ""    
    quantity_str = ""
    total_price : float = 0.0
    db = get_db()
    for book_id in session["cart"]:
        book = db.execute("""SELECT * FROM books 
                            WHERE book_id = ?;""", (book_id,)).fetchone()
        name = book["name"]
        names[book_id] = name
        quantity = session["cart"][book_id]
        quantities[book_id] = quantity
        name_str += str(name) + ", "
        books_id_str += str(book_id) + " "
        quantity_str += str(quantities[book_id]) + " "
        price = book["price"]
        prices[book_id] = price
        total_price = total_price + (prices[book_id]*quantities[book_id])
    db.execute("""INSERT INTO orders (customer_id, books_id_str, name_str, quantity_str, total_price)
               VALUES (?,?,?,?,?)""",(customer_id, books_id_str, name_str, quantity_str, total_price))
    db.commit()
    return render_template("checkout_buy.html", cart=session["cart"], names=names, prices=prices, total_price=total_price)

@app.route("/rent_order_placed", methods=["GET", "POST"])
@login_required
def rent_order_placed():
    customer_id = g.customer
    quantities={}
    db = get_db()
    order_id = db.execute("""SELECT order_id FROM orders WHERE customer_id = ? 
                            ORDER BY order_id DESC LIMIT 1;""", (customer_id,)).fetchone()
    for book_id in session["cart"]:
        quantity = session["cart"][book_id]
        quantities[book_id] = quantity
        stock = db.execute("""SELECT stock FROM books WHERE book_id = ?;""",(book_id,)).fetchone()
        # print(stock)
        new_stock = stock[0]-quantities[book_id]
        db.execute("""UPDATE books SET stock = ? WHERE book_id = ?""", (new_stock,book_id))
        db.commit()
    return render_template("rented.html", order_id=order_id)

@app.route("/buy_order_placed", methods=["GET", "POST"])
@login_required
def buy_order_placed():
    customer_id = g.customer
    quantities={}
    db = get_db()
    order_id = db.execute("""SELECT order_id FROM orders WHERE customer_id = ? 
                            ORDER BY order_id DESC LIMIT 1;""", (customer_id,)).fetchone()
    for book_id in session["cart"]:
        quantity = session["cart"][book_id]
        quantities[book_id] = quantity
        stock = db.execute("""SELECT stock FROM books WHERE book_id = ?;""",(book_id,)).fetchone()
        new_stock = stock[0]-quantities[book_id]
        db.execute("""UPDATE books SET stock = ? WHERE book_id = ?""", (new_stock,book_id))
        db.commit()
    return render_template("purchased.html", order_id=order_id)

@app.route("/past_orders", methods=["GET", "POST"])
@login_required
def past_orders():
    db = get_db()
    customer_id = g.customer
    previous_orders = db.execute("""SELECT * FROM orders WHERE customer_id = ?
                                    ORDER BY order_id DESC;""",(customer_id,)).fetchall()
    return render_template("past_orders.html", previous_orders=previous_orders)

@app.route("/manage_stock", methods=["GET", "POST"])
@admin_login_required
def manage_stock():
    form = ManageStock()
    db = get_db()
    books = db.execute("""SELECT * FROM books;""").fetchall()
    try:
        if form.validate_on_submit():
            add_stock_to_book_id : int = form.book_id.data
            # print(add_stock_to_book_id)
            # print(books)
            # print(books[0])
            quantity_to_add : int = form.new_quantity_to_add.data
            for add_stock_to_book_id in books[add_stock_to_book_id-1]:
                old_stock = db.execute("""SELECT stock FROM books WHERE book_id = ?;""",(add_stock_to_book_id,)).fetchone()
                new_stock : int = old_stock[0]+quantity_to_add
                break
            db.execute("""UPDATE books SET stock = ? WHERE book_id = ?""", (new_stock,add_stock_to_book_id))
            db.commit()    
            return redirect(url_for("manage_stock"))
        return render_template("manage_stock.html", books=books, form=form)
    except Exception as e: 
        return "This is an error: "+str(e)

@app.route("/manage_customers", methods=["GET", "POST"])
@admin_login_required
def manage_customers():
    db = get_db()
    customers = db.execute("""SELECT * FROM customers;""").fetchall()
    return render_template("manage_customers.html", customers=customers)

@app.route("/remove_customer/<customerid>", methods=["GET", "POST"])
@admin_login_required
def remove_customer(customerid):
    db = get_db()
    db.execute("""DELETE FROM customers WHERE customer_id = ?;""",(customerid,))
    db.commit()
    return redirect(url_for("manage_customers"))

