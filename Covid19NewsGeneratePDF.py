import pdfkit


def generate_pdf():
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {'page-size': 'A4', 'dpi': 400, "enable-local-file-access": "", "encoding": "UTF-8",
               "footer-right": "[page]"}
    more_stories_filename = "GoogleCovid-19MoreStories.html"
    numbers_filename = "GoogleCovid-19Numbers.html"
    search_loc_li = ['Pune', 'Kolkata', 'Bangalore']
    for loc in search_loc_li:
        html_filename = 'GoogleCovid-19NewsLetter_' + loc + '.html'
        pdf_filename= 'COVID-19NewsLetter_'+ loc +'.pdf'
        pdfkit.from_file([html_filename, numbers_filename, more_stories_filename],pdf_filename,
                     configuration=config, options=options)
    print('Completed execution of Covid-19 News PDF')
