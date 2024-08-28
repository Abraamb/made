from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import datetime
import json

app = Flask(__name__)

# email settings
app.config['MAIL_SERVER'] = 'smtp.ethereal.email'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'rebeka43@ethereal.email'
app.config['MAIL_PASSWORD'] = 'uJAsZj4pJvXmdfhSDq'

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

# laad barren in van json bestand
def load_bars_from_json():
    with open('bars.json', 'r') as json_file:
        bars = json.load(json_file)
    return bars

# laad de email counter op voor telle aantal mails 
def load_email_count_from_json():
    with open('email_count.json', 'r') as json_file:
        data = json.load(json_file)
        return data['count']

# verhoogt de email teller
def increment_email_count():
    with open('email_count.json', 'r') as json_file:
        data = json.load(json_file)
        data['count'] += 1
        with open('email_count.json', 'w') as updated_json_file:
            json.dump(data, updated_json_file, indent=4)

@app.route('/pickup_bags', methods=['GET'])
def pickup_bags():
    bars = load_bars_from_json()  # Load bars with bag counts

    if request.method == 'POST':
        location = request.form['location']
        bar_name = request.form['bar']
        add_bags = int(request.form.get('add_bags', 0))  # Number of bags to add

        # Update bag count for the selected bar
        for bar in bars:
            if bar['name'] == bar_name:
                bar['bags'] += add_bags
                break   

        # Save updated bag counts to JSON file
        with open('pick.json', 'w') as json_file:
            json.dump(bars, json_file, indent=4)

        # Send email notification
        send_email(location, bar_name, add_bags)

    return render_template('pickup_bags.html', bars=bars)

@app.route('/request_bags', methods=['GET', 'POST'])
def request_bags():
    bars = load_bars_from_json()  # bar teller

    if request.method == 'POST':
        location = request.form['location']
        bar_name = request.form['bar']
        add_bags = int(request.form.get('add_bags', 0))  # aantale zakken toegevoegd

        # update
        for bar in bars:
            if bar['name'] == bar_name:
                bar['bags'] += add_bags
                break

        # opslaan in json 
        with open('bars.json', 'w') as json_file:
            json.dump(bars, json_file, indent=4)

    return render_template('request_bags.html', bars=bars)

if __name__ == '__main__':
    app.run(debug=True)

