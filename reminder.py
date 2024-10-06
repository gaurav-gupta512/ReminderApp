# imports

from tkinter import * # basic gui
from tkinter import filedialog # file operations
import webbrowser # redirect to any file
import ttkbootstrap as tb # advanced gui
from ttkbootstrap.constants import * # constants imports so no need for string specifications
from ttkbootstrap.dialogs import Messagebox as mb # error , prompt , info , warnings
from ttkbootstrap.style import Style # for personalization
import database_operations as db # database functions
from time import * # time functions
from datetime import datetime # datetime functions
from PIL import ImageGrab # for screenshot
import honki_utility as util # utility functions
import os # os functions

# ++++++++++ starting with all the functions that will be proqued ++++++++++

    # ---------- Type A - utility functions ----------  
                                         
def take_screenshot(event=None): # 1. ss function

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", 
        filetypes=[("PNG files", "*.png"),
                   ("All files", "*.*")]
    ) # Prompt user to choose save directory and file name
    
    if not file_path:
        return  # If user cancels, exit the function
    
    # Capture the screen area occupied by the root window
    x = box.winfo_x()
    y = box.winfo_y()
    width = box.winfo_width()
    height = box.winfo_height()

    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
   
    box.deiconify()  # Show the root window again
    
    screenshot.save(file_path) # Save the screenshot to the chosen file path

    def open_file(): # open image
        webbrowser.open(file_path)
    
    result = mb.yesno(
            title="Screenshot Saved",
            message=f"Screenshot saved : {file_path}\nDo you want to open it?"
        )
        
    if result == 'Yes':  # If the user clicked "Yes"
        open_file()

def update(): # 2. window time update function

    currenttime=strftime("%X")
    label_toplefttext.config(text=f'{strftime("%Y-%m-%d")} {currenttime}')
    box.after(500,update) # recursion every 500 ms to keep time updated

def update_countdown(): #  4. Update countdown for all rows  

    for row in reminders_data.get_children():
        reminders_data.delete(row)

    databasevals = db.query_all()

    for row in databasevals:
        reminders_data.insert('','end',values=row)

    children = reminders_data.get_children()

    for item_id in children:

        item = reminders_data.item(item_id)
        date_str = item['values'][2]  # Date is in the second column
        time_str = item['values'][3]  # Time is in the third column
        countdown = date_str.split('/') + time_str.split(':')
        countdown = list(map(int, countdown))
        util.countdown_xd(*countdown)  # Update target_datetime with the new date and time
        countdown_time = util.update_countdown()  # Get the formatted countdown time    
        if spinbox.get() == 'Filter Mode': 
            reminders_data.item(item_id, values=(item['values'][0], item['values'][1], item['values'][2],
                                            item['values'][3],item['values'][4],'COUNTDOWN NOT VISIBLE'))
            return
        else:
            reminders_data.item(item_id, values=(item['values'][0], item['values'][1], item['values'][2],
                                            item['values'][3],item['values'][4], countdown_time))
            
    box.after(500,update_countdown)     # Call this function again after 500 ms

def spinbox_value_validator(spinboxz): # 5. spinbox option validator function
    value = spinboxz.get()
    if value == "" or value not in spinboxz['values']:
        mb.show_error(title='Invalid Selection',message='No option was selected from the spinbox')
        return False

    # ---------- Type A END ( utility functions ) ---------- 

