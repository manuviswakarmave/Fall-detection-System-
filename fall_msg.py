import matplotlib.pyplot as plt
import torch
import cv2
import math
from torchvision import transforms
import numpy as np
from tkinter.filedialog import askopenfile
import os
from utils.datasets import letterbox
from utils.general import non_max_suppression_kpt
from utils.plots import output_to_keypoint, plot_skeleton_kpts
from v8detection import find_cordinates
from iou import calculate_iou
from send_vid import tel_msg
from save_video import save_vid
from twilio.rest import Client
import threading
from alert import make_call,make_msg

def fall_vid(vid):



    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    weigths = torch.load('C:\\Users\\Manu\\Project Gui\\GUI\\yolov7-w6-pose.pt')
    model = weigths['model']
    model = model.half().to(device)
    _ = model.eval()


    
    
    video_path = vid
    #pass video to videocapture object
    cap = cv2.VideoCapture(video_path)
    #get video frame width
    frame_width = int(cap.get(3))

    #get video frame height
    frame_height = int(cap.get(4))

    #check if videocapture not opened
    if (cap.isOpened() == False):
        print('Error while trying to read video. Please check path again')



    #code to write a video
    vid_write_image = letterbox(cap.read()[1], (frame_width), stride=64, auto=True)[0]
    resize_height, resize_width = vid_write_image.shape[:2]
   

    out_video_name = "result"
    out = cv2.VideoWriter(f"{out_video_name}_keypoint.mp4",
                        cv2.VideoWriter_fourcc(*'mp4v'), 30,
                        (resize_width, resize_height))

    #count no of frames
    frame_count = 0
    #count total fps
    fall_datected = 0 
    flag = 0
    fall_frame = 0
    detect_flag = 0
    cordinates =[]
    #loop until cap opened or video not complete
    while(cap.isOpened):
        
        #print("Frame {} Processing".format(frame_count))
        frame_count += 1  
        #get frame and success from video capture
        ret, frame = cap.read()
        #if success is true, means frame exist
        if ret:
            
            #store frame
            orig_image = frame
            #bed detection
            if detect_flag == 0:
                cordinates = find_cordinates(frame)
                print(cordinates)
                print(len(cordinates))
                detect_flag =1 
                if not len(cordinates) == 0:

                    cordinates = cordinates[0]
                    bed_x = cordinates[0]
                    bed_y = cordinates[1]
                    bed_w = cordinates[2]
                    bed_h = cordinates[3]
                    top_left_bed = (int(bed_x-bed_w/2),int(bed_y-bed_h/2))
                    bottom_right_bed = (int(bed_x+bed_w/2),int(bed_y+bed_h/2))
                    print(top_left_bed,bottom_right_bed)
                   
            if fall_datected ==1 and fall_frame < 50:
                print("fall_frame",fall_frame)
                fall_frame += 1 
                if fall_frame == 50:
                 out.release()
                 p1 = threading.Thread(target=tel_msg)    
                 p1.start()
                 #tel_msg() 
                 fall_datected = 0
                 fall_frame = -1000 

                
                    

            #convert frame to RGB
            image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
            image = letterbox(image, (frame_width), stride=64, auto=True)[0]
            image_ = image.copy()
            image = transforms.ToTensor()(image)
            image = torch.tensor(np.array([image.numpy()]))
            
            #convert image data to device
            image = image.half().to(device)  
            
    
            
            #get predictions
            with torch.no_grad():
                output, _ = model(image)

            



            #Apply non max suppression
            output = non_max_suppression_kpt(output, 0.5, 0.65, nc=model.yaml['nc'], nkpt=model.yaml['nkpt'], kpt_label=True)
            output = output_to_keypoint(output)
            im0 = image[0].permute(1, 2, 0) * 255
            im0 = im0.cpu().numpy().astype(np.uint8)
            
            #reshape image format to (BGR)
            im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)
            empty = not np.any(output)
                    
            if empty:
                print(frame_count)
                cv2.putText(im0, 'Person Not Detected', (11, 100), 0, 1, [0, 0, 2550], thickness=3, lineType=cv2.LINE_AA)
                frame_count = frame_count + 1 
                if frame_count % 5000 == 0:
                    p2 = threading.Thread(target=make_msg)    
                    p2.start()
                    #make_msg()
                   


                    
                
            else:
                frame_count = 0
                

            for idx in range(output.shape[0]):
                #plot_skeleton_kpts(im0, output[idx, 7:].T, 3)
                xmin, ymin = (output[idx, 2]-output[idx, 4]/2), (output[idx, 3]-output[idx, 5]/2)
                xmax, ymax = (output[idx, 2]+output[idx, 4]/2), (output[idx, 3]+output[idx, 5]/2)

                left_shoulder_y= output[idx][23]
                left_shoulder_x= output[idx][22]
                left_shoulder_conf= output[idx][24]

                right_shoulder_y= output[idx][26]
                
                left_body_y = output[idx][41]
                left_body_x = output[idx][40]
                left_body_conf = output[idx][42]
                right_body_y = output[idx][44]

                len_factor = math.sqrt(((left_shoulder_y - left_body_y)**2 + (left_shoulder_x - left_body_x)**2 ))

                left_foot_y = output[idx][53]
                left_foot_conf = output[idx][54]
                right_foot_y = output[idx][56]

                #print(left_body_conf,left_shoulder_conf,left_foot_conf)
                #print(output[0].shape)
                
                if left_shoulder_y > left_foot_y - len_factor and left_body_y > left_foot_y - (len_factor / 2) and left_shoulder_y > left_body_y - (len_factor / 2) and (left_body_conf > 0.3) and (left_foot_conf > 0.3):
                

                    if not len(cordinates) == 0:
                        box_cordinates = [xmin,ymin,xmax,ymax]
                        bed_cordnates = [top_left_bed[0],top_left_bed[1],bottom_right_bed[0],bottom_right_bed[1]]
                        #print(box_cordinates,bed_cordnates)
                        iou = calculate_iou(box_cordinates,bed_cordnates)
                       # print(iou)

                        if iou >= 0.15:
                            cv2.rectangle(im0,(int(xmin), int(ymin)),(int(xmax), int(ymax)),color=(0, 255, 0),
                            thickness=5,lineType=cv2.LINE_AA)
                            cv2.putText(im0, 'Sleeping pose detected', (11, 100), 0, 1, [0, 255, 0], thickness=3, lineType=cv2.LINE_AA)
                        else:
                            cv2.rectangle(im0,(int(xmin), int(ymin)),(int(xmax), int(ymax)),color=(0, 0, 255),
                            thickness=5,lineType=cv2.LINE_AA)
                            cv2.putText(im0, 'Person Fell down', (11, 100), 0, 1, [0, 0, 2550], thickness=3, lineType=cv2.LINE_AA)
                            fall_datected = 1  
                            if flag == 0:
                                flag = 1
                                p3 = threading.Thread(target=make_call)    
                                p3.start()
                              
                                  
                            

                        

                    else:

                    
                
                        #Plotting key points on Image
                        cv2.rectangle(im0,(int(xmin), int(ymin)),(int(xmax), int(ymax)),color=(0, 0, 255),
                            thickness=5,lineType=cv2.LINE_AA)
                        cv2.putText(im0, 'Person Fell down', (11, 100), 0, 1, [0, 0, 2550], thickness=3, lineType=cv2.LINE_AA)
                        fall_datected=1
                        if flag == 0:
                                flag = 1
                                p4 = threading.Thread(target=make_call)    
                                p4.start()
                                
                          

                
                            
                
                
                                
                #add FPS on top of video
                #cv2.putText(im0, f'FPS: {int(fps)}', (11, 100), 0, 1, [255, 0, 0], thickness=2, lineType=cv2.LINE_AA)
           
            cv2.imshow('' , im0)
            out.write(im0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            if fall_datected == 1 and fall_frame < 50 and fall_frame > 1:
                 out.release()
                 tel_msg()

            break

    cap.release()
    cv2.destroyAllWindows()
    #avg_fps = total_fps / frame_count
    #print(f"Average FPS: {avg_fps:.3f}")
        
