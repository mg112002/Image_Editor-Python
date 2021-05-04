import tkinter as tk
from ttkthemes import themed_tk                   # yaru, breeze, breeze-dark, aqua 
from tkinter import ttk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont, ImageFilter
from PIL.ImageFilter import (BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN)

# ['scidsand', 'radiance', 'classic', 'clearlooks', 'itft1', 'default', 'winnative', 'winxpblue', 'equilux', 
# 'breeze', 'smog', 'adapta', 'scidmint', 'arc', 'vista', 'keramik', 'clam', 'plastik', 'alt', 'scidpurple', 'blue', 'aquativo', 'scidgrey',
#  'ubuntu', 'scidgreen', 'yaru', 'black', 'elegance', 'xpnative', 'scidblue', 'kroc', 'scidpink']

root = themed_tk.ThemedTk()
root.get_themes()    
root.set_theme('breeze')

root.title('Image Editor')
root.iconbitmap('Editor.ico')

# Code for Menubar
menubar = Menu(root)
root.config(menu=menubar)

# Code for Submenu
subMenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=subMenu)


def watermark(finl_image):
    global final_image
    width, height = finl_image.size

    draw = ImageDraw.Draw(finl_image)
    text = "Image Editor-MG"

    font = ImageFont.truetype('times.ttf', 50)
    textwidth, textheight = draw.textsize(text, font)

    # calculate the x,y coordinates of the text
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin

    # draw watermark in the bottom right corner
    draw.text((x, y), text, font=font, fill='cyan')
    final_image = finl_image


def imageviewer(selected_image):
    imgtoshow = selected_image.resize((800,500), Image.ANTIALIAS)
    show_img = ImageTk.PhotoImage(imgtoshow)
    imageWindow.config(image=show_img)
    imageWindow.photo_ref = show_img
    imageWindow.pack() 


def browse_file():
    try:
        global selected_img, filename, final_image
        filename = filedialog.askopenfilename()
        selected_img = Image.open(filename)
        final_image = selected_img
        imageviewer(selected_img)
    except:
        tk.messagebox.showwarning('Image Not Selected', 'Image not selected!!\nPlease select image file')
    

def blur():
    try:
        if selected_img is not NONE:
            blurwindow = themed_tk.ThemedTk()
            blurwindow.get_themes()
            blurwindow.set_theme('aquativo')

            blurwindow.title('Blur')
            blurwindow.iconbitmap('Editor.ico')
            blurwindow.geometry('200x110')

            def simple_blur():
                global final_image
                final_image = selected_img.filter(ImageFilter.BLUR)
                imageviewer(final_image)


            def box_blur():
                global final_image
                final_image = selected_img.filter(ImageFilter.BoxBlur(5))
                imageviewer(final_image)


            def gaussian_blur():
                global final_image
                final_image = selected_img.filter(ImageFilter.GaussianBlur(5))
                imageviewer(final_image)


            def close():
                imageviewer(final_image)
                blurwindow.destroy()


            simpleblurbtn = ttk.Button(blurwindow, text='Simple Blur', command=simple_blur)
            simpleblurbtn.pack(pady=5)

            boxblurbtn = ttk.Button(blurwindow, text='Box Blur', command=box_blur)
            boxblurbtn.pack(pady=5)

            gaussianblurbtn = ttk.Button(blurwindow, text='Gaussian Blur', command=gaussian_blur)
            gaussianblurbtn.pack(pady=5)

            blurwindow.protocol('WM_DELETE_WINDOW',close)
            blurwindow.mainloop()
    except:
        tk.messagebox.showerror('File not found', 'Image Editor could not find the file. Please select a file.')


