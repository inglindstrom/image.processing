import tkinter as tk
from tkinter import filedialog
import os
import cv2
import numpy as np
from PIL import Image, ImageTk


# ------- Open and Save image from dialog ---------
def open_image():
    filename = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    if not os.path.exists(filename):
        return
    image = cv2.imread(filename, 0)
    images['origin'] = image
    images['processed'] = None
    show_image()

def save_image():
    filename = filedialog.asksaveasfilename(initialdir = ".",title = "Select destination file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    if filename[:-4] != '.jpg' and filename[:-5] != '.jpeg':
        filename += '.jpg'
    if images['processed'] is not None:
        cv2.imwrite(filename, images['processed'])

# ------- End Open and Save image from dialog -----

# ------- Display Images --------------------------

class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.width = window_width / 2
        self.height = window_height
        self.parent = parent

    def on_resize(self,event):
        geo = self.parent.winfo_geometry()
        _geo = geo.split('+')
        size = _geo[0].split('x')
        self.width = int(size[0]) / 2
        self.height = int(size[1])
        self.config(width=self.width, height=self.height)
        show_image()

def show_image():
    geo = window.winfo_geometry()
    _geo = geo.split('+')
    size = _geo[0].split('x')
    width = int(size[0]) / 2
    height = int(size[1])    
    if images['origin'] is not None:
        origin_image = Image.fromarray(images['origin'])
        origin_photo = ImageTk.PhotoImage(origin_image)
        origin_canvas.create_image(width / 2, height / 2, image = origin_photo, anchor = tk.CENTER)
        origin_canvas.image = origin_photo
    else:
        origin_canvas.delete('all')

    if images['processed'] is not None:
        processed_image = Image.fromarray(images['processed'])
        processed_photo = ImageTk.PhotoImage(processed_image)
        processed_canvas.create_image(width / 2, height / 2, image = processed_photo, anchor = tk.CENTER)
        processed_canvas.image = processed_photo
    else:
        processed_canvas.delete('all')

# ------- End Display Images ----------------------

# ------- Image Processing ------------------------

def binarization():
    image = images['origin'].copy()
    
    image[np.where(image<128)] = 0
    image[np.where(image>127)] = 255
    
    images['processed'] = image
    
    show_image()
    
def canny_edge_detection():
    image = images['origin'].copy()
    
    blur_image = cv2.GaussianBlur(image, (3, 3), 0)
    canny = cv2.Canny(image, 50, 150)
    
    images['processed'] = canny
    
    show_image()
    
def copy_from_left_to_right():
    image = images['origin'].copy()
    
    images['origin'] = None
    
    images['processed'] = image
    
    show_image()
        
def copy_from_right_to_left():
    image = images['processed'].copy()
    
    images['processed'] = None

    images['origin'] = image
    
    show_image()
    
def pepper_and_salt_noise():
    image = images['origin'].copy()
    
    noise = np.random.normal(loc = 0, scale = 1.0, size = image.shape)
    
    image[np.where(noise < -2.5)] = 0

    image[np.where(noise > 2.5)] = 255
    
    images['processed'] = image
    
    show_image()
    
def gaussian_noise():
    image = images['origin'].copy()
    
    noise = np.random.normal(loc = 0, scale = 0.8, size = image.shape)
    
    image = image / 255.0
    
    image = np.clip(image * (1 + noise * 0.2), 0, 1)
    
    image = image * 255.0
    
    images['processed'] = image
    
    show_image()
#----------------------------------------------





#inverse
def Inverse():
    image = images['origin'].copy()
    image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
    imageinvere=(255-image)
    images['processed'] = imageinvere
    
    show_image()


#end inverse



def lowPass():
    img_src = images['origin'].copy()
     



    #prepare the 5x5 shaped filter
    kernel = np.array([[1, 1, 1, 1, 1], 
                      [1, 1, 1, 1, 1], 
                      [1, 1, 1, 1, 1], 
                      [1, 1, 1, 1, 1], 
                      [1, 1, 1, 1, 1]])
    kernel = kernel/sum(kernel)

    #filter the source image
    img_rst = cv2.filter2D(img_src,-1,kernel)

    
    images['processed'] = img_rst 
    
    show_image()

#end low pass

#blur
def blur():
    image = images['origin'].copy()
    blur = cv2.blur(image,(5,5))

    
    images['processed'] = blur
    
    show_image()


def reducenoise():
    image = images['origin'].copy()
    image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)

    result = cv2.fastNlMeansDenoisingColored(image,None,20,10,7,21)
    images['processed'] = result
    show_image()
   

def Contrast():
    img = images['origin'].copy()
    contrast_img = cv2.addWeighted(img, 2.5, np.zeros(img.shape, img.dtype), 0, 0)


    images['processed'] = contrast_img
    show_image()


    
#--------------end vos--------------------------------  
# ------- End Image Processing --------------------        
    
window_width = 800
window_height = 600    
    
window = tk.Tk()
window.title('Image Processing V1.0')
window.geometry('{}x{}'.format(window_width, window_height))
window.configure(background='black')

images = {
    'origin': None,
    'processed': None
}

#menu bar
menubar = tk.Menu(window)

# filemenu
filemenu = tk.Menu(menubar, tearoff=0)

processmenu = tk.Menu(menubar, tearoff=0)

operatermenu = tk.Menu(menubar, tearoff=0)

noisemenu = tk.Menu(menubar, tearoff=0)

#  filemenu - File
menubar.add_cascade(label='File', menu=filemenu)

#  filemenu - Open  Save 
filemenu.add_command(label='Open', command=open_image)
filemenu.add_command(label='Save', command=save_image)

# separator
filemenu.add_separator()

#exit
filemenu.add_command(label='Exit', command=window.quit)

menubar.add_cascade(label='Operater', menu=operatermenu)
operatermenu.add_command(label='Left --> Right', command=copy_from_left_to_right)
operatermenu.add_command(label='Left <-- Right', command=copy_from_right_to_left)

# processmenu 
menubar.add_cascade(label='Process', menu=processmenu)
# add processs option menu
processmenu.add_command(label='Binarization', command=binarization)
processmenu.add_command(label='Canny Edge Detection', command=canny_edge_detection)
processmenu.add_command(label='Inverse', command=Inverse)
processmenu.add_command(label='Blur', command=blur)
processmenu.add_command(label='Contrast', command=Contrast)
processmenu.add_command(label='LowPass', command=lowPass)


#noise option menu
menubar.add_cascade(label='Noise', menu=noisemenu)
noisemenu.add_command(label='Pepper and salt', command=pepper_and_salt_noise)
noisemenu.add_command(label='Gaussian noise', command=gaussian_noise)
noisemenu.add_command(label='Reduce Noise', command=reducenoise)
# 
window.config(menu=menubar)

origin_canvas = ResizingCanvas(window, width = window_width / 2, height = window_height)
origin_canvas.pack(side = tk.LEFT)

processed_canvas = ResizingCanvas(window, width = window_width / 2, height = window_height)
processed_canvas.pack(side = tk.LEFT)

window.mainloop()