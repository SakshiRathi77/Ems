import csv
import datetime
import tkinter as tk
from datetime import date
from datetime import datetime
from tkinter import filedialog, messagebox
import os
import numpy as np
from PIL import Image, ImageTk
from sys import platform
from src import scrollable

col_name = ['REG ID', 'NAME']


class UpdateApplicationData:
    def __init__(self, installation: bool = False):
        # installing or not
        self.installation = installation

        # Get application Details
        self.application_details = np.load('./records/application_data.npy', allow_pickle=True).item()

        # data file loc for student and staff
        self.data_file_loc_stud = tk.StringVar()
        self.data_file_loc_stud.set('')
        self.data_file_loc_staff = tk.StringVar()
        self.data_file_loc_staff.set('')

        # Delete old Data for student and staff
        self.delete_old_data_stud = tk.IntVar()
        self.delete_old_data_stud.set(1)
        self.delete_old_data_staff = tk.IntVar()
        self.delete_old_data_staff.set(1)

        # Capacity value
        self.capacity = tk.StringVar()
        self.capacity.set('' if installation else str(self.application_details['capacity']))

        # End time value
        self.endTimeHour = tk.StringVar()
        self.endTimeHour.set('0' if installation else str(self.application_details['end_time'].hour))
        self.endTimeMin = tk.StringVar()
        self.endTimeMin.set('0' if installation else str(self.application_details['end_time'].minute))
        self.endTimeSec = tk.StringVar()
        self.endTimeSec.set('0' if installation else str(self.application_details['end_time'].second))

        # Password value
        self.old_password = tk.StringVar()
        self.new_password = tk.StringVar()
        self.confirm_password = tk.StringVar()

        # Saving directory
        self.saving_directory = tk.StringVar()
        self.saving_directory.set('' if installation else str(self.application_details['saving_data_location']))

        # Create tkinter window
        self.window = tk.Toplevel()

        # Set title
        self.window.title("    EMS " + "Installation and Setup" if installation else "Update Data")

        # Get window size
        self.window_width = self.window.winfo_screenwidth() // 2
        self.window_height = self.window.winfo_screenheight() // 2

        # Get Screen Width
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Coordinates for the update window on top to MainWindow
        self.x_coordinate = int((self.screen_width // 2) - (self.window_width // 2))
        self.y_coordinate = int((self.screen_height // 2) - (self.window_height // 2))

        # Set Window size and Place Window in Center
        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height,
                                                  self.x_coordinate, self.y_coordinate))

        # Always keep window on top
        self.window.grab_set()

        # Set Application Icon
        self.window.iconphoto(False, tk.PhotoImage(file="./assets/icon.png"))

        # Add Scrolling Frame
        self.scroll_window = scrollable.ScrolledFrame(self.window)
        self.scroll_window.pack(expand=True, fill='both')

        # Data format image
        self.bg_image = Image.open("./assets/data_file_format.png")
        self.bg_image = self.bg_image.resize(((self.window_width - 48), int((self.window_width - 48) * 64 / 787)))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Warning text, frame and label for data stud frame
        self.warningDataStud = tk.StringVar()
        self.warningDataStud.set('')
        self.frameDataStud = None
        self.labelWarningDataStud = None

        # Warning text, frame and label for data staff frame
        self.warningDataStaff = tk.StringVar()
        self.warningDataStaff.set('')
        self.frameDataStaff = None
        self.labelWarningDataStaff = None

        # Warning text, frame and label for capacity frame
        self.warningCapacity = tk.StringVar()
        self.warningCapacity.set('')
        self.frameCapacity = None
        self.labelWarningCapacity = None

        # Warning text, frame and label for end time frame
        self.warningEndTime = tk.StringVar()
        self.warningEndTime.set('')
        self.frameEndTime = None
        self.labelWarningEndTime = None

        # Warning text, frame and label for saving directory frame
        self.warningSavingDirectory = tk.StringVar()
        self.warningSavingDirectory.set('')
        self.frameSavingDirectory = None
        self.labelWarningSavingDirectory = None

        # Warning text, frame and label for password frame
        self.warningPassword = tk.StringVar()
        self.warningPassword.set('')
        self.framePassword = None
        self.labelWarningPassword = None

        # Warning text, bool to detect any warning and label for overall warning
        self.warning = tk.StringVar()
        self.warning.set("Click on 'Update Changes' to save")
        self.warningRaised = False
        self.labelWarning = tk.Label(self.scroll_window.inner, textvariable=self.warning,
                                     fg='grey50', font='Ariel 10 bold')

        # Declare and Display Update data for student frame
        self.updateDataFrame('student')

        # Declare and Display Update data for staff frame
        self.updateDataFrame('staff')

        # Declare and Display Update capacity frame
        self.updateCapacityFrame()

        # Declare and Display Update end time frame
        self.updateEndTimeFrame()

        # Declare and Display Update saving directory frame
        self.updateSavingDirectoryFrame()

        # Declare and Display change password frame
        self.changePasswordFrame()

        # Declare and Display overall warning frame
        self.warningFrame()

        # Declare and Display Update changes frame
        self.updateChangesFrame()

        # Window Closing Action using close 'x' button, call onClosing function
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)

        # Loop the Process
        self.window.mainloop()

    # Update data frame widget for student and staff
    def updateDataFrame(self, stud_or_staff: str):
        labelframe = tk.LabelFrame(self.scroll_window.inner, text="   Update " + stud_or_staff + " Records :  ",
                                   font='Ariel 9 bold', highlightbackground='grey94', highlightthickness=2,
                                   highlightcolor='grey94')
        labelframe.pack(fill="both", expand=True, padx=6, pady=14)

        lbl_warning = tk.Label(labelframe,
                               textvariable=self.warningDataStud
                               if stud_or_staff == 'student' else self.warningDataStaff,
                               fg='red', font='Ariel 9 bold', state=tk.DISABLED)
        lbl_warning.pack()

        # assign the frame and label variable to the respective class variable for student and staff
        if stud_or_staff == 'student':
            self.frameDataStud = labelframe
            self.labelWarningDataStud = lbl_warning
        else:
            self.frameDataStaff = labelframe
            self.labelWarningDataStaff = lbl_warning

        lbl_text = tk.Label(labelframe, text='Please upload in the given format only')
        lbl_text.pack(padx=6, pady=6, anchor=tk.NW)

        label = tk.Label(labelframe, image=self.bg_image)
        label.pack(padx=6, pady=6, anchor=tk.NW)

        # Checkbox widget
        check_delete_old_stud = tk.Checkbutton(labelframe, text="Delete old " + stud_or_staff + " data", fg='red',
                                               variable=self.delete_old_data_stud
                                               if stud_or_staff == 'student' else self.delete_old_data_staff,
                                               onvalue=1, offvalue=0)
        check_delete_old_stud.pack(padx=20, pady=10, anchor=tk.NW)

        lbl_text = tk.Label(labelframe, text='File: ')
        lbl_text.pack(padx=20, pady=10, side=tk.LEFT)

        data_loc_stud_entry = tk.Entry(labelframe,
                                       textvariable=self.data_file_loc_stud
                                       if stud_or_staff == 'student' else self.data_file_loc_staff,
                                       width=51, state=tk.DISABLED)
        data_loc_stud_entry.configure({"disabledforeground": "#060606", "disabledbackground": "#f6f6f6"})
        data_loc_stud_entry.pack(padx=6, pady=10, side=tk.LEFT)

        button = tk.Button(labelframe, text="Browse File", command=lambda: self.getDataFileLocation(stud_or_staff))
        button.pack(padx=20, pady=10, side=tk.LEFT)

    # File picker inbuilt method caller for student or staff respectively
    def getDataFileLocation(self, stud_or_staff: str):
        x = self.openFileSelector('File')
        if stud_or_staff == 'student':
            self.data_file_loc_stud.set(x)
        else:
            self.data_file_loc_staff.set(x)
        return

    def openFileSelector(self, file_or_directory='File'):
        root = tk.Tk()
        root.lift()
        root.withdraw()  # Hide root window
        file_name = ''
        if file_or_directory == 'File':
            if platform.lower() == 'linux':
                file_name = filedialog.askopenfilename(parent=root, initialdir='/home',
                                                       filetypes=[("CSV Files", "*.csv")])
            else:
                file_name = filedialog.askopenfilename(parent=root, filetypes=[("CSV Files", "*.csv")])
        else:
            if platform.lower() == 'linux':
                file_name =  filedialog.askdirectory(parent=root, initialdir='/home')
            else:
                file_name =  filedialog.askdirectory(parent=root)
        root.destroy()
        return file_name

    # Update capacity frame widget
    def updateCapacityFrame(self):
        labelframe = tk.LabelFrame(self.scroll_window.inner, text="   Update Capacity :  ",
                                   font='Ariel 9 bold', highlightbackground='grey94', highlightthickness=2,
                                   highlightcolor='grey94')
        labelframe.pack(fill="both", expand=True, padx=6, pady=14)

        self.frameCapacity = labelframe

        self.labelWarningCapacity = tk.Label(labelframe, textvariable=self.warningCapacity,
                                             fg='red', font='Ariel 9 bold', state=tk.DISABLED)
        self.labelWarningCapacity.pack()

        lbl_text = tk.Label(labelframe, text='Please only enter numeric values only')
        lbl_text.pack(padx=6, pady=10, anchor=tk.NW)

        lbl_text = tk.Label(labelframe, text='Capacity: ')
        lbl_text.pack(padx=20, pady=(6, 16), side=tk.LEFT)

        # Validate function for that it is numeric
        vcmd = (self.window.register(self.capacityValidation), '%S')
        capacity_entry = tk.Entry(labelframe, textvariable=self.capacity,
                                  width=31, validate='key', vcmd=vcmd)
        capacity_entry.pack(padx=6, pady=(6, 16), side=tk.LEFT)

    # Validate the capacity to be numeric only, else set warning
    def capacityValidation(self, text: str):
        self.resetSpecificWarning(self.frameCapacity, self.labelWarningCapacity, self.warningCapacity)
        try:
            if text == '' and self.capacity.get() == '':
                self.capacity.set('0')
            elif text == '':
                return True
            else:
                int(text)
            return True
        except Exception as error:
            print(error)
            self.setWarning('***   Capacity must be Numeric Value   ***', self.frameCapacity,
                            self.labelWarningCapacity, self.warningCapacity)
            self.window.bell()
            return False

    # Update end time frame widget
    def updateEndTimeFrame(self):
        labelframe = tk.LabelFrame(self.scroll_window.inner, text="   Change End time :  ",
                                   font='Ariel 9 bold', highlightbackground='grey94', highlightthickness=2,
                                   highlightcolor='grey94')
        labelframe.pack(fill="both", expand=True, padx=6, pady=14)

        self.frameEndTime = labelframe

        self.labelWarningEndTime = tk.Label(labelframe, textvariable=self.warningEndTime,
                                            fg='red', font='Ariel 9 bold', state=tk.DISABLED)
        self.labelWarningEndTime.pack()

        lbl_text = tk.Label(labelframe, text='Please enter time in 24hr format')
        lbl_text.pack(padx=6, pady=10, anchor=tk.NW)

        frame_clock = tk.Frame(labelframe)
        frame_clock.pack(padx=20, anchor=tk.NW, side=tk.TOP)

        lbl_text = tk.Label(frame_clock, text=' TIme : ', justify=tk.CENTER)
        lbl_text.pack(pady=(6, 16), side=tk.LEFT)

        vcmd_hour = (self.window.register(lambda text: self.timeValidation(text, 'hour')), '%P')
        vcmd_min = (self.window.register(lambda text: self.timeValidation(text, 'min')), '%P')
        vcmd_sec = (self.window.register(lambda text: self.timeValidation(text, 'sec')), '%P')

        lbl_text = tk.Label(frame_clock, text='Hour ', justify=tk.CENTER)
        lbl_text.pack(padx=(20, 0), pady=(6, 16), side=tk.LEFT)
        hour_dial = tk.Spinbox(frame_clock, from_=0, to=23, textvariable=self.endTimeHour, wrap=True,
                               width=4, font='Ariel 10', validate="key", validatecommand=vcmd_hour)
        hour_dial.pack(padx=(4, 20), pady=(6, 16), side=tk.LEFT)

        lbl_text = tk.Label(frame_clock, text='Minute ', justify=tk.CENTER)
        lbl_text.pack(pady=(6, 16), side=tk.LEFT)
        min_dial = tk.Spinbox(frame_clock, from_=0, to=59, textvariable=self.endTimeMin, wrap=True,
                              width=4, font='Ariel 10', validate="key", validatecommand=vcmd_min)
        min_dial.pack(padx=(4, 20), pady=(6, 16), side=tk.LEFT)

        lbl_text = tk.Label(frame_clock, text='Seconds ', justify=tk.CENTER)
        lbl_text.pack(pady=(6, 16), side=tk.LEFT)
        sec_dial = tk.Spinbox(frame_clock, from_=0, to=59, textvariable=self.endTimeSec, wrap=True,
                              width=4, font='Ariel 10', validate="key", validatecommand=vcmd_sec)
        sec_dial.pack(padx=(4, 20), pady=(6, 16), side=tk.LEFT)

    # Validate the input time to be number and in 24hr format and must be numeric, else set warning
    def timeValidation(self, text: str, timeElement: str):
        self.resetSpecificWarning(self.frameEndTime, self.labelWarningEndTime, self.warningEndTime)
        d = {'hour': (0, 23), 'min': (0, 59), 'sec': (0, 59)}
        time = None
        try:
            if text == '':
                time = 0
            else:
                time = int(text)
        except Exception as error:
            print(error)
            self.setWarning('***   Time must be Numeric Value   ***', self.frameEndTime,
                            self.labelWarningEndTime, self.warningEndTime)
            self.window.bell()
            return False
        if d[timeElement][0] <= time <= d[timeElement][1]:
            return True
        self.window.bell()  # .bell() plays that ding sound telling you there was invalid input
        return False

    # Update saving directory frame widget
    def updateSavingDirectoryFrame(self):
        labelframe = tk.LabelFrame(self.scroll_window.inner, text="   Select Entries Directory :  ",
                                   font='Ariel 9 bold', highlightbackground='grey94', highlightthickness=2,
                                   highlightcolor='grey94')
        labelframe.pack(fill="both", expand=True, padx=6, pady=14)

        self.frameSavingDirectory = labelframe

        self.labelWarningSavingDirectory = tk.Label(labelframe, textvariable=self.warningSavingDirectory,
                                                    fg='red', font='Ariel 9 bold', state=tk.DISABLED)
        self.labelWarningSavingDirectory.pack()

        lbl_text = tk.Label(labelframe, text='Select the directory to save entry data')
        lbl_text.pack(padx=6, pady=10, anchor=tk.NW)

        lbl_text = tk.Label(labelframe, text='Location: ')
        lbl_text.pack(padx=20, pady=10, side=tk.LEFT)

        saving_dir_loc_entry = tk.Entry(labelframe, textvariable=self.saving_directory,
                                        width=51, state=tk.DISABLED)
        saving_dir_loc_entry.configure({"disabledforeground": "#060606", "disabledbackground": "#f6f6f6"})
        saving_dir_loc_entry.pack(padx=6, pady=10, side=tk.LEFT)

        button = tk.Button(labelframe, text="Browse Location", command=self.getSavingDirectoryLocation)
        button.pack(padx=20, pady=10, side=tk.LEFT)

    # Get the saving directory location using inbuilt folder selector window
    def getSavingDirectoryLocation(self):
        self.saving_directory.set(self.openFileSelector('Directory'))

    # Change password frame widget
    def changePasswordFrame(self):
        labelframe = tk.LabelFrame(self.scroll_window.inner, text="   Change Password :  ",
                                   font='Ariel 9 bold', highlightbackground='grey94', highlightthickness=2,
                                   highlightcolor='grey94')
        labelframe.pack(fill="both", expand=True, padx=6, pady=14)

        self.framePassword = labelframe

        self.labelWarningPassword = tk.Label(labelframe, textvariable=self.warningPassword,
                                             fg='red', font='Ariel 9 bold', state=tk.DISABLED)
        self.labelWarningPassword.pack()

        lbl_text = tk.Label(labelframe, text='Please only enter numeric values')
        lbl_text.pack(padx=6, pady=10, anchor=tk.NW)

        lname = ['Current', 'New', 'Confirm']
        lpad = [4, 20, 0]

        for i in range(3):
            frm1 = tk.Frame(labelframe)
            frm1.pack(anchor=tk.NW, side=tk.TOP)

            lbl_text = tk.Label(frm1, text=lname[i] + ' Password: ')
            lbl_text.pack(padx=20, pady=(6, 16), side=tk.LEFT)

            capacity_entry = tk.Entry(frm1, textvariable=self.old_password if i == 0 else (
                self.new_password if i == 1 else self.confirm_password), width=31)
            capacity_entry.pack(padx=8 + lpad[i], pady=(6, 16), side=tk.LEFT)

    # Display Warning Frame
    def warningFrame(self):
        self.labelWarning.pack()

    # Update changes button frame widget
    def updateChangesFrame(self):
        labelframe = tk.Frame(self.scroll_window.inner)
        labelframe.pack()

        button = tk.Button(labelframe, text="Update Changes", font='Ariel 9 bold', padx=10, pady=4,
                           fg='white', bg='#0288d1', command=self.updateChanges)
        button.pack(padx=20, pady=(10, 20), anchor=tk.CENTER, side=tk.LEFT)

        button = tk.Button(labelframe, text="Cancel", font='Ariel 9 bold', padx=10, pady=4, command=self.onClosing)
        button.pack(padx=20, pady=(10, 20), side=tk.LEFT)

    # Update Changes button callback, to validate the filled data and make decisions accordingly
    def updateChanges(self):
        # Reset all previous warnings
        self.resetAllWarning()

        data, reg_id_stud, reg_id_staff = dict(), set(), set()

        try:
            if self.installation:
                # Delete previous data if in installation
                self.delete_old_data_stud.set(1)
                self.delete_old_data_staff.set(1)

                # Process Student and staff Data
                data, reg_id_stud, reg_id_staff = self.processDataFile('student', data, reg_id_stud, reg_id_staff)
                data, reg_id_stud, reg_id_staff = self.processDataFile('staff', data, reg_id_stud, reg_id_staff)

                # check if capacity is given, else set warning for this widget
                if self.capacity.get() == '' or self.capacity.get() == '0':
                    self.setWarning('***   Please Enter Maximum Capacity   ***', self.frameCapacity,
                                    self.labelWarningCapacity, self.warningCapacity)
                    self.warningRaised = True

                # check if end time is given, else set warning for this widget
                if (self.endTimeHour.get() == '' and self.endTimeMin.get() == '' and self.endTimeSec.get() == '') or (
                        self.endTimeHour.get() == '0' and self.endTimeMin.get() == '0' and self.endTimeSec.get() == '0'):
                    self.setWarning("***   Please Enter Time Don't Leave Blank   ***", self.frameEndTime,
                                    self.labelWarningEndTime, self.warningEndTime)
                    self.warningRaised = True

                # check if saving dir is given, else set warning for this widget
                if self.saving_directory.get() == '':
                    self.setWarning('***   Please Select A Directory to Save Entries   ***', self.frameSavingDirectory,
                                    self.labelWarningSavingDirectory, self.warningSavingDirectory)
                    self.warningRaised = True

                # check if new and confirm password are same, else set warning for this widget
                if self.new_password.get() == '':
                    self.setWarning('***   Please Enter Password   ***', self.framePassword,
                                    self.labelWarningPassword, self.warningPassword)
                    self.warningRaised = True
                elif self.new_password.get() != self.confirm_password.get():
                    self.setWarning("***   New Password and Confirm Password Don't Match   ***", self.framePassword,
                                    self.labelWarningPassword, self.warningPassword)
                    self.warningRaised = True
            # if not in installation stage
            else:
                # check if to update stud data, if yes then process the data
                if self.data_file_loc_stud.get() != '':
                    data, reg_id_stud, reg_id_staff = self.processDataFile('student', data, reg_id_stud, reg_id_staff)

                # check if to update staff data, if yes then process the data
                if self.data_file_loc_staff.get() != '':
                    data, reg_id_stud, reg_id_staff = self.processDataFile('staff', data, reg_id_stud, reg_id_staff)

                # check if to update capacity, no then put old capacity into it
                if self.capacity.get() == '' or self.capacity.get() == '0':
                    self.setWarning('***   Please Enter Maximum Capacity   ***', self.frameCapacity,
                                    self.labelWarningCapacity, self.warningCapacity)
                    self.warningRaised = True

                # Check if to change saving directory, no then put old location
                if self.saving_directory.get() == '':
                    self.saving_directory.set(self.application_details['saving_data_location'])

                # Check if to change password, no then put old password
                if self.old_password.get() != '' or self.new_password.get() != '' or self.confirm_password.get() != '':
                    if self.old_password.get() != self.application_details['password']:
                        self.setWarning("***   Wrong Current Password   ***",
                                        self.framePassword,
                                        self.labelWarningPassword, self.warningPassword)
                        self.warningRaised = True
                    elif self.new_password.get() != self.confirm_password.get():
                        self.setWarning("***   New Password and Confirm Password Don't Match   ***",
                                        self.framePassword,
                                        self.labelWarningPassword, self.warningPassword)
                        self.warningRaised = True
                else:
                    self.new_password.set(self.application_details['password'])
                    self.confirm_password.set(self.application_details['password'])

            # If warning not raised then proceed to close the top window
            if not self.warningRaised:
                # Create saving data directory if it does not exists and folder under it
                if 'EMS Data' not in os.listdir(self.saving_directory.get()):
                    os.mkdir(self.saving_directory.get() + '/EMS Data')
                    os.mkdir(self.saving_directory.get() + '/EMS Data/ProfileData')
                    os.mkdir(self.saving_directory.get() + '/EMS Data/DailyData')
                    open(self.saving_directory.get() + '/EMS Data/errors.txt', 'w').close()

                # Stores the records and application data
                self.storeRecordsAndApplicationDetails(data, reg_id_stud, reg_id_staff)
                # Close the window
                self.onClosing()
        # If errors cause then add it to the errors file
        except Exception as error:
            f = open(self.application_details['saving_data_location']+"/EMS Data/errors.txt", 'a')
            f.write(str(date.today()) + "-" + str(datetime.now()) + "\n")
            f.write(str(error))
            f.write("\n Inside Update - While Updating data")
            f.write("\n==============================================================")
            f.write("==============================================================\n\n\n")
            f.close()

    # Process the Given data file and extract data
    # Only this function must be changed if the input data format changes
    def processDataFile(self, stud_or_staff: str, data: dict, reg_id_stud: set, reg_id_staff: set):
        reg_id = set()
        file_name = self.data_file_loc_stud.get() if stud_or_staff == 'student' else self.data_file_loc_staff.get()
        # If location not given then set warning
        if file_name == '':
            if stud_or_staff == 'student':
                self.setWarning('***   Please Select Student Data File   ***', self.frameDataStud,
                                self.labelWarningDataStud, self.warningDataStud)
            else:
                self.setWarning('***   Please Select Staff Data File   ***', self.frameDataStaff,
                                self.labelWarningDataStaff, self.warningDataStaff)
            self.warningRaised = True
        else:
            fr = csv.reader(open(file_name, mode='r'))
            i = 0
            for line in fr:
                if i == 0:
                    # If no. of columns does not match the given format then set warning
                    if len(line) != len(col_name):
                        if stud_or_staff == 'student':
                            self.setWarning('***   Student Data File is not as per Format   ***', self.frameDataStud,
                                            self.labelWarningDataStud, self.warningDataStud)
                        else:
                            self.setWarning('***   Staff Data File is not as per Format   ***', self.frameDataStaff,
                                            self.labelWarningDataStaff, self.warningDataStaff)
                        self.warningRaised = True
                    i += 1
                    continue
                # Add the data to data and reg_id
                line = [word.strip() for word in line]
                data[line[1].upper()] = data.get(line[1].upper(), line[2:])
                reg_id.add(line[1].upper())

        # Add the reg_id to there respective reg_id's for student and staff
        if stud_or_staff == 'student':
            reg_id_stud = reg_id
        else:
            reg_id_staff = reg_id
        return data, reg_id_stud, reg_id_staff

    def storeRecordsAndApplicationDetails(self, data: dict, reg_id_stud: set, reg_id_staff: set):

        # Save records
        if self.installation:
            # Save records
            np.save('./records/data.npy', data, allow_pickle=True)

            # Save reg_id
            reg_id = reg_id_stud | reg_id_staff
            fr = open('./records/reg_id.txt', 'w')
            fr.write("\n" + "\n".join(reg_id) + "\n")
            fr.close()

            # Save reg_id of student and staff differently
            fr = open('./records/reg_id_stud.txt', 'w')
            fr.write("\n" + "\n".join(reg_id_stud) + "\n")
            fr.close()
            fr = open('./records/reg_id_staff.txt', 'w')
            fr.write("\n" + "\n".join(reg_id_staff) + "\n")
            fr.close()
        else:
            # load the records
            data_old = np.load('./records/data.npy', allow_pickle=True).item()
            reg_id_old = set(open('./records/reg_id.txt', 'r').read().strip().split('\n'))
            reg_id_stud_old = set(open('./records/reg_id_stud.txt', 'r').read().strip().split('\n'))
            reg_id_staff_old = set(open('./records/reg_id_staff.txt', 'r').read().strip().split('\n'))

            # Remove any blank spaces considered as reg_id if the file is empty
            reg_id_old.discard('')
            reg_id_stud_old.discard('')
            reg_id_staff_old.discard('')

            # delete old student data
            if self.delete_old_data_stud.get() == 1 and self.data_file_loc_stud.get() != '':
                data_old, reg_id_old = self.deleteOldRecord(data_old, reg_id_old, reg_id_stud_old)
                reg_id_stud_old = set()

            # delete old staff data
            if self.delete_old_data_staff.get() == 1 and self.data_file_loc_staff.get() != '':
                data_old, reg_id_old = self.deleteOldRecord(data_old, reg_id_old, reg_id_staff_old)
                reg_id_staff_old = set()

            # Update data for student and staff
            data_new = dict()
            data_new.update(data_old)
            data_new.update(data)

            # Update reg_id for student and staff
            reg_id_new = reg_id_old | reg_id_stud | reg_id_staff
            reg_id_stud_new = reg_id_stud_old | reg_id_stud
            reg_id_staff_new = reg_id_staff_old | reg_id_staff

            # Save records
            np.save('./records/data.npy', data_new, allow_pickle=True)

            # Save reg_id
            fr = open('./records/reg_id.txt', 'w')
            fr.write("\n" + "\n".join(reg_id_new) + "\n")
            fr.close()

            # Save reg_id of student and staff differently
            fr = open('./records/reg_id_stud.txt', 'w')
            fr.write("\n" + "\n".join(reg_id_stud_new) + "\n")
            fr.close()
            fr = open('./records/reg_id_staff.txt', 'w')
            fr.write("\n" + "\n".join(reg_id_staff_new) + "\n")
            fr.close()

        today = date.today()
        end_time = str(today)+":"+self.endTimeHour.get()+"-"+self.endTimeMin.get()+"-"+self.endTimeSec.get()

        # Save Application Details
        self.application_details['saving_data_location'] = self.saving_directory.get()
        self.application_details['capacity'] = self.capacity.get()
        self.application_details['end_time'] = datetime.strptime(end_time, "%Y-%m-%d:%H-%M-%S")
        self.application_details['previous_session_date'] = date.today()
        self.application_details['password'] = self.new_password.get()

        np.save('./records/application_data.npy', self.application_details, allow_pickle=True)

    # Delete the student or staff records if delete old data set respectively
    # noinspection PyMethodMayBeStatic
    def deleteOldRecord(self, data_old: dict, reg_id_old: set, reg_id_remove: set):
        for id_remove in reg_id_remove:
            reg_id_old.discard(id_remove)
            data_old.pop(id_remove)

        return data_old, reg_id_old

    # Reset warning for a give frame
    def resetSpecificWarning(self, frame, label, warningVar):
        frame.configure(highlightbackground='grey94', highlightcolor='grey94')
        warningVar.set('')
        label.configure(pady=0, state=tk.NORMAL)

        self.warning.set("Click on 'Update Changes' to save")
        self.labelWarning.configure(fg='grey50')

    # Reset warning for all frames
    def resetAllWarning(self):
        self.warningRaised = False

        # Reset frame red border
        self.frameDataStud.configure(highlightbackground='grey94', highlightcolor='grey94')
        self.frameDataStaff.configure(highlightbackground='grey94', highlightcolor='grey94')
        self.frameCapacity.configure(highlightbackground='grey94', highlightcolor='grey94')
        self.frameSavingDirectory.configure(highlightbackground='grey94', highlightcolor='grey94')
        self.framePassword.configure(highlightbackground='grey94', highlightcolor='grey94')

        # Reset warning text
        self.warningDataStud.set('')
        self.warningDataStaff.set('')
        self.warningCapacity.set('')
        self.warningSavingDirectory.set('')
        self.warningPassword.set('')

        # Reset warning label
        self.labelWarningDataStud.configure(pady=0, state=tk.DISABLED)
        self.labelWarningDataStaff.configure(pady=0, state=tk.DISABLED)
        self.labelWarningCapacity.configure(pady=0, state=tk.DISABLED)
        self.labelWarningSavingDirectory.configure(pady=0, state=tk.DISABLED)
        self.labelWarningPassword.configure(pady=0, state=tk.DISABLED)

        # Reset the overall warning frame
        self.warning.set("Click on 'Update Changes' to save")
        self.labelWarning.configure(fg='grey50')

    # Set warning for given frame
    def setWarning(self, warningText, frame, label, warningVar):
        frame.configure(highlightbackground='red', highlightcolor='red')
        warningVar.set(warningText)
        label.configure(pady=0, state=tk.NORMAL)

        self.warning.set("***   ↑ Error Please Check Above ↑   *** \n\n Click on 'Update Changes' to save")
        self.labelWarning.configure(fg='red')

    # Close the update data window
    def onClosing(self):
        # if in installation state and all the data are not filed then notify the Admin user
        if any([self.application_details[key] is None for key in self.application_details.keys()]):
            self.showErrorMessage()
        # Destroy and close the window
        else:
            self.window.destroy()
            self.window.quit()

    def showErrorMessage(self):
        root = tk.Tk()
        root.lift()
        root.withdraw()  # Hide root window
        messagebox.showerror(parent=root,title="Error", message="Please Complete the Installation and Setup")

    # Return records and Application data to previous window
    def getUpdatedApplicationDetails(self):
        return self.application_details
