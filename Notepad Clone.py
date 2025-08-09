from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from tkinter import colorchooser

import webbrowser
from PIL import Image,ImageTk
default_size=12
root=Tk()
root.title("Notepad")
root.geometry("800x600")
#set a default font type & font size...
default_size=12
text_font=font.Font(family="Times New Roman", size=default_size)

#creating a text frame...
text_frame=Frame(root)
text_frame.pack(expand=1, fill='both')

#creating a text area...
text_area=Text(text_frame,undo=True, wrap='word', font=text_font)
text_area.pack(side=LEFT, expand=1, fill='both')

# Add vertical scrollbar to the text area
scrollbar = Scrollbar(text_frame, orient=VERTICAL, command=text_area.yview)
scrollbar.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scrollbar.set)

#Creating Menu bar...
menu_bar=Menu(root)
root.config(menu=menu_bar)



#File menu...
file_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='File',menu=file_menu)
#new-
def new_file():
      text_area.delete(1.0,END)
def open_file():
    file=filedialog.askopenfile(mode='r',filetypes=[("Text Files","*.txt")])
    if file: 
         contents=file.read()
         text_area.delete(1.0,END)
         text_area.insert(INSERT, contents)
         file.close()
def save_file():
    file=filedialog.asksaveasfile(mode='w', defaultextension=".txt", initialfile="Untitled.txt")
    if file:
        data=text_area.get(1.0,END)
        file.write(data)
        file.close()

file_menu.add_command(label='New    (Ctrl+N)', command=new_file)
file_menu.add_command(label='Open   (Ctrl+O)',command=open_file)
file_menu.add_command(label='Save    (Ctrl+S)',command=save_file)
file_menu.add_separator()
file_menu.add_command(label='Exit    (Alt+F4)', command=root.destroy)

#Edit menu...
edit_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='Edit',menu=edit_menu)

edit_menu.add_command(label="Undo  (Ctrl+Z)",command=lambda: text_area.event_generate("<<Undo>>"))
edit_menu.add_command(label="Redo  (Ctrl+Y)",command=lambda: text_area.event_generate("<<Redo>>"))
edit_menu.add_separator()
edit_menu.add_command(label="Cut   (Ctrl+X)",command=lambda: text_area.event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy  (Ctrl+C)",command=lambda: text_area.event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste  (Ctrl+V)",command=lambda: text_area.event_generate("<<Paste>>"))

#Insert menu...
insert_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='Insert',menu=insert_menu)

def insert_text():
      default_text="This is a default text.\nThis is a sample paragraph created to serve as a placeholder or template for future content. It demonstrates the general structure and flow of a well-formed paragraph. The main idea is introduced in the beginning, followed by supporting details and examples, and a concluding sentence that wraps up the thought. This format helps maintain clarity and coherence in writing, making it easier for readers to understand the message being conveyed."
      text_area.insert(INSERT, default_text)
def insert_img():
      file_img=filedialog.askopenfilename(title= "Select an image", filetypes=[("Image files","*.png;*.jpg;*.jpeg")])
      if file_img:
            img=Image.open(file_img)
            img=img.resize((200,150))
            tk_img=ImageTk.PhotoImage(img)#convert into tk img
            text_area.image_create(INSERT, image=tk_img)
            text_area.image=tk_img
                        
      
insert_menu.add_command(label="Default Text", command=insert_text)
insert_menu.add_command(label="Image", command=insert_img)
      
#format 
format_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='Format',menu=format_menu)

#function for color change...

def color_change():
    try:
        start = text_area.index("sel.first")
        end = text_area.index("sel.last")
        color = colorchooser.askcolor(title="Choose Font Color")[1]
        if color:
            text_area.tag_add("color", start, end)
            text_area.tag_config("color", foreground=color)
    except:
        pass

#function for bold, italic & underline...
def update_font_tags(start, end):
    current_tags = text_area.tag_names(start)
    current_font = font.Font(text_area, text_area.cget("font"))
    weight = 'bold' if "bold" in current_tags else 'normal'
    slant = 'italic' if "italic" in current_tags else 'roman'
    underline_val = 1 if "underline" in current_tags else 0
    current_font.configure(weight=weight, slant=slant, underline=underline_val)
    tag_name = f"font_{weight}_{slant}_{underline_val}"
    text_area.tag_config(tag_name, font=current_font)
    text_area.tag_add(tag_name, start, end)

def toggle_tag(tag_name):
    try:
        start = text_area.index("sel.first")
        end = text_area.index("sel.last")
        if tag_name in text_area.tag_names(start):
            text_area.tag_remove(tag_name, start, end)
        else:
            text_area.tag_add(tag_name, start, end)
        update_font_tags(start, end)
    except:
        pass

def bold(): toggle_tag("bold")
def italic(): toggle_tag("italic")
def underline(): toggle_tag("underline")
#function for changing font size...
def font_size(size):
    text_area.config(font=("Arial", size))
    
#function for changing font size...
def change_font_family(family):
    text_area.config(font=(family, 14))

# Font size submenu...
font_size_menu = Menu(format_menu, tearoff=0)
format_menu.add_cascade(label="Font Size", menu=font_size_menu)
for size in [10, 12, 14, 16, 18, 20, 24, 28, 32]:
    font_size_menu.add_command(label=str(size), command=lambda s=size: font_size(s))

# Font family submenu...
font_family_menu = Menu(format_menu, tearoff=0)
format_menu.add_cascade(label="Font Style", menu=font_family_menu)
for family in ["Arial", "Courier", "Times New Roman", "Helvetica", "Comic Sans MS"]:
    font_family_menu.add_command(label=family, command=lambda f=family: change_font_family(f))


format_menu.add_command(label="Font Color", command=color_change)
format_menu.add_separator()
format_menu.add_command(label="Bold", command=bold)
format_menu.add_command(label="Italic", command=italic)
format_menu.add_command(label="Underline", command=underline)


#View...
view_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='View',menu=view_menu)

def zoom_in():
      global default_size
      default_size+=2
      text_font.configure(size=default_size)
def zoom_out():
      global default_size
      default_size-=2
      text_font.configure(size=default_size)
      
view_menu.add_command(label='Zoom in (Ctrl+plus)', command=zoom_in)
view_menu.add_command(label='Zoom out (Ctrl+minus)', command=zoom_out)

#Help...
help_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='Help',menu=help_menu)

def open_link():
    webbrowser.open("https://www.bing.com/search?q=get+help+with+notepad+in+windows&filters=guid:%224466414-en-dia%22%20lang:%22en%22&form=T00032&ocid=HelpPane-BingIA")
def show_about():
    messagebox.showinfo(title="Notepad About", message="Notepad Clone\nVersion 1.0\n\nDeveloped by Sudeshna\n@ 2025 All rights reversed")
help_menu.add_command(label="View help", command=open_link)
help_menu.add_separator()
help_menu.add_command(label="About notepad", command=show_about)

#keyboard shortcuts...
root.bind('<Control-n>',lambda e: new_file())
root.bind('<Control-o>',lambda e: open_file())
root.bind('<Control-s>',lambda e: save_file())
root.bind('<Control-b>',lambda e: bold())
root.bind('<Control-i>',lambda e: italic())
root.bind('<Control-u>',lambda e: underline())

root.mainloop()
