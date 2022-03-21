from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, EqualTo, Length

class LoginForm(FlaskForm):
    customer_id = StringField("Customer id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    customer_id = StringField("Customer id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired(), Length(6,20,"Password must be at least 6 character long!")])
    password2 = PasswordField("Repeat password:",
         validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class AdminLoginForm(FlaskForm):
    admin_id = StringField("Admin id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class AdminRegistrationForm(FlaskForm):
    admin_id = StringField("Admin id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired(), Length(6,20,"Password must be at least 6 character long!")])
    password2 = PasswordField("Repeat password:",
         validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class ManageStock(FlaskForm):
    book_id = IntegerField("Book id to add stock to:", validators=[InputRequired()])
    new_quantity_to_add = IntegerField("New quantity to add to stock:", validators=[InputRequired()])
    submit = SubmitField("Submit")
