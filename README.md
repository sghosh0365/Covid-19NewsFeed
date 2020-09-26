# Covid-19NewsFeed

Dear Programmer,

Good day to you!

I am Snehasis Ghosh, a Data Engineer by profession. I would like to share with you a recent project I did on a daily Covid-19 newsletter. 

Introduction
============

The idea behind the project was to collate Covid-19 related news across different categories from differnt news agencies into one single bucket. The project uses the pygooglenews package to scrape Google News. Apart from the news, the newsletter also holds differnt stats on the current pandemic situation (updated daily). These are-

A geo heat map depicting the count of new confirmed cases across the globe

State wise stats in India

Daily and monthly average counts over last 6 months using a line graph

The newsletter is in .pdf format and is mailed to the recipients on a daily basis. You can customize the local news category based on user's location preference. Please browse the SampleNewsletters directory for sample newsletters.


Technology Stack
================

Python3

HTML

Pre-requisites
==============

Python 3 installation

orca (Plotly's image-exporting utilities) installation for generating image files of graphs created using plotly (https://github.com/plotly/orca)

wkhtmltopdf installation to convert html to pdf (https://wkhtmltopdf.org/)

Code Walkthrough
================

The project is comprised of 5 python scripts, the details of which are provided below-

Covid-19NewsMain.py: This is the main script which orchastrates the entire process. In this script, the main body of the newsletter is created including the the text table for the state wise stats in India of the stats page

Covid19NewsStats1.py: This creates the geo heat map depicting the count of new confirmed cases using plotly. The data is collected using the api https://api.covid19api.com/. The plot is then exported into a .png file which is placed in the top left corner of the stats page

Covid19NewsStats2.py: This creates the 2 line graphs depicting the average numbers over a period of time. The data is collected using the api https://api.covid19india.org/ and is exported into a .jpg file. The image is used in the stats page of the newsletter

Covid19NewsGeneratePDF.py: This converts the html newsletter into a .pdf file to be emailed to the recipients

Covid19NewsSendEmail.py: The script sends out the email to the appropriate recipients using a google account. You may configure the script and your email settings to use a different smtp server

All the image files associated with the .py files can be obtained from the NewsLetterImages directory

Please reach out to me in case you need help or you have suggestions. I am open to feedback.

Regards,

Snehasis Ghosh

LinkedIn: https://linkedin.com/in/snehasis-ghosh-b17b30a3
