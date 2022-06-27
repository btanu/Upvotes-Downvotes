from flask_wtf import FlaskForm #helps us create a form
from wtforms import StringField,TextAreaField,SubmitField #allows us to create a textfield, textarea field and a submit button
from wtforms.validators import InputRequired #prevents user from submittin empty value

class CommentInput(FlaskForm):
    comment = TextAreaField('Add Comment here . . .', validators=[InputRequired()]) #first is the label, second is a list of validators
    Submit= SubmitField('Submit')

class CategoryInput(FlaskForm):
    name = StringField('Category: ', validators=[InputRequired()])
    submit = SubmitField('Update')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you', validators=[InputRequired()])
    submit = SubmitField('Update')