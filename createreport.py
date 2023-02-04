import pandas as pd
from typing import Optional

import config
# import smtplib
# import ssl


def create_timestamps():
    from datetime import datetime

    today_date = datetime.today().strftime("%d %b, %Y")
    timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    return {
        "today_date": today_date,
        "timestamp": timestamp
    }


def load_from_excel(filename: str) -> Optional[pd.DataFrame]:
    while True:
        try:
            data = pd.read_excel(filename)
            break
        except IOError:
            usr_in = input("Could not open file! Please close Excel. Type A to abort or press Enter to retry: ")
            if usr_in.upper() == "A":
                return

    data = data.drop("Unnamed: 0", axis=1)
    return data


def create_plot_image(data: pd.DataFrame) -> str:
    import io
    import base64

    # create plot
    ax = data["A"].plot()
    data["B"].plot(ax=ax)
    data["C"].plot(ax=ax)

    # create figure from plot and save as file
    fig = ax.get_figure()

    # create string containing bit representation of the image file
    string_bytes = io.BytesIO()
    fig.savefig(string_bytes, format='png')  # instead of fig.savefig(imagefile)
    string_bytes.seek(0)
    base64_png_data = base64.b64encode(string_bytes.read()).decode("utf-8")
    return "data:;base64,{}".format(base64_png_data)


def html_report(context: dict) -> str:
    import jinja2

    # jinja stuff
    # create environment and loader
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    # create html string from template - placeholders are replaced with the items in the dict context
    template = template_env.get_template('report.html')
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

    pdf_config = pdfkit.configuration(
        wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_string(html_out, filename, options=options, configuration=pdf_config,
                       css='style.css')

    return filename


if __name__ == "__main__":
    print("main:")

    # get time strings for report and filename
    time = create_timestamps()
    print(f"Got new timestamp: {time['timestamp']}")

    # load dataframe from excel (first sheet)
    df = load_from_excel("testdata.xlsx")
    if df is None:
        print("Could not open source file. Aborted by user.")
    else:
        print(f"""DataFrame loaded:
        {df}
        """)

        # TODO: stuff with DataFrame comes here

        # create plot image as string
        img = create_plot_image(df)
        print(f"""Plot image created: 
            {img}
        """)

        # prepare context dict - needs placeholders for html template as keys, replacement strings as values
        context_dict = {'table': df.to_html(), 'img': img, 'date': time["today_date"]}

        # Jinja2 - generate html from template and context dicttionary
        html_string = html_report(context_dict)
        print(f"""html string prepared:
            {html_string}
        """)

        # set output pdf file name (and path if required)
        pdf_file = f"z_test_report_{time['timestamp']}.pdf"

        # pdfkit - convert html to pdf
        file = html_to_pdf(html_string, pdf_file, config.wkhtmltopdf_path)
        print(f"""pdf created:
            {file}
        """)
