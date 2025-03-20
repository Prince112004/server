from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests from React frontend

# Hardcoded list of receiver emails
receiver_emails = [
    "princechauhan112004@gmail.com",
    "sprashant96624@gmail.com",
    "swarajsingh494@gmail.com"
]

def send_alert_email(receiver_emails, user_name, tweet_id):
    sender_email = "sprashant96624@gmail.com"
    app_password = "lczz kxce kslt fmag"  # Use your actual app password
    subject = "Suspicious Activity Alert"

    # Construct the email message
    message = (f"{user_name} is suspicious and spreading hate/threat on social media.\n"
               f"With the following tweet ID: {tweet_id}\n"
               "Please look into this matter.")

    text = f"Subject: {subject}\n\n{message}"

    try:
        # Set up the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)

        # Send email to each receiver
        for receiver_email in receiver_emails:
            server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        if 'server' in locals():
            server.quit()

@app.route('/alert', methods=['POST'])
def send_alert():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Extract required information
        user_name = data.get("user_name", "Unknown User")
        tweet_id = data.get("tweet_id", "No Tweet ID Provided")

        # Send alert email
        send_alert_email(receiver_emails, user_name, tweet_id)

        return jsonify({"status": "success", "message": "Alert email sent!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5200)
