from selenium import webdriver
import time
import requests
import sys

try:
    chrome = webdriver.Chrome(sys.argv[1])
    chrome.get("https://www.medium.com")
    chrome.find_elements_by_xpath("//*[contains(text(), 'Sign in')]")[0].click()
    time.sleep(5)
    chrome.find_elements_by_xpath("//*[contains(text(), 'Sign in with Google')]")[0].click()
    time.sleep(5)
    chrome.find_elements_by_id('identifierId')[0].send_keys(sys.argv[2])
    chrome.find_elements_by_xpath("//*[contains(text(), 'Próxima')]")[0].click()
    time.sleep(5)
    chrome.find_element_by_name('password').send_keys(sys.argv[3])
    chrome.find_elements_by_xpath("//*[contains(text(), 'Próxima')]")[0].click()
    time.sleep(10)
    links = chrome.find_elements_by_css_selector(".ds-link")

    links = [link for link in links if len(link.get_attribute('href')) > 40]
    links = [link.get_attribute('href') for link in links]
    for link in list(set(links)):
        chrome.get(link)
        response_text = chrome.page_source.replace("/max/50", "/max/1080").replace("/max/30", "/max/1080").replace("Top highlight", "")

        content = response_text[response_text.find("<article"):response_text.find("</article>") + 10]
        if len(content) < 6000:
            continue
        author = content[content.find('<a ') + 3:]
        author = author[author.find('<a ') + 3:]
        author = author[author.find('>') + 1:]
        author = author[:author.find('<')]
        head = response_text[response_text.find("<head>") + 6:response_text.find("</head>")]
        title = response_text[response_text.find("<h1"):]
        title = title[title.find(">") + 1:title.find("</h1>")]
        description = response_text[response_text.find("<h2"):]
        description = description[description.find(">") + 1:description.find("</h2>")]
        image = response_text[response_text.find("<figure"):]
        image = image[image.find('<img') + 10:]
        image = image[image.find('<img'):]
        image = image[image.find('src="') + 5:]
        image = image[:image.find('"')]
        data = {
            'content': content + head,
            'title': title,
            'description': description,
            'image': image,
            'author': author,
            'url': link,
            'portal': 'Medium'
        }
        print(requests.post('https://newsletter-plus.herokuapp.com/api/news/', data=data).json())
finally:
    chrome.close()
