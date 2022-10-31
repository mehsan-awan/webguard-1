import math
import os
import json
import threading

import psutil
import time
import enum
from xml.sax.saxutils import escape
import requests
from datetime import date, datetime
import warnings
from urllib.request import Request, urlopen

from reportlab.lib import colors
from reportlab.platypus import Paragraph, PageBreak, TableStyle
from reportlab.platypus import Image, Table
from reportlab.lib.units import cm

from . import sendmail, Funtions, views, CheckSSL, SmsApi
from .crawler import crawler
from .pieChartPDF4 import pdfReport

import websocket as websocket_client


def CreateFile(filename, content, flag, request):
    # flag w to write
    # flag a append

    # Ehsan Code

    save_filename = filename + "-" + datetime.today().strftime(
        '%Y-%m-%d-%H:%M:%S') + ".txt"
    print(save_filename)

    # Ehsan Code End

    with open(views.GetCodeDirectory(request) + "Logs/" + save_filename, flag) as outfile:
        json.dump(content, outfile)


def CPUusage():
    # CPU
    #  print("CPU Percentage:" + str(psutil.cpu_percent(interval=0)))
    #  print("CPU Frequency (Mega Hertz):" + str(psutil.cpu_freq()[0]))
    Frequency = psutil.cpu_freq()[0]
    usage_percentage = psutil.cpu_percent(interval=0)

    return usage_percentage, Frequency


def memoryusage():
    # RAM
    # print("Total Memory: " + str((((psutil.virtual_memory()[0]) / 1024) / 1024) / 1024) + " GB")
    # print("Free Memory: " + str((((psutil.virtual_memory()[1]) / 1024) / 1024) / 1024) + " GB")
    Total = (((psutil.virtual_memory()[0]) / 1024) / 1024) / 1024
    Free = (((psutil.virtual_memory()[1]) / 1024) / 1024) / 1024
    return Total, Free


def HDD_Usage():
    # HDD
    hold = psutil.disk_usage('/')
    Total = (((hold[0] / 1024) / 1024) / 1024)
    Free = (((hold[1] / 1024) / 1024) / 1024)
    Percnet_Used = hold[3]

    return round(Total, 1), round(Free, 1), round(Percnet_Used, 1)


def Networ_Stats():
    # Active Connections
    len(psutil.net_connections())
    count = 0
    for x in psutil.net_connections():
        print(x[5])
        if x[5] == "ESTABLISHED" or x[5] == "LISTEN":
            count = count + 1
    # print("Total Active Connections: " + str(count) + "/" + str(len(psutil.net_connections())))
    Total = len(psutil.net_connections())
    Active = count
    return Total, Active


