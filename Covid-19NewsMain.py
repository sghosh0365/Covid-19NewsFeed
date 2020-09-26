from pygooglenews import GoogleNews
from datetime import date, timedelta, datetime
import os
import requests
import json
import pandas as pd
import sys
import time
import numpy as np
from Covid19NewsStats1 import generate_maps_1
from Covid19NewsStats2 import generate_maps_2
from Covid19NewsGeneratePDF import generate_pdf
from Covid19NewsSendEmail import send_email
coverpic_li = ['Covid-19CoverPagePic-1.jpg', 'Covid-19CoverPagePic-2.jpg', 'Covid-19CoverPagePic-3.jpg',
               'Covid-19CoverPagePic-4.jpg', 'Covid-19CoverPagePic-5.jpg', 'Covid-19CoverPagePic-5.jpg',
               'Covid-19CoverPagePic-6.jpg', 'Covid-19CoverPagePic-7.jpg']
search_loc_li=['Pune','Kolkata','Bangalore']
generate_maps_1()
generate_maps_2()


more_stories_filename = "GoogleCovid-19MoreStories.html"
Issue_counter_filename = "GoogleCovid-19NewsLetterIssue.txt"
numbers_filename = "GoogleCovid-19Numbers.html"
for loc in search_loc_li:
    html_filename = 'GoogleCovid-19NewsLetter_'+loc+'.html'
    if os.path.exists(html_filename):
        os.remove(html_filename)
    if os.path.exists(more_stories_filename):
        os.remove(more_stories_filename)
    if os.path.exists(numbers_filename):
        os.remove(numbers_filename)
    if os.path.exists(Issue_counter_filename):
        f_issue = open(Issue_counter_filename, "r")
        var_issue_counter = int(f_issue.readline())
        f_issue.close()
        var_issue_counter += 1
        f_issue = open(Issue_counter_filename, "w")
        f_issue.write(str(var_issue_counter))
        f_issue.close()
    else:
        var_issue_counter = 1
        f_issue = open(Issue_counter_filename, "w")
        f_issue.write(str(var_issue_counter))
        f_issue.close()

    today = date.today()
    issue_date = today.strftime("%B %d %Y")
    gn = GoogleNews(lang='en', country='IN')
    covid_news = gn.topic_headlines('CAAqIggKIhxDQkFTRHdvSkwyMHZNREZqY0hsNUVnSmxiaWdBUAE')
    covid_news_local=gn.search(f'coronavirus {loc}')
    f_more = open(more_stories_filename, encoding='utf-8', mode="a")
    f_more.write('<!DOCTYPE html>')
    f_more.write('<html>')
    f_more.write('<body>')
    f = open(html_filename, encoding='utf-8', mode="a")
    f.write('<!DOCTYPE html>')
    f.write('<html>')
    f.write('<body>')
    f.write('<div>')
    cover_image_idx=np.random.randint(0,7)
    cover_image=coverpic_li[cover_image_idx]
    f.write(f'<img src={cover_image} width="1000" height="400">')
    f.write(
        f'<p style="font-family:sans-serif;color:#686868;font-size:12px;"><b>Issue Date: {issue_date} Issue: {var_issue_counter}</b></p>')
    cnt = 0
    more_stories_flg = 0
    for story in covid_news['entries']:
        if cnt == 0:
            topic = 'Top news'
            local_news_flg = 0
        elif cnt == 4:
            topic = 'Local news'
            local_news_flg=1
            local_cnt=0
        elif cnt == 8:
            topic = 'Economic impact'
            local_news_flg = 0
        elif cnt == 12:
            topic = 'Science & research'
            local_news_flg = 0
        elif cnt == 16:
            topic = 'Travel impact'
            local_news_flg = 0
        elif cnt > 19:
            topic = 'More stories'
            local_news_flg = 0
            f = f_more
        else:
            pass
        if cnt % 4 == 0 and more_stories_flg == 0:
            if cnt > 0 and topic != 'More stories':
                f.write('</table>')
                f.write('<table><tr><td style = "padding:10px;"></td></tr></table>')
            if topic == 'More stories':
                more_stories_flg = 1
            f.write('<table style = "width:1000px; border: 1px solid black; border-radius:8px;padding-left:10px;">')
            f.write('<tr>')
            f.write(f'<th style = "font-size:40px;text-align: left; font-family:Helvetica;">{topic}</th>')
            f.write('</tr>')
            f.write('<tr><td style = "padding:10px;"></td></tr>')
        if local_news_flg == 1:
            story1= covid_news_local['entries'][local_cnt]
            local_cnt+=1
        else:
            story1=story

        article_title = ''.join(story1['title'].rsplit(' - ', 1)[0])
        article_link = story1['link']
        article_datetime = story1['published']
        article_datetime = datetime.strptime(article_datetime, '%a, %d %b %Y %H:%M:%S %Z')
        to_ist = timedelta(hours=5.5)
        article_datetime = article_datetime + to_ist
        article_datetime = article_datetime.strftime('%a, %d %b %Y %H:%M:%S') + ' IST'
        article_src_nm = story1['source']['title']
        article_src_link = story1['source']['href']
        f.write('<tr>')
        f.write(f'<td><a style = "font-size:25px;color:#003399;" href ={article_link}><b>{article_title}</b></a></td>')
        f.write('</tr>')
        if len(story1['sub_articles']) > 0:
            for sub_article in story1['sub_articles']:
                sub_article_link = sub_article['url']
                sub_article_title = sub_article['title']
                f.write('<tr>')
                f.write(
                    f'<td style="padding-left: 30px;font-family:sans-serif;font-size:15px; color:#000000;">{sub_article_title}<a style="padding-left: 10px;color:#5b5757;font-size:14px" href={sub_article_link}><b>Read</b></a></td>')
                f.write('</tr>')
        f.write('<tr>')
        f.write(
            f'<td style="font-family:sans-serif;font-size:15px; color:#000000;">Source:<a style="padding-left: 10px;color:#5b5757;font-size:14px" href={article_src_link}><b>{article_src_nm}</b></a></td>')
        f.write('</tr>')
        f.write('<tr>')
        f.write(
            f'<td style = "font-family:sans-serif;font-size:15px; color:#000000;">Published at: {article_datetime} </td>')
        f.write('</tr>')
        f.write('<tr><td style = "padding:10px;"></td></tr>')
        cnt += 1


    def publish_other_topics(html_filename, matches, url, topic):
        f = open(html_filename, encoding='utf-8', mode="a")
        latest = gn.topic_headlines(url)
        cnt = 0
        f.write('</table>')
        f.write('<table><tr><td style = "padding:10px;"></td></tr></table>')
        f.write('<table style = "width:1000px; border: 1px solid black; border-radius:8px;padding-left:10px;">')
        f.write('<tr>')
        f.write(f'<th style = "font-size:40px;text-align: left; font-family:Helvetica;">{topic}</th>')
        f.write('</tr>')
        f.write('<tr><td style = "padding:10px;"></td></tr>')
        for story in latest['entries']:
            if any(x in story['title'].upper() for x in matches):
                article_title = ''.join(story['title'].rsplit(' - ', 1)[0])
                article_link = story['link']
                article_datetime = story['published']
                article_datetime = datetime.strptime(article_datetime, '%a, %d %b %Y %H:%M:%S %Z')
                to_ist = timedelta(hours=5.5)
                article_datetime = article_datetime + to_ist
                article_datetime = article_datetime.strftime('%a, %d %b %Y %H:%M:%S') + ' IST'
                article_src_nm = story['source']['title']
                article_src_link = story['source']['href']
                f.write('<tr>')
                f.write(
                    f'<td><a style = "font-size:25px;color:#003399;" href ={article_link}><b>{article_title}</b></a></td>')
                f.write('</tr>')
                if len(story['sub_articles']) > 0:
                    for sub_article in story['sub_articles']:
                        sub_article_link = sub_article['url']
                        sub_article_title = sub_article['title']
                        f.write('<tr>')
                        f.write(
                            f'<td style="padding-left: 30px;font-family:sans-serif;font-size:15px; color:#000000;">{sub_article_title}<a style="padding-left: 10px;color:#5b5757;font-size:14px" href={sub_article_link}><b>Read</b></a></td>')
                        f.write('</tr>')
                f.write('<tr>')
                f.write(
                    f'<td style="font-family:sans-serif;font-size:15px; color:#000000;">Source:<a style="padding-left: 10px;color:#5b5757;font-size:14px" href={article_src_link}><b>{article_src_nm}</b></a></td>')
                f.write('</tr>')
                f.write('<tr>')
                f.write(
                    f'<td style = "font-family:sans-serif;font-size:15px; color:#000000;">Published at: {article_datetime} </td>')
                f.write('</tr>')
                f.write('<tr><td style = "padding:10px;"></td></tr>')
                if cnt == 3:
                    break
                cnt += 1
        return True

    matches = ["CORONAVIRUS", "COVID", "CORONA", "SARS-COV", "PANDEMIC", "SANITIZER", "N95", "COVID-19"]
    url = 'CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ'
    topic = 'Latest health news'
    publish_other_topics(html_filename, matches, url, topic)

    f.close()
    f_nums = open(numbers_filename, "w")
    f_nums.write(
        '<table style="width:1000px; border: 1px solid black; border-radius:8px;padding-left:10px;padding-right:10px;padding-bottom:10px;">')
    f_nums.write('<tr>')
    f_nums.write('<th style="font-size:40px;text-align: left; font-family:Helvetica;">Covid-19: In Numbers</th>')
    f_nums.write('<th></th>')
    f_nums.write('</tr>')
    f_nums.write('<tr><td style = "padding:10px;"></td></tr>')
    f_nums.write('<tr>')
    f_nums.write(
        '<td style="font-family:sans-serif;font-size:20px; color:#003399; text-align:center;"><b>World: New confirmed cases</b></td>')
    f_nums.write(
        '<td style="font-family:sans-serif;font-size:20px; color:#003399; text-align:left;"><b>India: State wise stats</b></td>')
    f_nums.write('</tr>')
    f_nums.write('<tr>')
    f_nums.write('<td style = "vertical-align:top;">')
    f_nums.write('<img src="covid-19map.png" width="600" height="400">')
    f_nums.write('</td>')
    resp = requests.get('https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST')
    resp_json = resp.json()
    df = pd.DataFrame(resp_json['regionData'])
    df.sort_values(by='totalInfected', ascending=False, inplace=True)
    f_nums.write('<td style = "vertical-align:top;">')
    f_nums.write(
        '<table style="border-collapse: collapse;border: 1px solid #dddddd;text-align: left;padding: 8px; width: 100%; ">')
    f_nums.write('<tr>')
    f_nums.write(
        '<th style="font-family:sans-serif;font-size:12px;padding-bottom:5px;padding-top:2px;padding-left:3px;"><b>State</b></th>')
    f_nums.write(
        '<th style="font-family:sans-serif;font-size:12px;padding-bottom:5px;padding-top:2px;color:red;"><b>Infected</b></th>')
    f_nums.write(
        '<th style="font-family:sans-serif;font-size:12px;padding-bottom:5px;padding-top:2px;color:green"><b>Recovered</b></th>')
    f_nums.write(
        '<th style="font-family:sans-serif;font-size:12px;padding-bottom:5px;padding-top:2px;padding-right:3px;"><b>Deceased</b></th>')
    f_nums.write('</tr>')
    cnt = 0
    for j in df.itertuples():
        cnt += 1
        if cnt % 2 == 0:
            bcg_color = '#dddddd'
        else:
            bcg_color = '#FDFEFE'
        i = j[0]
        f_nums.write(f'<tr style="background-color: {bcg_color}">')
        state = df.loc[i, 'region']
        tot_infected = df.loc[i, 'totalInfected']
        tot_recov = df.loc[i, 'recovered']
        tot_death = df.loc[i, 'deceased']
        f_nums.write(f'<td style="font-family:sans-serif;font-size:10px;padding-left:3px;">{state}</td>')
        f_nums.write(f'<td style="font-family:sans-serif;font-size:10px;">{tot_infected}</td>')
        f_nums.write(f'<td style="font-family:sans-serif;font-size:10px;">{tot_recov}</td>')
        f_nums.write(f'<td style="font-family:sans-serif;font-size:10px;">{tot_death}</td>')
        f_nums.write('</tr>')
    f_nums.write('</table>')
    f_nums.write('<tr><td style = "padding:10px;"></td></tr>')
    f_nums.write('<tr>')
    f_nums.write(
        '<td style="font-family:sans-serif;font-size:20px; color:#003399; text-align:left;"><b>India: Case wise counts</b></td>')
    f_nums.write('</tr>')
    f_nums.write('<tr>')
    f_nums.write('<td colspan=2 style = "vertical-align:top;">')
    f_nums.write('<img src="IndiaCovid-19Figures.jpg" width="900" height="400">')
    f_nums.write('</td>')
    f_nums.write('</tr>')
    f_nums.write('</table>')
    f_nums.close()
generate_pdf()
send_email()
print('Completed execution of Covid-19NewsMain.py')
