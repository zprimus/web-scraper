from selenium import webdriver
print('Enter url:')
url = input()

browser = webdriver.Firefox()
browser.get(url)

print('Enter css selector:')
css_selector = input()
print(browser.find_element_by_css_selector(css_selector))