def filter(): # 6. database filter mode function
    
    if spinbox_select_from.get() == 'ID':
        
        try:
            if not entry_value.get():
                mb.show_error(title='Invalid Input',message='Enter a valid entry')
                return
            for row in reminders_data.get_children():
                reminders_data.delete(row)

            for value in db.query_specific('rowid',entry_value.get()):
                reminders_data.insert('','end',values=value)
        
        except:

            mb.show_error(title='ValueError',message='Given value does not match with any value in the database\nPlease try again')

    if spinbox_select_from.get() == 'Label':
        
        try:
            if not entry_value.get():
                mb.show_error(title='Invalid Input',message='Enter a valid entry')
                return
            for row in reminders_data.get_children():
                reminders_data.delete(row)
            for value in db.query_specific('Label',entry_value.get()):
                reminders_data.insert('','end',values=value)

        except:

            mb.show_error(title='ValueError',message='Given value does not match with any value in the database\nPlease try again')

    if spinbox_select_from.get() == 'Date':
        
        try:
            
            if not entry_value.get():
                mb.show_error(title='Invalid Input',message='Enter a valid entry')
                return
            for row in reminders_data.get_children():
                reminders_data.delete(row)
            for value in db.query_specific('Date',entry_value.get()):
                reminders_data.insert('','end',values=value)

        except:

            mb.show_error(title='ValueError',message='Given value does not match with any value in the database\nPlease try again')

    if spinbox_select_from.get() == 'Time':
        
        try: 
            
            if not entry_value.get():
                mb.show_error(title='Invalid Input',message='Enter a valid entry')
                return
            for row in reminders_data.get_children():
                reminders_data.delete(row)
            for value in db.query_specific('Time',entry_value.get()):
                reminders_data.insert('','end',values=value)

        except:

            mb.show_error(title='ValueError',message='Given value does not match with any value in the database\nPlease try again')    

    if spinbox_select_from.get() == 'Doc. Date':
        
        try:
            
            if not entry_value.get():
                mb.show_error(title='Invalid Input',message='Enter a valid entry')
                return
            for row in reminders_data.get_children():
                reminders_data.delete(row)
            for value in db.query_specific('DocDate',entry_value.get()):
                reminders_data.insert('','end',values=value)

        except:

            mb.show_error(title='ValueError',message='Given value does not match with any value in the database\nPlease try again')
            
def delete(): # 7. database value delete function

    try:

        if spinbox_delete.get() == 'ID':
            if db.entry_validator('rowid',entry_delete.get()) == None:
                mb.show_error(title='Deletion Error',message="Entry doesn't exist / Invalid Entry")
            else:
                if not entry_delete.get():
                    mb.show_error(title='Invalid Input',message='Enter a valid entry')
                    return
                confirm = mb.yesno(title='Confirm Delete',message='Are you sure you want to delete')
                if confirm == 'Yes':
                    db.delete('rowid',entry_delete.get())
                    db.delete2('rowid',entry_delete.get())

        elif spinbox_delete.get() == 'Label' or 'Date' or 'Time':
            if db.entry_validator(spinbox_delete.get(),entry_delete.get()) == None:
                mb.show_error(title='Deletion Error',message="Entry doesn't exist / Invalid Entry")
            else:
                if not entry_delete.get():
                    mb.show_error(title='Invalid Input',message='Enter a valid entry')
                    return
                confirm = mb.yesno(title='Confirm Delete',message='Are you sure you want to delete')
                if confirm == 'Yes':
                    db.delete(spinbox_delete.get(),entry_delete.get())
                    db.delete2(spinbox_delete.get(),entry_delete.get())

    except:

        mb.show_error(title='Deletion Error',message='Could not delete / Entry doesnt exist')




    # ---------- Type B - reminders option functions ---------- 

def reminders(): # 1. function to control reminders' option/frame

    box.withdraw()
    frame_home.pack_forget()
    sleep(0.5)
    box.deiconify()

    # checking whether frame is already opened to avoid multiple frames opened simultaneously
    if not reminder_frame.winfo_ismapped():
        reminder_frame.pack(padx=25, pady=25,fill=BOTH,expand=True)

    options_frame.pack_forget() # removing other frame if its on the window
    content_frame.pack(padx=10, pady=10) # packing content of reminders' frame

    frame_treeview.pack() # packing seperate frame for treeview and scrollbar
    reminders_data.pack(side=LEFT,padx=(5,0),pady=12) # packing treeview ( database entries )
    scrollbar_y.pack(fill=Y,side=RIGHT,padx=(0,5),pady=12) # packing treeview scrollbar
    sep2.pack(fill=X,padx=5,pady=15,anchor=CENTER) # seperator
    spinbox_label.pack(padx=10,pady=12) # packing label indicating spinbox
    spinbox.pack(padx=10, pady=(12,0)) # packing database mode changer spinbox

    update_countdown() # calling for time updation of data entries

