import vlc
import time
import winsound
import numpy as np  #instalar con: pip install numpy
import cv2 #instalar con: pip install opencv-python
import win32gui

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


#cap = cv2.VideoCapture('rtsp://<username_of_camera>:<password_of_camera@<ip_address_of_camera')
#cap = cv2.VideoCapture('http://admin:usher@irv.sytes.net:8081')

#con cap = cv2.VideoCapture(0) se captura la web cam de la notebook

instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new('heavy_back_to_the_future360p.mp4')
player.set_media(media)
player.play()
player.set_fullscreen(True)

media = player.get_media()

cap = cv2.VideoCapture(0)
winname = "Camera"
cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.resizeWindow(winname, 320,180)
cv2.moveWindow(winname, 0,0) 

#Para traer al frente la toma de la camara
results = []
top_windows = []
win32gui.EnumWindows(windowEnumerationHandler, top_windows)
for i in top_windows:
 if winname in i[1]:
     camara=i[0]
     win32gui.ShowWindow(i[0],5)
     win32gui.SetForegroundWindow(i[0])
     break

frequency = 1000  # Set Frequency
duration = 200  # Set Duration To 1000 ms == 1 second

while(True):

    ret, frame = cap.read()
    cv2.imshow(winname,frame)
    
    #Para traer al frente la toma de la camara
    win32gui.SetForegroundWindow(camara) 

    #Si el video termina
    state = media.get_state()
    if str(state) == 'State.Ended':
      #Cargo una nueva pelicula
      media = instance.media_new('Relatos_Salvajes.mp4')
      player.set_media(media)
      player.play()
      #break

    k = cv2.waitKey(6) & 0xFF
    if k in [27, ord('q')]: #Salir
      break
    elif k == ord('p'): #Pausa Pelicula
      player.pause()
    elif k == ord('s'): #Sonido para probar
      winsound.Beep(frequency, duration)



cap.release()
cv2.destroyAllWindows()


