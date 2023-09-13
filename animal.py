import bs4, requests
import telegram
import asyncio
from selenium import webdriver
from datetime import timedelta, date
import time
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
warnings.filterwarnings('ignore')
        
        
class findmansoonbot():
    def __init__(self):
        #telegram 세팅
        self.message=True #True시 슬랙 전송, Fasle시 터미널 출력
        self.token='***'
        self.cid=***
        # self.cri_ymd=str(date.today()-timedelta(days=2))
        self.cri_ymd="2023-09-11"#테스트용 고정 날짜
        self.driverpath="/Users/yihoon-j/Documents/find_mansoon/chromedriver"
        
    def __main__(self):
        self.count=self.get_count()
        if self.count==0:
            asyncio.run(self.t_tx(tx=f"{self.cri_ymd} 기준 등록된 암컷 개 없음. 출력을 종료합니다."))
        else:
            cc=self.count
            asyncio.run(self.t_tx(tx=f"{self.cri_ymd} 총 {cc}건 조회됨")) #조회건수 메시지 전송
            self.final_message(urls=self.parse_info(), count=cc)
    
    #텔레그램 비동기 세팅
    async def t_ph(self, ph, m=False):
        m=self.message
        bot=telegram.Bot(token=self.token)
        if m==True:
            try:
                await bot.send_photo(chat_id=self.cid, photo=ph)
            except:
                await bot.send_message(chat_id=self.cid, text=f"이미지 로드 실패: {ph}")
        else:
            print('MSG:', ph)
    async def t_tx(self, tx, m=False):
        m=self.message
        bot=telegram.Bot(token=self.token)
        if m==True:
            await bot.send_message(chat_id=self.cid, text=tx)
        else:
            print('MSG:', tx)
                                
    #어제 암컷 개 등록 건수 리턴
    def get_count(self):
        url="https://www.animal.go.kr/front/awtis/protection/protectionList.do?csSignature=OawIKLjhdQUE3f9w1%2FQc1Q%3D%3D&boardId=&page=1&pageSize=10&desertionNo=&menuNo=1000000060&searchSDate="+self.cri_ymd+"&searchEDate="+self.cri_ymd+"&searchUprCd=&searchOrgCd=&searchCareRegNo=&searchUpKindCd=417000&searchKindCd=&searchSexCd=F&searchRfid=&&page=1"
        source=requests.get(url)
        soup = bs4.BeautifulSoup(source.content, 'html.parser')
        del source
        try:
            count=int(soup.select('#searchList > div.boardList > ul:nth-child(1) > li')[0].text.replace("총 ","").replace(" 건",""))
        except:
            count=0
        return count

    #각 건별 url 정보 수집
    #상세 url이 javascript개체인 관계로 selenium 사용
    def parse_info(self):
        count_page=(self.count//10)+1 #55마리가 조회될 경우 6페이지까지 존재
        urllist=[]
        for i in range(count_page): #페이지 단위 반복
            url="https://www.animal.go.kr/front/awtis/protection/protectionList.do?csSignature=OawIKLjhdQUE3f9w1%2FQc1Q%3D%3D&boardId=&page=1&pageSize=10&desertionNo=&menuNo=1000000060&searchSDate="+self.cri_ymd+"&searchEDate="+self.cri_ymd+"&searchUprCd=&searchOrgCd=&searchCareRegNo=&searchUpKindCd=417000&searchKindCd=&searchSexCd=F&searchRfid=&&page=1"
            driver=webdriver.Chrome(self.driverpath)
            driver.get(url)
            btnchk=True
            num=1
            while btnchk:  
                try:
                    detailbtn='//*[@id="searchList"]/div[4]/ul[2]/li['+str(num)+']/div[1]/a'
                    driver.find_element('xpath',detailbtn).click()
                    time.sleep(1)
                    urllist.append(driver.current_url)
                    driver.find_element('xpath','//*[@id="sub_con"]/div[2]/a/img').click() #목록으로 돌아오기
                    num+=1
                    time.sleep(1)
                except:
                    btnchk=False
        return urllist #개별 상세 url정보 
   
    #각 페이지 내에서 세부 정보 및 이미지 반환
    def parse_detail(self, page):
        source=requests.get(page)
        soup = bs4.BeautifulSoup(source.content, 'html.parser')
        del source
        pic_url="https://www.animal.go.kr"+soup.find_all('img')[0]['src']
        mng_nm=soup.find_all('form')[3].find_all('td')[0].text.lstrip().rstrip() #관리번호
        reg_nm=soup.find_all('form')[3].find_all('td')[1].text.lstrip().rstrip() #등록번호
        type=soup.find_all('form')[3].find_all('td')[2].text.lstrip().rstrip() #품종
        color=soup.find_all('form')[3].find_all('td')[3].text.lstrip().rstrip() #색상
        sex=soup.find_all('form')[3].find_all('td')[4].text.lstrip().rstrip() #성별
        neut=soup.find_all('form')[3].find_all('td')[5].text.lstrip().rstrip() #중성화 여부
        agewgt=soup.find_all('form')[3].find_all('td')[6].text.lstrip().rstrip().replace(' ','').replace("\r\n","").replace('\xa0','') #나이,체중
        feat=soup.find_all('form')[3].find_all('td')[7].text.lstrip().rstrip() #특징
        place=soup.find_all('form')[3].find_all('td')[8].text.lstrip().rstrip() #발견장소
        date=soup.find_all('form')[3].find_all('td')[9].text.lstrip().rstrip() #접수일시
        other=soup.find_all('form')[3].find_all('td')[10].text.lstrip().rstrip() #기타사항
        admin=soup.find_all('form')[3].find_all('td')[11].text.lstrip().rstrip().replace('\r\n','').replace(' ','') #관할기관
        stat=soup.find_all('form')[3].find_all('td')[12].text.lstrip().rstrip() #상태
        center=soup.find_all('form')[3].find_all('td')[13].text.lstrip().rstrip() #보호센터
        contact=soup.find_all('form')[3].find_all('td')[14].text.lstrip().rstrip()
        location=soup.find_all('form')[3].find_all('td')[15].text.lstrip().rstrip().replace('\xa0','')
        full_text=f"관리번호: {mng_nm}\n등록번호: {reg_nm}\n품종: {type}\n색상: {color}\n성별: {sex}\n중성화: {neut}\n연령/무게: {agewgt}\n특징: {feat}\n발견장소: {place}\n접수일시: {date}\n기타사항: {other}관할기관: {admin}\n상태: {stat}\n보호센터: {center}\n연락처: {contact}\nurl: {page}" 
        return pic_url, full_text
    
    #세부 페이지별로 정보 받아서 메시지 전송
    def final_message(self, urls, count):
        if count!=len(urls):
            asyncio.run(self.t_tx(tx='조회건수 안맞음... 만든놈한테 연락바람'))
        else:
            for i in range(len(urls)):
                picture,info=self.parse_detail(page=urls[i])
                asyncio.run(self.t_ph(ph=picture))
                asyncio.run(self.t_tx(tx=f"{i+1}/{count}\n{info}"))
            asyncio.run(self.t_tx("출력을 종료합니다."))
            
        
        
task=findmansoonbot()
task.__main__() 
        
        
        
#각 동물 정보
# all_list=soup.select('#searchList > div.boardList > ul:nth-child(2)')[0].text.\
#     replace("\n\n\n\n","").replace("\n\n","\n").replace('공고번호','공고번호: ').\
#     replace('접수일자','접수일자: ').replace('품종','품종: ').replace('상태','상태: ').\
#     replace('성별', '성별: ').replace('발견장소','발견장소: ').replace('특징','특징: ').\
#     replace('기타사항', '기타사항: ').replace('등록번호','등록번호: ').\
#     split(sep="자세히 보기\n\n")[1:]


# #각 동물 사진
# front_url="https://www.animal.go.kr"
# p=soup.find_all('div', {'class':'thumbnail'})
# urllist=[]
# for i in range(len(p)):
#     # urllist.append(front_url+str(p[i].find('img')['src']))#저용량 이미지
#     urllist.append(front_url+str(p[i].find('a')['href']))#고해상도 이미지




#메시지 전송하는 부분    
# if len(all_list)!=len(urllist):
#     asyncio.run(t_tx(tx=f"페이지 내 조회된 사진 개수와 동물 정보 개수가 맞지 않음. 수동 확인 요망\nurl"))
# else:
#     # for i in range(len(all_list)):
#     for i in range(3):
#         asyncio.run(t_ph(ph=urllist[i]))
#         asyncio.run(t_tx(tx=all_list[i]))

