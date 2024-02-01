import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.templating import Jinja2Templates

from config.config import setting
from src.general.response import error_response, get_message

templates = Jinja2Templates(directory="/home/mind/Book_Inventory_Management/templates")

# template_user = templates.get_template("user_main.html")
# template_admin = templates.get_template("admin_main.html")

template_user = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .welcome-container {
            text-align: center;
            background-color: rgb(105, 209, 166);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #000000;
        }

        p {
            color: #333333;
        }

        a {
            color: #000000;
            text-decoration: none;
            font-weight: bold;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="welcome-container">
        <h1>Welcome Admin to Our Website!</h1>
        <p>Thank you for signing up.</p>
        <p>Now, You Can Start Managing Book.</p>    
    </div>
</body>
</html>
"""

template_admin = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .welcome-container {
            text-align: center;
            background-color: #db8c8c;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #000000;
        }

        p {
            color: #333333;
        }

        a {
            color: #000000;
            text-decoration: none;
            font-weight: bold;
        }

        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="welcome-container">
        <h1>Welcome User to Our Website!</h1>
        <p>Thank you for signing up.</p>
        <p>Explore our website and read amazing Books.</p>    
    </div>
</body>
</html>
"""

def create_template(user_type):
    if user_type == ['admin']:
        template_str = template_admin
    else:
        template_str = template_user
    return str(template_str)


def send_email(to_email, subject, user_type):
    # Replace these values with your SMTP server details    
    smtp_server = setting.MAIL_SERVER
    smtp_port = setting.MAIL_PORT
    smtp_username = setting.MAIL_USERNAME
    smtp_password = setting.MAIL_PASSWORD

    template = create_template(user_type)

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = "nencypatel1412@gmail.com"
    message["To"] = "nency.patel@mindinventory.com"

    message.attach(MIMEText(template, 'html'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail("nencypatel1412@gmail.com", [to_email], message.as_string())

    except Exception as e:
        logging.error(f"Internal server error: {e.args}")
        return error_response(get_message("internal_server", "internal"), 500)

