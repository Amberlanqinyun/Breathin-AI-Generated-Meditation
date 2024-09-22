from flask import jsonify, render_template, request, redirect, url_for, flash, session
import stripe
import os
from mod_utilize import app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Stripe using environment variables for security
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'GET':
        return render_template('donate.html')
    
    elif request.method == 'POST':
        data = request.get_json()
        token = data.get('token')
        amount = data.get('amount')

        if not token or not amount:
            return jsonify({'success': False, 'error': 'Invalid data.'}), 400

        try:
            charge = stripe.Charge.create(
                amount=int(float(amount) * 100),  # Convert to cents
                currency='nzd',
                description='Donation',
                source=token
            )
            return jsonify({'success': True}), 200
        except stripe.error.CardError as e:
            return jsonify({'success': False, 'error': e.user_message}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': 'An error occurred.'}), 500
