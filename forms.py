from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired)


class LoginForm(Form):
    value = StringField('********', validators=[DataRequired()])