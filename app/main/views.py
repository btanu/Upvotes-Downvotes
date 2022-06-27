from crypt import methods
from flask import render_template, request, redirect, url_for, abort #takes in the name of a template file as an argument and automatically searches for the template file
#in our app/templates/subdirectory and loads it
from .forms import UpdateProfile
from . import main 
from app.models import User, Pitch, Category, Comments, UpVote, DownVote
from flask_login import login_required, current_user #will intercept a request and check if user is authenticated and if not the user is directed to the login page
from .. import db, photos
from .forms import CategoryInput, CommentInput, UpdateProfile
import markdown2

@main.route('/')
def index():

    pitches = Pitch.query.order_by(Pitch.posted.desc()).all()

    return render_template('index.html', pitches = pitches)

@main.route('/user/<int:id>', methods=['GET', 'POST'])
@login_required
def pitch(id):
    comments = Comments.query.filter_by(pitch_id = id).all()
    pitch = Pitch.query.get(id)
    if pitch is None:
        abort(404)
    form = CommentInput()
    if form.validate_on_submit():
        comment = Comments(comment = form.comment.data, pitch_id = id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        
        return redirect(url_for('.pitch',comments=comments, pitch = pitch, form=form, id=id ))

    return render_template('pitch.html', pitch = pitch, form=form, comments = comments)

@main.route('/add_pitch', methods=['GET', 'POST'])
@login_required
def add_pitch():
    title = request.args.get('title')
    content = request.args.get('content')
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    add_pitch = Pitch(title = title, content = content, user_id = user_id, category_id=category_id)
    db.session.add(add_pitch)
    db.session.commit()
    return redirect(url_for('.profile', uname=current_user.username))


@main.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    form = CategoryInput()
    if form.validate_on_submit():
        category = Category(name = form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('.index'))

    return render_template('category.html', form=form)


@main.route('/category/<int:category_id>', methods=['GET', 'POST'])
def get_category(category_id):
    pitches = Pitch.query.filter_by(category_id=category_id).all()
    category = Category.query.get(category_id)
    return render_template('by_category.html', pitches = pitches, category = category)

@main.route('/user/<uname>', methods=['GET', 'POST'])
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if User is None:
        abort(404)
    
    pitches = Pitch.get_my_posts(user.id).order_by(Pitch.posted.desc()).all()
    categories = Category.get_categories()

    return render_template("profile/profile.html", user = user, pitches=pitches, categories=categories)

@main.route('/user/<uname>/update', methods = ['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname = user.username))
    return render_template('profile/update.html', form = form)

@main.route('/upvote/int:<id>', methods = ['GET', 'POST'])
@login_required
def upVote(id):
    pitch = Pitch.query.get(id)
    if Pitch is None:
        abort(404)
    upVote = UpVote.query.filter_by(user_id=current_user.id, pitch_id=id).first()
    if upVote is not None:
        db.session.delete(upVote)
        db.session.commit()
        return redirect(url_for('.index'))
    vote = UpVote(user_id=current_user.id, pitch_id=id)
    db.session.add(vote)
    db.session.commit()

    return redirect(url_for('.index'))

@main.route('/downvote/int:<id>', methods = ['GET', 'POST'])
@login_required
def downVote(id):
    pitch = Pitch.query.get(id)
    if Pitch is None:
        abort(404)
    upVote = DownVote.query.filter_by(user_id=current_user.id, pitch_id=id).first()
    if upVote is not None:
        db.session.delete(upVote)
        db.session.commit()
        return redirect(url_for('.index'))
    vote = DownVote(user_id=current_user.id, pitch_id=id)
    db.session.add(vote)
    db.session.commit()

    return redirect(url_for('.index'))

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files: #request checks if any file with the name photo has been passed
        filename = photos.save(request.files['photo']) # the save method saves the file in our application
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))