def rotate():
    try:
        if selected_img is not NONE:
            rotatewindow = Tk()

            rotatewindow.title('Flip & Rotate')
            rotatewindow.geometry('250x100')
            rotatewindow.iconbitmap('Editor.ico')

            
            def rotated(rscale_posi):
                global final_image
                rscale_posi = int(rscale_posi)
                final_image = selected_img.rotate(rscale_posi)
                imageviewer(final_image)
                

            def flip():
                global final_image
                final_image = final_image.transpose(Image.FLIP_LEFT_RIGHT)
                imageviewer(final_image)


            def close():
                imageviewer(final_image)
                rotatewindow.destroy()
                        

            rotation_scale = Scale(rotatewindow, label='Rotate', from_=0, to=180, orient=HORIZONTAL, command=rotated)
            rotation_scale.pack()

            flipbtn = Button(rotatewindow, text='Mirror', command=flip)
            flipbtn.pack()

            rotatewindow.protocol('WM_DELETE_WINDOW', close)
            rotatewindow.mainloop()        
    except:
        tk.messagebox.showerror('File not found', 'Image Editor could not find the file. Please select a file.')


def adjust():
    try:
        if selected_img is not NONE:
            adjustwindow = Tk()

            adjustwindow.title('Brightness & Contrast')
            adjustwindow.geometry('300x150')
            adjustwindow.iconbitmap('Editor.ico')

            def set_brightness(bscale_posi):              # bscale_pos is the brightness scale position
                bscale_posi = float(bscale_posi)
                global final_image
                enhancer = ImageEnhance.Brightness(selected_img)
                final_image = enhancer.enhance(bscale_posi)
                imageviewer(final_image)


            def set_contrast(cscale_posi):                # cscale_pos is the contrast scale position
                cscale_posi = float(cscale_posi)
                global final_image
                enhancer = ImageEnhance.Contrast(final_image)
                final_image = enhancer.enhance(cscale_posi)
                imageviewer(final_image)

            brightness_scale = Scale(adjustwindow, label='Brightness', from_=0, to=3, orient=HORIZONTAL, resolution=0.05, command=set_brightness)
            brightness_scale.set(1)
            brightness_scale.pack()

            contrast_scale = Scale(adjustwindow, label='Contrast', from_=0, to=2, orient=HORIZONTAL, resolution=0.05, command=set_contrast)
            contrast_scale.set(1)
            contrast_scale.pack()

            adjustwindow.mainloop()
    except:
        tk.messagebox.showerror('File not found', 'Image Editor could not find the file. Please select a file.')            


def effects():
    try:
        if selected_img is not NONE:
            effectswindow = themed_tk.ThemedTk()
            effectswindow.get_themes()
            effectswindow.set_theme('aquativo')

            effectswindow.title('Effects')
            effectswindow.iconbitmap('Editor.ico')
            effectswindow.geometry('210x370')

            
            def minfilter():
                global final_image
                final_image = selected_img.filter(ImageFilter.MinFilter)
                imageviewer(final_image)


            def contour():
                global final_image
                final_image = selected_img.filter(CONTOUR)
                imageviewer(final_image)


            def detail():
                global final_image
                final_image = selected_img.filter(DETAIL)
                imageviewer(final_image)


            def edge_enhance():
                global final_image
                final_image = selected_img.filter(EDGE_ENHANCE)
                imageviewer(final_image)


            def edge_enhance_plus():
                global final_image
                final_image = selected_img.filter(EDGE_ENHANCE_MORE)
                imageviewer(final_image)


            def emboss():
                global final_image
                final_image = selected_img.filter(EMBOSS)
                imageviewer(final_image)


            def find_edges():
                global final_image
                final_image = selected_img.filter(FIND_EDGES)
                imageviewer(final_image)


            def smooth():
                global final_image
                final_image = selected_img.filter(SMOOTH)
                imageviewer(final_image)


            def smooth_plus():
                global final_image
                final_image = selected_img.filter(SMOOTH_MORE)
                imageviewer(final_image)


            def sharpen():
                global final_image
                final_image = selected_img.filter(SHARPEN)
                imageviewer(final_image)


            def close():
                imageviewer(final_image)
                effectswindow.destroy()

            
            minfilterbtn = ttk.Button(effectswindow, text='Minfilter', command=minfilter)
            minfilterbtn.pack(pady=5)

            contourbtn = ttk.Button(effectswindow, text='Contour', command=contour)
            contourbtn.pack(pady=5)

            detailbtn = ttk.Button(effectswindow, text='Detail', command=detail)
            detailbtn.pack(pady=5)

            edgenhancebtn = ttk.Button(effectswindow, text='Edge Enhance', command=edge_enhance)
            edgenhancebtn.pack(pady=5)

            edgenhanceplusbtn = ttk.Button(effectswindow, text='Edge Enhance +', command=edge_enhance_plus)
            edgenhanceplusbtn.pack(pady=5)

            embossbtn = ttk.Button(effectswindow, text='Emboss', command=emboss)
            embossbtn.pack(pady=5)

            findedgesbtn = ttk.Button(effectswindow, text='Find Edges', command=find_edges)
            findedgesbtn.pack(pady=5)

            smoothbtn = ttk.Button(effectswindow, text='Smooth', command=smooth)
            smoothbtn.pack(pady=5)

            smoothplusbtn = ttk.Button(effectswindow, text='Smooth +', command=smooth_plus)
            smoothplusbtn.pack(pady=5)

            sharpenbtn = ttk.Button(effectswindow, text='Sharpen', command=sharpen)
            sharpenbtn.pack(pady=5)

            effectswindow.protocol('WM_DELETE_WINDOW', close)
            effectswindow.mainloop() 
    except:
        tk.messagebox.showerror('File not found', 'Image Editor could not find the file. Please select a file.')


