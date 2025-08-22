# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_loan_confirmation_email(user, loan):
    subject = "Loan Application Confirmation"
    from_email = "noreply@myloanapp.com"
    to = [user.email]

    text_content = f"Hi {user.first_name},\nYour loan application has been received successfully."

    # Mapping codes to readable names
    loan_type_map = {
        "PL": "Personal Loan",
        "HL": "Home Loan",
        "VL": "Vehicle Loan",
        "EL": "Education Loan",
    }

    # Pick display value
    loan_display_type = loan_type_map.get(loan.loan_type, loan.loan_type)

    # Render with readable loan type
    html_content = render_to_string("emails/loan_confirmation.html", {
        "user": user,
        "loan": loan,
        "loan_display_type": loan_display_type,
    })

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

