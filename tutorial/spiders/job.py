import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from time import sleep



class JobSpider(scrapy.Spider):
    name = 'job'
    start_urls = ["https://www.gelbeseiten.de/Suche/zahntechniker/Bundesweit"]
    

    def remove_characters(self, value):
        new_value = value.strip("\xa0")
        print("Yes",value)
        return value.strip("\xa0")
    
    def __init__(self):
        self.chrome = webdriver.Chrome(
            executable_path="./chromedriver")
        self.chrome.get("https://www.gelbeseiten.de/Suche/Baggerbetrieb/Bundesweit")
        self.flag = True

        while True:
            try:
                input = self.chrome.find_element_by_xpath("//a[@title='Mehr Anzeigen']")
                input.click()
                # self.chrome.execute_script("window.stop();")
            except:
                if self.flag:
                    sleep(120)
                    self.flag = False
                    pass
                else:
                    sleep(10)
                    break           
            sleep(20)            
        
        self.html = self.chrome.page_source
        

    def parse(self, response):
        print("yes")
        resp = Selector(text=self.html)
        row = resp.xpath("//article[@class='mod mod-Treffer']")
        for i in row:
            firstname = i.xpath(".//h2[@data-wipe-name='Titel']/text()").get()
            rightname = i.xpath("//p[@class='mod-hervorhebung--partnerHervorhebung']/text()").get()
            first_location = i.xpath("normalize-space(.//p[@class='d-inline-block mod-Treffer--besteBranche']/text())").get()
            second_location = i.xpath("normalize-space(.//p[@data-wipe-name='Adresse']/text())").get()
            third_location = i.xpath("normalize-space(.//p[@data-wipe-name='Adresse']/span/text())").get()
            phone = i.xpath(".//p[@class='mod-AdresseKompakt__phoneNumber']/text()").get()
            link = i.xpath(".//a[@class='contains-icon-homepage gs-btn']/@href").get()
            yield{
                'firstname': firstname,
                'rightname': rightname,
                'first_location': first_location,
                'second_location': second_location,
                'third_location': third_location,
                'phone': phone,
                'link': link,               
            }
        


# //*[@id="gs_treffer"]/div/article row
# //*[@id="gs_treffer"]/div/article/a/h2 firstname
# //*[@id="gs_treffer"]/div/article/a/div/p right name
# //*[@id="gs_treffer"]/div/article/a/p/text() location 1
# //*[@id="gs_treffer"]/div/article/a/address/p[1]/text() location 2
# //*[@id="gs_treffer"]/div/article/a/address/p[2] phone
# //*[@id="gs_treffer"]/div/article/div/div/div/a[1]/@href website link
