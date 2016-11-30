from selenium import webdriver
import io
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

import os

def handleGroupAssignment():
    wait("student.pl")
    entry = browser.find_elements_by_xpath("//*[starts-with(@id, 'modalTrigger')]")[groupnumber]
    title = entry.text
    print(title)
    entry.click()

    browser.get("javascript:document.getElementById('modalRestrictionsContinue').click();")

    wait("Assignment-Responses")
    assignmenthtml = browser.page_source
    with io.open("Webassign Data" + '/' + title + ".html", 'w+', encoding="utf-16") as saveFile:
        saveFile.write(assignmenthtml)
    browser.save_screenshot("Webassign Data" + '/' + title + ".png")
    browser.back()

def wait(urlfrag):
    while not urlfrag in browser.current_url:
        time.sleep(0.1) #prevent server buffer overflows and taking unnecessary polls

browser = webdriver.Firefox()
browser.get("https://webassign.net/login.html")
print("Please login to start the fetching process:")
browser.find_element_by_id("WebAssignUsername").send_keys(raw_input("Username:"))
browser.find_element_by_id("WebAssignInstitution").send_keys(raw_input("Institution:"))
browser.find_element_by_id("WebAssignPassword").send_keys(raw_input("Password:"))
browser.find_element_by_id("loginbtn").click()

wait("student.pl")
print("Starting collection of assignments...")
pastclick = browser.find_element_by_xpath("//*[@id=\"webAssign\"]/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/p/a")
WebElement.click(pastclick)
homehtml = browser.page_source

if not os.path.exists(r"Webassign Data"):
    os.makedirs(r"Webassign Data")
groupnumber = 0
for i in range(7, homehtml.count("row container")): #TODO change back after debug
    try:
        wait("student.pl")
        entry = browser.find_element_by_xpath("//*[@id=\"webAssign\"]/div[2]/div[3]/div[2]/div[" + str(i + 2) +"]/div[1]/p[1]/a")
        title = entry.text
        print(title)
        entry.click()
        wait("Assignment-Responses")
        assignmenthtml = browser.page_source
        with io.open("Webassign Data" + '/' + title + ".html", 'w+', encoding="utf-16") as saveFile:
            saveFile.write(assignmenthtml)
        browser.save_screenshot("Webassign Data" + '/' + title + ".png")
        browser.back()
    except NoSuchElementException:
        #print("Encountered group assignment: Please save it manually")
        handleGroupAssignment()
        groupnumber += 1
        continue