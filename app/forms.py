from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

text_styles = {
'class': 'text-uppercase'
}



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TodoForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TodoDeleteForm(FlaskForm):
    
    delete = SubmitField('Delete', render_kw={'class': 'btn btn-danger'})


class TodoStatusUpdate(FlaskForm):
    update = SubmitField('Done/ToDo', render_kw={'class': 'btn btn'})
    

class TodoUpdateButton(FlaskForm):
    update = SubmitField('Update', render_kw={'class': 'btn btn-warning'})


class TodoUpdateForm(FlaskForm):
    description = StringField('New Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
