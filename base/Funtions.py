import json
import math

import exiftool
import filecmp
import glob
import hashlib
import os
import re
import ssl
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from difflib import ndiff
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup

from . import views
from .OrignalData2 import getFullSiteNameWithHTTP


def clearTemp(request):
    x = views.GetCodeDirectory(request)
    cmd = 'rm -R ' + x + 'temp'
    # cmd = 'head -8 /var/log/auth.log'
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out = out.decode(encoding="utf-8")
    err = err.decode(encoding="utf-8")
    cmd = 'mkdir ' + x + '/temp'
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out = out.decode(encoding="utf-8")
    err = err.decode(encoding="utf-8")


def clearCacheOneWebsite(url, request):
    print(url)
    x = views.GetCodeDirectory(request)
    try:
        allfiles = glob.glob(x + "Cache/*")
        for file in allfiles:
            if url in file:
                cmd = 'rm -R ' + file

                proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                (out, err) = proc.communicate()
                out = out.decode(encoding="utf-8")
                err = err.decode(encoding="utf-8")
        return True
    except Exception as ex:
        print(ex)
        return False


# line word character comparison funtions
def fileCounter(path):
    try:
        lst = []
        # path='/home/usman/Desktop/temp/ncsael.mcs.nust.edu.pk'
        cmd = 'wc -m '
        cmd = cmd + path
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        out = out.decode(encoding="utf-8")
        err = err.decode(encoding="utf-8")
        # print("total characters\n")
        out = out.split()
        # print(out[0] + '\n')
        lst.append(out[0])
        cmd = 'wc -l '
        cmd = cmd + path
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        out = out.decode(encoding="utf-8")
        err = err.decode(encoding="utf-8")
        # print("total lines\n")
        out = out.split()
        # print(out[0])
        lst.append(out[0])
        cmd = 'wc -w '
        cmd = cmd + path
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        out = out.decode(encoding="utf-8")
        err = err.decode(encoding="utf-8")
        # print("total words\n")
        out = out.split()
        # print(out[0] + '\n')
        lst.append(out[0])
        return lst
    except Exception as e:
        print(e)


def exactTextDiff(temppath, orignalpath):
    cmd = 'diff '
    cmd = cmd + orignalpath + "  " + temppath
    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out = out.decode(encoding="utf-8")
    print(out)
    err = err.decode(encoding="utf-8")
    return out


def LineWordCompare(temppath, orignalpath):
    templst = fileCounter(temppath)
    path2 = orignalpath
    orignallst = fileCounter(path2)
    print(len(orignallst))
    print(len(templst))
    count = 1

    if templst[0] != orignallst[0] and templst[1] == orignallst[1] and templst[2] == orignallst[2]:
        print(orignalpath + " Characters are not Identical")
        count = 1
    elif templst[2] != orignallst[2] and templst[0] != orignallst[0] and templst[1] == orignallst[1]:
        print(templst[0] + '      ' + orignallst[0] + '\n')
        print(templst[1] + '      ' + orignallst[1] + '\n')
        print(templst[2] + '      ' + orignallst[2] + '\n')
        print(orignalpath + " words and characters are not Identical")
        count = 1
    elif templst[2] != orignallst[2] and templst[0] != orignallst[0] and templst[1] != orignallst[1]:
        print(templst[0] + '      ' + orignallst[0] + '\n')
        print(templst[1] + '      ' + orignallst[1] + '\n')
        print(templst[2] + '      ' + orignallst[2] + '\n')
        print(orignalpath + "  words,characters and lines are not Identical")
        count = 1
    else:

        print(orignalpath + " are Identical")
        count = 0
        # if count is zero, is secure
        # if count is 1, is insecure

    changes = "NO CHANGE"

    if count == 1:
        changes = exactTextDiff(temppath, orignalpath)

    return count, changes


# Temp file Creation Funtions
def creatingTempFolder(sitename, request):
    # define the name of the directory to be created
    path = views.GetCodeDirectory(request) + 'temp/' + sitename
    try:
        if not os.path.exists(path):
            os.makedirs(path, 0o777)
            print("Successfully created the directory %s " % path)
    except Exception as ex:
        print(ex)
        print("Error.... Creating folder for websites in temp")