def spinner(): # 2. function to control spinbox that changes database mode
    
    if spinbox.get() == 'Add Mode':     # 1. Add mode on

        if not frame_add.winfo_ismapped():
            frame_add.pack(anchor=CENTER,pady=(25,0))

        frame_update.pack_forget()
        frame_filter.pack_forget()
        frame_delete.pack_forget()

        update_countdown()

        label_label.grid(row=2, column=0, padx=20, pady=10)
        label_date.grid(row=2, column=2, padx=20, pady=10)
        label_time.grid(row=2, column=4, padx=20, pady=10)

        entry_label.grid(row=2, column=1, padx=20,pady=10)
        entry_date.grid(row=2, column=3, padx=20,pady=10)
        entry_time.grid(row=2, column=5, padx=20,pady=10)

        button_submit.grid(row=3,columnspan=9,pady=30)

    if spinbox.get() == 'Update Mode':     # 2.Update mode on

        if not frame_update.winfo_ismapped():
            frame_update.pack(anchor=CENTER,pady=(25,0))


        frame_add.pack_forget()
        frame_filter.pack_forget()
        frame_delete.pack_forget()

        update_countdown()

        label_where_update.grid(row=2,column=0,padx=20, pady=7)
        label_select_attribute.grid(row=2,column=2,padx=20, pady=7)
        spinbox_value.grid(row=2,column=1,padx=20, pady=7)
        entry_update.grid(row=2,column=3,padx=20, pady=7)

        label_spinbox_new.grid(row=3,column=0,padx=20, pady=7)
        spinbox_new_value.grid(row=3,column=1,padx=20, pady=7)
        label_new_value.grid(row=3,column=2,padx=20, pady=7)
        entry_new_value.grid(row=3,column=3,padx=20, pady=7)

        button_confirm_changes.grid(row=4,columnspan=9, pady=25)

    if spinbox.get() == 'Filter Mode' :     # 3.Filter mode on

        frame_add.pack_forget()
        frame_update.pack_forget()
        frame_delete.pack_forget()
        
        if not frame_filter.winfo_ismapped():
            frame_filter.pack(anchor=CENTER,pady=(25,0))

        # update_countdown()

        label_select_from.grid(row=2,column=0,padx=20, pady=13)
        label_select_where.grid(row=2,column=2,padx=20, pady=13)

        spinbox_select_from.grid(row=2,column=1,padx=20, pady=13)
        entry_value.grid(row=2,column=3,padx=20, pady=13)

        button_filter.grid(row=4,columnspan=6,pady=30)

    if spinbox.get() == 'Delete Mode':     # 4.Delete mode on

        frame_add.pack_forget()
        frame_update.pack_forget()
        frame_filter.pack_forget()

        if not frame_delete.winfo_ismapped():
            frame_delete.pack(anchor=CENTER,pady=(25,0))

        update_countdown()

        label_delete_from.grid(row=0,column=0,padx=20, pady=13)
        label_delete_what.grid(row=0,column=2,padx=20, pady=13)

        spinbox_delete.grid(row=0,column=1,padx=20, pady=13)
        entry_delete.grid(row=0,column=3,padx=20, pady=13)

        button_delete.grid(row=2,columnspan=6, pady=30)

