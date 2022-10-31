from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import os
import requests
import getpass,re
import subprocess
from . import extensions
from urllib.request import Request, urlopen

from . import views


def extractImageName(mystr):
    mystr = mystr.split('/')
    return mystr[len(mystr) - 1]

def creatingCacheImageFolder(sitename, request):
    # define the name of the directory to be created
    # try:
    if "/" in sitename:
        split_res = sitename.split("/")
        sitename = split_res[0]
        page_name = split_res[-1]
    else:
        page_name = sitename

    path = views.GetCodeDirectory(request) + "Cache/" + sitename + "/Images/" + page_name



    try:
        if not os.path.exists(path):
            os.makedirs(path, 0o777)
            print("Successfully created the directory %s " % path)
        return path
    except Exception as ex:
        print("Error Creating Directory for Images of website. OriginalData2, Line 17")
        print(ex)
        return path


def writingCacheImages(tempath, fullsitename, sitename, request):
    url_site = sitename
    with open(tempath, 'r') as afile:
        buff = afile.read()
        soup = BeautifulSoup(buff, "lxml")
        lst = []
        imagelst = []
        # print(soup.prettify())
        sitename = sitename.split("/")[0]
        fullsitename = getFullSiteNameWithHTTP(sitename)
        total_images = soup.findAll('img')
        for img in total_images:
            try:
                # print(img) name of images from html file
                img = str(img)
                regex = r'src\s*=\s*"(.+?)"'
                m = re.search(regex, img)
                mystr = m.group(1)
                # All image names are added in a list
                imagelst.append(extractImageName(mystr))

                if "://" in mystr:
                    pass
                else:
                    mystr = fullsitename[0] + '/' + mystr
                print(mystr)
                lst.append(mystr)
                # tree = ET.ElementTree(ET.fromstring(buff))
            except Exception as ex:
                pass
        try:
            contents = str(soup)
            regex = r"background\-image\:.url\(+(([a-zA-z]+\/[a-zA-Z_/><?]+)([\.]+[a-zA-z]+))\)\;"
            match_pattern = re.findall(regex, contents)
            if match_pattern:
                for log in match_pattern:
                    mystr = log[0]
                    imagelst.append(extractImageName(mystr))
                    if sitename in mystr:
                        pass
                    else:
                        mystr = fullsitename[0] + '/' + mystr
                    print(mystr)
                    lst.append(mystr)
            else:
                contents = str(soup)
                regex = r"background\:.url\(+(([a-zA-z]+\/[a-zA-Z_/><?]+)([\.]+[a-zA-z]+))\)\;"
                match_pattern = re.findall(regex, contents)
                if match_pattern:
                    for log in match_pattern:
                        mystr = log[0]
                        imagelst.append(extractImageName(mystr))
                        if sitename in mystr:
                            pass
                        else:
                            mystr = fullsitename[0] + '/' + mystr
                        print(mystr)
                        lst.append(mystr)

        except:
            pass

        # lst = sorted(list(set(lst)))
        # imagelst = sorted(list(set(imagelst)))

        savepath = creatingCacheImageFolder(url_site, request)
        savepath2 = savepath

        # lst = list(set(lst))
        for i, images in enumerate(lst):
            try:
                completeName = os.path.join(savepath, imagelst[i])
                with open(completeName, 'wb') as f:
                    try:
                        headers = {
                            'User-Agent': 'Mozilla/5.0 '}
                        actual_img = requests.get(images, headers=headers, verify=False)
                        actual_img_cnt = actual_img.content
                        f.write(actual_img_cnt)
                    except BaseException as ex:
                        images = "https:" + images
                        headers = {
                            'User-Agent': 'Mozilla/5.0 '}
                        actual_img = requests.get(images,  headers=headers, verify=False)
                        actual_img_cnt = actual_img.content
                        f.write(actual_img_cnt)

            except BaseException as e:
                print(e)
        return imagelst


def creatingFolder(foldername, request):
    # define the name of the directory to be created

    if "/" in foldername:
        foldername = foldername.split("/")[0]
    path = views.GetCodeDirectory(request) + "Cache/" + foldername

    try:
        if not os.path.exists(path):
            os.makedirs(path, 0o777)
            print("Successfully created the directory %s " % path)
    except BaseException as ex:
        print("Error Creating Directory for Images of website. OriginalData2")
        print(ex)


def creatingFile(url, request, fullsitename):
    import ssl
    context = ssl._create_unverified_context()

    response = urllib.request.urlopen(fullsitename, context=context)

    webContent = response.read()

    if "/" in url:
        url_page = url.split("/")[-1]
        url = url.split("/")[0]
    else:
        url_page = url

    save_path = views.GetCodeDirectory(request) + 'Cache/' + url + '/' + url_page
    try:
        file1 = open(save_path, "wb")
        file1.write(webContent)
        file1.close()
    except BaseException as ex:
        print(ex)
        print("BaseException in creatingFile orignaldata2.py")
    return save_path


def getFullSiteNameWithHTTP(lst):
    import ssl
    # context = ssl._create_unverified_context()
    finallst = []

    if type(lst) is list:
        for url in lst:
            try:
                turl = 'https://' + url
                try:
                    response = requests.get(turl)
                except:
                    response = requests.get(turl, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
                response = response.status_code
                if response != "404":
                    finallst.append(turl)
            except:
                try:
                    turl = 'http://' + url
                    try:
                        response = requests.get(turl)
                    except:
                        response = requests.get(turl, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
                    response = response.status_code
                    if response != "404":
                        finallst.append(turl)
                except:
                    finallst.append(url)

    else:
        try:
            turl = 'https://' + lst
            try:
                response = requests.get(turl)
            except Exception as ex:
                response = requests.get(turl, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
            response = response.status_code
            if response != "404":
                finallst.append(turl)

        except:
            try:
                turl = 'http://' + lst
                try:
                    response = requests.get(turl)
                except:
                    response = requests.get(turl, headers={'User-Agent': 'Mozilla/5.0'})
                response = response.status_code
                if response != "404":
                    finallst.append(turl)
            except:
                finallst.append(lst)

    return finallst


def combine2(lst, request):

    try:
        finallst = []
        creatingFolder(lst, request)
        creatingCacheImageFolder(lst, request)
        fullsitename = getFullSiteNameWithHTTP(lst)

        x = creatingFile(lst, request, fullsitename[0])

        finallst.append(x)
        writingCacheImages(x, fullsitename[0], lst, request)
        return finallst
    except BaseException as ex:
        print(ex)
        print("BaseException in combine2 orignaldata2.py")

