import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_order_confirmation(to_email, order_summary):
    """
    Sends an order confirmation email using SendGrid.

    Args:
        to_email (str): Recipient's email address.
        order_summary (str): Text summary of the order.

    Returns:
        int | None: HTTP status code if successful, None if failed.
    """
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    
    if not SENDGRID_API_KEY:
        print("SendGrid API key is missing in environment variables.")
        return None

    message = Mail(
        from_email='your_verified_sender@example.com',  # replace with a verified sender
        to_emails=to_email,
        subject='Order Confirmation - Farmart',
        html_content=f"""
        <h2>Thank you for your order!</h2>
        <p>Here are your order details:</p>
        <pre>{order_summary}</pre>
        <p>We’ll be in touch when your order is on the way.</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email}. Status: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"SendGrid Error: {e}")
        return None
