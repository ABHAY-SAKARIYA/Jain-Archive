import os
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class Jain_Archive:

    def __init__(self) -> None:
        self.CSV_loc = "Jain Only Excel From Archive.csv"
        self.DataList = []
        self.DataDict = {"title":[],"creator":[],"date":[],"language":[],"publisher":[],"subject":[],"identifier":[]}
        self.__total_pdfs_found = 2988


    def Filter(self) -> None:

        df = pd.read_csv(self.CSV_loc)

        Filter_Dict = {"language":["eng","english","hin","hindi","san","sanskrit","gujarati","guj","prakrut"],
                      "mediatype":["texts"]}
        for i in range(0,len(df["identifier"])):
            if df["language"][i] in Filter_Dict["language"]:
                if df["mediatype"][i] in Filter_Dict["mediatype"]:
                    self.DataList.append(df["identifier"][i])
                    for k in self.DataDict.keys():
                        self.DataDict[k].append(df[k][i])


        DataDict_DataFrame = pd.DataFrame(self.DataDict)
        DataDict_DataFrame.to_excel("Jain-Only-Data-Excel-Sheet.xlsx")

        with open("identifier.json","a") as write:
            write.write(json.dumps(self.DataList,indent=4))
        

    def Create_Download_link(self):

        with open("identifier.json","r") as read:
            identifier = json.load(read)

        
        Download_link = []

        for i in identifier:
            createLink = f"http://archive.org/download/{i}"
            Download_link.append(createLink)

        with open("DownloadLink.json","a") as writefile:
            writefile.write(json.dumps(Download_link,indent=4))


    def download(self) -> None:
        dir_path = r"download_path"
        
        with open("DonwloadLink.json","r") as read:
            links = json.load(read)
        op = webdriver.ChromeOptions()
        p = {
            "download.default_directory":dir_path, 
        "safebrowsing.enabled":"false",
        "plugins.always_open_pdf_externally": True
        }
        op.add_experimental_option("prefs", p)
        driver = webdriver.Chrome(options=op)

        time.sleep(30)
        count = 0			

        for link in links[0:10:1]:  

            driver.get(link)
            soup = BeautifulSoup(driver.page_source,"html.parser")

            time.sleep(5)
            clickCount = 0
            sleepCount = 0
            try:
                for data in soup.select("pre a"):
                    pdf = data.text

                    if clickCount == 0:
                        if ".pdf" in pdf or ".rar" in pdf:
                            driver.find_element(By.XPATH,f"//a[@href='{data.get('href')}']").click()
                            clickCount+=1
                        else:
                            pass
                    else:
                        pass

                time.sleep(10)

                
                stop = True
                while stop:

                    filesinfolder = os.listdir(dir_path)
                    index = 0
                    unconfirm = 0
                    file_count = 0
                    minused = False

                    for f in filesinfolder:

                        if "unconfirmed" in f.lower() or ".crdownload" in f.lower():
                            unconfirm = index
                        else:
                            index+=1
                        file_count+=1
                    
                    check = file_count
                    print(f"FileName : {filesinfolder[unconfirm]}")

                    if "unconfirmed" in filesinfolder[unconfirm].lower() or ".crdownload" in filesinfolder[unconfirm].lower():
                        if minused == False:
                            file_count-=1
                            minused = True
                        else:
                            pass
                    else:
                        file_count+=1

                    print(f"Range Of File Found : {check}\nRange Of File - Unconfirmed File : {file_count}")
                    if file_count <= check:
                        if sleepCount >= 6:
                            stop = False
                        else:
                            time.sleep(20)
                            sleepCount += 1
                    else:
                        stop = False
                print(f"Files Downloaded : {count}")
                count+=1
            except:
                continue


Book = Jain_Archive()
# Book.Filter()
# Book.Create_Download_link()
