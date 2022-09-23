from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired, URL

import csv, os
import pandas


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)
CSRFProtect(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = URLField('Location URL', validators=[DataRequired(), URL()])
    open_time = StringField('Open Time', validators=[DataRequired()])
    closing_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating', choices=[('✘', '✘'), ('✘✘', '✘✘'), ('✘✘✘', '✘✘✘'), ('✘✘✘✘', '✘✘✘✘'), ('✘✘✘✘✘', '✘✘✘✘✘') ], validators=[DataRequired()])
    power_outlet_rating = SelectField('Power Outlet Rating', choices=[('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
       new_csv_data = {
            "Cafe Name": form.cafe.data,
            "Location": form.location_url.data,
            "Open": form.open_time.data,
            "Close": form.closing_time.data,
            "Coffee": form.coffee_rating.data,
            "Wifi": form.wifi_rating.data,
            "Power": form.power_outlet_rating.data,
       }
       # with open('cafe-data.csv', mode='a', newline="\n") as csv_data:
       #     updated_csv_data = DictWriter(csv_data, fieldnames=["Cafe Name", "Location", "Open", "Close",
       #                                                         "Coffee", "Wifi", "Power"])
       #     updated_csv_data.writerow(new_csv_data)
       # Make data frame of above data
       df = pandas.DataFrame([new_csv_data])

       # append data frame to CSV file
       df.to_csv('cafe-data.csv', mode='a', index=False, header=False)

       return "<h1> Updated1 </h1>"

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
