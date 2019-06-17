from selenium import webdriver
import time
import mysqlDb
from selenium.webdriver.chrome.options import Options

def get_Jingdong(url, page):
    try:
        print("启动浏览器 " + str((page+1)/2) + "页")
        webdriverUrl = r'C:\Users\Administrator\Desktop\jidong\chromedriver.exe'  
        chrome_options=Options()    
        chrome_options.add_argument('--headless')
        #,chrome_options=chrome_options
        driver = webdriver.Chrome(webdriverUrl,chrome_options=chrome_options)
        driver.get(url)
        #print(driver.page_source)
        prices_list = driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[2]/strong/i')
        commentNums_list = driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[4]/strong')
        productName_list = driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[3]/a/em')
        shopName_list = driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[5]/span/a')
        productId_lists = driver.find_elements_by_xpath('//li[@data-sku]')

        image_lists = driver.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[1]/a/img')
        #print(image_lists[0].get_attribute('src'))

        #print(type(image_lists))
        productId_list = [item.get_attribute('data-sku') for item in productId_lists]
        links = ['https://item.jd.com/{productId}.html'.format(productId=item) for item in productId_list]
        #for prices,commentNums,productName,shopName,productId in (prices_list,commentNums_list,productName_list,shopName_list,productId_list):
        #    mysqlDb.into_mysql(prices,commentNums,productName,shopName,productId)

        temp = 0
        for prices in prices_list:
            #print(prices.text,commentNums_list[temp].text,
            #                   productName_list[temp].text,shopName_list[temp].text,
            #                   productId_list[temp],links[temp])
            print(image_lists[temp].get_attribute('src'))
            mysqlDb.into_mysql(prices.text,commentNums_list[temp].text,
                               productName_list[temp].text,shopName_list[temp].text,
                               productId_list[temp],links[temp],image_lists[temp].get_attribute('src'))
            temp += 1

    except Exception as e:
        print(e)
    finally:
        driver.close()  

if __name__ == '__main__':
    keyword = "手机"
	#设置爬取页面
    page = 30
    page = page * 2
    print("开始爬取京东")
    base_url = 'https://search.jd.com/Search?keyword={key}&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq={key}&page={page}&click=0'
    for i in range(1, page, 2):
        url = base_url.format(key=keyword,page=i);
        get_Jingdong(url, i)
        time.sleep(5)