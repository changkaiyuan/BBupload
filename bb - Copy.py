from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox


class BbUpload:
    SCOPES = None
    folders=None
    serviceDrive=None
    window=None
    dropDownList=None
    dropDownBox=None
    dropDown_selected=None
    current_entry=None
    student_files_list=None
    itemList=None
    dropDown_selected_old = None
    
    
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.serviceDrive=self.getDriveService()
        self.folders = self.getFolders()
        self.dropDownList=self.update_dropDownList("") #setup dropDown
        self.current_entry=""
        self.dropDown_selected=""
        self.setupWindow()



    def start_window(self):
        self.window.mainloop()
    def end_window(self):
        try:
            self.window.destroy()
        except:
            pass
    
    def getDriveService(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service

    def getFolders(self):
        page_token = None
        response = None
        while True:
            response = self.serviceDrive.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            # for file in response.get('files', []):
                # Process change
                # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return response.get('files', [])
    
    def isExist(self,name):
        for file in self.folders:
            if file.get('name').lower() == name.lower():
                return True
        return False

    def createNewFolder(self,name):
        if(name == None or name == ""):
            # print("EmptyName")
            return
        elif(self.isExist(name)):
            # print("File Exist")
            return
        file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.serviceDrive.files().create(body=file_metadata,
                                            fields='id').execute()
        
        if file.get('id') =="":
            messagebox.showerror("Error","Fail to create student profile")
            return
        messagebox.showinfo("Success","New Student Profile has been created")
        self.folders=self.getFolders() #update folders
        self.update_dropDownList(self.current_entry)
        self.update_dropDownBox()
        # print ('Folder ID: %s Folder Name: %s is created' % (file.get('id') , name))

    def find_folder(self):
        for file in self.folders:
            if file.get('name').lower() == self.dropDown_selected.lower():
                return file
        return

    def upload_file(self):
        self.dropDown_selected = self.dropDownBox.get()
        # print(self.dropDown_selected)
        if self.dropDown_selected == "--No Matching Name--":
            # print("No matching")
            return
        
        file_name=filedialog.askopenfilename(initialdir="/", title="Select file")
        if file_name == "":
            # print("No selected File")
            return
        file_metadata = {'name':os.path.basename(file_name),
                        'parents':[self.find_folder().get('id')]}
        media = MediaFileUpload(file_name)
        file = self.serviceDrive.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

        if file.get('id') =="":
            messagebox.showerror("Error","Fail to upload file")
            return
        messagebox.showinfo("Success","File uploaded successful")

        self.update_student_file()
        # print(file)
        # print("FILE: ",file)
        # print(file.get("id"))

    def download_file(self):
        if self.itemList.size() ==0:
            return

        try:
            file_index = self.itemList.curselection()[0]
            file_id = self.student_files_list[file_index]['id']
        except:
            return
        
        request = self.serviceDrive.files().get_media(fileId=file_id)
        # fh = io.BytesIO()
        file_name = self.student_files_list[file_index]['name']
        # print(file_name)
        fh = io.FileIO(file_name,'wb')
        try:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                # print ("Download %d%%." % int(status.progress() * 100))
        except:
            # print("File cannot be download")
            return

    def newStudentPop(self):
        top = Toplevel(self.window)
        top.title("New")

        x = self.window.winfo_rootx()
        y = self.window.winfo_rooty()
        # height = self.window.winfo_height()
        geom = "+%d+%d" % (x, y)

        top.geometry(geom)
        top.resizable(0,0)

        top.grab_set()
        l = Label(top,text="Student Name")
        e = Entry(top)
        e.focus_force()
        
        bOk=Button(top,text="OK", width=10,command=lambda: [self.createNewFolder(e.get()),top.grab_release(),top.destroy()])
        bNo=Button(top,text="CANCEL", width=10, command=lambda: [top.grab_release(),top.destroy()])
        
        l.grid(row=0,column=0)
        e.grid(row=0,column=1)
        bOk.grid(row=1,column=0)
        bNo.grid(row=1,column=1)
        

    # def clear_dropDown(self):
    #     self.itemList.delete(0,'end')
    #     self.student_files_list=[]

    def update_student_file(self):
        i=0
        self.itemList.delete(0,'end')
        self.student_files_list=[]
        
        self.dropDown_selected = self.dropDownBox.get()
        selected_folder = self.find_folder()
        page_token = None
        while True:
            response = self.serviceDrive.files().list(q="'{}' in parents" .format(selected_folder.get('id')),
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                self.student_files_list.append(file)
                self.itemList.insert(i,file.get('name'))
            page_token = response.get('nextPageToken', None)
            # print(self.student_files_list[0]['id'])
            # print(self.itemList)
            # print(self.student_files_list[0]['id'])
            
            if page_token is None:
                break

    def about_app(self):
        messagebox.showinfo("About", "This App is written in Python by CHANGKAI YUAN. \n © 2020 CHANGKAI YUAN")

    def setupMenu(self):
        menu = Menu(self.window)
        newList = Menu(menu, tearoff=0)
        newList.add_command(label='Student Profile', command=self.newStudentPop)
        
        menu.add_cascade(label='New', menu=newList)
        menu.add_cascade(label='About', command=self.about_app)


        self.window.config(menu=menu)

    def update_dropDownList(self,name):
        self.dropDownList = []
        for file in self.folders:
            if name.lower() in file.get('name').lower():
                self.dropDownList.append(file.get('name'))
        
        if len(self.dropDownList)==0:
            self.dropDownList.append("--No Matching Name--")
        self.dropDownList.sort()
        # print(self.dropDownList)
        return self.dropDownList

    def update_dropDownBox(self):
        self.dropDownBox['values']=self.dropDownList
        self.dropDownBox.current(0)
        return self.dropDownBox

    def setupTopPanel(self, frame):
        def track_text(event):
            # self.dropDown_selected_old=self.dropDown_selected
            self.dropDownList = self.update_dropDownList(text_var.get())
            self.dropDownBox = self.update_dropDownBox()
            self.current_entry=text_var.get()
            # if not (self.dropDown_selected_old == self.dropDown_selected):
            #     self.update_student_file()
            
            

        l1 = Label(frame, text="Name")
        l1.place(relx = .22, rely=.3)

        self.dropDownList = self.update_dropDownList("")
        self.dropDownBox = ttk.Combobox(frame,values=self.dropDownList, width=30,font="Verdana 10", state="readonly")
        self.dropDownBox.bind("<<ComboboxSelected>>", lambda _: self.update_student_file())
        self.dropDownBox = self.update_dropDownBox()
        text_var=tk.StringVar()
        e1 = tk.Entry(frame,width=34, textvariable=text_var)
        e1.bind('<KeyRelease>',track_text)
        e1.place(height=30,relx = .3, rely=.3)
        self.dropDownBox.place(anchor="c", relx=.5,rely=.7)
        selectButton=Button(frame,bd=3,text="Show My Files", command=self.update_student_file)
        selectButton.place(anchor="c", relx=.86,rely=.7)

    def setupBotPanel(self,frame):
        listFrame = Frame(frame)
        listFrame.place(width=250, height=250)
        scrollbar = Scrollbar(listFrame)
        scrollbar.pack(side=RIGHT,fill=Y)

        self.itemList = Listbox(listFrame)
        
        self.itemList.place(x=0,y=0, width=233,height=250)

        self.itemList.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.itemList.yview)

        buttonFrame = Frame(frame)
        buttonFrame.place(x=280,width=250,height=250)
        downButton=Button(buttonFrame, bd=5,text="DOWNLOAD", command=self.download_file)
        downButton.place(width=250,height=125)

        upButton=Button(buttonFrame, bd=5,text="UPLOAD", command=self.upload_file)
        upButton.place(y=124,width=250,height=125)

    def setupWindow(self):
        self.window = tk.Tk()
        self.window.title("BB UPLOAD")
        self.window.geometry("500x500")
        self.window.resizable(0,0)

        self.setupMenu()

        frameTop = Frame(self.window,width=500,height=250)
        frameTop.grid(row=0, column=0)
        self.setupTopPanel(frameTop)

        frameBot = Frame(self.window)
        self.setupBotPanel(frameBot)
        frameBot.place(y=250,width=500,height=250)





def main():
    bb = BbUpload()
    bb.start_window()

    cc = BbUpload()
    # cc.start_window()

if __name__ == '__main__':
    main()