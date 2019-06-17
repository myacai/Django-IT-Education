import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
 
from lxml import etree
 
browser = webdriver.Chrome()
browser.get("https://www.baidu.com")
 
wait = WebDriverWait(browser,50)
def search():
	browser.get('https://www.jd.com/')
	try:
		input = wait.until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#key"))
		)#llist
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR,"#search > div > div.form > button"))
		)
		#input = browser.find_element_by_id('key')
		input[0].send_keys('python')
		submit.click()
 
		total = wait.until(
			EC.presence_of_all_elements_located(
				(By.CSS_SELECTOR,'#J_bottomPage > span.p-skip > em:nth-child(1) > b')
			)
		)
		html = browser.page_source
		prase_html(html)
		return total[0].text
	except TimeoutError:
		search()
 
def next_page(page_number):
	try:
		#�������ײ������س�����ʮ��������Ϣ
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(10)
        #��ҳ����
		button = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_bottomPage > span.p-num > a.pn-next > em'))
		)
		button.click()
		wait.until(
			EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#J_goodsList > ul > li:nth-child(60)"))
		)
	#�жϷ�ҳ�ɹ�
		wait.until(
			EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#J_bottomPage > span.p-num > a.curr"),str(page_number))
		)
		html = browser.page_source
		prase_html(html)
	except TimeoutError:
		return next_page(page_number)
 
def prase_html(html):
	html = etree.HTML(html)
	items = html.xpath('//li[@class="gl-item"]')
	for i in range(len(items)):
		if html.xpath('//div[@class="p-img"]//img')[i].get('data-lazy-img') != "done":
			print("img:", html.xpath('//div[@class="p-img"]//img')[i].get('data-lazy-img'))
		else :
			print("img:",html.xpath('//div[@class="p-img"]//img')[i].get('src'))
		print("title:", html.xpath('//div[@class="p-name"]//em')[i].xpath('string(.)'))
		print("price:",html.xpath('//div[@class="p-price"]//i')[i].text)
		print("commit", html.xpath('//div[@class="p-commit"]//a')[i].text)
		print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
def main():
    print("��",1,"ҳ��")
	total = int(search())
	for i in range(2,total+1):
		time.sleep(3)
		print("��",i,"ҳ��")
		next_page(i)
 
if __name__ == "__main__":
	main()