def getFullSiteNameWithHTTP(lst):
    finallst = []
    for url in lst:
        try:
            turl = 'https://' + url

            try:
                # response = urllib.request.urlopen(turl)
                headers = {
                    'User-Agent': 'Mozilla/5.0 '}

                response = requests.get(turl, headers=headers, verify=False)

            except BaseException as ex:
                req = Request(turl, headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(req)
            finallst.append(turl)
        except:
            try:
                turl = 'http://' + url

                try:
                    # response = urllib.request.urlopen(turl)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 '}

                    response = requests.get(turl, headers=headers, verify=False)
                except BaseException as ex:
                    req = Request(turl, headers={'User-Agent': 'Mozilla/5.0'})
                    response = urlopen(req)

                finallst.append(turl)
            except:
                finallst.append(url)
    return finallst


def getSiteName(address):
    mylst = []
    for values in address:
        values = values.split('/')
        mylst.append(values[len(values) - 1])
    return mylst


def imagesNameInFolders(filename, page_name, request):
    return os.listdir(views.GetCodeDirectory(request) + "Cache/" + filename + '/Images/' + page_name)


def getSiteNameFromConfig(request):
    data = []
    lst = []

    try:
        file = open(views.GetCodeDirectory(request) + "Config", "r+")
        data = file.readlines()
        file.close()
    except BaseException as e:
        print("Could not open file! Error From extensdions. getSiteNameFromConfig")
    for i, lines in enumerate(data):
        lines = lines.strip('\n')
        lst.append(lines)
    return lst


scans_per_minute = 0


def Scans_Per_Minutes():
    global scans_per_minute
    return scans_per_minute


def Image_Detailed_Comparison(sitename, page_name, new_images, deleted_images, request):
    import datetime
    import glob

    path = views.GetCodeDirectory(request) + "Cache/" + sitename + "/Images/" + page_name
    path_temp = views.GetCodeDirectory(request) + "temp/" + sitename + "/Images/" + page_name

    Config_Images = glob.glob(path + "/*")
    Config_Images = list(set(Config_Images) - set(deleted_images))
    Config_Images = sorted(Config_Images)

    Temp_Images = glob.glob(path_temp + "/*")
    Temp_Images = list(set(Temp_Images) - set(new_images))
    Temp_Images = sorted(Temp_Images)

    if len(Temp_Images) == len(Config_Images):
        print("yahoo, its working 1")
        from skimage.measure import compare_ssim
        import imutils
        import cv2
        issue = 0
        defaced_img_count = 0
        Images_names = []
        # print ("kaka g")
        try:
            # x=0
            for xx in range(0, len(Config_Images)):
                print("yahoo, its working x")
                try:
                    # Reading Images
                    # print(Config_Images[x])
                    imageA = cv2.imread(Config_Images[xx])
                    imageB = cv2.imread(Temp_Images[xx])

                    # converting to grey scale
                    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
                    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

                    # Calculating SSIM index for threshold
                    (score, diff) = compare_ssim(grayA, grayB, full=True)
                    diff = (diff * 255).astype("uint8")
                    # score = score * 100

                    print("SSIM: {}".format(score))
                    if (score >= 0.999):
                        print(str(Config_Images[xx]) + " : Image In depth comparison passed, NO ISSUES")
                    else:
                        print("Defaced: Image in depth comparison failing...!!" + str(Config_Images[xx]))
                        defaced_img_count = defaced_img_count + 1
                        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        cnts = imutils.grab_contours(cnts)

                        # loop over the contours
                        for c in cnts:
                            # compute the bounding box of the contour and then draw the
                            # bounding box on both input images to represent where the two
                            # images differ
                            (x, y, w, h) = cv2.boundingRect(c)
                            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        # print(os.path.basename(Config_Images[x]))
                        # print(datetime.datetime.now())
                        date_now = datetime.datetime.now()

                        cv2.imwrite(views.GetCodeDirectory(request) + "Defaced_Images/" + str(
                            datetime.datetime.now()) + " @ " + sitename + " @ " + os.path.basename(
                            Config_Images[xx]), imageB)

                        Images_names.append((Config_Images[xx].split("/")[-1]))
                except BaseException as e:
                    print(e)
                    issue = issue + 1
                    pass
        except Exception as e:
            print("Error in Image Detailed(Inside A.I Comparison. Extensions Line 293...!!")
            print(e)

    else:
        print("Number of Images in Config and temp mismatch, consider running cache again.")
        pass
        return 0, 1, []
    return issue, defaced_img_count, Images_names


Breaker = 0


def Stop_Bot():
    global Breaker
    Breaker = 1


def getcachefolderpath(url, request):
    path = views.GetCodeDirectory(request) + "Cache/" + url + "/"
    return path


def gettempfolderpath(url, request):
    path = views.GetCodeDirectory(request) + "temp/" + url + "/"
    return path


def getcachesitenames(url, request):
    path = views.GetCodeDirectory(request) + "Cache/" + url + "/Images/"
    cache_sitenames = os.listdir(path)
    return cache_sitenames


Currently_Under_Scan = ""


def test_socket(request):
    x = threading.Thread(target=Home_FUN, args=(request,))
    x.start()


def Home_FUN(request):
    remote_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    port_number = request.META['SERVER_PORT']
    host_address = request.headers._store["host"][1]
    print(host_address)
    ws = websocket_client.WebSocket()

    global Breaker
    Breaker = 0
    warnings.filterwarnings("ignore")

    initial_time = datetime.now()
    while True:

        Current_time = datetime.now()
        minutes_diff = (Current_time - initial_time)
        print(minutes_diff.total_seconds())
        sec = int(minutes_diff.total_seconds())

        if sec > 60:
            global scans_per_minute
            scans_per_minute = scans_per_minute + 1
            sec = 0
            initial_time = Current_time
        if Breaker >= 1:
            print("Bot Stopped")
            break

        Funtions.clearTemp(request)

        sites_in_config = getSiteNameFromConfig(request)

        for i in sites_in_config:

            filesInConfig = [i]

            fullsitename = getFullSiteNameWithHTTP(filesInConfig)
            print(fullsitename)

            x = {'value': str(1), 'value2': f"Starting Scan on {i}"}
            y = json.dumps(x)

            addr = f'ws://{host_address}/ws/' + str(request.user.id) + "/"
            print("Printing Address before trying to connect")
            print(addr)
            ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
            ws.send(y)
            ws.close()

            # region Crawler
            print("Starting Crawler")
            if Breaker >= 1:
                print("Bot Stopped")

            x = {'value': "", 'value2': "Searching for Internal links"}
            y = json.dumps(x)
            ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
            ws.send(y)
            ws.close()
            crawl_handler = crawler()
            print(fullsitename[0])
            crawl_handler.crawl(fullsitename[0])
            internal = crawl_handler.internal_urls
            external = crawl_handler.external_urls

            x = {'value': "10", 'value2': f"{str(len(internal))} Internal links found."}
            y = json.dumps(x)
            ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
            ws.send(y)
            ws.close()

            if Breaker >= 1:
                print("Bot Stopped")
                break

            file_link = []
            pages_link = set()

            # drop link if it is a image or file
            for internal_link in internal:
                if internal_link.split(".")[-1] in ["jpg", "docx", "doc", "txt", "docs", "jpeg", "png", "PNG", "pdf",
                                                    "gif", "tiff", "svg"]:
                    file_link.append(internal_link)
                else:
                    a = internal_link.split("/")
                    if a[2] == str(filesInConfig[0]):
                        link = internal_link.lower()
                        if link[-1] == "/":  # remove / at the end if exist
                            link = link[:-1]
                        link = link.split("//")[1]
                        if "tel:" not in link and "mail:" not in link:
                            pages_link.add(link)
            page_link = list(pages_link)
            # endregion

            Funtions.creatingTempFolder(filesInConfig[0], request)

            livepath = Funtions.combine(page_link, request, ws, host_address)

            sitenames = getSiteName(livepath)
            x = {'value': "", 'value2': f"{str(len(sitenames))} pages downloaded."}
            y = json.dumps(x)
            ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
            ws.send(y)
            ws.close()

            cachesitenames = getcachesitenames(filesInConfig[0], request)

            new_added_pages = list(set(sitenames) - set(cachesitenames))
            deleted_pages = list(set(cachesitenames) - set(sitenames))
            sitenames = list((set(sitenames) - set(new_added_pages)) - set(deleted_pages))
            # new_added_pages = ["news.html", "index.html", "add.html"]
            # deleted_pages = ["delete.html", "del.html"]

            temp_base_path = gettempfolderpath(filesInConfig[0], request)
            cache_base_path = getcachefolderpath(filesInConfig[0], request)
            count = 0

            reportPDF = pdfReport(filesInConfig[0], request)
            reportPDF.generate_pdf()
            reportPDF.doc.multiBuild(reportPDF.elements)
            elements = reportPDF.elements

            if Breaker >= 1:
                print("Bot Stopped")

                break

            if new_added_pages or deleted_pages:
                elements.append(reportPDF.doHeading("Total no of Pages Changed", reportPDF.h1))

                if new_added_pages:
                    elements.append(reportPDF.doHeading("New Added Pages", reportPDF.h2))
                    for i, page in enumerate(new_added_pages):
                        tbl_data = [
                            [Paragraph(f'<br />{i + 1}', reportPDF.bodyStyle),
                             Paragraph(f"<br />{page}", reportPDF.bodyStyle)],
                        ]
                        tbl = Table(tbl_data, (1 * cm, 17 * cm))

                        elements.append(tbl)
                if deleted_pages:
                    elements.append(reportPDF.doHeading("Deleted Pages", reportPDF.h2))
                    for i, page in enumerate(deleted_pages):
                        tbl_data = [
                            [Paragraph(f'<br />{i + 1}', reportPDF.bodyStyle),
                             Paragraph(f"<br />{page}", reportPDF.bodyStyle)],
                        ]
                        tbl = Table(tbl_data, (1 * cm, 17 * cm))
                        elements.append(tbl)
                elements.append(PageBreak())

            reportPDF.doc.multiBuild(reportPDF.elements)
            elements.append(reportPDF.doHeading("Detail Page wise Report", reportPDF.h1))

            total_compromised_entities = set()
            total_defacement_tested = 0
            total_defacement_detected = 0
            h2_num = 1

            if Breaker >= 1:
                print("Bot Stopped")

                break

            total_pages = len(sitenames)
            print(f"Total Pages Found: {total_pages}")
            page_no = 0
            x = {'value': "25", 'value2': "All content downloaded."}
            y = json.dumps(x)
            ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
            ws.send(y)
            ws.close()
            for site in sitenames:
                try:
                    page_no += 1
                    page_percent = (73 * page_no) / total_pages
                    page_percent = math.floor(page_percent)
                    x = {'value': str(25 + page_percent), 'value2': f"Scanning {site} page."}
                    y = json.dumps(x)
                    ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
                    ws.send(y)
                    ws.close()

                    # site = "newsandevents.html"
                    page_element = []
                    total_defacement_tested += 8
                    h3_num = 0

                    total_defacement_cnt = 0
                    page_element.append(reportPDF.doHeading(str(h2_num) + " " + " " + site, reportPDF.H_Centered))
                    page_element.append(Paragraph("Compromised Entities", reportPDF.body_heading))

                    jsonObject = {
                        "Line Test": "Secure",
                        "Hack Words": "Secure",
                        "Hash": "Secure",
                        "DOM": "Secure",
                        "Tag Count": "Secure",
                        "Image Comparison": "Secure",
                        "SSL": "Secure",
                        "AI 1": "Secure",
                        "AI 2": "Secure",
                        "Severity": "None",
                        "Final_Report": "None"
                    }

                    temp_path = temp_base_path + site
                    cache_path = cache_base_path + site
                    line_change = 0
                    report = ''
                    print(
                        f"\n************************* Result of website :  + {site} *******************************\n")

                    # region LINE WORD COMPARISON
                    resulttt, changes = Funtions.LineWordCompare(temp_path, cache_path)

                    changesss = changes.splitlines()
                    changes_list = []
                    for i in changesss:
                        if i != "---" and i != "< " and i != "> ":
                            changes_list.append(i)

                    if resulttt == 1:
                        jsonObject["Line Test"] = "Insecure"
                        count += 1
                        line_change = 1
                        total_defacement_cnt += 1
                        total_compromised_entities.add("Text Comparison")
                        h3_num += 1

                        page_element.append(
                            reportPDF.doHeading(f"<br />{str(h2_num)}.{str(h3_num)} <b><u>Text Comparison "
                                                f"Failed</u></b>", reportPDF.h3))
                        page_element.append(Paragraph('<b> Changes:</b><br /><br />', reportPDF.bodyStyle))
                        tbl_data = []
                        for i in changes_list:
                            try:
                                if i[0] == "<":
                                    tbl_row = [

                                        [Paragraph('<b>Original Tag:</b>', reportPDF.bodyGreen)],
                                        [Paragraph(f"{escape(i[1:])} ", reportPDF.bodyGreen)],

                                    ]
                                elif i[0] == ">":
                                    tbl_row = [

                                        [Paragraph('<b>Current Tag:</b>', reportPDF.bodyRed)],
                                        [Paragraph(f"{escape(i[1:])} ", reportPDF.bodyRed)],

                                    ]
                                else:
                                    tbl_row = [
                                        [Paragraph('<b>Line No:</b>', reportPDF.bodyStyle)],
                                        [Paragraph(f"{escape(i)} ", reportPDF.bodyStyle)],

                                    ]
                                tbl_data.append(tbl_row)
                            except Exception as e:
                                print(e)

                        tbl = Table(tbl_data, (4 * cm, 11 * cm))
                        style = TableStyle([

                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

                            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),

                            ("GRID", (0, 0), (-1, -1), 1, colors.black),

                            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

                            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
                        ])
                        tbl.setStyle(style)
                        page_element.append(tbl)

                    if Breaker >= 1:
                        print("Bot Stopped")

                        break

                    report = report + Funtions.showReport(1, "Line,Word,Char Comparison", resulttt) + '\n'
                    # endregion

                    # region HACK WORD TEST
                    result_words = []
                    if line_change == 1:
                        result, result_words = Funtions.checkHackWords(changes)

                        if result == 1:
                            jsonObject["Hack Words"] = "Insecure"
                            count += 1
                            total_defacement_cnt += 1
                            total_compromised_entities.add("Hack Words")
                            h3_num += 1

                            page_element.append(reportPDF.doHeading(
                                f"<br />{str(h2_num)}.{str(h3_num)} <b><u>Hack Word Test Failed</u></b>",
                                reportPDF.h3))
                            page_element.append(Paragraph('<b> Words:</b>', reportPDF.bodyStyle))
                            page_element.append(Paragraph(escape(str(result_words)), reportPDF.bodyStyle))

                        report = report + Funtions.showReport(2, "Hack Word Check ", result) + '\n'

                    # endregion

                    # region COMPUTING HASH FUNCTION
                    print('\nComparing Hash Work')
                    result, org_hash, temp_hash = Funtions.checkComputhinghash(cache_path, temp_path)
                    if result == 1:
                        jsonObject["Hash"] = "Insecure"
                        count += 1
                        total_defacement_cnt += 1
                        total_compromised_entities.add("Hash")
                        h3_num += 1

                        page_element.append(
                            reportPDF.doHeading(f"<br />{str(h2_num)}.{str(h3_num)} <b><u>Hash Comparison "
                                                f"Failed</u></b>", reportPDF.h3))

                        tbl_data = [
                            [Paragraph('<b>Original Hash</b>', reportPDF.bodyStyle),
                             Paragraph(f"{escape(org_hash)}", reportPDF.bodyStyle)],

                            [Paragraph('<b>Current Hash</b>', reportPDF.bodyStyle),
                             Paragraph(f"{escape(temp_hash)}", reportPDF.bodyStyle)],
                        ]

                        tbl = Table(tbl_data, (5 * cm, 10 * cm))
                        style = TableStyle([

                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

                            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),

                            ("GRID", (0, 0), (-1, -1), 1, colors.black),

                            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

                            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
                        ])
                        tbl.setStyle(style)
                        page_element.append(tbl)

                    report = report + Funtions.showReport(3, " Computing Hash", result) + '\n'

                    print(
                        "\n*************************************************************************************\n")

                    # endregion
                    if Breaker >= 1:
                        print("Bot Stopped")

                        break

                    # region COMPUTING DOM DATA
                    Funtions.savingDomDataForTemp(temp_path)
                    print('\nComparing Dom Data')
                    result, domDiff = Funtions.comparingDomData(cache_path, temp_path)

                    if result >= 1:
                        jsonObject["DOM"] = "Insecure"
                        count += 1
                        total_defacement_cnt += 1
                        total_compromised_entities.add("DOM")
                        h3_num += 1
                        page_element.append(
                            reportPDF.doHeading(f"<br />{str(h2_num)}.{str(h3_num)} <b><u>DOM Comparison "
                                                f"Failed</u></b>", reportPDF.h3))

                        tbl_data = []
                        for diff in domDiff:
                            tbl_row = [
                                [Paragraph('', reportPDF.bodyBlue),
                                 Paragraph(f"{escape(diff)}", reportPDF.bodyBlue)],
                            ]
                            tbl_data.append(tbl_row)

                        tbl = Table(tbl_data, (15 * cm))
                        style = TableStyle([

                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

                            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),

                            ("GRID", (0, 0), (-1, -1), 1, colors.black),

                            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

                            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
                        ])
                        tbl.setStyle(style)
                        page_element.append(tbl)
                    report = report + Funtions.showReport(4, "Comparing Dom Data", result) + '\n'

                    # endregion
                    if Breaker >= 1:
                        print("Bot Stopped")

                        break
                    # region COUNTING TAG

                    print(
                        "\n*******************************************************************************\n")
                    print('\nCounting Dom Tag')
                    result, tag_pdf = Funtions.countTagDomWork(cache_path, temp_path)

                    if result == 1:
                        jsonObject["Tag Count"] = "Insecure"
                        count += 1
                        total_defacement_cnt += 1
                        total_compromised_entities.add("Tag Count")
                        h3_num += 1

                        page_element.append(
                            reportPDF.doHeading(f"<br />{str(h2_num)}.{str(h3_num)} <b><u>Tag Comparison "
                                                f"Failed</u></b>", reportPDF.h3))

                        tbl_data = []
                        tbl_row = [
                            [Paragraph(f"<b>Tag Name</b>", reportPDF.bodyStyle)],
                            [Paragraph(f"<b>Original Copy No</b>", reportPDF.bodyStyle)],
                            [Paragraph(f"<b>Current Copy No</b>", reportPDF.bodyStyle)]
                        ]
                        tbl_data.append(tbl_row)
                        for tag in tag_pdf:
                            tbl_row = [
                                [Paragraph(f"<b>{escape(str(tag[0]))}</b>", reportPDF.bodyStyle)],
                                [Paragraph(f"{escape(str(tag[1]))}", reportPDF.bodyStyle)],
                                [Paragraph(f"{escape(str(tag[2]))}", reportPDF.bodyStyle)]
                            ]
                            tbl_data.append(tbl_row)

                        tbl = Table(tbl_data, (5 * cm, 5 * cm, 5 * cm))
                        style = TableStyle([

                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

                            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),

                            ("GRID", (0, 0), (-1, -1), 1, colors.black),

                            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

                            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
                        ])
                        tbl.setStyle(style)
                        page_element.append(tbl)

                    report = report + Funtions.showReport(5, "Counting Tag ", result) + '\n'

                    # endregion
                    if Breaker >= 1:
                        print("Bot Stopped")

                        break

                    # region IMAGE CONTENT COMPARISON
                    print(
                        "\n***************************************************************************************\n")
                    print('\nImage Content Comparison Result')
                    # Imagework
                    imagefolderpath = Funtions.creatingTempImageFolder(filesInConfig[0], site, request)

                    # page_name = filesInConfig[0] + "/" + site
                    imagenamelst = Funtions.writingTempImages(temp_path, filesInConfig, site, request)
                    # geting temp site data
                    temp_data_list = Funtions.readingTempImages(imagefolderpath, imagenamelst)

                    orignalimagepath = Funtions.getOrignalFolderPathOfImages(filesInConfig[0], site, request)
                    orignalimagesnamelist = imagesNameInFolders(filesInConfig[0], site, request)
                    orignal_data_list = Funtions.readingTempImages(orignalimagepath, orignalimagesnamelist)
                    if Breaker >= 1:
                        print("Bot Stopped")

                        break
                    new_images_path = []
                    deleted_images_path = []

                    if len(list(set(imagenamelst))) != len(list(set(orignalimagesnamelist))):

                        new_images = list(set(imagenamelst) - set(orignalimagesnamelist))
                        deleted_images = list(set(orignalimagesnamelist) - set(imagenamelst))
                        h3_num += 1
                        page_element.append(reportPDF.doHeading(f"<br />{str(h2_num)}.{str(h3_num)} <b><u>Image "
                                                                f"Comparison Failed</u></b>", reportPDF.h3))

                        if new_images:

                            page_element.append(Paragraph('<b>New Added Images</b>', reportPDF.bodyStyle))

                            for i in new_images:
                                newimagepath = temp_base_path + "Images/" + site + "/" + i
                                new_images_path.append(newimagepath)

                                filename = Image(newimagepath, 5 * cm, 5 * cm)
                                page_element.append(filename)
                                page_element.append(Paragraph(f"<br /> {escape(i)} ", reportPDF.body_Centered))

                        if deleted_images:

                            # page_element.append(reportPDF.doHeading('<b><u>Image Comparison Failed</u></b>',
                            # reportPDF.h3))
                            page_element.append(Paragraph('<b>Following Images are deleted</b>', reportPDF.bodyStyle))

                            for i in deleted_images:
                                newimagepath = cache_base_path + "Images/" + site + "/" + i
                                deleted_images_path.append(newimagepath)

                                filename = Image(newimagepath, 5 * cm, 5 * cm)
                                page_element.append(filename)
                                page_element.append(Paragraph(f"<br /> {escape(i)} ", reportPDF.body_Centered))
                    if Breaker >= 1:
                        print("Bot Stopped")

                        break
                    defaced_img_count = 0
                    Images_names = []
                    try:
                        issue, defaced_img_count, Images_names = Image_Detailed_Comparison(filesInConfig[0], site,
                                                                                           new_images_path,
                                                                                           deleted_images_path, request)
                    except Exception as e:
                        print(e)
                        defaced_img_count = defaced_img_count + 1

                    report = report + Funtions.showReport(6, "Image  Content Comparison:", defaced_img_count) + '\n'

                    if defaced_img_count >= 1:
                        jsonObject["Image Comparison"] = "Insecure"
                        total_defacement_cnt += 1
                        total_compromised_entities.add("Image Comparison")
                        h3_num += 1
                        page_element.append(
                            reportPDF.doHeading(f"<br />{str(h2_num)}.{str(h3_num)} <b><u>Image Content "
                                                f"Comparison Failed</u></b>", reportPDF.h3))

                        for i in Images_names:
                            tempimage_path = temp_base_path + "/Images/" + site + "/" + i
                            cacheimage_path = cache_base_path + "/Images/" + site + "/" + i

                            cachefilename = Image(cacheimage_path, 5 * cm, 5 * cm)
                            tempfilename = Image(tempimage_path, 5 * cm, 5 * cm)

                            tbl_data = [
                                [cachefilename, tempfilename],
                                [Paragraph(f"<br /> {escape(i)} ", reportPDF.bodyStyle),
                                 Paragraph(f"<br /> {escape(i)} ",
                                           reportPDF.bodyStyle)],
                                [Paragraph("Original Image", reportPDF.bodyStyle), Paragraph("Altered Image",
                                                                                             reportPDF.bodyStyle)]
                            ]

                            tbl = Table(tbl_data, (8 * cm, 8 * cm))
                            page_element.append(tbl)

                        print(
                            "********************\nList of Defaced Images\n******************")

                        count = count + 1

                    # endregion

                    if Breaker >= 1:
                        print("Bot Stopped")

                        break

                    # region IMAGE META COMPARISON
                    print(
                        "\n*********************************************************************************\n")
                    print('\nImage Meta Comparison Result')
                    try:
                        result = Funtions.combiningAllImageDifference(orignal_data_list, temp_data_list)
                    except:
                        result = 1
                    if result >= 1:
                        jsonObject["Image Comparison"] = "Insecure"
                        total_compromised_entities.add("Image Metadata Comparison")

                        h3_num += 1

                        page_element.append(
                            reportPDF.doHeading(
                                f"<br />{str(h2_num)}.{str(h3_num)} <b><u>Image Metadata Comparison Failed</u></b>",
                                reportPDF.h3))

                        count += 1
                    report = report + Funtions.showReport(7, "Image Meta Comparison", result) + '\n'
                    # endregion

                    # region CHECK SSL
                    print("******************************************************************************")
                    print("SSL Certificate")
                    try:
                        ls = CheckSSL.main(filesInConfig[0])
                        CheckSSL.getBeforeDate(str(ls[0]))
                        afterdate = CheckSSL.getAfterData(str(ls[0]))
                        today = date.today()
                        if afterdate > today:
                            result = 0

                        else:
                            jsonObject["SSL"] = "Insecure"
                            total_compromised_entities.add("SSL")
                            total_defacement_cnt += 1
                            h3_num += 1
                            page_element.append(
                                reportPDF.doHeading(f"<br />{str(h2_num)}.{str(h3_num)} <b><u>SSL Check Failed</u></b>",
                                                    reportPDF.h3))

                            result = 1
                            count += 1
                        report = report + Funtions.showReport(8, "SSL Certificate", result) + '\n'
                        print(
                            "\n\n------------------------------------------------------------------------------------")
                    except:
                        jsonObject["SSL"] = "Insecure"
                        total_defacement_cnt += 1
                        total_compromised_entities.add("SSL")
                        h3_num += 1
                        page_element.append(
                            reportPDF.doHeading(
                                f"<br />{str(h2_num)}.{str(h3_num)} <b><u>SSL Certificate Failed</u></b>",
                                reportPDF.h3))

                        result = 1
                        count += 1
                        report = report + Funtions.showReport2(8, "SSL Certificate", result) + '\n'
                        print(
                            "\n\n------------------------------------------------------------------------------")

                    # endregion
                    if Breaker >= 1:
                        print("Bot Stopped")
                        break
                    print("\n\n\nTotal def detected : " + str(count))
                    page_element.append(Paragraph(f"<br /><br /><b>Total Defacement Detected:</b>"
                                                  f" {str(total_defacement_cnt)}", reportPDF.bodyStyle))

                    total_defacement_detected += int(total_defacement_cnt)
                    # region REPORT AND SAVING JSON
                    print(
                        "\n\n************************************************************************************\n")
                    print("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tWeb Defacement Detection Bot Report\n")
                    # print(report)
                    print(report + "\n" + str(result_words))
                    # report = report + "\n" + str(result_words)
                    out = "Findings: \n"
                    if not result_words:
                        pass
                    else:
                        for val in result_words:
                            out = out + "\n" + val
                    report = report + "\n" + out
                    Severity = Funtions.checkSeverity(count)
                    jsonObject["Severity"] = Severity
                    jsonObject["Final_Report"] = report

                    # endregion
                    page_element.append(
                        Paragraph('<br /><br />_________________________________________________________________<br />',
                                  reportPDF.body_Centered))
                    # elements.append(PageBreak())
                    if Breaker >= 1:
                        print("Bot Stopped")
                        break
                    if total_defacement_cnt > 0:
                        h2_num += 1
                        for ele in range(len(page_element)):
                            try:
                                reportPDF.doc.multiBuild(reportPDF.elements)
                                elements.append(page_element[ele])
                            except Exception as ex:

                                elements.pop(-1)
                                elements.pop(-1)
                                elements.append(PageBreak())

                                elements.append(page_element[ele - 2])
                                elements.append(page_element[ele - 1])
                                elements.append(page_element[ele])
                                # reportPDF.doc.multiBuild(reportPDF.elements)

                    CreateFile((filesInConfig[0] + "---" + site), jsonObject, "w", request)
                    print("in loop pdf saved")
                except Exception as ex:
                    print(ex)
            print("OUT OF LOOP")
            x = {'value': "99", 'value2': "Scan Completed. Now generating report."}
            y = json.dumps(x)
            ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
            ws.send(y)
            ws.close()
            if Breaker >= 1:
                print("Bot Stopped")
                break
            # elements.append(PageBreak())
            elements.append(PageBreak())
            tbl_data = []
            for ent in total_compromised_entities:
                tbl_row = [
                    [Paragraph('', reportPDF.bodyStyle),
                     Paragraph(f"{escape(ent)}", reportPDF.bodyStyle)],
                ]
                tbl_data.append(tbl_row)

            tbl = Table(tbl_data, (15 * cm))
            style = TableStyle([

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

                ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),

                ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ])
            tbl.setStyle(style)
            graph_pos = reportPDF.graph_pos
            elements.insert(graph_pos, tbl)

            ptext = Paragraph(f'<b>Total Tested:</b> {str(total_defacement_tested)}', reportPDF.bodyStyle)
            elements.insert(graph_pos + 1, ptext)

            ptext = Paragraph(f'<b>Total Defaced:</b> {str(total_defacement_detected)}', reportPDF.bodyStyle)
            elements.insert(graph_pos + 2, ptext)

            barChart = reportPDF.make_drawing(total_defacement_tested, total_defacement_detected)
            elements.insert(graph_pos + 3, barChart)

            elements.append(reportPDF.doHeading("Conclusion", reportPDF.h1))
            ptext = Paragraph(f'Write conclusion here', reportPDF.bodyStyle)
            elements.append(ptext)

            # elements.insert(graph_pos, reportPDF.doHeading("Graph", reportPDF.h1))
            # elements.append(reportPDF.doHeading("Comparison Graph", reportPDF.h1))
            #

            # elements.append(barChart)

            # elements1 = summary_page.generateSummary(list(total_compromised_entities), total_defacement_tested,
            #                                          total_defacement_detected, filesInConfig[0])
            try:
                reportPDF.doc.multiBuild(reportPDF.elements)
            except Exception as ex:
                print(ex)
                pass

            print("File report generated")

            x = {'value': "100", 'value2': "Scan completed and report generated."}
            y = json.dumps(x)
            ws.connect(f'ws://{host_address}/ws/' + str(request.user.id) + "/")
            ws.send(y)
            ws.close()

            # region SEND MAIL
            print("********************* FULL WEBSITE SCAN COMPLETED *************************")
            if count >= 2:
                try:
                    sendmail.gmail(filesInConfig[0], reportPDF.pdf_filename, request)
                    SmsApi.sendSms(filesInConfig[0])
                except Exception as ex:
                    print(ex)
                    print("Exception in sending email.")
            # endregion
            print(
                "*********************************************************************************************\n")

            print(
                "\n===========================================================================================")

            time.sleep(300)

            if Breaker >= 1:
                print("Bot Stopped")
                break

        time.sleep(500)
        if Breaker >= 1:
            print("Bot Stopped")
            break


class Environment(enum.Enum):
    Development = 1
    Production = 2
