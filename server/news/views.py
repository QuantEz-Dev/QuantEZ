from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def index(request):
    sise_data = top3(request)
    organ_data = top7(request)
    top10_data = top10(request)  # top10 data1, data2를 하나의 리스트로

    # index로 각자 접근
    data1 = top10_data[0]
    data2 = top10_data[1]

    comps = pop(request)
    context = kospitop50(request)

    plus = {
        'sise_data': sise_data,
        'organ_data': organ_data,
        'data1': data1,
        'data2': data2,
        'comps': comps,
        'context': context,
    }
    return Response(plus)

def top3(request):
    urls = 'https://finance.naver.com/main/main.nhn'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    res = requests.get(urls, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    sise1 = list()
    sise2 = list()

    sise_title = soup.select('#content > div.article > div.section2 > div.section_top.section_top_first > ul > li > p.item > a > strong')
    sise_diff = soup.select('#content > div.article > div.section2 > div.section_top.section_top_first > ul > li > p.item > em')

    for s1 in sise_title:
        sise1.append(s1.text.strip())

    for i in range(len(sise1)):
        title = sise_title[i].text.strip()
        diff = sise_diff[i].text.strip()

        sise_obj = {
            'title': title,
            'diff': diff,
        }
        sise2.append(sise_obj)
    sise_data = sise2

    return sise_data

def top7(request):
    url = 'https://finance.naver.com/sise/sise_deal_rank.nhn'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    organ_name = soup.find_all('a', class_='company')
    organ_price = soup.find_all('td', class_='number')

    organ1 = list()
    total_organ = list()

    for o in organ_name[0:7]:
        organ1.append(o.text.strip())

    for o2 in range(len(organ1)):
        title = organ_name[o2].text.strip()
        price = organ_price[o2].text.strip()

        organ_obj = {
            'title': title,
            'price': price,
        }
        total_organ.append(organ_obj)
    organ_data = total_organ

    return organ_data

def top10(request):
    url = "http://finance.naver.com/sise/"
    res = requests.get(url).text
    soup = BeautifulSoup(res, "html.parser")

    top101 = soup.select("#popularItemList > li > a")
    top102 = soup.select("#popularItemList > li")

    top10list1 = list()
    top10list2 = list()

    top101list = list()
    top102list = list()

    for top11 in top101:
        top10list1.append(top11.text.strip())

    for top22 in top102:
        top10list2.append(top22.text.strip())

    top10_data = []

    for i in range(len(top10list1)):
        toptext1 = top101[i].text.strip()
        item_objs = {
            'toptext1': toptext1,
        }
        top101list.append(item_objs)

    top10_data.append(top101list)

    for i in range(len(top10list2)):
        toptext2 = top102[i].text.strip()
        item_objs = {
            'toptext2': toptext2,
        }
        top102list.append(item_objs)

    top10_data.append(top102list)

    return top10_data

def pop(request):
    urls = 'https://finance.naver.com/'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    res = requests.get(urls, headers=headers)
    soups = BeautifulSoup(res.text, 'html.parser')

    top = soups.select(
        "#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr > th")

    toplist = list()
    top2 = list()

    for tops in top:
        toplist.append(tops.text.strip())

    for i in range(len(toplist)):
        comp = top[i].text.strip()

        item_objs = {
            'comp': comp,
        }
        top2.append(item_objs)

    comps = top2
    return comps

def kospitop50(request):
    res = requests.get('https://finance.naver.com/sise/sise_market_sum.naver')
    soup = BeautifulSoup(res.content, 'html.parser')
    context = []
    section = soup.find('tbody')
    items = section.find_all('tr', onmouseover="mouseOver(this)")
    for item in items:
        basic_info = item.get_text()
        sinfo = basic_info.split("\n")
        context.append(sinfo[1] + " " + sinfo[2] + " " + sinfo[3])
    return context
