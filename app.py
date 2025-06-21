from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# MongoDB connection using new tickets database URI
uri = "mongodb+srv://tickets:Bmpg%402003%23@cluster0.mac44lr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['tickets_db']  # Use a suitable database name for tickets
users = db['users']
tickets = db['tickets']
history = db['history']
notifications = db['notifications']

# Gold Loan DB (existing)
uri_gold = "mongodb+srv://tickets:Bmpg%402003%23@cluster0.mac44lr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client_gold = MongoClient(uri_gold, server_api=ServerApi('1'))
db_gold = client_gold['tickets_db']
tickets_gold = db_gold['tickets']
history_gold = db_gold['history']
notifications_gold = db_gold['notifications']

# Property Loan DB
uri_property = "mongodb+srv://bmpg:Bmpg%402003%23@cluster0.0jrodq6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client_property = MongoClient(uri_property, server_api=ServerApi('1'))
db_property = client_property['property_db']
tickets_property = db_property['tickets']
history_property = db_property['history']
notifications_property = db_property['notifications']

# Automobile Loan DB
uri_auto = "mongodb+srv://bmpg:Bmpg%402003%23@cluster0.0gk0rg0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client_auto = MongoClient(uri_auto, server_api=ServerApi('1'))
db_auto = client_auto['automobile_db']
tickets_auto = db_auto['tickets']
history_auto = db_auto['history']
notifications_auto = db_auto['notifications']

# Test MongoDB connection at startup
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        if users.find_one({'username': username, 'user_type': user_type}):
            flash('User already exists!')
            return redirect(url_for('signup'))
        hashed_pw = generate_password_hash(password)
        users.insert_one({'username': username, 'password': hashed_pw, 'user_type': user_type})
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        user = users.find_one({'username': username, 'user_type': user_type})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['user_type'] = user_type
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user_type = session['user_type']
        if user_type == 'employee':
            return redirect(url_for('employee_dashboard'))
        else:
            return redirect(url_for('customer_dashboard'))
    else:
        flash('Please login first!')
        return redirect(url_for('login'))

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    username = session['username']
    assigned_tickets = list(tickets.find({'$or': [{'assigned_to': username}, {'assigned_to': {'$exists': False}}]}))
    employee_notifications = list(notifications.find({'employee': username}))
    notifications.delete_many({'employee': username})
    return render_template('employee_dashboard.html', username=username, tickets=assigned_tickets, notifications=employee_notifications, is_employee=True)

@app.route('/customer_dashboard')
def customer_dashboard():
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    username = session['username']
    return render_template('dashboard.html', username=username, user_type='customer', is_employee=False)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/gold_loan', methods=['GET', 'POST'])
def gold_loan():
    if 'username' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    user_type = session.get('user_type')
    username = session.get('username')

    if user_type == 'customer':
        user_tickets = list(tickets_gold.find({'username': username}))
        if request.method == 'POST' and not user_tickets:
            # Handle gold loan verification form submission
            name = request.form.get('name')
            dob = request.form.get('dob')
            id_number = request.form.get('id_number')
            file = request.files.get('gov_id_pdf')
            gold_type = request.form.get('gold_type')
            gold_weight = request.form.get('gold_weight')
            place_bought = request.form.get('place_bought')
            jeweler_address = request.form.get('jeweler_address')
            gold_photo = request.files.get('gold_photo')
            declaration = request.form.get('declaration')
            account_number = request.form.get('account_number')
            account_name = request.form.get('account_name')
            account_type = request.form.get('account_type')
            ifsc_code = request.form.get('ifsc_code')
            bank_name = request.form.get('bank_name')
            branch_name = request.form.get('branch_name')

            gov_id_pdf_filename = None
            gold_photo_filename = None
            if file and file.filename:
                gov_id_pdf_filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], gov_id_pdf_filename))
            if gold_photo and gold_photo.filename:
                gold_photo_filename = secure_filename(gold_photo.filename)
                gold_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], gold_photo_filename))

            ticket = {
                'username': username,
                'name': name,
                'dob': dob,
                'id_number': id_number,
                'gov_id_pdf': gov_id_pdf_filename,
                'gold_type': gold_type,
                'gold_weight': gold_weight,
                'place_bought': place_bought,
                'jeweler_address': jeweler_address,
                'gold_photo': gold_photo_filename,
                'declaration': declaration,
                'bank_details': {
                    'account_number': account_number,
                    'account_name': account_name,
                    'account_type': account_type,
                    'ifsc_code': ifsc_code,
                    'bank_name': bank_name,
                    'branch_name': branch_name
                },
                'status': 'pending'
            }
            tickets_gold.insert_one(ticket)
            flash('Ticket raised successfully! Await employee approval.')
            return redirect(url_for('gold_loan'))
        if not user_tickets:
            # No tickets, let user proceed to verification (render verification form)
            return render_template('gold_loan_auth.html', username=username)
        else:
            # Show tickets and their status
            return render_template('customer_tickets.html', tickets=user_tickets)
    elif user_type == 'employee':
        all_tickets = list(tickets_gold.find())
        return render_template('employee_tickets.html', tickets=all_tickets)
    else:
        flash('Invalid user type!')
        return redirect(url_for('dashboard'))