def inputdata(): # 3. function to add entered submissions to the treeview

    label_value = entry_label.get()
    date_value = entry_date.get()
    time_value = entry_time.get()

    if not(label_value and date_value and time_value):
        mb.show_error(title='Invalid Input',message='Please fill all fields')
        return
    else:
        if util.validate_date(date_value):
            pass
        else:
            mb.show_error(title='Date Entry',message='''Enter date in DD/MM/YYYY format''')
            return
        
        if util.validate_time(time_value):
            pass
        else:
            mb.show_error(title='Time Entry',message='''Enter time in HH:MM 24 hour format''')
            return
        
        check = db.entry_validator('Label',label_value)
        if check is None:
            curt = strftime("%X")
            db.add_one(label_value,date_value,time_value,
                        docdate=f'{strftime("%Y-%m-%d")} {curt}')  # adding to database 
            db.add_one2('Ended , Not Yet Notified',label_value,date_value,time_value)
            update_countdown()
            last_item = reminders_data.get_children()[-1]
            reminders_data.see(last_item)
        else:
            mb.show_error(title='Entry Validation',message='Entry with the same Label already exists')

def dbupdate(): # 4. function to operate 'Update' Mode

    if spinbox_value.get() == 'Time':
        if not entry_update.get():
            mb.show_error(title='Invalid Input',message='Enter a valid entry')
            return
        if util.validate_time(entry_update.get()):
            pass
        else:
            mb.show_error(title='Time Entry',message='''Enter time in HH:MM 24 hour format''')
            return
            
    if spinbox_value.get() == 'Label':
        if not entry_update.get():
            mb.show_error(title='Invalid Input',message='Enter a valid entry')
            return
        check = db.entry_validator('Label',entry_value.get())
        if check is None:
            pass
        else:
            mb.show_error(title='Entry Validation',message='Entry with the same Label already exists')
            return
    
    if spinbox_value.get() == 'Date':
        if not entry_update.get():
            mb.show_error(title='Invalid Input',message='Enter a valid entry')
            return
        if util.validate_date(entry_update.get()):
            pass
        else:
            mb.show_error(title='Date Validation',message='''Enter date in DD/MM/YYYY format''')
            return
        
    if spinbox_new_value.get() == 'Time':
        if not entry_new_value.get():
            mb.show_error(title='Invalid Input',message='Enter a valid entry')
            return
        if util.validate_time(entry_new_value.get()):
            pass
        else:
            mb.show_error(title='Time Entry',message='''Enter time in HH:MM 24 hour format''')
            return
            
    if spinbox_new_value.get() == 'Label':
        if not entry_new_value.get():
            mb.show_error(title='Invalid Input',message='Enter a valid entry')
            return
        check = db.entry_validator('Label',entry_new_value.get())
        if check is None:
            pass
        else:
            mb.show_error(title='Entry Validation',message='Entry with the same Label already exists')
            return
    
    if spinbox_new_value.get() == 'Date':
        if not entry_new_value.get():
            mb.show_error(title='Invalid Input',message='Enter a valid entry')
            return
        if util.validate_date(entry_new_value.get()):
            pass
        else:
            mb.show_error(title='Date Validation',message='''Enter date in DD/MM/YYYY format''')
            return

    if spinbox_value_validator(spinbox_value) == False:
        return
    if spinbox_value_validator(spinbox_new_value) == False:
        return

    confirm_update = mb.yesno(title='Confirm Changes',message='Are you sure you want to update the data ?')

    if confirm_update == 'Yes':

        db.update_table(spinbox_value.get(),entry_update.get(),
                        spinbox_new_value.get(),entry_new_value.get())     
        db.update_table2(spinbox_value.get(),entry_update.get(),
                        spinbox_new_value.get(),entry_new_value.get())
        curt = datetime.now().replace(second=0,microsecond=0)
        for results in db.query_all2():
            trigger = f'{results[3]} {results[4]}'
            target_time = datetime.strptime(trigger, "%d/%m/%Y %H:%M")
            if not curt >= target_time:
                db.update_table2('rowid',results[0],'notified','Ended , Not Yet Notified')

    # ---------- Type B END ( reminders option functions ) ---------- 

    # ---------- Type C - 'options' option functions ----------

