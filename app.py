import json
import os
from datetime import datetime
from msw.get_conditions import get_report, get_current
from flask import Flask, render_template, redirect, session, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, IntegerField, RadioField
from wtforms.validators import Required, Email, Length

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

# Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	phone = db.Column(db.Integer, unique=True, nullable=True)
	max_wave_height = db.Column(db.Integer)

	def __repr__(self):
		return '<User %r>' % self.username

# Forms and Views
class Register(FlaskForm):
	username = StringField('Choose a username', validators=[Required()])
	phone = StringField('Enter Phone Number', validators=[Required(), Length(min=10, max=11)])
	max_wave_height = RadioField('Max Wave Height',
								choices=[(3, '3ft'), (4, '4ft'), (5, '5ft'), (6, '6ft')],
								coerce=int,
								validators=[Required()])
	submit = SubmitField('Submit')


# Shell command and Database migrations
def make_shell_context():
	return dict(app=app, db=db, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

def myround(x, base=5):
    return int(base * round(float(x)/base))

# Custom view filters
@app.template_filter('dateformat')
def dateformat(value, format='%A, %b %-d %-I:%M %p'):
    return datetime.fromtimestamp(value).strftime(format)


# Routes
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/')
def index():
	current = {'sonoma': get_current(305), 'mendo': get_current(303)}
	
	return render_template('index.html', current=current)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = Register()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None:
			user = User(username=form.username.data, 
						phone=form.phone.data, 
						max_wave_height=form.max_wave_height.data)
			db.session.add(user)
			db.session.commit()
			session['known'] = False 
		else:
			session['known'] = True
		session['name'] = form.username.data
		form.username.data = ''
		session['logged_in'] = True
		return redirect(url_for('index'))
	if form.errors:
		for field, error in form.errors.items():
			message = '%s: %s' % (field, error[0])
			flash(message)
	return render_template('register.html', form=form, name=session.get('name'),
							known=session.get('known', False))

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session['name'] = ''
	flash('You were logged out')
	return redirect(url_for('index'))


if __name__ == '__main__':
	manager.run()
