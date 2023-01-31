import jinja2
import pdfkit
import pandas as pd
import base64
import os
from datetime import datetime

today_date = datetime.today().strftime("%d %b, %Y")

df = pd.read_excel("testdata.xlsx")
timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

ax = df["A"].plot()
df["B"].plot(ax=ax)
df["C"].plot(ax=ax)
fig = ax.get_figure()
imagefile = 'test_'+timestamp+'.png'
fig.savefig(imagefile)

with open(imagefile, 'rb') as image_file:
    img = "data:;base64,{}".format(base64.b64encode(image_file.read()).decode("utf-8"))

os.remove(imagefile)

context = {'table': df.to_html(), 'img': img, 'date': today_date}

# jinja stuff
# create environment and loader
template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)

template = template_env.get_template('report.html')
output_text = template.render(context)


filename = 'report_out_{}.pdf'.format(timestamp)

config = pdfkit.configuration(wkhtmltopdf='C://Users//Matyas//OneDrive - Zifo RnD Solutions//Matyas//Python//wkhtmltox//bin//wkhtmltopdf.exe')
pdfkit.from_string(output_text, filename, options={"enable-local-file-access": ""}, configuration=config, css='style.css')