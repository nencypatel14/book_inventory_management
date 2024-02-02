from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from jinja2 import Template


def create_template(user_type):
    file_name = 'user_main.html'
    if user_type == 'admin':
         file_name = 'admin_main.html'  
    with open(f"templates/{file_name}", "r") as file:
            template_str = file.read()
        
    jinja_template = Template(template_str)
    return jinja_template

def send_email(to_email, subject, user_type):
    # Replace these values with your SMTP server details    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'nencypatel1412@gmail.com'
    smtp_password = 'aetx bmau uoih lnhz'

    template = create_template(user_type)
    rendered_template = template.render({
         "first_name":"Vatsal"
    })  # Render the Jinja template

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = "nencypatel1412@gmail.com"
    message["To"] = "nency.patel@mindinventory.com"

    message.attach(MIMEText(rendered_template, 'html'))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail("nencypatel1412@gmail.com", [to_email], message.as_string())


send_email('nency.patel@mindinventory.com',"test test", user_type='admin')
