from ftplib import FTP, error_perm
import os.path, os

# ftp = FTP('ftp.lynx-infosec.com')
# ftp.login(user='lynxinfo@ncsael.lynx-infosec.com', passwd='d6v9,Jy%C-@1')
#
# folder_name = "website"  # folder to be uploaded


def ftp_login(server, username, password):
    ftp = FTP(server)
    ftp.login(user=username, passwd=password)
    return ftp


def ftp_logout(ftp):
    ftp.quit()


def upload_files(ftp, folder_path):
    for name in os.listdir(folder_path):
        print("******************* Uploading file via ftp *******************")
        print(name)
        localpath = os.path.join(folder_path, name)
        if os.path.isfile(localpath):
            # print("STOR", name, localpath)
            ftp.storbinary('STOR ' + name, open(localpath, 'rb'))
        elif os.path.isdir(localpath):
            # print("MKD", name)

            try:
                ftp.mkd(name)

            # ignore "directory already exists"
            except error_perm as e:
                if not e.args[0].startswith('550'):
                    pass

            # print("CWD", name)
            ftp.cwd(name)
            upload_files(ftp, localpath)
            # print("CWD", "..")
            ftp.cwd("..")


if __name__ == '__main__':
    path = 'website'  # path of folder tobe uploaded

    ftp = ftp_login('ftp.lynx-infosec.com', 'lynxinfo@ncsael.lynx-infosec.com', 'd6v9,Jy%C-@1')
    upload_files(ftp, path)
