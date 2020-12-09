# David Tan Sang Tran (davidtt2)
# CS 410 Course Project Fall 2020
# Python Data Retrieval

import json
import os
import pandas
import unicodedata
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def get_list_of_companies():
    url = "https://en.wikipedia.org/wiki/List_of_largest_technology_companies_by_revenue"
    read_from = pandas.read_html(url)
    companies_df = read_from[1] # index 1 = newest company ranking
    comp_col = companies_df.columns[2] # index 3 = list of companies
    companies = companies_df[comp_col].tolist()
    companies.sort()
    return companies

def get_companies_info(company_list): 
    #driver = webdriver.Edge("msedgedriver.exe")
    driver = webdriver.Chrome("chromedriver.exe")

    company_info = {} # dictionary
    for company in company_list:
        if company == "Samsung Electronics":
            company = "Samsung"
        company_info[company] = {} # dictionary of each company info
        driver.get("https://www.wikipedia.org/")
        search_id = "searchInput"
        search = driver.find_element_by_id(search_id)
        search.send_keys(company + " " + "company")
        search.send_keys(Keys.RETURN)
        if ("search" in driver.current_url): # stuck in search results
            if company == "HP":
                first_link_x_path = "/html/body/div[3]/div[3]/div[4]/div[3]/ul/li[2]/div[1]/a"
            else:
                first_link_x_path = "/html/body/div[3]/div[3]/div[4]/div[3]/ul/li[1]/div[1]/a"
            first_link = driver.find_element_by_xpath(first_link_x_path)
            first_link.click()
            print(company, "had to click URL from search results.")
        else:
            print(company, "went direct to page.")
        #print(driver.current_url) # current driver url

        useful_info = {}
        driver.implicitly_wait(3)
        print(driver.current_url)
        try:
            logo_x_path = "/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[1]/td/a/img"
            logo_link = driver.find_element_by_xpath(logo_x_path)
        except NoSuchElementException:
            logo_x_path = "/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[1]/td/a/img"
            logo_link = driver.find_element_by_xpath(logo_x_path)
        useful_info["Logo"] = logo_link.get_attribute("src") # url of company logo
        page_info = pandas.read_html(driver.current_url)
        info = pandas.read_html(driver.current_url)[0]
        try:
            if ("This article does not follow Wikipedia's guidelines" in info.iloc[0][1]):
                info = pandas.read_html(driver.current_url)[1]
            elif ("This article needs to be updated" in info.iloc[0][1]):
                info = pandas.read_html(driver.current_url)[1]
        except TypeError:
            pass
        #print(info) # dataframe of info

        for row in info.itertuples(index=False):
            temp_dict = row._asdict()
            corres_data = temp_dict["_1"]
            if (temp_dict["_0"] == "Founded"): # Founded Date
                corres_data = corres_data.split(";")[0].strip()
                useful_info[temp_dict["_0"]] = unicodedata.normalize("NFKD", corres_data)
            elif (temp_dict["_0"] == "Founders") or (temp_dict["_0"] == "Founder"): # Founders Names
                new_str = ""
                current_idx = 0
                if company == "Facebook":
                    span = 2
                    words = corres_data.split(" ")
                    new_str_l = [" ".join(words[i:i+span]) for i in range(0, len(words), span)]
                    for i in range(len(new_str_l)):
                        if i != (len(new_str_l)-1):
                            new_str += new_str_l[i] + ", ";
                    useful_info[temp_dict["_0"]] = new_str[:-2]
                else:
                    for idx in range(len(corres_data)):
                        if (idx > 0) and (corres_data[idx].isupper() == True):
                            if (corres_data[idx - 1] != " ") and (corres_data[idx - 1] != "."):
                                new_str += corres_data[current_idx:idx]
                                current_idx = idx
                                if (idx != len(corres_data)-1):
                                    new_str += ", "
                        if (idx == len(corres_data)-1):
                            new_str += corres_data[current_idx::]
                    new_str = new_str.replace("ō", "o")
                    new_str = new_str.split("(")[0].strip()
                    useful_info[temp_dict["_0"]] = new_str
            elif (temp_dict["_0"] == "Headquarters"): # Headquarters Location
                if "°" in corres_data:
                    corres_data = corres_data.split("°")[0].strip()
                corres_data_l = list(corres_data)
                for i in range(len(corres_data_l) - 1, 0, -1):
                    if corres_data_l[i].isnumeric():
                        corres_data_l.pop(i)
                    else:
                        break
                corres_data = "".join(corres_data_l)
                new_str = ""
                current_idx = 0
                for idx in range(len(corres_data)):
                    if (idx > 0) and (corres_data[idx].isupper() == True):
                        if (corres_data[idx - 1] != " ") and (corres_data[idx - 1] != "."):
                            new_str += corres_data[current_idx:idx]
                            current_idx = idx
                            if (idx != len(corres_data)-1):
                                new_str += ", "
                    if (idx == len(corres_data)-1):
                        new_str += corres_data[current_idx::]
                useful_info[temp_dict["_0"]] = new_str
            elif (temp_dict["_0"] == "Website"): # Website URL
                useful_info[temp_dict["_0"]] = corres_data
                
        company_info[company] = useful_info

    #for company in company_list:
    #    print(company_info[company])

    driver.quit()
    
    return(company_info)

