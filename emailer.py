"""
Email module which handles the crafting and sending of emails.
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from tabulate import tabulate
import config


def send_deals(args, deals):
    # craft email
    headers = [['Price', 'Link']]
    text = '{table}'
    html = """
    <html>
        <body>
            {table}
        </body>
    </html>
    """
    deals = [(deal.price, deal.title, deal.link) for deal in deals.values()]
    text = text.format(table=tabulate(headers + deals, headers='firstrow', tablefmt='grid'))
    html = html.format(table=tabulate(
        headers +  [(r[0], '<a href="{1}" target="_blank">{0}</a>'.format(r[1], r[2])) for r in deals],
        headers='firstrow',
        tablefmt='html')
                      )

    # send email to subscribers
    message = MIMEMultipart('alternative', None, [MIMEText(text), MIMEText(html, 'html')])
    message['Subject'] = 'Your Dam Deals'
    message['From'] = args.user
    message['To'] = config.subscribers

    server = smtplib.SMTP_SSL(args.smtp)
    server.login(args.user, args.password)
    server.send_message(message)
    server.quit()

    print('Updated list has been sent!')
