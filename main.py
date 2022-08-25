from multiprocessing.spawn import import_main_path
from protein_scrape import MuscleAndStrengthProtein
from sendemail import SendGridEmailer
import os

if __name__ == "__main__":
    email_api_key = os.environ.get('SENDGRID_API_KEY')
    to_email = os.environ.get("TO_EMAIL")
    from_email = os.environ.get("FROM_EMAIL")
    ms = MuscleAndStrengthProtein()
    get_page = ms.get_url()
    results = ms.parse_results(get_page)
    send = SendGridEmailer(to_email=to_email, from_email=from_email, subject="Automated Protein Deal Alerts")
    send.add_body_and_format(results)
    send.send_email()