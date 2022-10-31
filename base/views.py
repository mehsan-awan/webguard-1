import json
import os
import subprocess
import threading
import time

import websocket as websocket_client
from django.conf import settings as download_settings
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, password_validation
from django.urls import reverse_lazy
from django import forms
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from . import extensions, Funtions, sendmail
from .OrignalData2 import getFullSiteNameWithHTTP, combine2
from .crawler import crawler
from .ip_tracker import ip_based_map
from .ftp_uploader import upload_files, ftp_login, ftp_logout
import socket
import requests as req

# Create your views here.
Bot_Running_Status = 0


class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.TextInput(attrs={'autocomplete': 'username', 'placeholder': 'Username', 'size': 30}),

    )
    password1 = forms.CharField(
        label=_(""),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password', 'size': 30}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_(""),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password', 'size': 30}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    email = forms.EmailField(
        required=True,
        label=_(""),
        widget=forms.TextInput(attrs={'autocomplete': 'email', 'placeholder': 'Email', 'size': 30}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


def GetCodeDirectory(request):
    current_user = request.user.username
    path = f"{os.getcwd()}/base/Clients/{current_user}/"
    return str(path)


def GetBasePath():
    path = f"{os.getcwd()}/base/"
    return str(path)


def is_connected(hostname):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception as ex:
        print(ex)
    return False


@login_required(login_url='/login/')
def register(request):
    if str(request.user) != "admin":
        return redirect('index')
    elif request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            path = f"{os.getcwd()}/base/Clients/{username}/"
            # path_to_Create = os.path.join(os.getcwd() + "/UI/app/home/Clients/", str(username))

            try:
                if not os.path.exists(path):
                    os.makedirs(path, 0o777)
                    os.makedirs(os.path.join(path, "Cache"), 0o777)
                    os.makedirs(os.path.join(path, "Logs"), 0o777)
                    os.makedirs(os.path.join(path, "Defaced_Images"), 0o777)
                    os.makedirs(os.path.join(path, "subdomains"), 0o777)
                    os.makedirs(os.path.join(path, "Reports"), 0o777)
                    os.makedirs(os.path.join(path, "temp"), 0o777)
                    os.makedirs(os.path.join(path, "revert"), 0o777)

                    with open(path + "/emailalert.txt", "w") as f:
                        f.close()
                    with open(path + "/Config", "w") as f:
                        f.close()

                    print("Successfully created the directory %s " % path)
            except Exception as e:
                print(e)

            # user = authenticate(username=username, password=raw_password)
            return redirect(reverse_lazy('admin'))
    else:
        form = MyUserCreationForm()
    return render(request, 'login/register.html', {'form': form})


@login_required(login_url='/login/')
def delete_user(request):
    if str(request.user) != "admin":
        return redirect('index')
    elif request.method == 'POST':
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            user.delete()
            print(username)
            path = f"{os.getcwd()}/base/Clients/{username}/"

            try:
                if os.path.exists(path):
                    # os.rmdir(path)
                    cmd = 'rm -R ' + path
                    # cmd = 'head -8 /var/log/auth.log'
                    proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    (out, err) = proc.communicate()
                    out = out.decode(encoding="utf-8")
                    err = err.decode(encoding="utf-8")
                    print("Successfully Deleted User Directory")
            except Exception as e:
                print(e)

            return render(request, 'login/delete.html', {"success": f"User {username} deleted successfully!!"})
        except Exception as ex:
            print(ex)
            print("User Does not Exist")
            return render(request, 'login/delete.html', {"error": f"User {username} does not exist!!"})

    else:
        return render(request, 'login/delete.html')


@login_required(login_url='/login/')
def deactivate_user(request):
    page = "Deactivate"
    if str(request.user) != "admin":
        return redirect('index')
    elif request.method == 'POST':
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            print(username)
            user.is_active = False
            user.save()
            return render(request, 'login/deactivate.html',
                          {"page": page, "success": f"User {username} deactivated successfully!!"})
        except Exception as ex:
            print(ex)
            print("User Does not Exist")
            return render(request, 'login/deactivate.html',
                          {"page": page, "error": f"User {username} does not exist!!"})

    else:
        return render(request, 'login/deactivate.html', {"page": page, })


@login_required(login_url='/login/')
def activate_user(request):
    page = "Activate"
    if str(request.user) != "admin":
        return redirect('index')
    elif request.method == 'POST':
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            print(username)
            user.is_active = True
            user.save()
            return render(request, 'login/deactivate.html',
                          {"page": page, "success": f"User {username} activated successfully!!"})
        except Exception as ex:
            print(ex)
            print("User Does not Exist")
            return render(request, 'login/deactivate.html',
                          {"page": page, "error": f"User {username} does not exist!!"})

    else:
        return render(request, 'login/deactivate.html', {"page": page, })


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        form.new_password1 = forms.CharField(
            label=_("New password"),
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
            strip=False,
            help_text=password_validation.password_validators_help_text_html(),
        )

        form.new_password12 = forms.CharField(
            label=_("Confirm password"),
            strip=False,
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        )

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        form.new_password1 = forms.CharField(
            label=_("New password"),
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
            strip=False,
            help_text=password_validation.password_validators_help_text_html(),
        )

        form.new_password12 = forms.CharField(
            label=_("Confirm password"),
            strip=False,
            widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        )
    return render(request, 'login/change_password.html', {
        'form': form
    })


@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login/')
def admin(request):
    if str(request.user) != "admin":
        return redirect('index')
    else:
        path = GetBasePath()

        with open(path + "siteslist.txt") as file:
            file_data = file.readlines()
            file.close()
        # print(file_data)
        file_data = sorted(list(set(file_data)))
        user = []
        user_site = []
        for i in file_data:
            user.append(i.split(":")[0])
            user_site.append(i.split(":")[1])

        zip_list = zip(user, user_site)
        no_of_user = len(os.listdir(f"{path}Clients"))
        admin_stats = [no_of_user, len(user_site)]

        if "id" in request.GET:
            site = request.GET["id"]
            try:
                site_data = (req.get("https://" + site + "/webdefacement/ips.txt").content.decode("utf-8"))

                site_data = site_data.split("\n")
                site_data = (list(set(site_data)))
                site_data1 = []

                for i in site_data:
                    if i != "":
                        site_data1.append(i)

                ip_map = ip_based_map()
                city_list = ip_map.plot_map(site_data1)
                zip_list_ips = zip(site_data1, city_list)
            except Exception as ex:
                print(ex)
                return render(request, 'admin.html', {"error": f'Unable to connect to "{site}" server to get logs !!',
                                                      "zip_list": zip_list,
                                                      "user_site": user_site,
                                                      "admin_stats": admin_stats})

            file = open(path + 'ips_list.txt', 'w')
            for i in site_data1:
                file.write(i + "\n")
            file.write(site)
            file.close()

            return render(request, 'admin.html', {"zip_list_ips": zip_list_ips,
                                                  "zip_list": zip_list,
                                                  "data": site,
                                                  "admin_stats": admin_stats,
                                                  "site_data": site_data1})


        else:

            return render(request, 'admin.html',
                          {"zip_list": zip_list, "user_site": user_site, "admin_stats": admin_stats})


@login_required(login_url='/login/')
def fetch(request, user_id):
    a = request.headers._store["host"][1]
    print(a)

    return render(request, 'fetch.html')


@login_required(login_url='/login/')
def subdomains(request):
    if request.method == "POST":
        domain = request.POST.get("base_url")
        print(domain)
        if "http" in domain:
            domain = domain.split('/')[2]
        if "www" in domain:
            domain = domain[4:]
        print(domain)
        output_file = "subdomains." + domain + ".txt"
        path1 = GetCodeDirectory(request)
        dir_path = path1 + "/subdomains/"

        path = os.path.join(dir_path, output_file)

        if output_file in os.listdir(dir_path):
            with open(path, "r") as f:
                discovered_domains = f.readlines()
                f.close()
            with open(path1 + "Config", 'w') as f:
                for url in discovered_domains:
                    f.write(url + '\n')
                f.close()

        else:
            crawl_handler = crawler()
            fullsitename = getFullSiteNameWithHTTP(domain)
            crawl_handler.crawl(fullsitename[0])

            internal = crawl_handler.internal_urls
            external = crawl_handler.external_urls
            file_link = []
            subdomain = set()
            for internal_link in internal:
                if internal_link.split(".")[-1] in ["jpg", "docx", "doc", "txt", "docs", "jpeg", "png", "PNG", "pdf",
                                                    "gif", "tiff", "svg"]:
                    file_link.append(internal_link)
                else:
                    a = internal_link.split("/")
                    if a[2] != str(domain):
                        link = a[2].lower()
                        subdomain.add(link)
            discovered_domains = list(subdomain)

            with open(path, 'w') as f:
                for url in discovered_domains:
                    f.write(url + '\n')
                f.close()
            with open(path1 + "Config", 'w') as f:
                f.write(domain + '\n')
                for url in discovered_domains:
                    f.write(url + '\n')
                f.close()

        return redirect('bot_conf')

    return render(request, 'subdomains.html')


@login_required(login_url='/login/')
def StopBot(request):
    internet_status = is_connected("one.one.one.one")
    if internet_status:
        # p.terminate()
        print("Stopping Code...!!")
        print("Internet Connected......!!")
        Bot_Running_Status = 0
        extensions.Stop_Bot()
    else:
        print("Error: Internet is not working....!!")
    jsonReturnObject = {
        "Message": "Success",
        "StatusCode": 200,
        "Result": "B8"
    }
    return JsonResponse(jsonReturnObject)


@login_required(login_url='/login/')
def StartBot(request):
    internet_status = is_connected("one.one.one.one")
    # remote_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    # port_number = request.META['SERVER_PORT']
    try:
        if internet_status:
            print("Internet Connected......!!")
            global Bot_Running_Status

            Bot_Running_Status = 1
            extensions.test_socket(request)
            print("Internet Connected......!!")
        else:
            print("Error: Internet is not working....!!")
    except BaseException as e:
        print(e)

    ############################
    jsonReturnObject = {
        "Message": "Success",
        "StatusCode": 200,
        "Result": ""
    }
    return JsonResponse(jsonReturnObject)
    ############################


@login_required(login_url='/login/')
def revertBackendChanges(request):
    # if request.method == 'POST':
    #     ftp_backend_server = request.POST.get("ftp_backend_server")
    #     ftp_backend_user = request.POST.get("ftp_backend_user")
    #     ftp_backend_pass = request.POST.get("ftp_backend_pass")
    print("Revert Back called")
    if request.is_ajax:
        updatedData = json.loads(request.body.decode('UTF-8'))
        back_website = updatedData["back_website"]
        ftp_backend_server = updatedData["ftp_backend_server"]
        ftp_backend_user = updatedData["ftp_backend_user"]
        ftp_backend_pass = updatedData["ftp_backend_pass"]
        print(ftp_backend_pass, ftp_backend_user, ftp_backend_server)
        # Call FTP Function
        path = GetCodeDirectory(request) + "revert/" + back_website + "/backend"
        print(path)
        ftp = ftp_login(ftp_backend_server, ftp_backend_user, ftp_backend_pass)
        upload_files(ftp, path)
        ftp_logout(ftp)

    jsonReturnObject = {
        "StatusCode": 200,
    }
    return JsonResponse(jsonReturnObject)


@login_required(login_url='/login/')
def revertFrontendChanges(request):
    # if request.method == 'POST':
    #     ftp_frontend_server = request.POST.get("ftp_frontend_server")
    #     ftp_frontend_user = request.POST.get("ftp_frontend_user")
    #     ftp_frontend_pass = request.POST.get("ftp_frontend_pass")

    print("Revert Front called")
    if request.is_ajax:
        updatedData = json.loads(request.body.decode('UTF-8'))
        front_website = updatedData["front_website"]
        ftp_frontend_server = updatedData["ftp_frontend_server"]
        ftp_frontend_user = updatedData["ftp_frontend_user"]
        ftp_frontend_pass = updatedData["ftp_frontend_pass"]
        print(ftp_frontend_pass, ftp_frontend_user, ftp_frontend_server)
        # Call FTP Function
        path = GetCodeDirectory(request) + "revert/" + front_website + "/frontend"
        print(path)
        ftp = ftp_login(ftp_frontend_server, ftp_frontend_user, ftp_frontend_pass)
        upload_files(ftp, path)
        ftp_logout(ftp)

    jsonReturnObject = {
        "StatusCode": 200,
    }
    return JsonResponse(jsonReturnObject)



@login_required(login_url='/login/')
def revertChanges(request):
    if request.method == 'POST':
        ftp_backend_server = request.POST.get("ftp_backend_server")
        ftp_backend_user = request.POST.get("ftp_backend_user")
        ftp_backend_pass = request.POST.get("ftp_backend_pass")
    return render(request, 'revert.html')


@login_required(login_url='/login/')
def GetTrustedConfig(request):
    url = request.GET["url"]
    Funtions.clearCacheOneWebsite(url, request)
    crawl_handler = crawler()
    if "http" in url:
        crawl_handler.crawl(url)
    else:
        # url1 = "https://" + url
        fullsitename = getFullSiteNameWithHTTP(url)
        print("fullsitename")
        print(fullsitename)
        crawl_handler.crawl(fullsitename[0])

    internal = crawl_handler.internal_urls
    external = crawl_handler.external_urls

    file_link = []
    pages_link = set()

    # drop link if it is a image or file
    for internal_link in internal:
        if internal_link.split(".")[-1] in ["jpg", "docx", "doc", "txt", "docs", "jpeg", "png", "PNG", "pdf",
                                            "gif", "tiff", "svg"]:
            file_link.append(internal_link)
        else:
            a = internal_link.split("/")
            if a[2] == str(url):
                # link = internal_link.lower()
                link = internal_link
                if link[-1] == "/":  # remove / at the end if exist
                    link = link[:-1]
                link = link.split("//")[1]
                if "tel:" not in link and "mail:" not in link:
                    pages_link.add(link)

    for page in list(pages_link):
        try:
            print(f"URL UNDER SCAN \n***************************{page}*************************")
            lst = combine2(page, request)
            if lst:
                for paths in lst:
                    Funtions.savingDomDataForOrignal(paths)
        except Exception as ex:
            print(ex)
    sendmail.gmailfornewtrusted(url, request)
    print("********************** TRUSTED CONFIGURATION SAVED *************************************")
    returnOutput = {
        "Message": "Success",
        "StatusCode": 200,
        "Urls": url
    }
    return JsonResponse(returnOutput)


@login_required(login_url='/login/')
def GetBotValues(request):
    path = GetCodeDirectory(request)
    fileObj = open(path + "Config", "r")
    file_data = fileObj.read()
    return_data = {
        "urls": file_data

    }
    return JsonResponse(return_data)
    # else:
    #     return None


@login_required(login_url='/login/')
def GetResources(request):
    if request.is_ajax():
        cpu = extensions.CPUusage()
        memory = extensions.memoryusage()
        network = extensions.Networ_Stats()
        HDD = extensions.HDD_Usage()

        path1 = GetCodeDirectory(request)

        # Checking the total urls count in Config file

        with open(path1 + 'Config') as f:
            import os
            text = f.readlines()

            size = len(text)
            hold = os.stat(path1 + 'Config')

        import datetime
        statbuf = hold.st_atime
        statbuf = datetime.datetime.fromtimestamp(statbuf / 1e3)
        global Bot_Running_Status
        if Bot_Running_Status == 1:
            send = 1
        else:
            send = 0

        scans_per_mintues = extensions.Scans_Per_Minutes()
        HDD_Total_Used = str(HDD[1]) + " / " + str(HDD[0]) + " GB"
        HDD_Percentage = str(HDD[2]) + str(" %")
        returnObject = {
            "CPU": {
                "Percentage": cpu[0],
                "Frequence": cpu[1]
            },
            "Memory": {
                "Total": memory[0],
                "Used": memory[0] - memory[1]
            },
            "Network": {
                "Total": network[0],
                "Active": network[1]
            },
            "Header_Stats": {
                "Total_Files": size,
                "Config_Last_Modified": statbuf,
                "Bot_Status": send,
                "Scans_per_minutes": scans_per_mintues,
                "HDD_Total_Used": HDD_Total_Used,
                "HDD_Percentage": HDD_Percentage
            }
        }
        return JsonResponse(returnObject)
    else:
        return None


@csrf_exempt
@login_required(login_url='/login/')
def SaveBotValues(request):
    a = request.body
    current_user = request.user.username
    fileObj = open(GetCodeDirectory(request) + "Config", "w")
    path2 = GetBasePath()

    fileObj.write(str(a.decode('utf-8')))
    fileObj.close()

    urls = []

    with open(path2 + "siteslist.txt", "r") as f:
        file_data = f.readlines()
        f.close()
    for i in file_data:
        if str(current_user) != i.split(":")[0]:
            urls.append(i)

    with open(path2 + "siteslist.txt", "w") as f:
        data = a.decode('utf-8')
        data = data.splitlines()
        for i in data:
            user_site = str(current_user) + ":" + i + "\n"
            f.writelines(user_site)

        f.writelines(urls)
        f.close()

    with open(GetCodeDirectory(request) + "Config", "r") as f:
        lines = f.readlines()
        f.close()

    Count = len(lines)
    returnObject = {
        "Header_Stats": {
            "New_Website_Count": Count
        }
    }
    return JsonResponse(returnObject)
    # else:
    #     return None


@login_required(login_url='/login/')
def GetUrls(request):
    # if request.is_ajax():
    path = GetCodeDirectory(request)
    file = open(path + "Config", "r")
    urls = file.read()
    returnOutput = {
        "Message": "Success",
        "StatusCode": 200,
        "Urls": urls
    }
    return JsonResponse(returnOutput)
    # else:
    #     return None


@login_required(login_url='/login/')
def bot_conf(request):
    return render(request, 'maps.html')


@login_required(login_url='/login/')
def logsResults(request):
    return render(request, 'profile.html')


@login_required(login_url='/login/')
def download_report(request):
    path = GetCodeDirectory(request) + "Reports/"
    if "id" in request.GET:
        filename = request.GET["id"]
        file_path = path + filename
        file_path = os.path.join(download_settings.MEDIA_ROOT, file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404

    print("Downloaded")
    all_reports = os.listdir(path)
    reports = []
    for report in all_reports:
        name = report.split("$")
        site = name[0]
        date = name[1]
        time = name[2]
        report_name = name[3]
        my_tuple = (report_name, site, date, time, report)
        reports.append(my_tuple)

    return render(request, 'download_report.html', {"reports": reports})


@login_required(login_url='/login/')
def GetLogs(request):
    import glob
    path = GetCodeDirectory(request) + "Logs"

    # if extensions.GetEnvironmentType() == extensions.Environment.Production.name:
    #     path = extensions.GetCodeDirectory() + "Logs"
    # else:
    #     path = extensions.GetAlternateCodeDirectory() + "Logs"

    allfiles = glob.glob(path + '/*')
    fileText = []
    for x in allfiles:
        data = open(x, "r")
        fileData = data.read()
        filename = os.path.basename(x)
        datetime = filename[-23:-4]
        filename = filename[:-24]
        fileText.append({"FileName": filename, "DateTime": datetime, "FileData": json.loads(fileData)})
    jsonReturnObject = {
        "Message": "Success",
        "StatusCode": 200,
        "Result": fileText
    }
    return JsonResponse(jsonReturnObject)


@login_required(login_url='/login/')
def GetLogsTry(request):
    import glob
    path = GetCodeDirectory(request) + "Logs"

    allfiles = glob.glob(path + '/*')

    fileText = []
    for x in allfiles:
        data = open(x, "r")
        fileData = data.read()
        filename = os.path.basename(x)
        datetime = filename[-23:-4]
        filename = filename[:-24]
        fileText.append({"FileName": filename, "DateTime": datetime, "FileData": json.loads(fileData)})
    # fileText.append({"Images":images})
    jsonReturnObject = {
        "Message": "Success",
        "StatusCode": 200,
        "Result": fileText
    }
    return JsonResponse(jsonReturnObject)


@login_required(login_url='/login/')
def GetImageLogs(request):
    import glob
    path = GetCodeDirectory(request) + "Defaced_Images"

    allfiles = glob.glob(path + '/*')

    for x in range(0, len(allfiles)):
        allfiles[x] = os.path.basename(allfiles[x])
    jsonReturnObject = {
        "Message": "Success",
        "StatusCode": 200,
        "Result": allfiles
    }
    # print(allfiles)
    return JsonResponse(jsonReturnObject)


@login_required(login_url='/login/')
def open_def_img(request, filename):
    img_path = GetCodeDirectory(request) + "Defaced_Images/" + filename
    img = open(img_path, "rb").read()
    return HttpResponse(img, content_type="image/png")


@login_required(login_url='/login/')
def alertconf(request):
    path = GetCodeDirectory(request)
    with open(path + "emailalert.txt") as file:
        file_data = file.readlines()
        file.close()
    if request.method == "POST":
        email = request.POST.get("alert_email")
        with open(path + "emailalert.txt", "a") as file:
            file.write(email + "\n")
            file.close()
        file_data.append(email)

    if "id" in request.GET:
        try:
            rm_email = request.GET["id"]
            print(rm_email)
            stripped_data = []
            for i in file_data:
                stripped_data.append(i.strip())
            stripped_data.remove(rm_email)
            file_data = stripped_data

            # file_data = list(set(stripped_data) - set(rm_email))
            with open(path + "emailalert.txt", "w") as file:
                for element in file_data:
                    file.write(element + "\n")
                file.close()
        except Exception as ex:
            print(ex)
    return render(request, 'alertconf.html', {"data": file_data})


def error_404(request, exception):
    return render(request, 'errors/error_404.html')


def error_500(request):
    return render(request, 'errors/error_500.html')


def error_403(request, exception):
    return render(request, 'errors/error_403.html')


def error_400(request, exception):
    return render(request, 'errors/error_400.html')
