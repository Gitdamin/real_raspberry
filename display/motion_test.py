#움직이는 git 파일을 tkinter를 사용해서 full screen 출력

import sys
if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *
 
root = Tk()
 
#frame
frameCnt = 2
frames = [PhotoImage(file='/home/pi/Documents/display/test_cat.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
 
def update(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)
 
# fullscreen
# F11: fullscreen toggle, Esc : exit fullscreen mode 
root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen",
                                    not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
 
#window center position
positionRight = root.winfo_screenwidth()/2 
positionDown = root.winfo_screenheight()/2
 
#set image
label = Label(root, bg='black')
label.place(x=positionRight,y=positionDown,anchor=CENTER)
root.after(0, update, 0)
 
#background color
root.configure(bg='black')
 
root.mainloop()
