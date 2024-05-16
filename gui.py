

from fall_msg import fall_vid
from fall_cam import fall_camera
import mysql.connector

import multiprocessing


if __name__ == '__main__':
    multiprocessing.freeze_support()




import re
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

from kivy.lang import Builder
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import NoTransition
from process import check
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivy.uix.videoplayer import VideoPlayer
from plyer import filechooser
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

if __name__ == "__main__":

    
    LabelBase.register( name="SPoppins", fn_regular="C:/Users/Manu/Project Gui/Poppins/Poppins-SemiBold.ttf")
    LabelBase.register( name="RPoppins", fn_regular="C:/Users/Manu/Project Gui/Poppins/Poppins-Regular.ttf")
    LabelBase.register( name="EPoppins", fn_regular="C:/Users/Manu/Project Gui/Poppins/Poppins-ExtraLight.ttf")

     

    class UI(MDApp):
        
        email_con = "^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"
        phone_con = "^[0-9]*$"
        database = mysql.connector.connect(host="localhost", user = "root", password = "root", database = "fall_detection")
        cursor = database.cursor()
    
        
        def build(self):
            
            print("entered")
            
            
            database = mysql.connector.connect(host="localhost", user = "root", password = "root", database = "fall_detection")
            cursor = database.cursor()
            
            return Builder.load_file("gui.kv")
    
    
    

        def select_image(self):
            filechooser.filters = ["*.mp4", "*.mkv", "*.mov"]
            filechooser.open_file (on_selection=self.selected_image)
