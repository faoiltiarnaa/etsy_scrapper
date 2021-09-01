from flask import Flask, _app_ctx_stack, render_template, request, redirect
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from etsy import scrape_product

import models
from database import SessionMaker, engine

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
CORS(app)
app.session = scoped_session(SessionMaker, scopefunc=_app_ctx_stack.__ident_func__)


def add_product(product_dict):
    """Adds a new product to the product table using product_dict."""
    product = models.Product(**product_dict)
    app.session.merge(product)
    app.session.commit()



@app.route("/get_all_products")
def get_all_products():
    """Returns all products as an array from Product Table."""
    products = app.session.query(models.Product).all()
    return products


@app.route('/', methods=['POST', 'GET'])
def index():
    error_msg = ''
    if request.method == 'POST':
        etsy_link = request.form['content']
        try:
            result = scrape_product(etsy_link)
            add_product(result)
        except Exception as e:
            error_msg = str(e)
    
       
    products = app.session.query(models.Product).all()
    return render_template("home.html", products=products, error=error_msg)



@app.route('/delete/<int:product_id>')
def delete(product_id):
    product = app.session.query(models.Product)\
                .filter(models.Product.product_id == product_id).first()
    try:
        app.session.delete(product)
        app.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting product from database'

@app.route('/get_product', methods=['POST', 'GET'])
def get_product():
    if request.method == 'POST':
        product_id = request.form['content']
        try:
            product = app.session.query(models.Product)\
                .filter(models.Product.product_id == product_id).first()
            if product:
                return render_template("product.html", product=product)
            else:
                error_msg = "There is no such record in the database."
        except Exception as e:
            error_msg = str(e)
        return render_template("product.html", error=error_msg)
    else:
        return render_template("product.html")
    



@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


if __name__ == '__main__':
    app.run()