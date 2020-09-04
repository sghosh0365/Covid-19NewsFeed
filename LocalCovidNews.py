from pygooglenews import GoogleNews
gn = GoogleNews(lang='en', country='IN')
local_news= gn.search('coronavirus kolkata')
print(local_news)