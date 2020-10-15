import requests
import csv
import os
import time
from bs4 import BeautifulSoup


def get_request(url):
    res = requests.get(url)
    return res


def get_soup(content):
    return BeautifulSoup(content, 'html5lib')


def write_csv(lines):
    with open(file=save_path, encoding='utf-8', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)


def main():
    count = 0
    while True:
        count = count + 1
        req_url = 'https://api.searchspring.net/api/search/search.json?siteId=96dulv&page={}'.format(count)
        response = get_request(req_url)
        if response.status_code == 400:
            break
        content = response.json()['results']
        soup = get_soup(content)
        links = soup.find_all(attrs={'class': 'item'})
        for link in links:
            url = 'https://www.tackledirect.com/' + link.find('a')['href']
            cont = get_request(url)
            soup = get_soup(cont.text)
            tables = soup.select('#tab1 table.order-specs-tb .model-code a')
            for table in tables:
                link = 'https://www.tackledirect.com/' + table['href']
                link_res = get_request(link)
                link_soup = get_soup(link_res.text)
                title = link_soup.find(attrs={'class': 'cyc-item-h1'}).text
                image = link_soup.find(attrs={'class': 'cyc-item-image-main'})['src']
                qty = link_soup.find(attrs={'name': 'vwquantity0'})['value']
                line = [title, image, qty]
                tds = link_soup.find(id='tab1').find(attrs={'class': 'order-specs-tb'}).find('tr').find_all('td')
                for td in tds:
                    td_value = td.text.strip()
                    line.append(td_value)
                description = link_soup.find(attrs={'itemprop': 'description'}).text.strip()
                line.append(description)
                print(line)
                write_csv([line])


def page():
    base_cont = get_request(url=base_url)
    base_soup = get_soup(base_cont.text)
    base_lists = base_soup.select('.wsmenu-list > li')
    for base_list in base_lists:
        category = base_list.find('a', attrs={'class': 'mainnav'}).text
        sub_categories = base_list.select('.megamenu ul > li > a')
        for sub_category in sub_categories:
            sub_cat = sub_category.text
            category_link = 'https://www.tackledirect.com/' + sub_category['href']
            category_res = get_request(category_link)
            category_soup = get_soup(category_res.content)
            cards = category_soup.select('.cycNxtBtnPrimary')
            if len(cards) > 0:
                print('ok, ', category_link)
            else:
                print('no, ', category_link)
    exit()

    urls = [
        'https://www.tackledirect.com/strike-king-kvd-1-5-deep-crankbait.html',
        'https://www.tackledirect.com/megabass-destroyer-usa-rods.html'
    ]


if __name__ == '__main__':
    save_path = 'result.csv'
    if not os.path.isfile(save_path):
        header = [['Title', 'Image', 'Qty', 'Model TD Code', 'Description on Order', 'Length', 'Weight', 'Depth', 'Hook Size', 'Color', 'Price', 'Description']]
        write_csv(header)
    base_url = 'https://www.tackledirect.com/'
    main()
