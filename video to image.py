import cv2
import os


vid = cv2.VideoCapture("video.mp4")
fps=vid.get(cv2.CAP_PROP_FPS)
print(fps)

try:

    if not os.path.exists('data'):
        os.makedirs('data')


except OSError:
    print('Error: Creating directory of data')
n=0
i=0
currentFrame = 0

while (True):

  
    success, frame = vid.read()

    if success:
        
        if ( n)%(2*fps)==0:
            resize = cv2.resize(frame, (300,300))
            name = './data/frame' + str(currentFrame) + '.jpg'
            print('Creating...' + name)

        
            cv2.imwrite(name, frame)
            i+=1
            currentFrame+=1
        n+=1

        

    else:
        break


vid.release()
