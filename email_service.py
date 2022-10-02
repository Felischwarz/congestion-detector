import smtplib, ssl

from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD


def send_email(receiver_email, message):
	port = 465  # For SSL

	# Create a secure SSL context
	context = ssl.create_default_context()

	try:
		with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
			server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
			server.sendmail(EMAIL_ADDRESS, receiver_email, ("Subject: Staumelder \n" + message).encode('utf-8'))

	except Exception as e:
		print(f"Error sending E-Mail to {receiver_email}: {e}")

