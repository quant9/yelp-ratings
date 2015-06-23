
import requests
from lxml import etree
import sys, json


URL_FORMAT = '{}/ratings_histogram/'

def get_root_from_url(biz_string):
    url = URL_FORMAT.format(biz_string)
    res = requests.get(url)
    data = json.loads(res.text)['body']
    parser = etree.HTMLParser()
    root = etree.fromstring(data, parser)
    return root

def get_ratings_from_root(root):
    five_star = int(root.xpath('//td[@class="histogram_count"][1]/text()')[0])
    four_star = int(root.xpath('//td[@class="histogram_count"][2]/text()')[0])
    three_star = int(root.xpath('//td[@class="histogram_count"][3]/text()')[0])
    two_star = int(root.xpath('//td[@class="histogram_count"][4]/text()')[0])
    one_star = int(root.xpath('//td[@class="histogram_count"][5]/text()')[0])

    return {
        5: five_star,
        4: four_star,
        3: three_star,
        2: two_star,
        1: one_star,
    }

def get_avg_and_stddev(ratings_dict):
    avg_list = [key * ratings_dict[key] for key in ratings_dict.keys()]
    ratings_no = [ratings_dict[key] for key in ratings_dict.keys()]
    avg = reduce(lambda x, y: x + y, avg_list) / float(sum(ratings_no))
    deviations = [number * ((rating - avg) ** 2) for rating, number in ratings_dict.items()]
    sigma2 = float(sum(deviations)) / float(sum(ratings_no))
    return {
        'mu': avg,
        'sigma2': sigma2,
        'sigma': sigma2 ** (0.5),
    }