def options(): # 1. place Options frame and widgets

    if not options_frame.winfo_ismapped():
        options_frame.pack(padx=25, pady=25,fill=BOTH,expand=True)

    box.withdraw()
    frame_home.pack_forget()
    reminder_frame.pack_forget()
    sleep(0.5)
    box.deiconify()

    options_frame_content.pack(anchor=CENTER,pady=(25,0))

    label_app_theme.grid(row=1,column=0,padx=20)
    label_widgettheme.grid(row=4,column=0,padx=20, pady=10)
    label_widgetnote.grid(row=5,columnspan=2,padx=20, pady=10)
    label_help.grid(row=9,column=0,padx=20, pady=10)
    label_about.grid(row=13,column=0,padx=20, pady=10)

    combobox_theme_light.grid(row=0,column=1,padx=20)
    combobox_theme_dark.grid(row=2,column=1,padx=20,pady=(0,10))
    combobox_theme_widget.grid(row=4,column=1,padx=20, pady=10)
    button_user_manual.grid(row=9,column=1,padx=20, pady=10)
    button_about.grid(row=13,column=1,padx=20, pady=10)

    tb.Separator(options_frame_content,style=widgettheme).grid(sticky=EW,row=1,column=1,columnspan=2)
    tb.Separator(options_frame_content,style=widgettheme).grid(sticky=EW,row=3,columnspan=3,pady=10)
    tb.Separator(options_frame_content,style=widgettheme).grid(row=8,sticky=EW,columnspan=3,pady=10)
    tb.Separator(options_frame_content,style=widgettheme).grid(row=12,sticky=EW,columnspan=3,padx=20,pady=10)

def themechanger_light(event): # 2. Light theme changer function
    db.update_table3('theme',combobox_theme_light.get())
    themeupdator()
    tb.Style(theme=mainthemeval)

def themechanger_dark(event): # 3. Dark theme changer function
    db.update_table3('theme',combobox_theme_dark.get())
    themeupdator()
    tb.Style(theme=mainthemeval)

def themechanger_widget(event): # 4. Widget theme changer function
    db.update_table3('widgettheme',combobox_theme_widget.get())
    themeupdator()
    response = mb.yesno(title='Widget Theme',message='The theme was successfully changed.\nRestart now to apply changes') # Restart the application by re-executing the script
    if response == 'Yes': 
        box.destroy()
        import os
        import sys
        os.execl(sys.executable, sys.executable, *sys.argv) 
    
def open_usermanual(): # 6. open user manual function
    pdf_path = 'usermanual.pdf'
    if os.path.exists(pdf_path):     # Check if the file exists before trying to open it
        webbrowser.open_new(pdf_path)
    else:
        mb.show_error(title='File Missing',message="The file couldn't be opened / unable to find")

def open_about(): # 7. open about function
    note_path = 'about.txt'
    if os.path.exists(note_path):    # Check if the file exists before trying to open it
        webbrowser.open_new(note_path)
    else:
        mb.show_error(title='File Missing',message="The file couldn't be opened / unable to find")

    # ---------- Type C END - options' option functions ---------- 

# setting some values to save user settings

mainthemeval = None
widgetthemeval = None
firstime = None

def themeupdator():
    mainthemeval_get = db.query_all3()
    for i in mainthemeval_get:
        global mainthemeval,widgetthemeval,notif_val,firstime
        mainthemeval = i[1]
        widgetthemeval = i[2]
        notif_val = int(i[3])
        firstime = i[4]

themeupdator()

widgettheme = widgetthemeval

# +++++++++++ start of gui elements +++++++++++

    # ---------- Type A - Window configs ----------

box=tb.Window(themename=mainthemeval) # window creation
box.attributes('-fullscreen',True)
box.resizable(width=False,height=False) # keeping a fixed window size
box.title("Reminder") # app's Title/Name

    # ---------- Type A END - Window configs ----------

