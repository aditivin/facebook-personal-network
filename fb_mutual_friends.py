# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from BeautifulSoup import BeautifulSoup
from selenium.common.exceptions import TimeoutException
import re


#Open the ChromeDriver
driver = webdriver.Chrome('/Users/aditi/Downloads/chromedriver')
driver.implicitly_wait(15)  # seconds
# Facebook account user and password
usr = "******@gmail.com"
pwd = "*****"

def main():
    # Login to Facebook
    driver.get("http://www.facebook.org")
    elem = driver.find_element_by_id("email")
    elem.send_keys(usr)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)

    # Get the list of Facebook friends
    friend_links = get_friend_list()
    # Go through each friend's mutual friends, and add them to the list. This can take ages, depending on internet speed
    get_friend_network()
    # Make sure there are only mutual friends in the list and remove duplicates
    clean_up(friend_links)
    print "ALL DONE!"

def get_friend_list():
    friend_links = []
    links = []
    html_page = open("fb_friends_complete.htm").read()

    '''
    driver.get("https://www.facebook.com/aditivin/friends?source_ref=pb_friends_tl")
    driver.implicitly_wait(15)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            driver.find_element_by_id("pagelet_timeline_medley_photos")
            break
        except:
            continue
    html_page = driver.page_source
    print "Page is ready!"
    '''
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a'):
        links.append(link.get('href'))

    for link in links:
        if re.search(r'(\?fref|\&fref|hc_local)', str(link)):
            friend_links.append(link)

    friend_links = list(set(friend_links))

    fileW = open("fb_friend_out.csv", "w")

    for link in friend_links:
        fileW.write(usr + "," + str(link) + "\n")

    fileW2 = open("fb_friend_mutual.csv", "w")
    for link in friend_links:
        link = str(link)
        link = link.replace("?fref=pb&hc_location=friends_tab", "/friends_mutual")
        link = link.replace("&fref=pb&hc_location=friends_tab",
                            "&sk=friends&collection_token=100005147223403%3A2356318349%3A3")
        fileW2.write(link + "\n")

    return friend_links


def get_friend_network():
    mutual_friends = open("fb_friend_mutual.csv", "r").readlines()
    start_from = 0
    count = start_from

    fileW3 = open("fb_friend_mutual_links.csv", "a")

    for friend in mutual_friends[start_from:]:
        links = []
        friend_links = []
        print count
        print friend
        count += 1
        try:
            driver.get(friend)
            driver.implicitly_wait(15)
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                try:
                    driver.find_element_by_id("pagelet_timeline_medley_photos")
                    break
                except:
                    continue
            html_page = driver.page_source
            print "Page is ready!"
            soup = BeautifulSoup(html_page)
            for link in soup.findAll('a'):
                links.append(link.get('href'))

            for link in links:
                try:
                    if re.search(r'(\?fref|\&fref|hc_local)', str(link)):
                        friend_links.append(link)
                except:
                    if re.search(r'(\?fref|\&fref|hc_local)', u' '.join((link)).encode('utf-8')):
                        friend_links.append(link)

            friend_links = list(set(friend_links))

            for link in friend_links:
                link = str(link)
                link = link.replace("?fref=pb&hc_location=friends_tab", "")
                link = link.replace("&fref=pb&hc_location=friends_tab", "")
                friend = friend.replace("/friends_mutual", "")
                friend = friend.replace("&sk=friends&collection_token=100005147223403%3A2356318349%3A3", "")
                fileW3.write(friend.strip() + "," + link + "\n")

        except TimeoutException:
            print "Loading took too much time!"

def clean_up(friend_links):
    mutual_friends = open("fb_friend_mutual_links.csv", "r").readlines()
    mutual_friends_cleaned = []
    friend = []

    for i in range(0, len(friend_links)):
        mutual_friends_cleaned.append(mutual_friends[i])
        friend.append(mutual_friends[i].split(',')[1].strip())

    for i in range(len(friend_links) + 1, len(mutual_friends)):
        mf = mutual_friends[i].split(',')[1].strip()
        if mf in friend:
            mutual_friends_cleaned.append(mutual_friends[i])

    mutual_friends_cleaned = list(set(mutual_friends_cleaned))

    fileW = open("fb_friend_mutual_links.csv", "w")

    for mf_cleaned in mutual_friends_cleaned:
        fileW.write(mf_cleaned)


if __name__ == '__main__':
    main()
