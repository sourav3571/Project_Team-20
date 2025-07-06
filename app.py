from flask import Flask, render_template, redirect, url_for, flash
from forms import SignupForm, LoginForm
from flask import flash,request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3d6cfa835c3cbe8f5c091e3d479f06127eac1db1e7f4b5d842063b387472e01'  

testimonials = [
    {
        'name': 'Ravi S.',
        'rating': 5,
        'text': 'Shoes are very good comfort & soft. Good quality, best pricing & on time delivery. Thanks to Neemans!',
        'product': 'Everyday Basic Slip Ons'
    },
    {
        'name': 'Priya M.',
        'rating': 5,
        'text': "It's comfortable and stylish. Good fit as well. Great shoe at this price.",
        'product': 'Tread Basics'
    },
    {
        'name': 'Arjun K.',
        'rating': 5,
        'text': 'Really loved them... looking for more in my collection',
        'product': 'PureWhoosh Duo Glides'
    },
    {
        'name': 'Sneha T.',
        'rating': 5,
        'text': 'Best comfortable shoes in price. Very satisfied with the purchase.',
        'product': 'Everyday Basic Sneakers'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home", testimonials=testimonials)

products_data = {
    1: {"name": "Classic Oxford", "price": 3599, "image": "images/shoes/shoe1.jpg"},
    2: {"name": "Urban Sneakers", "price": 4299, "image": "images/shoes/shoe2.jpg"},
    3: {"name": "Adventure Boots", "price": 5399, "image": "images/shoes/shoe3.jpg"},
    4: {"name": "Business Loafers", "price": 4799, "image": "images/shoes/shoe4.jpg"},
    5: {"name": "Sport Runners", "price": 3899, "image": "images/shoes/shoe5.jpg"},
    6: {"name": "Casual Walkers", "price": 3199, "image": "images/shoes/shoe6.jpg"},

    7: {"name": "Elegant Heels", "price": 5499, "image": "images/shoes/shoe7.jpg"},
    8: {"name": "Chic Flats", "price": 2899, "image": "images/shoes/shoe8.jpg"},
    9: {"name": "Fashion Boots", "price": 4999, "image": "images/shoes/shoe9.jpg"},
    10: {"name": "Designer Pumps", "price": 6299, "image": "images/shoes/shoe10.jpg"},
    11: {"name": "Comfort Sandals", "price": 2399, "image": "images/shoes/shoe11.jpg"},
    12: {"name": "Athletic Sneakers", "price": 4199, "image": "images/shoes/shoe12.jpg"},

    13: {"name": "Neon Kicks", "price": 4599, "image": "images/shoes/shoe13.jpg"},
    14: {"name": "Retro Waves", "price": 3999, "image": "images/shoes/shoe14.jpg"},
    15: {"name": "Holographic Dreams", "price": 4899, "image": "images/shoes/shoe15.jpg"},
    16: {"name": "Rainbow Runners", "price": 5299, "image": "images/shoes/shoe16.jpg"},
    17: {"name": "Cosmic Drift", "price": 4899, "image": "images/shoes/shoe17.jpg"},
    18: {"name": "Galaxy Pulse", "price": 5599, "image": "images/shoes/shoe18.jpg"},
}


@app.route("/products")
def products():
    men_products = {k: v for k, v in products_data.items() if 1 <= k <= 6}
    women_products = {k: v for k, v in products_data.items() if 7 <= k <= 12}
    genz_products = {k: v for k, v in products_data.items() if 13 <= k <= 18}
    
    return render_template(
        "products.html",
        title="Our Collection",
        men_products=men_products,
        women_products=women_products,
        genz_products=genz_products,
        coupon="team20"
    )



@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us")

@app.route("/about")
def about():
    return render_template("about.html", title="About Us")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('home'))
    return render_template("signup.html", title="Sign Up", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Logged in as {form.email.data}", "success")
        return redirect(url_for('home'))
    return render_template("login.html", title="Login", form=form)



@app.route('/buy/<int:product_id>', methods=["GET", "POST"])
def buy(product_id):
    shoe = products_data.get(product_id)
    if not shoe:
        flash("Product not found!", "danger")
        return redirect(url_for('products'))

    original_price = shoe['price']
    discounted_price = None
    invalid_coupon = False

    if request.method == "POST":
        entered_coupon = request.form.get("coupon", "").strip().lower()
        if entered_coupon == "team20":
            discount = int(original_price * 0.10)
            discounted_price = original_price - discount
        else:
            invalid_coupon = True

    return render_template(
        "checkout.html",
        product_id=product_id,
        name=shoe['name'],
        original=original_price,
        discounted=discounted_price,
        invalid=invalid_coupon
    )

if __name__ == "__main__":
    app.run(debug=True)
