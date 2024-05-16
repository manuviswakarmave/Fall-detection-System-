import telepot
import moviepy.editor as mp

def tel_msg():
  

        try:

                token = '6046652745:AAGFB3xAOjBc__9XmgCXk1WF40xGmW3lcbo' # telegram token
                receiver_id = 587445552 # https://api.telegram.org/bot<TOKEN>/getUpdates

                clip = mp.VideoFileClip(r"C:\\Users\\Manu\\Project Gui\\GUI\\result_keypoint.mp4")
                length = clip.duration
                start = clip.duration - 8
                cropped = clip.subclip(start,length)
                cropped.write_videofile(r"C:\\Users\\Manu\\Project Gui\\GUI\\fall_detected.mp4")


                bot = telepot.Bot(token)

                bot.sendMessage(receiver_id, 'Fall Detected , Please provide assistance.') # send a activation message to telegram receiver id

               
                bot.sendVideo(receiver_id, video=open('C:\\Users\\Manu\\Project Gui\\GUI\\fall_detected.mp4', 'rb')) # send message to telegram
                print("message sent")
        except:
                print("some error occured while sending video message ")