def creatingFolder(foldername, request):
    # define the name of the directory to be created

    if "/" in foldername:
        foldername = foldername.split("/")[0]

    path = views.GetCodeDirectory(request) + "temp/" + foldername

    try:
        try:
            if not os.path.exists(path):
                os.makedirs(path, 0o777)
                print("Successfully created the directory %s " % path)
            return path
        except Exception as ex:
            print("Error Creating Directory for website. Function,creatingFolder")
            print(ex)
            return path

    except BaseException as ex:
        print("Creation of the directory %s failed" % path + str(ex))

    return path


def combine(url_link, request, ws, host_address):
    finallst = []
    lst = url_link
    page_no = 0
    total_pages = len(url_link)
    for values in lst:
        # x = creatingTempFile(values)
        try:
            print(values)


            page_no += 1
            page_percent = (15 * page_no) / total_pages
            page_percent = math.floor(page_percent)
            x = {'value': str(10 + page_percent), 'value2': f"Downloading {values}"}
            y = json.dumps(x)
            ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
            ws.send(y)
            ws.close()

            creatingFolder(values, request)
            x = writingTempFiles(values, request)
            finallst.append(x)
        except Exception as ex:
            print(ex)

    return finallst


def writingTempFiles(url, request):
    # ssl._create_default_https_context = ssl._create_unverified_context
    context = ssl._create_unverified_context()
    sitename = url
    fullsitename = getFullSiteNameWithHTTP(url)[0]
    response = urllib.request.urlopen(fullsitename, context=context)

    webContent = response.read()
    if "/" in url:
        url_page = url.split("/")[-1]
        url = url.split("/")[0]
    else:
        url_page = url

    save_path = views.GetCodeDirectory(request) + 'temp/' + url + '/' + url_page
    file1 = open(save_path, "wb")
    file1.write(webContent)
    file1.close()
    return save_path


# Hack Word Check Funtions
def checkHackWords(file):
    # file1 = open(path, "r")
    # file = file1.readlines()
    # file1.close()
    file = file.split("\n")

    file1 = open(os.getcwd() + "/base/wordlist.txt", "r")

    hackedwords = file1.readlines()
    file1.close()
    for i, lines in enumerate(hackedwords):
        hackedwords[i] = hackedwords[i].strip('\n')
    # for i, lines in enumerate(file):
    #     file[i] = file[i].strip('\n')
    lst = []
    count = 0
    for lines in file:
        # print(lines)
        # if any(word in lines for word in hackedwords):
        #    count += 1
        for words in hackedwords:
            if words in lines:
                lst.append('hack word: ' + words + ' Exists')  # gui HACK WORD DISPALY HERE
                #                lst.append('hack word: ' + words + ' Exists in line :' + lines)  # gui HACK WORD DISPALY HERE

                count += 1

    if count == 0:
        print("No hack word detected")
        return 0, ["No Findings Found"]
    else:
        print('\n \nHack word exits in ')
        if not lst:
            pass
        else:
            for lines in lst:
                print(lines)
        return 1, lst


