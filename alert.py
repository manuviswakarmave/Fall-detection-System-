from twilio.rest import Client

account_sid ='AC76622ccc872b9267c835c9649a23ed77'
auth_token ='8d5f6891e58fc8f107a6de285c9c98d5'

def make_call():
    try:
            client = Client(account_sid,auth_token)

            call = client.calls.create(
                                        twiml='<Response><Say>Fall detected please provide assistance </Say></Response>',
                                        from_='+12525168217',
                                        to='+918921767709')
            print("call sent")
    except:
          print("please check your connection ")

def make_msg():
    try:
                                    client = Client(account_sid,auth_token)

                                    call = client.calls.create(
                                        twiml='<Response><Say>Person has moved out of the frame for some time and has not returned please check on them</Say></Response>',
                                        from_='+12525168217',
                                        to='+918921767709')
                                    print("message sent")
    except:
                                    pass    

 