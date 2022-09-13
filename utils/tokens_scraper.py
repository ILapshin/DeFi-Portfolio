from unicodedata import name
import requests
from bs4 import BeautifulSoup
import json
  

def get_adress_list(url):

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    r = requests.get(url, headers=headers)  
    soup = BeautifulSoup(r.content, 'html5lib') 
    tokens = soup.find_all('a', attrs = {'class':'text-primary'}) 
    
    result = {}

    for token in tokens:

        address = token['href'].split('/')[2]
        symbol = token.text.split('(')[-1][:-1]

        result[symbol] = address
    
    return result


def get_all_tokens(url_template, num_pages):

    result = {}

    for i in range(num_pages):
        url = url_template.format(num_page=i)
        result.update(get_adress_list(url))

    return result


def create_json(file_name, url_template, num_pages):

    all_tokens_dict = get_all_tokens(url_template, num_pages)
    json_object = json.dumps(all_tokens_dict)

    with open(f"{file_name}.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':

    polygon_url = 'https://polygonscan.com/tokens?p={num_page}'
    polygon_num_pages = 9

    bsc_url = 'https://bscscan.com/tokens?p={num_page}'
    bsc_num_pages = 9

    eth_url = 'https://etherscan.io/tokens?p={num_page}'
    eth_num_pages = 20

    create_json('eth_tokens', eth_url, 4)
    create_json('bsc_tokens', bsc_url, 4)
    create_json('polygon_tokens', polygon_url, 4)
