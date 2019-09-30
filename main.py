# enconding: utf-8
import vlc #pip install python-vlc
import time
import sys
import os
import winsound
import random
import tensorflow as tf
import xml.etree.ElementTree as ET
import numpy as np  #pip install numpy
import cv2 #pip install opencv-python
import win32gui #conda install -c anaconda pywin32y
from main_argument_parser import ExpoArgumentParser
from utils.queryvideo import QueryTrailer


# DEFAULT_CAMERA = 'rtsp://<username_of_camera>:<password_of_camera@<ip_address_of_camera'
# DEFAULT_CAMERA = 'http://admin:usher@irv.sytes.net:8081'
# DEFAULT_CAMERA = '0' se captura la web cam de la notebook
DEFAULT_CAMERA = '0'

# DEFAULT_BACK_COLOR GRAY "cv2.COLOR_BGR2GRAY"
# DEFAULT_BACK_COLOR HSV "cv2.COLOR_BGR2HSV"
# DEFAULT_BACK_COLOR RGB "cv2.COLOR_BGR2RGB"
DEFAULT_BACK_COLOR = "cv2.COLOR_BGR2GRAY"

DEFAULT_THRESHOLD = 0.60
DEFAULT_WINDOWS_NAME = 'Camera'
DEFAULT_LABELS = 'c:/example/labels.pbtxt'
DEFAULT_FROZEN = 'c:/example/frozen.pb'
DEFAULT_INPUT = 'c:/example/in'
DEFAULT_XML_BOXES = 'c:/example/boxes.xml'

MAX_NUM_CLASSES = 2
DEFAULT_FREQUENCY = 1000 # Set Frequency
DEFAULT_DURATION = 200 # Set Duration To 1000 ms == 1 second
VIDEO_EXTENSION = ['.mov', '.avi', '.mpeg', '.mp4']


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_list_videos(video_input, video_filetype):
  videos_db = []
  for root, subdirs, files in os.walk(video_input):
    for file in files:
      if os.path.splitext(file)[1].lower() in video_filetype:
        video = QueryTrailer(os.path.join(root, file))
        videos_db.append(video)
  if len(videos_db) == 0:
        print('No existen videos')
  return videos_db


def set_camera(stream_origin, winname):
  cap = cv2.VideoCapture(stream_origin)
  cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
  cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  cv2.resizeWindow(winname, 320,180)
  cv2.moveWindow(winname, 0,0)
  return cap


def verificar_personas_sentadas(boxes, boxes_xml):
      
  # Codigo para leer el XML
  root = ET.parse(boxes_xml).getroot()

  boxes_from_file = []
  # Mi cabeza no da mas
  # https://stackoverflow.com/questions/1912434/how-do-i-parse-xml-in-python
  for form in root.findall("./object/bndbox/"):
      x=(form.attrib)
      z=list(x)
      for i in z:
        # hay que ver como traer los datos del xml que es una pavada pero hay que devuguear para no cagarla aca y est esta todo roto
        boxes_from_file.append(x[i])


  # Codigo para superponer las Box con las levantadas de un archivo
  for box in boxes:
    # el if de abajo tiene que tener la logica para la superposicion de boxes con la db que hay que traer
    if 1:
      return True
    else:
      return False

def main():
  
  # Tensorflow
  detection_graph = tf.Graph()

  # Lista de Videos
  trailers_cine_db = get_list_videos(DEFAULT_INPUT, VIDEO_EXTENSION)

  # Creamos nuestro Stream de Video para TF
  cap = set_camera(DEFAULT_CAMERA, DEFAULT_WINDOWS_NAME)

  #Para traer al frente la toma de la camara
  list_top_windows = []
  win32gui.EnumWindows(windowEnumerationHandler, list_top_windows)
  for window in list_top_windows:
    if DEFAULT_WINDOWS_NAME in window[1]:
        camara=window[0]
        win32gui.ShowWindow(camara,5)
        win32gui.SetForegroundWindow(camara)
        # Hacerla transparente a la ventana de la captura de video de TF
        win32gui.SetWindowLong(camara, win32con.GWL_EXSTYLE, win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(camara, 0, 192, win32con.LWA_ALPHA)
        break

  trailer_on = False

  while True:
    # Selecciono un QueryVideo random que deberia tener todas las propiedades del objeto Video, incluyendo su poster
    trailer = random.choice(trailers_cine_db)

    # Activador del Trailer
    if (trailer_on):
      trailer.open_trailer()

    #Si el video termina
    if str(trailer.media.get_stage()) is 'State.Ended':
      #Cargo una nueva pelicula
      trailer2 = random.choice(trailers_cine_db)
      trailer2.open_trailer()
      break

    # Empieza el codigo de inicio del Stream para TF
    ret, frame = cap.read()
    # Sin frames
    if(frame is None):
      break

    # Tratamiento de color para la TF
    color_frame = cv2.cvtColor(frame, DEFAULT_BACK_COLOR)
    cv2.imshow(DEFAULT_CAMERA,frame)
    #Para traer al frente la toma de la camara
    win32gui.SetForegroundWindow(camara) 

    #Tensorflow de vuelta
    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(DEFAULT_FROZEN, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    with detection_graph.as_default():
      sess = tf.Session(graph=detection_graph)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
      detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # Aca abajo se abren los frames por frames del video dle flujo de openCV
      while True:
        # Al obtener el frame a analizar se lo expande con numpy
        image_np_expanded = np.expand_dims(frame, axis=0)
        (boxes, scores, classes_, num_) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections], feed_dict={image_tensor: image_np_expanded})
        for i, box in enumerate(np.squeeze(boxes)):
            if(np.squeeze(scores)[i] > DEFAULT_THRESHOLD):
              # Aca dibujo la Box en el video abierto por OpenCV
              # Aca creoq eu tengo que comparar si las boxes estan dentro del marco deseado
              # if (verificar_personas_sentadas(boxes, DEFAULT_XML_BOXES)):
              if 1:
                # Si estoy aca es porque las dos sillas estan detectadas, cambio un estado para disparar el trailer
                trailer_on = True
              else:
                trailer_on = False

      k = cv2.waitKey(6) & 0xFF
      if k in [27, ord('q')]: # Salir
        break
      elif k == ord('p'): # Pausa Pelicula
        player.pause()
      elif k == ord('s'): # Sonido para probar
        winsound.Beep(DEFAULT_FREQUENCY, DEFAULT_DURATION)

  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
    main()