# defnining some frames so that they don't get repeated without existence checks

reminder_frame = None
options_frame = None

    # ---------- Type B - Window header ----------

frame_header = tb.Frame(box)
frame_header.pack(fill="x") # header frame

label_toplefttext=tb.Label(frame_header,
                           style=widgettheme,
                           text='',
                           font=("Stencil",15,'bold')) 
label_toplefttext.pack(padx=25,pady=25,side=RIGHT) # live clock label

menu_topright=tb.Menubutton(frame_header,
                            text="Menu",
                            style=f"outline {widgettheme}")
menu_topright.pack(padx=25,pady=25,side=LEFT)
menu_toprightoptions=tb.Menu(menu_topright) # main menu on top-right

# main menu options

menu_toprightoptions.add_radiobutton(label='Reminders',
                                     font=('Arial',10,'bold'),
                                     command=reminders)
menu_toprightoptions.add_radiobutton(label='Options',
                                     font=('Arial',10,'bold'),
                                     command=options)

menu_topright['menu']=menu_toprightoptions

tb.Separator(style=widgettheme).pack(padx=25,fill=X) # seperator

    # ---------- Type B END - Window header ----------

    # ---------- Type C - start reminders frame ----------
    
reminder_frame = tb.LabelFrame(box,
                               style=widgettheme,
                               text=' Reminders ',
                               borderwidth=2) # frame of reminders mode

content_frame = tb.Frame(reminder_frame) # frame for content inside reminders mode
frame_treeview = tb.Frame(content_frame) # frame for treeview and scrollbar

scrollbar_y = tb.Scrollbar(frame_treeview,
                           orient=VERTICAL,
                           style=LIGHT) # the scrollbar
reminders_data = tb.Treeview(frame_treeview,
                             style=widgettheme,
                             columns=('ID','Label','Date','Time','Doc. Date','Time Left'),
                             show=HEADINGS,
                             height=15,
                             yscrollcommand=scrollbar_y.set
                            ) # treeview for database

for columns in ('ID','Label','Date','Time','Doc. Date','Time Left'): # adding columns 
    reminders_data.heading(columns,text=columns,anchor=CENTER)
reminders_data.column('ID', width=100, anchor=CENTER)
reminders_data.column('Label', width=300, anchor=CENTER)
reminders_data.column('Date', width=170, anchor=CENTER)
reminders_data.column('Time', width=135, anchor=CENTER)
reminders_data.column('Doc. Date', width=285, anchor=CENTER)
reminders_data.column('Time Left', width=285, anchor=CENTER)

scrollbar_y.config(command=reminders_data.yview) # Scrollbar configuration

spinbox_label = tb.Label(content_frame,
                         text='Operation Mode ( Use up/down arrow key to navigate )',                       style=widgettheme,
                         font=('Arial', 12, 'bold'),
                         ) # indtcatior for spinbox below spinbox to control db modes

spinbox = tb.Spinbox(content_frame,
                     style=widgettheme,
                    state='readonly',
                    font=('Arial', 12, 'bold'),
                    width=14,
                    values=['Add Mode','Update Mode','Filter Mode','Delete Mode'],
                    command=spinner) # spinbox to control db modes
    
def spinbox_focus(event): # binded with 'esc'

    spinbox.focus_set()

box.bind("<Escape>",spinbox_focus)
spinbox.set('Click/Press esc') # base dummy value for user understanding
sep2=tb.Separator(content_frame,style=widgettheme)

    # ---------- Type C END - start reminders frame ----------

    # ---------- Type D - Database Modes ----------

        # 1. Add Mode

frame_add = tb.Frame(content_frame) 

label_label = tb.Label(frame_add,
                       style=widgettheme,
                       text='Label',
                       font=('Arial', 13, 'bold'))
label_date = tb.Label(frame_add,
                      style=widgettheme,
                      text='Date',
                      font=('Arial', 13, 'bold'))
