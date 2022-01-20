from audioop import add
from apps import app
from flask import render_template, redirect, url_for
from apps.forms import RegisterForm, RegisterPhoneNumber

@app.route('/')
def index():
    my_name = 'Hector'
    my_city = 'The Woodlands'
    my_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    my_person = {
        'name' :'Ferris Bueller',
        'age': 18,
        'best_friend': 'Cameron'
    }
    return render_template('index.html', name=my_name, city=my_city, colors=my_colors, person=my_person)


@app.route('/name')
def name():
    my_name = 'Hector'
    return render_template('name.html', name=my_name)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('FORM HAS BEEN VALIDATED!')
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/phonebook', methods=['GET', 'POST'])
def phonebook():
    form = RegisterPhoneNumber()
    if form.validate_on_submit():
        print('FORM HAS BEEN ADDED TO PHONEBOOK')
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        print(name, phone_number, address)
        return redirect(url_for('index'))
    return render_template('phonebook.html', form=form)
