The default credentials and token is only for testing 
You may get new credential and token to authorize this app to use your account

Help:
	MenuBar: New -> student profile will create a new folder in google drive 

	Type student name in the text entry to search for a student name

	Select a name from the dropdown

	Click "Show My Files" to update student file list 
		-"Show My Files" button is not neccessary if you manually select a name
		- manually select a name will automatically update student files

	Downloaded file will go to the same folder as this "readme.txt" file.
	Uploaded file will go to the folder with the name in the dropdown


update 1	(04/05/2020):
	MAJOR:

		*In menubar, now you can create a new class (folder) for selected student

		*Created new student profile is now under the "students" folder, and each student folder will have two subfolders (code, other)
	
		*removed the "show my file" button, student files will be present when the student name is selected automatically
	
		*Download: File will be downloaded to "desktop", if file with the same name exist, the downloaded file will be "File name" + "copy.py"
				- file will not be overwrite
	
		*Upload: '.py' file will be uploaded to the 'code' folder under the selected student name
			 other files will be uploaded to the 'other' folder under the selected student name

	MINORS:

		*Message box will present when upload or download is performed or complete

		*redesigned the code structure to increase the readability of the code, and increase the speed of the program
