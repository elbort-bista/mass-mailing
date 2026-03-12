import smtplib
import ssl
import csv
import time
import re
import mimetypes

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from django.shortcuts import render
from django.conf import settings
from .models import User


def index(request):
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})


def mail(request):
    if request.method != 'POST':
        return render(request, 'home.html', {'code': 'Invalid request method'})

    mails = []
    code = ""

    subject = request.POST.get('Subject')
    message = request.POST.get('message')
    username_input = request.POST.get('username', '')

    if not all([subject, message]):
        return render(request, 'home.html', {'code': 'All fields are required'})

    if 'myfile' not in request.FILES:
        return render(request, 'home.html', {'code': 'CSV file is required'})

    # ================= SMTP CONFIG =================
    try:
        from .models import SMTPConfiguration
        smtp = SMTPConfiguration.objects.get(is_active=True)

        smtp_host = smtp.smtp_host
        smtp_port = int(smtp.smtp_port)
        smtp_username = smtp.smtp_username
        smtp_password = smtp.smtp_password
        smtp_use_tls = smtp.smtp_use_tls
        smtp_use_ssl = smtp.smtp_use_ssl
    except:
        smtp_host = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_username = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD
        smtp_use_tls = settings.EMAIL_USE_TLS
        smtp_use_ssl = settings.EMAIL_USE_SSL

    sender_email = smtp_username
    password = smtp_password

    # ================= SMTP CONNECT =================
    try:
        if smtp_use_ssl:
            server = smtplib.SMTP_SSL(
                smtp_host,
                smtp_port,
                context=ssl.create_default_context()
            )
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
            if smtp_use_tls:
                server.starttls(context=ssl.create_default_context())

        server.ehlo()
        server.login(sender_email, password)
        code = "SMTP Login Successful ✅"

    except smtplib.SMTPAuthenticationError:
        return render(request, 'home.html', {
            'code': 'SMTP Auth Failed ❌ (Use App Password)'
        })
    except Exception as e:
        return render(request, 'home.html', {
            'code': f'SMTP Error ❌ {str(e)}'
        })

    # ================= CSV LOAD =================
    file = request.FILES['myfile']

    try:
        data = file.read().decode('utf-8').splitlines()
    except:
        return render(request, 'home.html', {'code': 'CSV must be UTF-8 encoded'})

    reader = csv.reader(data)
    next(reader, None)

    preloaded_attachments = []
    if 'attachment' in request.FILES:
        for f in request.FILES.getlist('attachment'):
            try:
                filename = f.name
                content = f.read()
                mime_type, _ = mimetypes.guess_type(filename)
                if mime_type:
                    maintype, subtype = mime_type.split('/', 1)
                else:
                    maintype, subtype = 'application', 'octet-stream'
                preloaded_attachments.append((filename, content, maintype, subtype))
            finally:
                try:
                    f.seek(0)
                except Exception:
                    pass
    if 'attachment2' in request.FILES:
        for f in request.FILES.getlist('attachment2'):
            try:
                filename = f.name
                content = f.read()
                mime_type, _ = mimetypes.guess_type(filename)
                if mime_type:
                    maintype, subtype = mime_type.split('/', 1)
                else:
                    maintype, subtype = 'application', 'octet-stream'
                preloaded_attachments.append((filename, content, maintype, subtype))
            finally:
                try:
                    f.seek(0)
                except Exception:
                    pass

    # ================= USERNAME =================
    custom_username = None
    if '=' in username_input:
        custom_username = username_input.split('=')[0].strip()

    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    count = 0

    for row in reader:
        if not row or count >= 200:
            break

        email_address = row[0].strip()
        first_name = row[1].strip() if len(row) > 1 else ""
        last_name = row[2].strip() if len(row) > 2 else ""
        gender = row[3].strip().lower() if len(row) > 3 else ""

        if not email_regex.match(email_address):
            continue

        username = custom_username if custom_username else email_address.split('@')[0]

        # ================= SALUTATION =================
        if gender == "male":
            salutation = "Sir"
        elif gender == "female":
            salutation = "Ma'am"
        else:
            salutation = "Sir/Ma'am"

        body = f"Respected {first_name} {salutation},\n\n{message}"

        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email_address
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            for filename, content, maintype, subtype in preloaded_attachments:
                part = MIMEBase(maintype, subtype)
                part.set_payload(content)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)

            server.sendmail(sender_email, email_address, msg.as_string())

            mails.append([email_address, username, "Sent"])
            count += 1

            # ================= COOLDOWN =================
            if count % 80 == 0:
                server.quit()
                time.sleep(200)

                if smtp_use_ssl:
                    server = smtplib.SMTP_SSL(
                        smtp_host,
                        smtp_port,
                        context=ssl.create_default_context()
                    )
                else:
                    server = smtplib.SMTP(smtp_host, smtp_port)
                    if smtp_use_tls:
                        server.starttls(context=ssl.create_default_context())

                server.login(sender_email, password)

        except Exception as e:
            mails.append([email_address, username, f"Failed: {str(e)}"])

    server.quit()

    return render(request, 'home.html', {
        'mail': mails,
        'code': f"{code} | Total Sent: {count}"
    })


def custom_404(request, exception):
    return render(request, '404.html', status=404)
