#the purpose of this program is to find locations for the starlink to work
import os
import time

import pandas as pd
import requests
import csv
import math

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#browser = webdriver.Chrome('/Users/seanpluemer/Documents/GitHub/Starlink_Search_area/chromedriver')
#safari_browser = webdriver.Safari()


def main():

    link = "https://www.starlink.com/"
    #location = "859CF6GG+7PM"

    left_start_point = 37.001470
    right_start_point = -114.049698

    miles_wide = 100
    miles_high = 50

    calculated_wide = math.ceil(miles_wide / 25)
    calculated_high =  math.ceil(miles_high / 27)

    print(calculated_high, calculated_wide)

    print("this will take ", ((calculated_wide*calculated_high*10)/60), "min ")

    left, right = calculate_gps_spots(left_start_point,right_start_point, calculated_high, calculated_wide)
    data_dict = convert_gps_to_point(left,right)

    data_dict["Avail"] =[]


    print(data_dict)

    print(len(data_dict.get('PlusPoint')))
    plus_point = data_dict.get('PlusPoint')
    for i in range(len(plus_point)):
        location = plus_point[i]
        if (get_result(link,location)):
            print(location)
            print("location is avalable!")
            data_dict["Avail"].append("Y")
        else:
            #print("location not avalable")
            data_dict["Avail"].append("N")

    df =  pd.DataFrame(data_dict)
    df.to_csv("test.csv", encoding='utf-8')


def convert_gps_to_point(left,right):
    data_dict = {"GPS":[] , "PlusPoint":[]}
    for i in range(len(left)):
        print(i)
        for j in range (len(right)):
            test = str(left[i])+ "," + str(right[j])

            link = "https://plus.codes/api?address="+test
            response = (requests.get(link))
            dict_data = response.text
            if "global_code" in dict_data:
                point = dict_data[39:50]
                data_dict["GPS"].append(test)
                data_dict["PlusPoint"].append(point)
    return data_dict


def calculate_gps_spots(left, right, number_of_left_points, number_of_right_points):

    left_points,right_points = [left], [right]

    n = 0.333
    for i in range(number_of_left_points-1):

        left = left + n
        left_points.append(left) #this is going up

    j = 0.5
    for i in range(number_of_right_points-1):
        right = right+j
        right_points.append(right) #this is going to the right,

    return left_points, right_points




def get_result(link, location):
    chrome_options = webdriver.ChromeOptions();
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(executable_path=r"/Users/seanpluemer/Documents/GitHub/Starlink_Search_area/chromedriver",
                               options=chrome_options);

    browser.get(link)
    input_search = browser.find_element_by_id("service-input")
    input_search.send_keys(location)
    time.sleep(1)

    # location that works!
    # 859CF6GG+7PM

    results_search = browser.find_element_by_xpath(
        '/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-landing/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/div[2]/div/a')
    results_search.click()
    time.sleep(1)

    button_search = browser.find_element_by_xpath(
        '/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-landing/div[2]/div[1]/div[2]/div/div[2]/form/div[2]/button')
    button_search.click()
    time.sleep(5)
    text_results = '/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-order/div[1]/div/div[2]/div/div[4]'

    try:
        search_result = browser.find_element_by_xpath(
            '/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-preorder/div[1]/div/div[2]/div/div[4]')
        #print(search_result.text)
        return 0
    except:
        return 1
        #print("available")


if __name__ == "__main__":
    main()

