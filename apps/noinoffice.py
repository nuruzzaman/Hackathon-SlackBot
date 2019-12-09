from . import on_command
import smtplib, ssl

# Source Code
#https://realpython.com/python-send-email/

@on_command(['NOINOFFICE'])
def run(robot, channel, user, tokens):

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "bigdata.enterprise@gmail.com"
    receiver_email = "mohammad.nuruzzaman@elmolearning.com.au"
    password = "Rayo@0304"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.login(sender_email, password)

        # TODO: Send email here
        email_message = """\
        Subject: Hackathon 2019 Contest 

        This message is sent from ELMO Hackaton Bot ."""
        server.sendmail(sender_email, receiver_email, email_message)

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()


    return channel, 'I have sent email successfully. What else I can do for you? '