label_time = tb.Label(frame_add,
                      style=widgettheme,
                      text='Time',
                      font=('Arial', 13, 'bold'))

entry_label = tb.Entry(frame_add,
                       style=widgettheme,
                       font=('Arial', 11, 'bold'))
entry_date = tb.Entry(frame_add,
                      style=widgettheme,
                      font=('Arial', 11, 'bold'))
entry_time = tb.Entry(frame_add,
                      style=widgettheme,
                      font=('Arial', 11, 'bold'))


button_submit = tb.Button(frame_add,
                          style=widgettheme,
                          text='Submit',
                          command=inputdata) # button for submission

        # 2. Update Mode

frame_update = tb.Frame(content_frame)

label_where_update = tb.Label(frame_update,
                              style=widgettheme,
                              text='Select Column', 
                              font=('Arial', 12, 'bold'))
label_select_attribute = tb.Label(frame_update,
                                  style=widgettheme,
                                  text='Current Value', 
                                  font=('Arial', 12, 'bold'))
label_spinbox_new = tb.Label(frame_update,
                             style=widgettheme,
                             justify=CENTER,
                             text='Select Column\nof new value', 
                             font=('Arial', 12, 'bold'))
label_new_value = tb.Label(frame_update,
                           style=widgettheme,
                           text='New Value',
                           font=('Arial', 12, 'bold'))

spinbox_value = tb.Spinbox(frame_update,
                           style=widgettheme,
                           state='readonly',
                           font=('Arial', 10, 'bold'),
                           width=10,
                           values=['ID','Label','Date','Time']) 
spinbox_new_value = tb.Spinbox(frame_update,
                               style=widgettheme,
                               state='readonly',font=('Arial', 10, 'bold'),
                               width=10,
                               values=['Label','Date','Time']) 

entry_update = tb.Entry(frame_update,
                        style=widgettheme,
                        font=('Arial', 11, 'bold')) 
entry_new_value = tb.Entry(frame_update,
                           style=widgettheme,
                           font=('Arial', 11, 'bold'))

button_confirm_changes = tb.Button(frame_update,
                                   style=widgettheme,
                                   text='Confirm Changes',
                                   command=dbupdate)

    # 3. Filter Mode

frame_filter = tb.Frame(content_frame)

label_select_from = tb.Label(frame_filter,
                             style=widgettheme,
                             text='Select Column',
                             font=('Arial', 12, 'bold'))
label_select_where = tb.Label(frame_filter,
                              style=widgettheme,
                              text='Current Value',
                              font=('Arial', 12, 'bold'))

spinbox_select_from = tb.Spinbox(frame_filter,
                                 style=widgettheme,
                                 state='readonly',
                                 width=10,
                                 font=('Arial', 11, 'bold'),
                                 values=['ID','Label','Date','Time']) 

entry_value = tb.Entry(frame_filter,
                       style=widgettheme,
                       font=('Arial', 12, 'bold')) 

button_filter = tb.Button(frame_filter,
                          style=widgettheme,
                          text='Filter',
                          command=filter)

        # 4. Delete Mode

frame_delete = tb.Frame(content_frame)

label_delete_from = tb.Label(frame_delete,
                             style=widgettheme,
                             text='Select Column',
                             font=('Arial', 12, 'bold'))
label_delete_what = tb.Label(frame_delete,
                             style=widgettheme,
                             text='Current Value',
                             font=('Arial', 12, 'bold'))

spinbox_delete = tb.Spinbox(frame_delete,
                            style=widgettheme,
                            state='readonly',
                            font=('Arial', 11, 'bold'),
                            width=10,
                            values=['ID','Label','Date','Time'])

entry_delete = tb.Entry(frame_delete,
                        style=widgettheme,
                        font=('Arial', 12, 'bold'))

button_delete = tb.Button(frame_delete,
                          style=widgettheme,
                          text='Delete',
                          command=delete)

    # ---------- Type D END - Database Modes ----------

    # ---------- Type E - Options frame ----------

