from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

# from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox

"""
class Student:
    name = None
    name_folder_id=None
    code_folder_id=None
    other_folder_id=None

    def __init__(self, name, name_folder_id, code_folder_id, other_folder_id):
        self.name = name
        self.name_folder_id=name_folder_id
        self.code_folder_id = code_folder_id
        self.other_folder_id = other_folder_id

    def get_name(self):
        return self.name

    def get_name_folder_id(self):
        return self.name_folder_id

    def get_code_folder(self):
        return self.code_folder_id

    def get_other_folder(self):
        return self.other_folder_id
"""

class G_drive:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    drive_service = None
    folders_dic = {}
    default_folder="1AH6x_N0XatI8jCK16KdWuOC2KJ_d-ybA"
    name_list=None
    show_list=None
    selected_student=None
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop')
    # desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 

    def __init__(self):
        self.drive_service = self.get_drive_service()
        self.get_folders_dic()
        self.name_list=list(self.folders_dic.keys())
        self.show_list=["--Please Select--"]
        self.show_list.extend(self.name_list)


    def get_drive_service(self):
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

    def get_folders_dic(self):
        
        page_token = None
        response = None
        while True:
            response = self.drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and '1AH6x_N0XatI8jCK16KdWuOC2KJ_d-ybA' in parents and trashed=false",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                children={}
                page_token_inner=None
                response_inner = self.drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and '{}' in parents and trashed=false" .format(file.get('id')),
                                                    spaces='drive',
                                                    fields='nextPageToken, files(id, name)',
                                                    pageToken=page_token_inner).execute()
                for file_inner in response_inner.get('files', []):
                    children[file_inner.get('name')]=file_inner.get('id')

                self.folders_dic[file.get('name')]={
                    'id':file.get('id'),
                    'children':children
                }

            

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    def is_student_exist(self, name):
        try:
            self.folders_dic[name]
            return True
        except:
            return False
        return False

    def create_new_student(self, student_name):
        if student_name==None or student_name=="":
            return

        if self.is_student_exist(student_name):
            messagebox.showinfo("Fail","Fail to create new student folder - Student Exist")
            return 
        if not self.is_student_exist(student_name):
            file_metadata = {
            'name': student_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents':[self.default_folder]
            }
            file = self.drive_service.files().create(body=file_metadata,
                                                fields='id').execute()
            
            code_metadata = {
            'name': "code",
            'mimeType': 'application/vnd.google-apps.folder',
            'parents':[file.get('id')]
            }

            new_code_folder = self.drive_service.files().create(body=code_metadata,
                                                            fields='id').execute()

            other_metadata = {
            'name': "other",
            'mimeType': 'application/vnd.google-apps.folder',
            'parents':[file.get('id')]
            }

            new_other_folder = self.drive_service.files().create(body=other_metadata,
                                                            fields='id').execute()
            self.folders_dic[student_name]={
                'id':file.get('id'),
                'children':{
                    'code':new_code_folder.get('id'),
                    'other':new_other_folder.get('id')
                }
            }
            if file.get('id')=="":
                messagebox.showerror("Fail", "Fail to create new profile")
            messagebox.showinfo("Success", "New Student Profile has been created")
            self.name_list.append(student_name)
            
    def update_show_list(self, user_entry=""):
        # update show_list depend on the user entry
        self.show_list=[]
        if user_entry==None or user_entry=="":
            self.show_list=["--Please Select--"]
            self.show_list.extend(self.name_list)
            return
        try:
            for name in self.name_list:
                if user_entry.lower() in name.lower():
                    self.show_list.append(name)
                
            if len(self.show_list)==0:
                self.show_list.append("--No Matching Name--")
                return
        

            self.show_list.insert(0,"--Please Select--")
            self.show_list.sort()
        except:
            return
        
    def get_code_foder_files(self, student):
        # print(self.folders_dic)
        student_files=[]
        page_token = None
        while True:
            response = self.drive_service.files().list(q="'{}' in parents and trashed=false" .format(self.folders_dic[student]['children']['code']),
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                student_files.append(file)
            page_token = response.get('nextPageToken', None)
            
            if page_token is None:
                break
        return student_files

    def download_file(self, file_id=None, file_name=None):

        try:
            file_path = os.path.join(self.desktop_path,file_name)
            # shutil.copy(file_name, self.desktop_path)
            while os.path.isfile(file_path):
                file_path += " copy.py"
            request = self.drive_service.files().get_media(fileId=file_id)
            fh = io.FileIO(file_path,'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                # print ("Download %d%%." % int(status.progress() * 100))
            messagebox.showinfo("OK","File downloaded")
        except:
            messagebox.showerror("Fail", "Fail to download file")
            return

    def upload_file(self, student_name):
        if not self.is_student_exist(student_name):
            messagebox.showinfo("","Please select a student")
            return
        file_name = filedialog.askopenfilename(initialdir="/", title="Select file")




        if file_name==None or file_name=="":
            messagebox.showinfo("","No file selected")
            return
        

        #check extension
        file_parent=None
        if file_name.lower().endswith('.py'):
            file_parent=self.folders_dic[student_name]['children']['code']
        else:
            file_parent=self.folders_dic[student_name]['children']['other']
            messagebox.showinfo("", "Non py file selected, file will be upload to 'other' folder")


        try:

            file_metadata = {'name':os.path.basename(file_name),
                            'parents':[file_parent]}
            media = MediaFileUpload(file_name)
            file = self.drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
            if len(file.get('id'))>1:
                messagebox.showinfo("", "File uploaded")
        except:
            messagebox.showerror("","Failed to upload file")

    def create_new_class(self, student_name=None, folder_name=None):

        def is_folder_exist():
            try:
                self.folders_dic[student_name]['children'][folder_name]
                return True
            except:
                return False

        if student_name==None or student_name=="":
            return
        if folder_name == None or folder_name=="":
            folder_name = "New Folder"

        if not self.is_student_exist(student_name):
            messagebox.showerror("Fail", "Please select a student from the dropdown")
            return

        if self.is_student_exist(student_name):
            if is_folder_exist():
                messagebox.showinfo("", folder_name + " exists for " + student_name)
                return

            new_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents':[self.folders_dic[student_name]['id'] ]
            }

            new_folder = self.drive_service.files().create(body=new_metadata,
                                                            fields='id').execute()

            if new_folder.get('id')=="":
                messagebox.showerror("Fail", "Fail to create new profile")
                return

            
            self.folders_dic[student_name]['children'][folder_name]= new_folder.get(id)

            messagebox.showinfo("Success",  folder_name + " has been created for "+student_name)



class Bb_window:
    my_drive = None
    window = None
    drop_down_box=None
    item_list=None
    student_files=[]

    def __init__(self):
        self.my_drive=G_drive()
        self.set_window()
        self.set_menu()
        self.set_top()
        self.set_bot()

    


    def new_student_popup(self):
        top = tk.Toplevel(self.window)
        top.title("NEW")

        x = self.window.winfo_rootx()
        y = self.window.winfo_rooty()
        geom = "+%d+%d" % (x, y)

        top.geometry(geom)
        top.resizable(0,0)

        top.grab_set()
        l = tk.Label(top,text="Student Name")
        e = tk.Entry(top)
        e.focus_force()

        def update_command():
            # e.delete(0, 'end')
            self.my_drive.update_show_list()
            self.drop_down_box['value']=self.my_drive.show_list


        bOk=tk.Button(top,text="OK", width=10,command=lambda: [self.my_drive.create_new_student(e.get()),update_command(), top.destroy()])
        bNo=tk.Button(top,text="CANCEL", width=10, command=lambda: [top.destroy()])
        
        l.grid(row=0,column=0)
        e.grid(row=0,column=1)
        bOk.grid(row=1,column=0)
        bNo.grid(row=1,column=1)

    def new_class_popup(self):
        top2 = tk.Toplevel(self.window)
        top2.title("NEW")

        x = self.window.winfo_rootx()
        y = self.window.winfo_rooty()
        geom = "+%d+%d" % (x, y)

        top2.geometry(geom)
        top2.resizable(0,0)

        top2.grab_set()
        l2 = tk.Label(top2,text="Class Name")
        e2 = tk.Entry(top2)
        e2.focus_force()


        bOk2=tk.Button(top2,text="OK", width=10,command=lambda: [self.my_drive.create_new_class(student_name=self.drop_down_box.get() ,folder_name=e2.get()), top2.destroy()])
        bNo2=tk.Button(top2,text="CANCEL", width=10, command=lambda: [top2.destroy()])
        
        l2.grid(row=0,column=0)
        e2.grid(row=0,column=1)
        bOk2.grid(row=1,column=0)
        bNo2.grid(row=1,column=1)

        
    def show_student_file(self, event=None):
        self.item_list.delete(0,'end')
        self.student_files=[]
        if self.drop_down_box.get() == "--Please Select--" or self.drop_down_box.get() == "--No Matching Name--":
            return

        i=0
        
        student_files = self.my_drive.get_code_foder_files(self.drop_down_box.get())
        for item in student_files:
            self.item_list.insert(i,item.get('name'))
            self.student_files.append(item.get('id'))
            i+=1

    def set_menu(self):
        menu = tk.Menu(self.window)
        newList = tk.Menu(menu, tearoff=0)
        newList.add_command(label='Student Profile', command=self.new_student_popup)
        newList.add_command(label='Class', command=self.new_class_popup)
        
        menu.add_cascade(label='New', menu=newList)

        def about_app():
            messagebox.showinfo("","This app is written in python by CHANGKAI YUAN")


        menu.add_command(label='About', command=about_app)


        self.window.config(menu=menu)

    def set_top(self):
        frame = tk.Frame(self.window)
        frame.place(width = 500, height = 250 )
        l1 = tk.Label(frame, text="Name")
        l1.place(relx = .22, rely=.3)
        text_var=tk.StringVar()
        e1 = tk.Entry(frame,width=34, textvariable=text_var)

        def track_text(event=None):
            self.my_drive.update_show_list(text_var.get())
            self.drop_down_box['value']=self.my_drive.show_list
            self.drop_down_box.current(0)

        e1.bind('<KeyRelease>',track_text)
        e1.place(height=30,relx = .3, rely=.3)

        self.drop_down_box = ttk.Combobox(frame,values=self.my_drive.show_list, width=30,font="Verdana 10", state="readonly")
        self.drop_down_box.place(anchor="c", relx=.5,rely=.7)
        self.drop_down_box.current(0)

        self.drop_down_box.bind("<<ComboboxSelected>>",self.show_student_file)


    def set_bot(self):
        frame = tk.Frame(self.window)
        frame.place(y=250, width = 500, height = 250 )

        list_frame = tk.Frame(frame)
        list_frame.place(width=250, height=250)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        self.item_list = tk.Listbox(list_frame)
        
        self.item_list.place(x=0,y=0, width=233,height=250)

        self.item_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.item_list.yview)

        button_frame = tk.Frame(frame)
        button_frame.place(x=250,width=250,height=250)

        def download_pack():
            try:
                self.my_drive.download_file(
                                    self.student_files[self.item_list.curselection()[0]], 
                                        self.item_list.get(self.item_list.curselection()))
            except:
                messagebox.showinfo("","Please select a file")


        down_button=tk.Button(button_frame, bd=5,text="DOWNLOAD", command= download_pack)

        # down_button=tk.Button(button_frame, bd=5,text="DOWNLOAD", command= 
        #                         lambda: self.my_drive.download_file(
        #                             self.student_files[self.item_list.curselection()[0]], 
        #                                 self.item_list.get(self.item_list.curselection())))
        
        down_button.place(width=250,height=125)


        up_button=tk.Button(button_frame, bd=5,text="UPLOAD", command=lambda : [self.my_drive.upload_file(self.drop_down_box.get()), self.show_student_file()] )
        up_button.place(y=124,width=250,height=125)


    def set_window(self):
        self.window = tk.Tk()
        self.window.title("BB UPLOAD")
        self.window.geometry("500x500")
        self.window.resizable(0,0)

    def run(self):
        self.window.mainloop()





def main():
    bb = Bb_window()
    bb.run()

if __name__ == '__main__':
    main()
