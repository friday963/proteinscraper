from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGridEmailer:
    def __init__(self, to_email, from_email, subject) -> None:
        self.to_email = to_email
        self.from_email = from_email
        self.subject = subject
        self.api_key = ""
        self.body = ""
    def add_body_and_format(self,body):
        formatted_body = f"""
            <html>
                <head/>
                <body>
            """
        for deal in body:
            for deal_desc, deal_meta in deal.items():
                formatted_body += f"<u><h3>{deal_desc}</h3></u>"
                formatted_body += f"<p>{deal_meta['Price']}</p>"        
                formatted_body += f"<p>{deal_meta['Link']}</p>"        
                formatted_body += f"<p>{deal_meta['Deal']}</p>"        
        formatted_body += """
            </body>
            </html>
        """
        self.body = formatted_body
    def send_email(self):
        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_email,
            subject=self.subject,
            html_content=self.body)
        try:
            sg = SendGridAPIClient()
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

if __name__ == "__main__":
    send = SendGridEmailer(to_email="", from_email="", subject="Test email job")
    send.add_body_and_format("")
    send.send_email()