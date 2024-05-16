from twilio.rest import Client

account_sid ='********************'
auth_token ='************'

def make_call():
    try:
            client = Client(account_sid,auth_token)

            call = client.calls.create(
                                        twiml='<Response><Say>Fall detected please provide assistance </Say></Response>',
                                        from_='********',
                                        to='*********')
            print("call sent")
    except:
          print("please check your connection ")

def make_msg():
    try:
                                    client = Client(account_sid,auth_token)

                                    call = client.calls.create(
                                        twiml='<Response><Say>Person has moved out of the frame for some time and has not returned please check on them</Say></Response>',
                                        from_='********',
                                        to='*******')
                                    print("message sent")
    except:
                                    pass    

 
