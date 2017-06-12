import os
from flask import Flask, render_template, request
import stripe

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

# Token is created using Stripe.js or Checkout!
# Get the payment token submitted by the form:
# token = POST['stripeToken'] # Using Flask


@app.route('/')
def index():
    return render_template('index.html',key=stripe_keys['publishable_key'])
@app.route('/charge', methods=['POST'])
def charge():
  amount=999
  #amt in cents
# Create a Customer:
  customer = stripe.Customer.create(
    email="paying.user@example.com",
    source=request.form['stripeToken']
    )

# Charge the user's card:
  charge = stripe.Charge.create(
    customer=customer.id,
    amount=amount,
    currency='usd',
    description="ReeDistribute Charge"
  )
  with open("database3.txt","w+") as f:
      f.write("Customer ID: " + str(customer.id) + '\n' + "Amount Charged (cents): " + str(charge.amount)
       +'\n' + "email: " + str(customer.email))
      print(f)
      #this prints any information we may want to store onto a .txt file
      #right now, customer-id,amount,email
  
  return render_template('charge.html',amount=amount)


if __name__ == '__main__':
    app.run(debug=True)


