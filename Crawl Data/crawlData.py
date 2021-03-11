from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


f = open("anime.csv", "w",  encoding="utf-8")
headers = "title#episode#image_src#views#cmt#categorys#series#season#year#description \n"
f.write(headers)
for i in range(122):
    url = 'https://anime47.com/tim-nang-cao/?status=&season=&year=&sort=popular&page='+i
    req = ureq.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = ureq.urlopen(req)
    page_soup = soup(page.read(), 'html.parser')

    containers = page_soup.findAll(
        'ul', {'class': 'last-film-box'})[0].findAll('li')

    for con in containers:
        try:
            herf = con.a['href'][1:]
#         print(herf)
            image_src = con.a.div.div.div['style'].split("'")[1]
#         print(image_src)
            title = con.findAll('div', {'class': 'movie-title-1'})[0].text
#         print(title)
            episode = con.findAll('span')[2].text
#         print(episode)
            views = con.findAll('span')[1].text
#         print(views)
            cmt = con.findAll('span')[0].text
#         print(cmt)
            url = "https://anime47.com" + herf
#         print(url)

            req_detail = ureq.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            page_detail = ureq.urlopen(req_detail)
            page_detail_soup = soup(page_detail.read(), 'html.parser')

            container_detail = page_detail_soup.findAll(
            'dl', {'class': 'movie-dl'})
            categorys = container_detail[0].findAll('dd')[1].findAll('a')
            categorys_list = []
            for c in categorys:
                categorys_list.append(c.text.strip())
            categorys = "|".join(categorys_list)
#         print(categorys)

            series = container_detail[0].findAll('dd')[2].a.text
#         print(series)
            season = container_detail[0].findAll('dd')[3].a.text
#         print(season)
            year = container_detail[0].findAll('dd')[4].a.text
#         print(year)
            content = page_detail_soup.findAll('div', {'class': 'news-article'})
            description = content[0].findAll('p')[0].text
#         print(description)
            print("------------------------------")
            line = title+"#" + episode+"#" + image_src+"#"+views+"#"+cmt+"#" + \
                categorys+"#"+series+"#"+season+"#"+year+"#"+description+" \n"
            print(line)
            f.write(line)
        except:
            continue
f.close()
