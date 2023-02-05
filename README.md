# Example / Teamplate for a "Report Generator":
Tried to seperate code into functions as I thought it made sense. Imports on function level for easy reuseability.

Example script demoing useage of the functions can be found in main function. Test by executing createreport.py.

* reads first sheet of testdata file as pandas dataframe, currently includes (and possibly expects) 3 columns in plot
* uses report.html as template for pdf
* outputs z_test_report_[timestamp].pdf
* sends mail with attachment (mail details in config.py!)

Instructions:
* Install dependencies: 
	* python packages - see requirements.txt (or use pip install -r requirements.txt) 
	* download wkhtmltopdf
* create config.py from config_template.py (will your contain email credentials, local and smtp configuration)
* run createreport.py

## No License
Just playing around, use what you like.
I'm not responsible for any negative results or effects.
I am, however, responsible if this generates money. 
I'm sure that's how this works :)