@app.route('/approve_ticket/<ticket_id>', methods=['POST'])
def approve_ticket(ticket_id):
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    username = session['username']
    tickets_gold.update_one({'_id': ObjectId(ticket_id)}, {'$set': {'status': 'approved', 'assigned_to': username}})
    flash('Ticket approved!')
    return redirect(url_for('dashboard'))

@app.route('/decline_ticket/<ticket_id>', methods=['POST'])
def decline_ticket(ticket_id):
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    username = session['username']
    ticket = tickets_gold.find_one({'_id': ObjectId(ticket_id)})
    if ticket:
        ticket['status'] = 'declined_by_employee'
        ticket['assigned_to'] = username
        history_gold.insert_one(ticket)
        tickets_gold.delete_one({'_id': ObjectId(ticket_id)})
    flash('Ticket declined and moved to customer history.')
    return redirect(url_for('employee_dashboard'))

@app.route('/complete_ticket/<ticket_id>', methods=['POST'])
def complete_ticket(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    # Instead of deleting, show money option page
    return redirect(url_for('money_option', ticket_id=ticket_id))

@app.route('/money_option/<ticket_id>', methods=['GET'])
def money_option(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    return render_template('money_option.html', ticket_id=ticket_id)

@app.route('/receive_money/<ticket_id>', methods=['POST'])
def receive_money(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    tickets_gold.delete_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    flash('Congratulations! You have received your gold loan amount.')
    return redirect(url_for('customer_dashboard'))

@app.route('/decline_money/<ticket_id>', methods=['POST'])
def decline_money(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    tickets_gold.delete_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    flash('You have declined to receive the gold loan amount. Your ticket has been cancelled.')
    return redirect(url_for('customer_dashboard'))

@app.route('/send_offer/<ticket_id>', methods=['POST'])
def send_offer(ticket_id):
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    offer_amount = request.form.get('offer_amount')
    ticket = tickets_gold.find_one({'_id': ObjectId(ticket_id)})
    if ticket:
        # Calculate offer based on type
        if ticket.get('gold_type'):
            offer = float(ticket.get('gold_weight', 0)) * 9000 * 0.9
        elif ticket.get('property_type'):
            offer = float(ticket.get('area', 0)) * 3000
        elif ticket.get('automobile_type'):
            offer = float(ticket.get('bought_for', 0)) * 0.7
        else:
            offer = float(offer_amount or 0)
        tickets_gold.update_one({'_id': ObjectId(ticket_id)}, {'$set': {'offer_amount': round(offer, 2), 'status': 'offer_sent', 'assigned_to': session['username']}})
        flash('Offer sent to customer!')
    return redirect(url_for('employee_dashboard'))

@app.route('/accept_offer/<ticket_id>', methods=['POST'])
def accept_offer(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    ticket = tickets_gold.find_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    if ticket:
        ticket['status'] = 'offer_accepted'
        # Ensure assigned_to is present in history
        if 'assigned_to' not in ticket:
            ticket['assigned_to'] = None
        history_gold.insert_one(ticket)
        tickets_gold.delete_one({'_id': ObjectId(ticket_id), 'username': session['username']})
        if 'assigned_to' in ticket:
            notifications_gold.insert_one({'employee': ticket['assigned_to'], 'message': f"Customer {ticket['username']} accepted the offer for ticket {ticket['_id']}.", 'type': 'accepted'})
    flash('You have accepted the offer! Please submit your gold and collect your cash. Ticket moved to history.')
    return redirect(url_for('gold_loan'))

@app.route('/decline_offer/<ticket_id>', methods=['POST'])
def decline_offer(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    ticket = tickets_gold.find_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    if ticket:
        ticket['status'] = 'offer_declined'
        if 'assigned_to' not in ticket:
            ticket['assigned_to'] = None
        history_gold.insert_one(ticket)
        tickets_gold.delete_one({'_id': ObjectId(ticket_id), 'username': session['username']})
        if 'assigned_to' in ticket:
            notifications_gold.insert_one({'employee': ticket['assigned_to'], 'message': f"Customer {ticket['username']} declined the offer for ticket {ticket['_id']}.", 'type': 'declined'})
    flash('You have declined the offer. Ticket moved to history.')
    return redirect(url_for('gold_loan'))

@app.route('/employee_history')
def employee_history():
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    username = session['username']
    tickets_handled = list(history_gold.find({'assigned_to': username}))
    return render_template('employee_history.html', tickets=tickets_handled)

@app.route('/previous_tickets')
def previous_tickets():
    if 'username' not in session:
        flash('Please login first!')
        return redirect(url_for('login'))
    username = session['username']
    gold_tickets = list(history_gold.find({'username': username}))
    property_tickets = list(history_property.find({'username': username}))
    auto_tickets = list(history_auto.find({'username': username}))
    all_tickets = gold_tickets + property_tickets + auto_tickets
    # Sort by a timestamp if available, assuming one is stored.
    # For now, just combining them.
    return render_template('previous_tickets.html', tickets=all_tickets)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# Property Loan
@app.route('/property_loan', methods=['GET', 'POST'])
def property_loan():
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Please login first!')
        return redirect(url_for('login'))
    username = session['username']
    # Check for existing active property loan ticket
    user_tickets = list(tickets_property.find({'username': username, 'property_type': 'Property Loan'}))
    if request.method == 'POST':
        if user_tickets:
            flash('You already have an active property loan ticket. Please complete or close it before creating a new one.')
            return redirect(url_for('property_loan'))
        survey_number = request.form.get('survey_number')
        owner_name = request.form.get('owner_name')
        area = request.form.get('area')
        doc_file = request.files.get('property_doc')
        doc_filename = None
        if doc_file and doc_file.filename:
            doc_filename = secure_filename(doc_file.filename)
            doc_file.save(os.path.join(app.config['UPLOAD_FOLDER'], doc_filename))
        ticket = {
            'username': username,
            'property_type': 'Property Loan',
            'survey_number': survey_number,
            'owner_name': owner_name,
            'area': area,
            'property_doc': doc_filename,
            'status': 'pending'
        }
        tickets_property.insert_one(ticket)
        flash('Property loan ticket raised!')
        return redirect(url_for('property_loan'))
    return render_template('property_loan_form.html', username=username, tickets=user_tickets)

# Automobile Loan
@app.route('/automobile_loan', methods=['GET', 'POST'])
def automobile_loan():
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Please login first!')
        return redirect(url_for('login'))
    username = session['username']
    # Check for existing active automobile loan ticket
    user_tickets = list(tickets_auto.find({'username': username, 'automobile_type': {'$exists': True}}))
    if request.method == 'POST':
        if user_tickets:
            flash('You already have an active automobile loan ticket. Please complete or close it before creating a new one.')
            return redirect(url_for('automobile_loan'))
        auto_type = request.form.get('auto_type')
        owner_name = request.form.get('owner_name')
        purchased_year = request.form.get('purchased_year')
        rc_file = request.files.get('rc_doc')
        license_file = request.files.get('license_doc')
        bought_for = request.form.get('bought_for')
        rc_filename = None
        license_filename = None
        if rc_file and rc_file.filename:
            rc_filename = secure_filename(rc_file.filename)
            rc_file.save(os.path.join(app.config['UPLOAD_FOLDER'], rc_filename))
        if license_file and license_file.filename:
            license_filename = secure_filename(license_file.filename)
            license_file.save(os.path.join(app.config['UPLOAD_FOLDER'], license_filename))
        ticket = {
            'username': username,
            'automobile_type': auto_type,
            'owner_name': owner_name,
            'purchased_year': purchased_year,
            'rc_doc': rc_filename,
            'license_doc': license_filename,
            'bought_for': bought_for,
            'status': 'pending'
        }
        tickets_auto.insert_one(ticket)
        flash('Automobile loan ticket raised!')
        return redirect(url_for('automobile_loan'))
    return render_template('automobile_loan_form.html', username=username, tickets=user_tickets)

@app.route('/employee_property_tickets')
def employee_property_tickets():
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    tickets_list = list(tickets_property.find())
    return render_template('employee_property_tickets.html', tickets=tickets_list)

@app.route('/employee_automobile_tickets')
def employee_automobile_tickets():
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    tickets_list = list(tickets_auto.find())
    return render_template('employee_automobile_tickets.html', tickets=tickets_list)

@app.route('/send_offer_property/<ticket_id>', methods=['POST'])
def send_offer_property(ticket_id):
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    offer_amount = request.form.get('offer_amount')
    ticket = tickets_property.find_one({'_id': ObjectId(ticket_id)})
    if ticket:
        offer = float(ticket.get('area', 0)) * 3000
        tickets_property.update_one({'_id': ObjectId(ticket_id)}, {'$set': {'offer_amount': round(offer, 2), 'status': 'offer_sent', 'assigned_to': session['username']}})
        flash('Offer sent to customer!')
    return redirect(url_for('employee_property_tickets'))

@app.route('/decline_property_ticket/<ticket_id>', methods=['POST'])
def decline_property_ticket(ticket_id):
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    username = session['username']
    ticket = tickets_property.find_one({'_id': ObjectId(ticket_id)})
    if ticket:
        ticket['status'] = 'declined_by_employee'
        ticket['assigned_to'] = username
        history_property.insert_one(ticket)
        tickets_property.delete_one({'_id': ObjectId(ticket_id)})
    flash('Ticket declined and moved to customer history.')
    return redirect(url_for('employee_property_tickets'))

@app.route('/send_offer_automobile/<ticket_id>', methods=['POST'])
def send_offer_automobile(ticket_id):
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    offer_amount = request.form.get('offer_amount')
    ticket = tickets_auto.find_one({'_id': ObjectId(ticket_id)})
    if ticket:
        offer = float(ticket.get('bought_for', 0)) * 0.7
        tickets_auto.update_one({'_id': ObjectId(ticket_id)}, {'$set': {'offer_amount': round(offer, 2), 'status': 'offer_sent', 'assigned_to': session['username']}})
        flash('Offer sent to customer!')
    return redirect(url_for('employee_automobile_tickets'))

@app.route('/decline_automobile_ticket/<ticket_id>', methods=['POST'])
def decline_automobile_ticket(ticket_id):
    if 'username' not in session or session.get('user_type') != 'employee':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    username = session['username']
    ticket = tickets_auto.find_one({'_id': ObjectId(ticket_id)})
    if ticket:
        ticket['status'] = 'declined_by_employee'
        ticket['assigned_to'] = username
        history_auto.insert_one(ticket)
        tickets_auto.delete_one({'_id': ObjectId(ticket_id)})
    flash('Ticket declined and moved to customer history.')
    return redirect(url_for('employee_automobile_tickets'))

@app.route('/accept_offer_property/<ticket_id>', methods=['POST'])
def accept_offer_property(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    ticket = tickets_property.find_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    if ticket:
        ticket['status'] = 'offer_accepted'
        if 'assigned_to' not in ticket:
            ticket['assigned_to'] = None
        history_property.insert_one(ticket)
        tickets_property.delete_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    flash('You have accepted the offer! Please proceed with your property loan process. Ticket moved to history.')
    return redirect(url_for('property_loan'))

@app.route('/decline_offer_property/<ticket_id>', methods=['POST'])
def decline_offer_property(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    ticket = tickets_property.find_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    if ticket:
        ticket['status'] = 'offer_declined'
        if 'assigned_to' not in ticket:
            ticket['assigned_to'] = None
        history_property.insert_one(ticket)
        tickets_property.delete_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    flash('You have declined the offer. Ticket moved to history.')
    return redirect(url_for('property_loan'))

@app.route('/accept_offer_automobile/<ticket_id>', methods=['POST'])
def accept_offer_automobile(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    ticket = tickets_auto.find_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    if ticket:
        ticket['status'] = 'offer_accepted'
        if 'assigned_to' not in ticket:
            ticket['assigned_to'] = None
        history_auto.insert_one(ticket)
        tickets_auto.delete_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    flash('You have accepted the offer! Please proceed with your automobile loan process. Ticket moved to history.')
    return redirect(url_for('automobile_loan'))

@app.route('/decline_offer_automobile/<ticket_id>', methods=['POST'])
def decline_offer_automobile(ticket_id):
    if 'username' not in session or session.get('user_type') != 'customer':
        flash('Unauthorized!')
        return redirect(url_for('login'))
    ticket = tickets_auto.find_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    if ticket:
        ticket['status'] = 'offer_declined'
        if 'assigned_to' not in ticket:
            ticket['assigned_to'] = None
        history_auto.insert_one(ticket)
        tickets_auto.delete_one({'_id': ObjectId(ticket_id), 'username': session['username']})
    flash('You have declined the offer. Ticket moved to history.')
    return redirect(url_for('automobile_loan'))

if __name__ == '__main__':
    app.run(debug=True) 