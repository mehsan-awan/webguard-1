from twilio.rest import Client
import datetime

def sendSms(sitename):
    try:
        subject = "Websitee name " + sitename + " excedded thresh hold its look like that yourr website has been changed."

        # Your Account SID from twilio.com/console
        account_sid = "AC7dcf11d355b7b07599fecdc4e713c300"
        # Your Auth Token from twilio.com/console
        auth_token = "c6621c7110b45fa58f55bae415d4512b"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+923448223246",
            from_="+19516665781",
            body=subject)
        print(message.sid)
    except BaseException as ex:
        print("Error in Sending SMS: SMS Limit Reached or Internet not Connected....!!")
        print("Exception is "+ str(ex))
        pass



def sendSms_Update_Notification(sitename):
    try:
        subject = "Websitee name " + sitename + ", we just fetched the latest copy at Time: " + str(datetime.datetime.now())
        # Your Account SID from twilio.com/console
        account_sid = "AC7dcf11d355b7b07599fecdc4e713c300"
        # Your Auth Token from twilio.com/console
        auth_token = "c6621c7110b45fa58f55bae415d4512b"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to="+923448223246",
            from_="+19516665781",
            body=subject)

        print(message.sid)
    except BaseException as ex:
        print("Error in Sending SMS: SMS Limit Reached or Internet not Connected....!!")
        print("Exception is "+ str(ex))
        pass

