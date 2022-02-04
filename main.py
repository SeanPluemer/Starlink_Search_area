#the purpose of this program is to find locations for the starlink to work
import os
import time

import pandas as pd
import requests
import math

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import multiprocessing

#pd.set_option('mode.chained_assignment', None)

def main():

    csv_name = "San_diego.csv"
    resume_run = 0

    left_start_point = 33.904524


    right_start_point = -116.316315


    miles_wide = 15 #I actually think this is tall
    miles_high = 15 #this is wide


    calculated_wide = math.ceil(miles_wide)
    print(calculated_wide)
    calculated_high =  math.ceil(miles_high)

    print(calculated_high, calculated_wide)
   # print("this will take ", ((calculated_wide*calculated_high*10)/60), "min ")

    if(resume_run==0):
    #    left, right = calculate_gps_spots_square_corner(left_start_point,right_start_point, calculated_high, calculated_wide)
        left, right = calculate_gps_spots_square_center(left_start_point,right_start_point, calculated_high, calculated_wide)
        data_dict = convert_gps_to_point(left,right)
        df = pd.DataFrame(data_dict)
        #df["Avail"] = "Nada"
    else:
        test = pd.read_csv (csv_name,index_col=False)
        df = test[test['Avail'].str.contains('Nada')]
        print(df)

    #this needs to be sent a list of points to test

    #print(df.PlusPoint)

    df.to_csv(csv_name, encoding='utf-8', index=False)
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=30 )
    #print(df)
    hello_there = pool.map(par_test_points, df.PlusPoint)
    print(hello_there)
    df["Avail"]= hello_there
    print(df)

    df.to_csv(csv_name, encoding='utf-8', index=False)



def par_test_points(plus_point):
    try:
            print("testing point: ", plus_point)
            if (get_result(plus_point)):
                print("location is avalable!", plus_point)
                return(plus_point)
             #   df.at[i, "Avail"] = "Y"
           # else:
              #  df.at[i, "Avail"] = "N  "
    except Exception as e:
            print("error at point: ", plus_point)
            print(e)
    return "nope"
         #   df.at[i, "Avail"] = "FAILED"

        #df.to_csv(csv_name, encoding='utf-8', index=False)


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

def calculate_gps_spots_square_center(left, right, wide_radius, high_radius):

    left_points,right_points = [left], [right]

    n = 0.012*8 #.333 is ~27 miles
    #n is the accuracy, a higher number is futher apart points
    up = left
    down = left

    for i in range((high_radius//2)-1): #this is actually width

        up = up + n
        down = down - n
        left_points.append(up) #this is going up
        left_points.append(down)

    right_dir = right
    left_dir = right
    j = 0.025*8
    # j is the accuracy, a higher number is futher apart points
    for i in range((wide_radius // 2) - 1): #this is actually height
        right_dir = right_dir + j
        left_dir = left_dir - j
        right_points.append(right_dir)  # this is going up
        right_points.append(left_dir)

    return left_points, right_points


def calculate_gps_spots_square_corner(left, right, number_of_left_points, number_of_right_points):

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




def get_result(location):
    link = "https://www.starlink.com/"

    chrome_options = webdriver.ChromeOptions();
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(executable_path=r"/Users/seanpluemer/Documents/GitHub/Starlink_Search_area/chromedriver",
                               options=chrome_options);

    browser.get(link)
    input_search = browser.find_element_by_id("service-input")
    input_search.send_keys(location)
    time.sleep(3)

    # location that works!
    # 859CF6GG+7PM
    try:
        #results_search = browser.find_element_by_xpath( '/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-landing/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/div[2]/div/a')
        results_search = browser.find_element_by_xpath( '//*[@id="feature"]/div[2]/div/div[2]/form/div[1]/div[2]/div/a')
        results_search.click()
        time.sleep(1)

        button_search = browser.find_element_by_xpath('/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-landing/div[2]/div[1]/div[2]/div/div[2]/form/div[2]/button')
        button_search.click()
        time.sleep(10)
        text_results = '/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-order/div[1]/div/div[2]/div/div[4]'

        try:
            #search_result = browser.find_element_by_xpath( '/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-preorder/div[1]/div/div[2]/div/div[4]')
            search_result = browser.find_element_by_xpath( '/html/body/app-root/public-header-navigation/div/mat-drawer-container/mat-drawer-content/div/app-order/div[1]/div/div[2]/div/div[4]')
            print('I AM RIGHT HERE', location)
            browser.close()
            return 1
        except Exception as e:
           # print('I AM RIGHT HERE', location)
            browser.close()
            return 0
            #print("available")
    except Exception as e:
        print("something went wrong at point:",location,  e)
        browser.close()
        return 0

if __name__ == "__main__":
    main()

