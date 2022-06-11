from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox


#طراحی شده برای پروژه درس اصول طراحی نرم افزار
#نام استاد : مریم حاجی اسمعیلی
#نام دانشجو : مهدی شریفی

root = Tk()
root.title("مدیریت افراد گمشده")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="gray88")

#============================VARIABLES===================================
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
number = StringVar()



#============================METHODS=====================================

def Database():
    conn = sqlite3.connect("MISSINGS.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, age TEXT, address TEXT, number TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()


def search_record () : 
    lookup_record = fname_entry.get()
    print(lookup_record)
    for record in tree.get_children() : 
        tree.delete(record)
    conn = sqlite3.connect("MISSINGS.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM member WHERE firstname like ?",(lookup_record,) )
    record=cursor.fetchall()
    for data in record:
        tree.insert('', 'end', values=(data))
    NewWindow.destroy()


def SubmitData():
    if  FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or number.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("MISSINGS.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` ( firstname,lastname ,gender ,  age, address ,number ) VALUES(?, ?, ?, ?, ?, ?)", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get()), str(number.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        number.set("")

def UpdateData():
    if GENDER.get() == "":
       result = tkMessageBox.showwarning('', 'لطفا فیلد های الزامی را بررسی کنید', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("MISSINGS.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `number` = ?, `address` = ?, `age` =?, `gender` = ?,  `lastname` = ?, `firstname` = ? WHERE `mem_id` = ?", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(AGE.get()), str(ADDRESS.get()), str(number.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        number.set("")
        
    
def OnSelected():
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    number.set("")
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    number.set(selecteditem[6])
    UpdateWindow = Toplevel()
    UpdateWindow.title("مدیریت افراد گمشده")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) ) - (width/2)
    y = ((screen_height/2) ) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    #===================FRAMES==============================
    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    missingForm = Frame(UpdateWindow)
    missingForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(missingForm)
    Female = Radiobutton(RadioGroup, text="زن", variable=AGE, value="زن",padx=50,  font=('arial', 14)).pack(side=LEFT)
    Male = Radiobutton(RadioGroup, text="مرد", variable=AGE, value="مرد",  font=('arial', 14)).pack(side=LEFT)

    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="بروز رسانی", font=('arial', 16), bg="aquamarine4",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(missingForm, text="نام", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_firstname.grid(row=0, column=1, sticky=E)
    lbl_lastname = Label(missingForm, text="نام خانوادگی", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_lastname.grid(row=1, column=1, sticky=E)
    lbl_gender = Label(missingForm, text="جنسیت", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_gender.grid(row=2, column=1, sticky=E)
    lbl_age = Label(missingForm, text="سن", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_age.grid(row=3, column=1, sticky=E)
    lbl_address = Label(missingForm, text="آدرس", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_address.grid(row=4, column=1, sticky=E)
    lbl_missing = Label(missingForm, text="شماره تماس", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_missing.grid(row=5, column=1, sticky=E)

    #===================ENTRY===============================
    firstname = Entry(missingForm, textvariable=number,justify=RIGHT, font=('arial', 14))
    firstname.grid(row=0)
    lastname = Entry(missingForm, textvariable=ADDRESS,justify=RIGHT, font=('arial', 14))
    lastname.grid(row=1)
    RadioGroup.grid(row=2)
    age = Entry(missingForm, textvariable=GENDER,justify=RIGHT,  font=('arial', 14))
    age.grid(row=3)
    address = Entry(missingForm, textvariable=LASTNAME,justify=RIGHT,  font=('arial', 14))
    address.grid(row=4)
    missing = Entry(missingForm, textvariable=FIRSTNAME,justify=RIGHT,  font=('arial', 14))
    missing.grid(row=5)
    

    #==================BUTTONS==============================
    btn_updatecon = Button(missingForm, text="بروز رسانی", width=50, command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)


def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('', '! لطفا ابتدا یک داده را انتخاب کنید', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'آیا از حذف کردن این داده مطمئن هستید ؟', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("MISSINGS.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    number.set("")
    NewWindow = Toplevel()
    NewWindow.title("سیستم یافتن افراد گمشده")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) ) - (width/2)
    y = ((screen_height/2) ) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    
    #===================FRAMES==============================
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    missingForm = Frame(NewWindow)
    missingForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(missingForm)
    Female = Radiobutton(RadioGroup, text="زن", variable=GENDER, value="زن",padx=50,  font=('arial', 14)).pack(side=LEFT)
    Male = Radiobutton(RadioGroup, text="مرد", variable=GENDER, value="مرد",  font=('arial', 14)).pack(side=LEFT)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="اضافه کردن", font=('arial', 16), bg="aquamarine4",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(missingForm, text=": نام", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_firstname.grid(row=0, column=1, sticky=E)
    lbl_lastname = Label(missingForm, text=": نام خانوادگی", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_lastname.grid(row=1, column=1, sticky=E)
    lbl_gender = Label(missingForm, text=": جنسیت", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_gender.grid(row=2, column=1, sticky=E)
    lbl_age = Label(missingForm, text=": سن", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_age.grid(row=3, column=1, sticky=E)
    lbl_address = Label(missingForm, text=": آدرس", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_address.grid(row=4, column=1, sticky=E)
    lbl_missing = Label(missingForm, text=": شماره تماس", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_missing.grid(row=5, column=1, sticky=E)

    #===================ENTRY===============================
    firstname = Entry(missingForm, textvariable=FIRSTNAME,justify = RIGHT, font=('arial', 14))
    firstname.grid(row=0 )
    lastname = Entry(missingForm, textvariable=LASTNAME,justify = RIGHT, font=('arial', 14))
    lastname.grid(row=1)
    RadioGroup.grid(row=2)
    age = Entry(missingForm, textvariable=AGE,justify = RIGHT,  font=('arial', 14))
    age.grid(row=3)
    address = Entry(missingForm, textvariable=ADDRESS,justify = RIGHT,  font=('arial', 14))
    address.grid(row=4)
    missing = Entry(missingForm, textvariable=number,justify = RIGHT,  font=('arial', 14))
    missing.grid(row=5)
    

    #==================BUTTONS==============================
    btn_addcon = Button(missingForm, text="ذخیره کردن", width=50, command=SubmitData)
    btn_addcon.grid(row=6, columnspan=2, pady=10)
def AddNewWindow2():
    global list ,fname_entry
    global NewWindow
    FIRSTNAME.set("")
    NewWindow = Toplevel()
    NewWindow.title("جستجو")
    width = 400
    height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) ) - (width/2)
    y = ((screen_height/2)) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    
    #===================FRAMES==============================
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    missingForm = Frame(NewWindow)
    missingForm.pack(side=TOP, pady=10)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="جستجو کردن", font=('arial', 16), bg="aquamarine4",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(missingForm, text=": نام", font=('arial', 14), bd=5,justify=RIGHT)
    lbl_firstname.grid(row=0, column=1, sticky=E)
    #===================ENTRY===============================
    fname_entry = Entry(missingForm, textvariable=FIRSTNAME,justify = RIGHT, font=('arial', 14))
    fname_entry.grid(row=0 ,column=0,padx=10)

    #==================BUTTONS==============================
    btn_addcon = Button(missingForm, text="جستجو کردن",width=10, command=search_record)
    btn_addcon.grid(row=4,column=0,sticky=E+W,padx=40 ,pady=50)


#============================FRAMES======================================
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500,  bg="gray88")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="gray88")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
#============================LABELS======================================
lbl_title = Label(Top, text="سیستم مدیریت افراد گمشده", font=('arial', 16), width=500)
lbl_title.pack(fill=X)


#============================BUTTONS=====================================
btn_add = Button(MidRight, text="+ اضافه کردن", bg="gray65", command=AddNewWindow)
btn_add.pack(side=LEFT)
btn_search = Button(MidLeftPadding, text="جستجو کردن", bg="gray65", command=AddNewWindow2 )
btn_search.pack(padx=80)
btn_delete = Button(MidLeft, text="- حذف کردن", bg="gray65", command=DeleteData)
btn_delete.pack(side=RIGHT)

#============================TABLES======================================
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "number"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set  )
scrollbary.config(command=tree.yview )
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=E )
tree.heading('#7', text="نام", anchor=E)
tree.heading('#6', text="نام خانوادگی", anchor=E)
tree.heading('#5', text="جنسیت", anchor=E)
tree.heading('#4', text="سن", anchor=E)
tree.heading('#3', text="آدرس", anchor=E)
tree.heading('#2', text="شماره تماس", anchor=E)


tree.column('#0', stretch=NO, minwidth=0, width=0, anchor=E )
tree.column('#1', stretch=NO, minwidth=0, width=0, anchor=E )

tree.column('#6', stretch=NO, minwidth=0, width=120, anchor=E )
tree.column('#7', stretch=NO, minwidth=0, width=90, anchor=E )
tree.column('#4', stretch=NO, minwidth=0, width=80, anchor=E )
tree.column('#3', stretch=NO, minwidth=0, width=120, anchor=E )
tree.column('#2', stretch=NO, minwidth=0, width=120, anchor=E )
tree.column('#5', stretch=NO, minwidth=0, width=80, anchor=E )
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

#============================INITIALIZATION==============================
if __name__ == '__main__':
    Database()
    root.mainloop()



