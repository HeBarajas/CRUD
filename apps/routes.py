from apps import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from apps.forms import RegisterForm, RegisterPhoneNumber, LoginForm
from apps.models import PhoneBook, User

@app.route('/')
def index():
    phonebooks = PhoneBook.query.all()
    return render_template('index.html', phonebooks=phonebooks)


@app.route('/name')
@login_required
def name():
    my_name = 'Hector'
    return render_template('name.html', name=my_name)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Get the data from the form
        username = form.username.data
        email = form.email.data
        password = form.password.data
       
        #Check if either the username or email is alrady in db
        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()
        
        #if it is, return back to register
        if user_exists:
            return redirect(url_for('register'))

        #Create a new user instance using form data
        User(username=username, email=email, password = password)


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
        PhoneBook(name=name, phone_number=phone_number, address=address)
        print(name, phone_number, address)
        return redirect(url_for('index'))
    return render_template('phonebook.html', form=form)

@app.route('/login', methods=['GET', 'POST'] )
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #grab the data from the form
        username = form.username.data
        password = form.password.data

        #Query user table for user with username
        user = User.query.filter_by(username=username).first()

        #if the user does not exist or the user has an incorrect password
        if not user or not user.check_password(password):
            #redirect to login page
            print('That username and password is incorrect')
            return redirect(url_for('login'))

    #if user does exist and correct password, log user in
        login_user(user)
        print('User has been logged in')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/edit_registry/<int:p_id>/edit', methods=["GET", "POST"])
def edit_registry(p_id): 
    phonebooks = PhoneBook.query.get_or_404(p_id)
    form = RegisterPhoneNumber()
    if form.validate_on_submit():
        # Get data from form
        name = form.name.data
        phone_number = form.phone_number.data
        address = form.address.data
        # Update the product with the new info
        phonebooks.name = name
        phonebooks.phone_number = phone_number
        phonebooks.address = address

        phonebooks.save()

        # flash message
        flash(f"{phonebooks.name} has been updated", "primary")
        return redirect(url_for('index', p_id=phonebooks.id))

    return render_template('edit_registry.html', phonebooks=phonebooks, form=form)

@app.route('/edit_registry/<int:p_id>/delete')
def delete_phonebooks(p_id):
    phonebooks = PhoneBook.query.get_or_404(p_id)
    phonebooks.delete()
    flash(f'{phonebooks.name} has been deleted', 'danger')
    return redirect(url_for('index'))