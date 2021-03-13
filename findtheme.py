import urllib.request
from bs4 import BeautifulSoup
from operator import eq
import re, time

def no_space(text):
	text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', text)
	text2 = re.sub('\n\n', '', text1)
	return text2

search_stock = input('종목명을 입력해주세요. 코스닥 종목은 한 칸을 띄우고 *를 넣어주세요. ex)"셀트리온헬스케어 *" : ')
time.sleep(3)
print('Please wait... Currently searching keyword you selected with naver theme menu...')
i = 1

while i <= 6:
    url = 'https://finance.naver.com/sise/theme.nhn?&page='
    url_naver_theme = url + str(i)
    html = urllib.request.urlopen(url_naver_theme).read()
    soup = BeautifulSoup(html, 'html.parser')
    
    theme_kind = soup.find('table', attrs = {'class':'type_1 theme'})
    theme_names = theme_kind.find_all('td', attrs = {'class':'col_type1'})

    for theme_name in theme_names:
        theme_list = [] #이 리스트형 변수에 리턴할 테마명과 주소가 있음 즉, 검색어와 일치한다면 이 theme_list를 리턴해주면됨 [1]
        return_theme_name = theme_name.get_text()
        related_stock_addresses = 'https://finance.naver.com/' + theme_name.a['href']

        html = urllib.request.urlopen(related_stock_addresses).read()
        soup = BeautifulSoup(html, 'html.parser') 

        stocks = soup.find_all('tr', attrs={'onmouseout':'mouseOut(this)'})
        theme_list.extend([return_theme_name, related_stock_addresses])
        stock_list = [] #이 리스트형 변수에 해당 테마의 종목들과 등락폭이 저장되 있음 즉, 검색어와 일치한다면 이 stock_list를 리턴해주면 됨[2]

        for stock in stocks:
            name = stock.find('div', attrs={'class':'name_area'}).get_text()
            
            # 테마 편입이유 일단 주석 (길어서)
            # reason = stock.find('p', attrs={'class':'info_txt'})
            # print(reason.get_text()) #테마편입이유

            rate = stock.find('span', attrs={'class':['tah p11 red01','tah p11', 'tah p11 nv01']}).get_text()
            rate = no_space(rate).strip() 
            stock_list.extend([name, rate])

           
        if any(search_stock in s for s in stock_list): #in 뒤는 변수이어야만 가능함 변수안에서 search_stock이란 값이 있냐 없냐 입력어가 정확해야함.
            print()
            print(search_stock + '의 테마와 관련주 아래를 참고하세요. 테마명, 네이버 링크로 나뉘어지며 관련테마로 엮인 종목들을 실시간으로 상승폭이 큰 순서대로 알려줍니다. 종목옆은 실시간 변동폭입니다.')
            print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            print(theme_list)
            print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            print(stock_list)
            print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print('6개 페이지 중 ' + str(i) +'번째 페이지 검색 완료')
    i = i + 1

print(search_stock + '의 네이버 테마메뉴에 대한 검색이 끝났습니다. ' + search_stock + '에 대한 결과가 없다면 네이버 테마에 해당 종목이 등록되어 있지 않거나 검색어가 부정확한 경우입니다.' )