# Computing Hash
def checkComputhinghash(orignalpath, temppath):
    hasher = hashlib.md5()
    with open(orignalpath, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    a = hasher.hexdigest()
    print(a)

    hasher2 = hashlib.md5()
    with open(temppath, 'rb') as afile:
        buf = afile.read()
        hasher2.update(buf)
    b = hasher2.hexdigest()
    print(b)

    # print(str(a) == str(b))
    if str(a) == str(b):
        print("True for site   :" + orignalpath)
        return 0, a, b
    else:
        print("False for site :" + orignalpath)
        return 1, a, b


# Dom Work
class MyHTMLParser(HTMLParser):
    html_struct = []

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        self.html_struct.append("Encountered a start tag: {}".format(tag))

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        self.html_struct.append("Encountered an end tag : {}".format(tag))

    def get_html_entities(self):
        return self.html_struct


class FileOperations:
    def FileWriting(self, HtmlFileName, NewFileName):
        parser = MyHTMLParser()
        htmlFile = open(r"" + HtmlFileName, "r")
        HtmlContent = htmlFile.read()
        htmlFile.close()
        parser.html_struct = []
        parser.feed(HtmlContent)
        tags = parser.get_html_entities()
        JoinedTags = ''
        for values in tags:
            JoinedTags = JoinedTags + values + '\n'

        TextFile = open(NewFileName, "w")  # opens file with name of "test.txt"

        TextFile.write(JoinedTags)
        TextFile.close()


def savingDomDataForOrignal(path):
    fileOperation = FileOperations()
    orignal = path + '_Orignal.txt'
    fileOperation.FileWriting(path, orignal)


def savingDomDataForTemp(path):
    fileOperation = FileOperations()
    orignal = path + '_Temp.txt'
    fileOperation.FileWriting(path, orignal)  #


def comparingDomData(pathorignal, pathtemp):
    filename1 = str(pathorignal) + '_Orignal.txt'
    filename2 = str(pathtemp) + '_Temp.txt'
    try:
        f1_lines = [line.rstrip('\n') for line in open(filename1)]
        f2_lines = [line.rstrip('\n') for line in open(filename2)]
    except BaseException as ex:
        print(ex)
    val = filecmp.cmp(filename1, filename2)
    print("Are both files same? : {}".format(val))
    domDiff = []
    if not val:
        diff = ndiff(f1_lines, f2_lines)
        for index, item in enumerate(diff):
            if "-" in item:
                print(">Tag Added/Changed on", "Line-%d" % (index + 1), item)
                domDiff.append(f">Tag Added or Changed on Line - {index + 1} : {item}")
            elif "+" in item:
                print(">Tag Missing on", "Line-%d" % (index + 1), item)
                domDiff.append(f">Tag Removed from Line        - {index + 1} : {item}")

    print(domDiff)
    if val == False:
        return 1, domDiff
    else:
        return 0, domDiff


def countTagDomWork(pathorignal, pathtemp):
    orignal = pathorignal
    temp = pathtemp
    global total1, total
    from bs4 import BeautifulSoup as bs
    # Load the HTML content
    html_file1 = open(orignal, 'r')
    html_file = open(temp, 'r')
    html_content1 = html_file1.read()
    html_content = html_file.read()
    html_file.close()  # clean up

    # Initialize the BS object
    soup1 = bs(html_content1, 'html.parser')
    soup = bs(html_content, 'html.parser')
    tags = ['img', 'p', 'div', 'script', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'body', 'br',
            'hr', 'form', 'input', 'textarea', 'button', 'select', 'optgroup', 'option',
            'label', 'fieldset', 'legend', 'datalist', 'output', 'frame', 'frameset', 'noframes',
            'iframe', 'map', 'area', 'canvas', 'figcaption', 'figure', 'picture', 'svg', 'audio',
            'video', 'source', 'track', 'a', 'link', 'nav', 'ul', 'ol', 'li', 'dir', 'dl', 'dt', 'dd',
            'table', 'noscript', 'head', 'meta', 'base', 'basefront', 'aaplet', 'embed', 'object', 'param']
    count = 0
    tag_pdf = []
    for tag in tags:
        tag_found1 = soup1.findAll(tag)
        tag_found = soup.findAll(tag)

        total1 = "{} found {} times".format(tag, len(tag_found1))
        # print(total1)
        total = "{} found {} times".format(tag, len(tag_found))
        # print(total)

        if total1 == total:
            print("pass")

        else:
            print("fail")
            if len(tag_found) > 0 or len(tag_found1) > 0:
                tag_pdf.append((tag, len(tag_found1), len(tag_found)))
            count = 1
    return count, tag_pdf


# Image Work
def creatingTempImageFolder(sitename, page_name, request):
    # define the name of the directory to be created
    path = views.GetCodeDirectory(request) + 'temp/' + sitename + '/Images/' + page_name

    try:
        if not os.path.exists(path):
            os.makedirs(path, 0o777)
            print("Successfully created the directory %s " % path)
        return path
    except Exception as e:
        print("Error Creating Directory for Images of website. Functions, creatingTempImageFolder")
        print(e)
        return path

    # return path


def extractImageName(mystr):
    if mystr[-1] == "/":
        mystr = mystr[:-1]
    mystr = mystr.split('/')
    return mystr[len(mystr) - 1]


def writingTempImages(tempath, sitename, page_name, request):
    with open(tempath, 'r') as afile:
        buff = afile.read()
        soup = BeautifulSoup(buff, "lxml")
        lst = []
        imagelst = []
        # print(soup.prettify())
        for img in soup.findAll('img'):
            try:

                # print(img) name of images from html file
                img = str(img)
                regex = r'src\s*=\s*"(.+?)"'
                m = re.search(regex, img)
                mystr = m.group(1)
                # All image names are added in a list
                imagelst.append(extractImageName(mystr))
                # print(mystr)

                # sitename = sitename.split("/")[0]
                fullsitename = getFullSiteNameWithHTTP(sitename)

                if "https://" in mystr or "http://" in mystr:
                    pass
                else:
                    mystr = fullsitename[0] + '/' + mystr

                lst.append(mystr)
                # tree = ET.ElementTree(ET.fromstring(buff))
            except Exception as ex:
                print(ex)

        try:
            contents = str(soup)
            regex = r"background\-image\:.url\(+(([a-zA-z]+\/[a-zA-Z_/><?]+)([\.]+[a-zA-z]+))\)\;"
            match_pattern = re.findall(regex, contents)
            if match_pattern:
                for log in match_pattern:
                    mystr = log[0]
                    imagelst.append(extractImageName(mystr))
                    if sitename[0] in mystr:
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
        except BaseException as ex:
            pass

        # lst = sorted(list(set(lst)))
        # imagelst = sorted(list(set(imagelst)))

        savepath = creatingTempImageFolder(sitename[0], page_name, request)
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
                        actual_img = requests.get(images, headers=headers, verify=False)
                        actual_img_cnt = actual_img.content
                        f.write(actual_img_cnt)
            except BaseException as e:
                print(e)
        return imagelst


def readingTempImages(imagespath, imagesname):
    new = getImagesNamesForAllign(imagespath)
    finallist = []
    path = imagespath
    imagesname = Remove(new)
    for images in imagesname:
        files = [path + "/" + images]
        print(files)
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata_batch(files)
            # print(str(metadata[0]))
            regex1 = "(File:FileName\':\s*\'(.*?)')"
            regex2 = "(File:FileType\':\s*\'(.*?)\')"
            regex3 = "(Composite:ImageSize\':\s*\'(.*?)\')"
            regex4 = "(Composite:Megapixels\':\s*(\d\.?\d*))"
            m1 = re.search(regex1, str(metadata[0]))
            m2 = re.search(regex2, str(metadata[0]))
            m3 = re.search(regex3, str(metadata[0]))
            m4 = re.search(regex4, str(metadata[0]))
            finalstring = ''
            try:
                finalstring = finalstring + m1.group(0) + '\n' + m2.group(0) + '\n' + m3.group(0) + '\n' + m4.group(
                    0) + '\n'
                # print(m1.group(0))
                finallist.append(finalstring)
            except:
                finallist.append("Unknown data")
    return finallist


def getOrignalFolderPathOfImages(websitename, page_name, request):
    path = views.GetCodeDirectory(request) + '/Cache/' + websitename + '/Images/' + page_name
    return path


# Python code to remove duplicate elements
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


def combiningAllImageDifference(origanlimagelist, tempimagelist):
    list1 = tempimagelist
    list2 = origanlimagelist
    count = 0
    for i, values in enumerate(list1):
        tempimages = list1[i].split('\n')
        orignalimages = list2[i].split('\n')
        try:
            if (tempimages[0] == orignalimages[0] and tempimages[1] == orignalimages[1] and tempimages[2] ==
                    orignalimages[2]):  # and tempimages[3] == orignalimages[3]):
                pass
            elif (tempimages[0] != orignalimages[0] and tempimages[1] == orignalimages[1] and tempimages[2] ==
                  orignalimages[2]):  # and tempimages[3] == orignalimages[3]):
                print('\n')
                count += 1
                print("Change Detected in File name \n" + orignalimages[0] + ' Has been changed')
            elif (tempimages[0] == orignalimages[0] and tempimages[1] != orignalimages[1] and tempimages[2] ==
                  orignalimages[2]):  # and tempimages[3] == orignalimages[3]):
                print('\n')
                print("Change Detected in File Type \n" + orignalimages[1] + ' Has been changed')
                count += 1
            elif (tempimages[0] == orignalimages[0]) and (tempimages[1] == orignalimages[1]) and (
                    tempimages[2] != orignalimages[2]):  # and (tempimages[3] == orignalimages[3]):
                print('\n')
                print("Change Detected in Image Size\n" + orignalimages[2] + ' Has been changed')
                count += 1
            # elif (tempimages[0] == orignalimages[0] and tempimages[1] == orignalimages[1] and tempimages[2] ==
            # orignalimages[2] ):#and tempimages[3] != orignalimages[3]):
            elif tempimages[3] != orignalimages[3]:  # and tempimages[3] != orignalimages[3]):
                print('\n')
                print("Change Detected in Mega Pixels \n" + orignalimages[3] + ' Has been changed')
                count += 1

        except:
            pass
    return count


def getImagesNamesForAllign(pth):
    # pth = getorignalImagePath()
    # print(glob(pth))
    '''files = os.listdir(pth)
    lst=[]
    for name in files:
        lst.append(name)
    #print(lst)'''
    a = [s for s in os.listdir(pth)
         if os.path.isfile(os.path.join(pth, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(pth, s)))
    return a

    #
    # #AI Work
    # def Load_Models():
    #     from UI.app.home import extensions
    #     print(str(extensions.GetCodeDirectory())+'Models/CNN')
    #
    # if (GetEnvironmentType() == Environment.Production.name):
    #     CNN = load_model(extensions.GetCodeDirectory()+r'/Models/CNN')
    #     LSTM = load_model(extensions.GetCodeDirectory() + r'/Models/LSTM')
    #     DNN = load_model(extensions.GetCodeDirectory() + r'/Models/DNN')
    # else:
    #     CNN = load_model(extensions.GetAlternateCodeDirectory()+r'/Models/CNN')
    #     LSTM = load_model(extensions.GetAlternateCodeDirectory() + r'/Models/LSTM')
    #     DNN = load_model(extensions.GetAlternateCodeDirectory() + r'/Models/DNN')

    # CNN = load_model(GetCodeDirectory()+r'Models/CNN')
    # LSTM = load_model(GetCodeDirectory()+r'Models/LSTM')
    # DNN = load_model(GetCodeDirectory()+r'Models/DNN')

    # print("Models Loaded...!!")
    # return CNN, LSTM, DNN


def creatingTempFileForAI(url):
    import ssl
    count = 0
    context = ssl._create_unverified_context()
    sitename = url
    try:
        turl = 'https://' + url
        # print(url)
        # url = 'https://ncsael.mcs.nust.edu.pk/'
        response = urllib.request.urlopen(turl, context=context)
        count = 1
    except Exception as e:
        try:
            # print(url)
            turl = 'http://' + url
            # print(url)
            # url = 'https://ncsael.mcs.nust.edu.pk/'
            response = urllib.request.urlopen(turl, context=context)
            count = 1
        except Exception as e:
            response = urllib.request.urlopen(url, context=context)
            count = 2
    return response


def showReport(tasknumber, taskname, count):
    if count == 0:
        output = '\t\t\t\t\tTest ' + str(tasknumber) + ' :- ' + "Test name:  " + taskname + \
                 "\n\t\t\t\t\t          " + "Test Result: " + " PASS "
    else:
        output = '\t\t\t\t\tTest ' + str(tasknumber) + ' :- ' + "Test Name:  " + taskname + \
                 "\n\t\t\t\t\t          " + "Test Result: " + " FAIL "

    return output


def showReport2(tasknumber, taskname, count):
    output = '\t\t\t\t\tTest ' + str(tasknumber) + ' :- ' + "Test Name:  " + taskname + \
             "\n\t\t\t\t\t          " + "Test Result: " + " FAIL (SSL Not Found)"
    return output


def checkSeverity(count):
    if count <= 3:
        print("\n\t\t\t\t\tSeverity Level is Low\n")
        return "Low"
    elif count > 3 and count <= 4:
        print("\n\t\t\t\t\tSeverity Level is Medium\n")
        return "Medium"

    else:
        print("\n\t\t\t\t\tSeverity Level is high\n")
        return "High: Send SMS"
