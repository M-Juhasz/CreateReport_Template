import jinja2
import pdfkit
import pandas as pd
import base64
import os
from datetime import datetime

today_date = datetime.today().strftime("%d %b, %Y")

print(__name__)

while True: 
    try:
        myfile = open("testdata.xlsx", "r")
        myfile.close()
        break                            
    except IOError:
        input("Could not open file! Please close Excel. Press Enter to retry.")

df = pd.read_excel("testdata.xlsx")
df = df.drop("Unnamed: 0",axis=1)

timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

# create plot
ax = df["A"].plot()
df["B"].plot(ax=ax)
df["C"].plot(ax=ax)

# create figure from plot and save as file
fig = ax.get_figure()
imagefile = 'test_'+timestamp+'.png'
fig.savefig(imagefile)

# create string containing bit representation of the image file
with open(imagefile, 'rb') as image_file:
    img = "data:;base64,{}".format(base64.b64encode(image_file.read()).decode("utf-8"))
    print(str(image_file.read()))

# remove file TODO: find way to create image bitstring in the fly without saving to HD
os.remove(imagefile)

context = {'table': df.to_html(), 'img': img, 'date': today_date}

# jinja stuff
# create environment and loader
template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)

# create html string from template - placeholders are replaced with the items in the dict context
template = template_env.get_template('report.html')
output_text = template.render(context)

# set up pdfkit to use wkhtmltopdf.exe (TODO: include exe in project folder) and use the from_string method to output pdf file based on html string
filename = 'report_out_{}.pdf'.format(timestamp)

config = pdfkit.configuration(wkhtmltopdf='C://Users//Matyas//OneDrive - Zifo RnD Solutions//Matyas//Python//wkhtmltox//bin//wkhtmltopdf.exe')
pdfkit.from_string(output_text, filename, options={"enable-local-file-access": ""}, configuration=config, css='style.css')