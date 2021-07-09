import requests
from bs4 import BeautifulSoup

def bookname2bookpage(abname):
    abname=abname.replace(' ','+')
    #print(abname)
    searchurl='https://audiobooklabs.com/?s='+abname
    print(searchurl)
    searchresultpage=requests.get(searchurl)
    soup=BeautifulSoup(searchresultpage.content,'html.parser')
    #print(soup.prettify)
    resultbox = soup.find(id="primary")
    #print(resultbox)
    results = resultbox.find("h2", class_="entry-title")
    print(results)
    if results==None:
        return 0
    bookpage=results.find('a')
    bookpageurl=bookpage['href']
    print(bookpageurl)
    return bookpageurl

def bookpage2playerpage(bookpage):
    if bookpage==0:
        return 0
    dunnowhut=requests.get(bookpage)
    soup=BeautifulSoup(dunnowhut.content, 'html.parser')
    #print(soup)
    for link in soup.find_all('a', href=True):
        if (link['href']).split('?')[0]=='https://audiobooklabs.com/file-downloads':
            playerpage=link['href']
            break
    return playerpage


def playerpage2fileurl(playerpage):
    if playerpage==0:
        return []
    weirdbs=requests.get(playerpage)
    (weirdbs.text)
    soup = BeautifulSoup(weirdbs.content, "html.parser")
    links=[]
    for link in soup.find_all('a', href=True):
        if link['href'].split('.')[-1] == 'mp3':
            print(link['href'])
            links.append(link['href'])
    return links


def downloadfromfile(links):
    if len(links)>0:
        filenum=1
        for link in links:
            r = requests.get(link, stream = True)
            name=link.split('/')[-1]
            with open(f"{filenum}_{name}","wb") as mp3:
                for chunk in r.iter_content(chunk_size=8*1024):
                     # writing one chunk at a time to audio file
                    if chunk:
                        mp3.write(chunk)
            filenum=filenum+1
        print("Successful download")
    else:
        print('Book not found')

inputtext=input("Enter something : ")
downloadfromfile(playerpage2fileurl(bookpage2playerpage(bookname2bookpage(inputtext))))