options_frame = tb.LabelFrame(box,
                              text=' Options ',
                              style=widgettheme,
                              borderwidth=2)
options_frame_content = tb.Frame(options_frame)

label_app_theme = tb.Label(options_frame_content,
                           text='App Theme',
                           style=widgettheme,
                           font=('Arial', 12, 'bold'))
label_widgettheme = tb.Label(options_frame_content,
                             style=widgettheme,
                             text='Widget Theme',
                             font=('Arial',12,'bold'))
label_help = tb.Label(options_frame_content,
                      style=widgettheme,
                      text='Help',
                      font=('Arial', 12, 'bold'))
label_about = tb.Label(options_frame_content,
                       style=widgettheme,
                       text='About',
                       font=('Arial', 12, 'bold'))
label_widgetnote = tb.Label(options_frame_content,
                            style=widgettheme,
                            text='''( ⚠️ Some themes might not match with the App's theme )''',
                            font=('Arial', 8))

themelist_light = [ 'cosmo','flatly','journal','litera','lumen','minty',
                    'pulse','sandstone','united','yeti','morph','simplex','cerculean' ]
themelist_dark = [ 'solar','superhero','darkly','cyborg','vapor' ]
themelist_widget = [ 'primary','secondary','succcess','info','warning','danger','light','dark' ]

combobox_theme_light = tb.Combobox(options_frame_content,
                                   width=14,
                                   style=widgettheme,
                                   values=themelist_light,
                                   font=('Arial',12,'bold'),
                                   state=READONLY)
combobox_theme_dark = tb.Combobox(options_frame_content,
                                  width=14,
                                  style=widgettheme,
                                  values=themelist_dark,
                                  font=('Arial',12,'bold'),
                                  state=READONLY)
combobox_theme_widget = tb.Combobox(options_frame_content,
                                    width=14,
                                    style=widgettheme,
                                    values=themelist_widget,
                                    font=('Arial',12,'bold'),
                                    state=READONLY)

combobox_theme_light.bind("<<ComboboxSelected>>",themechanger_light)
combobox_theme_dark.bind("<<ComboboxSelected>>",themechanger_dark)
combobox_theme_widget.bind("<<ComboboxSelected>>",themechanger_widget)

if mainthemeval in themelist_light:
    combobox_theme_light.set(mainthemeval)
else:
    combobox_theme_light.set('Light Themes')
if mainthemeval in themelist_dark:
    combobox_theme_dark.set(mainthemeval)
else:
    combobox_theme_dark.set('Dark Themes')
combobox_theme_widget.set(widgettheme)

button_user_manual = tb.Button(options_frame_content,
                               style=widgettheme,
                               text='Open User Manual',
                               command=open_usermanual)
button_about = tb.Button(options_frame_content,
                         style=widgettheme,
                         text="Open note",
                         command=open_about)

    # ---------- Type E END - Options frame ----------

    # ---------- Type F - Text on the start page ----------

frame_home = tb.Frame(box)
frame_home.pack(fill=BOTH,expand=True)
label_initial = tb.Label(frame_home,
                         style=widgettheme,
                         justify=CENTER,
                         font=('Yu Mincho',18,'bold'),
                         text='''Get started by adding some reminders.\nClick on 'Reminders' option from the top-left Menu''')
label_wcback = tb.Label(frame_home,
                        style=widgettheme,
                        justify=CENTER,
                        font=('Yu Mincho',25,'bold'),
                        text='Welcome Back')

if firstime == 'Yes':
    label_initial.pack(anchor=CENTER,expand=True)
    db.update_table3('firsttime','No')
    themeupdator()
else:
    label_wcback.pack(anchor=CENTER,expand=True)

    # ---------- Type F END - Text on the start page ----------

# +++++++++++ END of gui elements +++++++++++

box.bind('<Control-s>', take_screenshot)
update()

box.mainloop() # 決戦