def export_json(info_dict):
    json_dict = {}
    json_dict["length"] = len(info_dict)
    json_res = []
    for key, value in info_dict.items():
        row_data = []
        row_data.append(key)
        if "Logo" in value:
            row_data.append(value["Logo"])
        if "Founded" in value:
           row_data.append(value["Founded"])
        else:
            row_data.append("Unknown")
        if "Founders" in value:
            row_data.append(value["Founders"])
        elif "Founder" in value:
            row_data.append(value["Founder"])
        else:
            row_data.append("Unknown")
        if "Headquarters" in value:
            row_data.append(value["Headquarters"])
        else:
            row_data.append("Unknown")
        if "Website" in value:
            row_data.append(value["Website"])
        else:
            row_data.append("Unknown")
        json_res.append(row_data)
    json_dict["data"] = json_res
        
    with open("companies.json", "w", encoding="utf-8") as write_file:
        json.dump(json_dict, write_file, indent=4)

    print("companies.json file created at root")

def export_json_into_angular_project(info_dict):
    os.chdir("cs410-project")
    os.chdir("src")
    os.chdir("app")
    os.chdir("companies")
    json_dict = {}
    json_dict["length"] = len(info_dict)
    json_res = []
    for key, value in info_dict.items():
        row_data = []
        row_data.append(key)
        if "Logo" in value:
            row_data.append(value["Logo"])
        if "Founded" in value:
           row_data.append(value["Founded"])
        else:
            row_data.append("Unknown")
        if "Founders" in value:
            row_data.append(value["Founders"])
        elif "Founder" in value:
            row_data.append(value["Founder"])
        else:
            row_data.append("Unknown")
        if "Headquarters" in value:
            row_data.append(value["Headquarters"])
        else:
            row_data.append("Unknown")
        if "Website" in value:
            row_data.append(value["Website"])
        else:
            row_data.append("Unknown")
        json_res.append(row_data)
    json_dict["data"] = json_res
        
    with open("companies.json", "w", encoding="utf-8") as write_file:
        json.dump(json_dict, write_file, indent=4)

    print("companies.json file created at root/cs410-project/src/app/companies")
    
def main():
    companies = get_list_of_companies()
    print(companies)
    companies_info = get_companies_info(companies)
    export_json(companies_info)
    export_json_into_angular_project(companies_info)
    
    
if __name__ == "__main__":
    main()

# David Tan Sang Tran (davidtt2)
# CS 410 Course Project Fall 2020
# Python Data Retrieval
