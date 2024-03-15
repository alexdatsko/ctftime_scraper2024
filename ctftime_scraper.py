import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

outputdir = "/mnt/hacking/_dataset/ctftime" # where to store scraped files
time_delay = .5   # seconds in between solutions to scrape

print(f"\nCTFtime Scraper 2024")
print(f"crypticsilenc3@gmail.com\n")

i=38750   # First (most current) writeup to start with, and work our way back
num=0     # How many items did we successfully scrape?
u="https://ctftime.org/writeup/"   # URL to start with
id_to_find = "id_description"      # div Id of writeup

fjson=open(f"{outputdir}/_writeups.json","w")
fjson.write("[")
options = webdriver.ChromeOptions()
#options.headless = True
options.add_argument("--headless=new")
with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
  while i>1:
    url=u+str(i)
    driver.get(url)
    print(f"{i = } - [Page URL]", driver.current_url, " - [Page Title]", driver.title, end='\r')
    try:
      ctfname = driver.title.split(' / ')[1].strip()
      user = driver.find_element(By.XPATH,'//a[contains(@href,"/user/")]').text
      team = driver.find_element(By.XPATH,'//a[contains(@href,"/team/")]').text
      title = driver.find_element(By.TAG_NAME,"h2").text
    except:
      print(f"[!] Error reading element(s): ctfname:{ctfname}, user:{user}, team:{team}, title:{title}")
    try:
      div = driver.find_element(By.ID,f"{id_to_find}").text
    except:
      print(f"[!] Error: div couldn't be found, {type(div)} {div}")
    if div:
      fname=f"{outputdir}/{i}.txt"
      f=open(fname,"w")
      fjson.write('{'+f'"ctfname":"{ctfname}","team":"{team}","user":"{user}","title":"{title}","filename":"{fname}"'+'},')
      f.write(div)
      f.close()
      num+=1
    sleep(time_delay)
    i=i-1
#  exit(1)
print(f"[!] Done! {num} files written.")
fjson.write("]")
fjson.close()