def clear():
    try: 
        if selected_img is not NONE:      
            global final_image
            final_image = selected_img
            imageviewer(selected_img)
    except:
        tk.messagebox.showerror('File not found', 'Image Editor could not find the file. Please select a file.')
    
    
def close():
    msgbox = tk.messagebox.askquestion('Image Editor', 'Do you really want to exit?')
    if msgbox == 'yes':
        root.destroy()
    else:
        tk.messagebox.showinfo('Return', 'Returning to the Editor')


def SaveAs():
    try:
        if selected_img is not NONE: 
            global final_image
            watermark(final_image)
            savefile = filedialog.asksaveasfilename(defaultextension=".jpg")
            final_image.save(savefile)
    except:
        tk.messagebox.showerror('File not found', 'Image Editor could not find the file. Please select a file.')        


def Save():
    watermark(final_image)
    final_image.save(filename)


subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Save", command=Save)
subMenu.add_command(label="Save As", command=SaveAs)
subMenu.add_command(label="Exit", command=close)


def about_us():
    tk.messagebox.showinfo('About Image Editor',
                        '"Image Editor" is a free software for basic editing of images.\nThis software has different effects which changes the looks of your image.\n Created by ----- Mangalam Gupta -----')
    

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

topframe = Frame(root)
topframe.pack(padx=10, pady=10)

Newbtn = ttk.Button(topframe, text="+ NEW", command=browse_file)
Newbtn.grid(row=0, column=0, padx=10, pady=10)

Blurbtn = ttk.Button(topframe, text="BLUR", command=blur)
Blurbtn.grid(row=0, column=1, padx=10, pady=10)

Rotatebtn = ttk.Button(topframe, text="ROTATE & MIRROR", command=rotate)
Rotatebtn.grid(row=0, column=2, padx=10, pady=10)

Adjustbtn = ttk.Button(topframe, text="ADJUST", command=adjust)
Adjustbtn.grid(row=0, column=3, padx=10, pady=10)

Effectsbtn = ttk.Button(topframe, text="EFFECTS", command=effects)
Effectsbtn.grid(row=0, column=4, padx=10, pady=10)

ClrAllbtn = ttk.Button(topframe, text="RESET", command=clear)
ClrAllbtn.grid(row=0, column=5, padx=10, pady=10)

Savebtn = ttk.Button(topframe, text="SAVE", command=Save)
Savebtn.grid(row=0, column=6, padx=10, pady=10)

SaveAsbtn = ttk.Button(topframe, text="SAVE AS", command=SaveAs)
SaveAsbtn.grid(row=0, column=7, padx=10, pady=10)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill=tk.X, padx=10, pady=5)

imageframe = Frame(root)
imageframe.pack(padx=10, pady=30)

imageWindow = Label(imageframe)
imageWindow.pack()

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
