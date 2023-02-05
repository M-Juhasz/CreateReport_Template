from email.mime.multipart import MIMEMultipart

import pandas
# MIMEMultipart and pandas are imported on module level only for type hinting. TODO: Find better solution.
# Required import statements are given for each function seperately.


def create_timestamps() -> dict:
    from datetime import datetime
    dtnow = datetime.now()
    return {
        "today_date": dtnow.strftime("%d %b, %Y"),
        "today_time": dtnow.strftime("%H:%M:%S " + dtnow.astimezone().tzname()),
        "timestamp": dtnow.strftime("%m-%d-%Y_%H-%M-%S")
    }


def load_from_excel(filename: str) -> pandas.DataFrame:
    import pandas as pd

    try:
        data = pd.read_excel(filename)
    except IOError as err:
        raise IOError(str(err) + " - Please close Excel.")

    data = data.drop("Unnamed: 0", axis=1)
    return data


# TODO: actually DO stuff with the data - this would be the place


def create_plot_image(data: pandas.DataFrame) -> str:
    import io
    import base64

    # create plot TODO: make more dynamic - loop through column, try grouping to subplots, experiment with plot format
    ax = data["A"].plot()
    data["B"].plot(ax=ax)
    data["C"].plot(ax=ax)

    # create figure from plot and save as file
    fig = ax.get_figure()

    # create string containing bit representation of the image file
    string_bytes = io.BytesIO()
    fig.savefig(string_bytes, format='png')
    string_bytes.seek(0)
    base64_png_data = base64.b64encode(string_bytes.read()).decode("utf-8")
    return f"data:;base64,{base64_png_data}"


def html_report(context: dict, template: str) -> str:
    import jinja2

    # jinja stuff
    # create environment and loader
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    # create html string from template - placeholders are replaced with the items in the dict context
    template = template_env.get_template(template)
    return template.render(context)


def html_to_pdf(html_out: str, filename: str, wkhtmltopdf_path: str) -> str:
    import pdfkit
    # set up pdfkit to use wkhtmltopdf.exe

    options = {
        'page-size': 'A4',
        'margin-top': '0.50in',
        'margin-right': '0.50in',
        'margin-bottom': '0.50in',
        'margin-left': '0.50in',
        'encoding': "UTF-8",
        'no-outline': None,
        # "enable-local-file-access": ""
    }

    try:
        pdf_config = pdfkit.configuration(
            wkhtmltopdf=wkhtmltopdf_path)
        pdfkit.from_string(html_out, filename, options=options, configuration=pdf_config,
                           css='style.css')
        return filename
    except OSError as err:
        raise OSError(str(err))


def mail_create_msg(to: list, cc: list, body_plain: str, body_html: str = "") -> MIMEMultipart:
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    message = MIMEMultipart('alternative')
    message['Subject'] = "createreport.py testmail"
    message['To'] = to
    message['Cc'] = cc

    # Email clients try to render last part first - that should be html
    part1 = MIMEText(body_plain, "plain")
    message.attach(part1)

    if body_html != "":
        part2 = MIMEText(body_html, "html")
        message.attach(part2)

    return message


def mail_attach_file(message: MIMEMultipart, file: str):
    from email import encoders
    from email.mime.base import MIMEBase

    # Open file in binary mode
    with open(file, "rb") as attachment:
        # Read file and set as application/octet-stream. Email clients should recognize this as attachment
        att_part = MIMEBase("application", "octet-stream")
        att_part.set_payload(attachment.read())

    # Encode binary to ASCII
    encoders.encode_base64(att_part)

    # Add header
    att_part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file}",
    )

    # add attachment to message
    message.attach(att_part)


def mail_send(smtp_server: str, port: int, sender: str, password: str, receiver: list, message: MIMEMultipart):
    import smtplib
    import ssl
    import socket

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
    except smtplib.SMTPAuthenticationError as err:
        raise ValueError(str(err) + """
        Could not log in to smtp server. Please check your credentials in config.py. 
        Note that some mail providers require you to set up an application password!""")
    except socket.gaierror as err:
        raise ValueError(str(err) + """
        Could not connect to smtp server. Please check your smtp connection details in config.py.""")


def main():
    import sys
    import config

    print("main:")

    # Get time strings for report and filename
    time = create_timestamps()
    print(f"Got new timestamp: {time['timestamp']}")

    # Load dataframe from excel (first sheet)
    try:
        df = load_from_excel("testdata.xlsx")
    except IOError as error:
        sys.exit(str(error))

    print(f"""DataFrame loaded:
    {df}
    """)

    # TODO: stuff with DataFrame comes here

    # Create plot image as string
    img = create_plot_image(df)
    print(f"""Plot image created: 
        {img}
    """)

    # Prepare context dict - needs placeholders for html template as keys, replacement strings as values
    context_dict = {'table': df.to_html(), 'img': img, 'date': time["today_date"], 'time': time["today_time"],
                    'stats': df.describe().to_html()}

    # Jinja2 - generate html from template and context dicttionary
    html_string = html_report(context_dict, config.html_template)
    print(f"""html string prepared:
        {html_string}
    """)

    # Set output pdf file name (and path if required)
    pdf_file = f"z_test_report_{time['timestamp']}.pdf"

    # Pdfkit - convert html to pdf
    try:
        file_ret = html_to_pdf(html_string, pdf_file, config.wkhtmltopdf_path)
    except OSError as error:
        sys.exit(str(error))

    print(f"""pdf created:
        {file_ret}
    """)

    # Create MIMEMultipart message - bcc not included
    msg = mail_create_msg(config.to, config.cc, config.body_plain, config.body_html)

    # add file attachement to message
    mail_attach_file(msg, file_ret)

    # create list of receivers and send
    receiver_list = config.cc.split(",") + config.bcc.split(",") + config.to.split(",")
    try:
        mail_send(config.smtp_server, config.port, config.sender_email, config.password, receiver_list, msg)
    except ValueError as error:
        sys.exit(str(error))

    print("Mail sent to: " + str(receiver_list))


if __name__ == "__main__":
    main()
