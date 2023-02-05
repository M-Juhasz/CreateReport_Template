# Example / Teamplate for a "Report Generator":

* reads first sheet of testdata file as pandas dataframe, currently includes (and possibly expects) 3 columns in plot
* uses report.html as template for pdf
* outputs z_test_report_[timestamp].pdf
* sends mail with attachment (mail details in config.py!)

Instructions:
* Install dependencies: 
	* python packages - see requirements.txt (or use pip install -r requirements.txt) 
	* download wkhtmltopdf
* create config.py from config_template.py
* run createreport.py

## No License
Just playing around, use what you like.
I'm not responsible for any negative results of effects.
I am, however, responsible if this generates money. 
I'm sure that's how this works :)