#evide algorithm - video demo
        def selected_image(self, selection):
            if selection:
                if selection[0].endswith((".mp4", ".mkv", ".mov")):
                    p1 = multiprocessing.Process(target=fall_vid,args=(selection[0],))    
                    p1.start()
                # fall_vid(selection[0])
                    #self.img_path = selection[0]
                    #print(selection[0])
                    #self.root.ids.videoplayer.source = selection[0]

                else:
                    def on_ok(button_widget):
                        self.root.ids.videoplayer.source= ""
                        image_alert.dismiss()

                    image_alert = MDDialog(title="Error", text="Please select an video file (*.mp4, *.mkv, *.mov)",
                                        buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                    text_color=self.theme_cls.primary_color, on_release=on_ok)])
                    image_alert.open()
        def check_cred(self):
            def check_in():
                    email =  self.root.ids.email_log.text
                    flag = check(email)
                    if flag:
                        self.root.manager.transition.direction = "left"
                        self.root.manager.current = "videogui"
                    else:
                        dia = MDDialog(title="Error", text="Check your email")
                        dia.open()

        def visibility(self):
            if self.root.ids.Pass.password == True:
                self.root.ids.eye.icon = "eye-outline"
                self.root.ids.Pass.password = False
            elif self.root.ids.Pass.password == False:
                self.root.ids.eye.icon = "eye-off-outline"
                self.root.ids.Pass.password = True
    
        def visibility_2(self):
            if self.root.ids.password_signup.password == True:
                self.root.ids.eye_signup.icon = 'eye-outline'
                self.root.ids.password_signup.password = False

            elif self.root.ids.password_signup.password == False:
                self.root.ids.eye_signup.icon = 'eye-off-outline'
                self.root.ids.password_signup.password = True

        def open_cam(self):
            print("pressed")
            #self.root.ids.videoplayer.source= ""
            #on_camera()
            p2 = multiprocessing.Process(target=fall_vid,args=(0,))    
            p2.start()

            #fall_vid(0)

        def send_data(self):

            user_email = self.root.ids.email_signup.text
            user_password = self.root.ids.password_signup.text
            fname = self.root.ids.name_1.text
            lname = self.root.ids.name_2.text
            pno = self.root.ids.number.text
    

            if user_email!='' and user_password != '' and fname!='' and lname!='' and pno!='':
                if re.search(self.email_con, user_email) and re.search(self.phone_con, pno) and len(pno)==10:
                    try:
                        self.cursor.execute(f"insert into users values('{user_email}','{fname}','{lname}','{int(pno)}','{user_password}')")
                        self.database.commit()

                        def on_ok_4(button_widget):
                            self.root.ids.email_signup.text = ""
                            self.root.ids.password_signup.text = ""
                            self.root.ids.name_1.text = ""
                            self.root.ids.name_2.text = ""
                            self.root.ids.number.text = ""
                            screen = self.root.ids.scr
                            screen.current = 'login'
                            alert_z.dismiss()

                        alert_z = MDDialog(title="Message", text="Account created successfully! ",
                                                buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                                        text_color=self.theme_cls.primary_color,
                                                                        on_release=on_ok_4)])
                        alert_z.open()
                        
                    except:
                        def on_ok_3(button_widget):
                            self.root.ids.email_signup.text = ""
                            self.root.ids.password_signup.text = ""
                            self.root.ids.name_1.text = ""
                            self.root.ids.name_2.text = ""
                            self.root.ids.number.text = ""
                            screen = self.root.ids.scr
                            screen.current = 'login'
                            alert_o.dismiss()

                        alert_o = MDDialog(title="Error", text="A user with the email already exist!",
                                                buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                                        text_color=self.theme_cls.primary_color,
                                                                        on_release=on_ok_3)])
                        alert_o.open()

                
                else:
                    def on_ok_2(button_widget):
                        self.root.ids.email_signup.text = ""
                        self.root.ids.number.text = ""
                        alert_t.dismiss()

                    alert_t = MDDialog(title="Error", text="Please verify your email / phone number !",
                                            buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                                    text_color=self.theme_cls.primary_color,
                                                                    on_release=on_ok_2)])
                    alert_t.open()

            else:
                def on_ok_1(button_widget):
                    alert_n.dismiss()

                alert_n = MDDialog(title="Error", text="Please Fill all details!",
                                        buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                                text_color=self.theme_cls.primary_color,
                                                                on_release=on_ok_1)])
                alert_n.open()

        def receive_data(self):
            user_email = self.root.ids.email_log.text
            user_password = self.root.ids.Pass.text
            self.cursor.execute("select * from users")
            email_list = []

            for i in self.cursor.fetchall():
                email_list.append(i[0])
            

            if user_email in email_list and user_email!="":
                self.cursor.execute(f"select password from users where email_id='{user_email}'")
                for j in self.cursor:
                    if user_password == j[0]:
                        self.root.ids.email_log.text = ""
                        self.root.ids.Pass.text = ""
                        self.cursor.execute(f"select email_id, first_name, last_name, phone_no from users where email_id='{user_email}'")
                        for k in self.cursor:
                            email_id = k[0]
                            user = k[1] + " " +k[2] 
                            num = k[3]
                        
                        self.set_gui(email_id, user, num)
                        screen = self.root.ids.scr
                        screen.current = 'videogui'
                                        
                        print("Successful!")
                    else:
                        def on_ok_5(button_widget):
                            self.root.ids.email_log.text = ""
                            self.root.ids.Pass.text = ""
                            alert_a.dismiss()

                            alert_a = MDDialog(title="Error", text="Incorrect password!",
                                                    buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                                            text_color=self.theme_cls.primary_color,
                                                                            on_release=on_ok_5)])
                            alert_a.open()
                            screen = self.root.ids.scr
                            screen.current = 'login'    
            else: 
                def on_ok_6(button_widget):
                    self.root.ids.email_log.text = ""
                    self.root.ids.Pass.text = ""
                    alert_b.dismiss()

                alert_b = MDDialog(title="Error", text="User doesn't exist!",
                                        buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                                text_color=self.theme_cls.primary_color,
                                                                on_release=on_ok_6)])
                alert_b.open()
                screen = self.root.ids.scr
                screen.current = 'login' 

        def check_user(self):
            user_email = self.root.ids.email_forgot.text
            self.cursor.execute("select * from users")
            email_list = []

            for i in self.cursor.fetchall():
                email_list.append(i[0])
            

            if user_email in email_list and user_email!="":
                def on_ok_8(button_widget):
                    self.root.ids.email_forgot.text = ""
                    #twilio code....
                    alert_d.dismiss()

                alert_d= MDDialog(title="Error", text="Password has been sent, go back and login",
                                        buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                                text_color=self.theme_cls.primary_color,
                                                                on_release=on_ok_8)])
                alert_d.open() 
            else: 
                def on_ok_7(button_widget):
                    self.root.ids.email_forgot.text = ""
                    alert_c.dismiss()

                alert_c = MDDialog(title="Error", text="User doesn't exist!",
                                        buttons=[MDFlatButton(text="OK", theme_text_color="Custom",
                                                                text_color=self.theme_cls.primary_color,
                                                                on_release=on_ok_7)])
                alert_c.open() 
        
        def set_gui(self, email, name, number):
            self.root.ids.user_name_gui.text = name
            self.root.ids.email_gui.text = email
            self.root.ids.phone_no_gui.text = str(number)
            print(email, name, number)
        
        def clear_screen(self):
            self.root.ids.user_name_gui.text = ""
            self.root.ids.email_gui.text = ""
            self.root.ids.phone_no_gui.text = ""
            self.root.ids.videoplayer.source= ""

    UI().run()

    





