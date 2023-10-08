import csv
import os
import sys
import tkinter as tk
from datetime import date
from datetime import datetime
from datetime import timedelta
from tkinter import messagebox
from tkinter.simpledialog import askstring
import numpy as np
from PIL import Image, ImageTk
from src import update
import re
from sys import platform
import pickle
# os.chdir(sys._MEIPASS)

def destroyWindow(win):
    win.destroy()
    win.quit()

def notFound(parent_window, reg_id, win_width, win_height):
    win = tk.Toplevel(parent_window)

    # Get window size
    window_width = win_width // 2
    window_height = win_height // 5

    # Coordinates for the update window on top to MainWindow
    x_coordinate = int((win_width // 2) - (window_width // 2))
    y_coordinate = int((win_height // 2) - (window_height // 2))

    # Set Window size and Place Window in Center
    win.geometry("{}x{}+{}+{}".format(window_width, window_height,
                                      x_coordinate, y_coordinate))

    lbl = tk.Label(win, text=reg_id + " NOT FOUND", padx=50, pady=13,
                   border=4, font=('Arial', 35, 'bold'), fg='red')
    lbl.pack(side=tk.TOP, pady=5)

    win.after(1500, lambda: destroyWindow(win))
    win.mainloop()


class MainWindow:

    def __init__(self):
        # Store today's date
        self.today = date.today()
        # Dictionary to save user records with key as reg_id
        self.data = None
        # String to save reg_id of user separated by \n, used to search the if reg_id exists or not
        self.reg_id = None
        # Application data Value
        self.application_details = np.load('records/application_data.npy', allow_pickle=True).item()
        # Create tkinter window
        self.window = tk.Tk()
        # Set title
        self.window.title("    EMS")
        # Set window size as fullscreen
        if platform.lower() == 'linux':
            self.window.attributes('-zoomed', True)
        else:
            self.window.state('zoomed')

        # Get window size
        self.window_width = self.window.winfo_screenwidth()
        self.window_height = self.window.winfo_screenheight()

        self.window_width_multiplier = self.window_width / 1280
        self.window_height_multiplier = self.window_height / 720

        # Set Application Icon
        self.window.iconphoto(False, tk.PhotoImage(file="assets/icon.png"))

        # End time value
        self.endTime = tk.StringVar()
        self.endTime.set(self.getFormattedEndTime())

        # Capacity Value
        self.capacity = tk.StringVar()
        if self.application_details['capacity'] is not None:
            self.capacity.set("    " +
                              str(int(self.application_details['capacity']) -
                                  len(np.load("./cache/inside_cache.npy",
                                              allow_pickle=True).item().keys()))
                              if self.application_details['capacity'] is not None else "200")

        # Set background image
        # Input and resize image
        bg_image = Image.open("./assets/background_image.png")
        bg_image = bg_image.resize((self.window_width, self.window_height))
        bg_image = ImageTk.PhotoImage(bg_image)
        # Create Canvas
        self.canvas = tk.Canvas(self.window)
        self.canvas.grid(row=0, column=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # Display image
        self.canvas.create_image(0, 0, image=bg_image, anchor=tk.NW)

        # Update the window state
        self.window.update()

        # Text entry widget
        self.entry = tk.Entry(self.window, width=24, borderwidth=4, font=('Arial', int(22 * self.window_height_multiplier)))
        self.entry.focus_set()
        # call entryButton function when 'ENTER' button pressed on keyboard
        self.entry.bind("<Return>", self.entryButton)

        # Enter Button
        self.button_enter = tk.Button(self.window, text="Enter", font=('Arial', int(16 * self.window_height_multiplier)),
                                      padx=40 / self.window_width_multiplier,
                                      pady=8 / self.window_height_multiplier, border=4,
                                      command=self.entryButton)

        # Capacity Text
        self.capacity_text = tk.Label(self.window, text="Capacity :",
                                      padx=50 / self.window_width_multiplier,
                                      pady=13 / self.window_height_multiplier,
                                      border=4, font=('Arial', int(16 * self.window_height_multiplier)))

        # Capacity widget
        self.capacity_entry = tk.Entry(self.window, textvariable=self.capacity, width=10,
                                       borderwidth=4, font=('Arial', int(19 * self.window_height_multiplier)), state=tk.DISABLED)
        self.capacity_entry.configure({"disabledforeground": "#060606", "disabledbackground": "#f6f6f6"})


        # End Time Text
        self.end_time_text = tk.Label(self.window, text="End Time :",
                                      padx=50 / self.window_width_multiplier,
                                      pady=13 / self.window_height_multiplier,
                                      border=4, font=('Arial', int(16 * self.window_height_multiplier)))

        # Capacity widget
        self.end_time_entry = tk.Entry(self.window, textvariable=self.endTime, width=10,
                                       borderwidth=4, font=('Arial', int(19 * self.window_height_multiplier)), state=tk.DISABLED)
        self.end_time_entry.configure({"disabledforeground": "#060606", "disabledbackground": "#f6f6f6"})

        # End Day Button
        self.button_end_day = tk.Button(self.window, text="End Day", font=('Arial', int(16 * self.window_height_multiplier)),
                                        padx=40 / self.window_width_multiplier,
                                        pady=8 / self.window_height_multiplier,
                                        border=4, command=self.onClosing)

        # Update Data
        self.button_update_data = tk.Button(self.window, text="Update Data", font=('Arial', int(16 * self.window_height_multiplier)),
                                            padx=40 / self.window_width_multiplier,
                                            pady=8 / self.window_height_multiplier,
                                            border=4, command=self.updateData)

        # Window Closing Action using close 'x' button, call onClosing function
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
        # Display all the widgets
        self.displayWindow()
        # Loop the Process
        self.window.mainloop()

    def displayWindow(self):
        # Display Entry widgets
        self.canvas.create_window(120 * self.window_width_multiplier, 80 * self.window_height_multiplier,
                                  anchor=tk.NW, window=self.entry)
        self.canvas.create_window(self.window_width - 340 * self.window_width_multiplier,
                                  70 * self.window_height_multiplier, anchor=tk.NW, window=self.button_enter)

        # Display Capacity widgets
        self.canvas.create_window(120 * self.window_width_multiplier, 260 * self.window_height_multiplier,
                                  anchor=tk.NW, window=self.capacity_text)
        self.canvas.create_window(390 * self.window_width_multiplier, 270 * self.window_height_multiplier,
                                  anchor=tk.NW, window=self.capacity_entry)

        # Display End time widgets
        self.canvas.create_window(790 * self.window_width_multiplier, 260 * self.window_height_multiplier,
                                  anchor=tk.NW, window=self.end_time_text)
        self.canvas.create_window(1020 * self.window_width_multiplier, 270 * self.window_height_multiplier,
                                  anchor=tk.NW, window=self.end_time_entry)

        # Display End day widgets
        self.canvas.create_window(120 * self.window_width_multiplier, 450 * self.window_height_multiplier,
                                  anchor=tk.NW, window=self.button_end_day)

        # Display update data widgets
        self.canvas.create_window(self.window_width - 340 * self.window_width_multiplier,
                                  450 * self.window_height_multiplier,
                                  anchor=tk.NW, window=self.button_update_data)

        # Check for initial installation condition if yes then open the update.py to update data
        if any([self.application_details[key] is None for key in self.application_details.keys()]):
            self.updateData()
        # Load reg_ids and data.npy
        self.loadRecords()

        # check the date, and if it's different ,save all previous session records
        if self.today - self.application_details['previous_session_date'] >= timedelta(days=1):
            cache = np.load("./cache/inside_cache.npy", allow_pickle=True).item()
            daily_cache = open("./cache/daily_cache.csv", 'r').read()
            print(daily_cache)
            if cache != {} or daily_cache != "":
                try:

                    self.saveEntries()
                    self.application_details['previous_session_date'] = self.today
                    np.save('./records/application_data.npy', self.application_details, allow_pickle=True)
                except Exception as error:
                    f = open(self.application_details['saving_data_location'] + "/EMS Data/errors.txt", 'a')
                    f.write(str(datetime.now()) + "\n")
                    f.write(str(error))
                    f.write("\n Inside Main - While saving Daily and Profile Data")
                    f.write("\n==============================================================\n")
                    f.write("==============================================================\n\n")
                    f.close()
            else:
                self.application_details['previous_session_date'] = self.today
                np.save('./records/application_data.npy', self.application_details, allow_pickle=True)
        # Check if the previous logged in day greater than today, if yes then warn user if to check system date
        elif self.today - self.application_details['previous_session_date'] < timedelta(days=0):
            messagebox.showwarning("Warning", "The system was logged in " +
                                    str(self.today - self.application_details['previous_session_date']) +
                                    " ago" + "\n\n Please check the system date if changed")

        # Update the canvas and window to show the widgets
        self.canvas.update()
        self.window.update()

    # It loads the records (data, reg_id) in to the variables
    def loadRecords(self):
        self.data = np.load('./records/data.npy', allow_pickle=True).item()
        self.reg_id = open('./records/reg_id.txt', 'r').read()

    # Perform task for given Entry
    # noinspection PyUnusedLocal
    def entryButton(self, enterPressed=True):

        # Get entry time
        input_time = datetime.now()
        # Get the reg_id for that entry
        reg_id_entry = self.entry.get().upper()
        # Clear the entry widget display
        self.entry.delete(0, tk.END)

        # find all the reg_id that matches the entry reg_id with tolerance of two letters on both side
        ids_list = None
        # This search is for staff reg_id
        if len(reg_id_entry) < 4:
            ids_list = re.findall("\s(" + reg_id_entry + ")\s", self.reg_id)
        # This search is for student reg_id
        else:
            ids_list = re.findall("\s(" + reg_id_entry + ")\s", self.reg_id)

        n = len(ids_list)
        # If length of ids_list > 1, then there are many possible reg_id (The input might not be proper)
        if n > 1 or n == 0:
            f = open(self.application_details['saving_data_location'] + "/EMS Data/Not Found.txt", 'a')
            f.write(str(datetime.now()) + "\n")
            f.write(reg_id_entry + " -- Not Found\n")
            f.write("==============================================================\n")
            f.close()
            notFound(self.window, reg_id_entry, self.window.winfo_screenwidth(), self.window.winfo_screenheight())


        else:
            # Load inside_cache file
            cache = np.load("./cache/inside_cache.npy", allow_pickle=True).item()
            exists_inside = cache.get(ids_list[0], False)
            # Check if the entry_reg_id is in inside_cache if yes then remove that form there and add it to daily_cache
            # This means that the user has exited
            if exists_inside:
                daily_cache = csv.writer(open("cache/daily_cache.csv", 'a', newline=''))
                # If the ids_list is in dictionary
                if ids_list[0] in self.data:
                    daily_cache.writerow([ids_list[0]] + [self.data[ids_list[0]]] +
                                         [str(self.today), exists_inside.strftime("%X"),
                                          input_time.strftime("%X")])
                # Handle the case where the key does not exist
                else:
                    print("Key ",ids_list[0]," not found in self.data")
                # Remove the reg_id from inside_cache
                cache.pop(ids_list[0])
                # Update the capacity
                self.capacity.set(str(int(self.capacity.get()) + 1))

            # User is not inside the room add him in inside_cache and the IN TIME
            else:
                if int(self.capacity.get())<=0:
                    # Update the capacity again to 200
                    self.capacity.set(str(int(self.application_details['capacity'])))
            # Add user to inside cache with IN TIME
                cache[ids_list[0]] = input_time
                # Update the capacity
                self.capacity.set(str(int(self.capacity.get()) - 1))
            # Save the changes made to inside_cache into the file
            np.save("./cache/inside_cache.npy", cache, allow_pickle=True)

    # Format time from datetime.datetime to a string ' HH : MM : SS'
    def getFormattedEndTime(self):
        if self.application_details['end_time'] is None:
            return '00:00:00'
        h = str(self.application_details['end_time'].hour)
        m = str(self.application_details['end_time'].minute)
        s = str(self.application_details['end_time'].second)
        if len(h) == 1:
            h = '0' + h
        if len(m) == 1:
            m = '0' + m
        if len(s) == 1:
            s = '0' + s

        return ' ' + h + ' : ' + m + ' : ' + s

    # Closing the application
    def onClosing(self):
        # Destroy the window
        self.window.destroy()
        self.window.quit()
        # Close the exe file operation
        sys.exit()

    # Save Data for the day
    def saveEntries(self):
        # Get year, month and ay as a string from datetime.datetime
        year, month, day = str(self.application_details['previous_session_date']).split('-')
        # load inside_cache
        cache = np.load("./cache/inside_cache.npy", allow_pickle=True).item()
        # Get out time with today's date as datetime.datetime
        out_time = datetime(int(year), int(month), int(day), int(self.endTime.get()[1:3]),
                            int(self.endTime.get()[6:8]), int(self.endTime.get()[11:]))

        # load daily_cache as append to append remaining inside_cache
        daily_cache = csv.writer(open("./cache/daily_cache.csv", 'a', newline=''))

        # If there is any entries remaining in inside_cache save it to daily_cache with the end time as out time
        for key in cache.keys():
            if key in self.data:
                daily_cache.writerow([key] + [self.data[key]] +
                                     [str(self.application_details['previous_session_date']), cache[key].strftime("%X"),
                                      out_time.strftime("%X")])

        # load daily_cache as readonly for sorting and unique retrieval

        daily_cache = csv.reader(open("./cache/daily_cache.csv", 'r'))
        daily_data = []
        daily_data_unique = set()  # Unique reg_id entries
        # Add daily and unique daily entries
        for line in daily_cache:
            daily_data.append(line)
            daily_data_unique.add(",".join(line[:3]))

        # Get saving directory location
        saving_dir = self.application_details['saving_data_location'] + "/EMS Data"
        saving_dir_year_month = saving_dir + "/DailyData/" + year + "/" + month + "] " + getMonthName(int(month))

        # Create directory if not exist
        if year not in os.listdir(saving_dir + "/DailyData"):
            os.mkdir(saving_dir + "/DailyData/" + year)
        if month + "] " + getMonthName(int(month)) not in os.listdir(saving_dir + "/DailyData/" + year):
            os.mkdir(saving_dir_year_month)

        # save data profile wise
        for profile_entry in daily_data:
            writer = None
            if profile_entry[0] + ".csv" not in os.listdir(saving_dir + "/ProfileData"):
                writer = csv.writer(open(saving_dir + "/ProfileData/" + profile_entry[0] + ".csv", "a", newline=''))
                writer.writerow(['DATE', 'IN Time', 'OUT TIME'])
            else:
                writer = csv.writer(open(saving_dir + "/ProfileData/" + profile_entry[0] + ".csv", "a", newline=''))
            writer.writerow(profile_entry[2:])

        # If file for daily data present then add the entries to the daily_data
        daily_fr=open(saving_dir_year_month + "/" + str(self.application_details['previous_session_date']) + ".csv", 'w')
        if str(self.application_details['previous_session_date']) + ".csv" in os.listdir(saving_dir_year_month):
            i = 0
            for line in csv.reader(open(saving_dir_year_month + "/" + str(self.application_details['previous_session_date']) + ".csv", 'r')):
                if i == 0:
                    i += 1
                    continue
                daily_data.append(line)

        # If file for daily data unique present then add the entries to the daily_data_unique
        unique_fr = open(
            saving_dir_year_month + "/" + str(self.application_details['previous_session_date']) + "-unique.csv", "w")
        if str(self.application_details['previous_session_date']) + "-unique.csv" in os.listdir(saving_dir_year_month):
            i = 0
            for line in csv.reader(open(saving_dir_year_month + "/" + str(self.application_details['previous_session_date']) + "-unique.csv", 'r')):
                if i == 0:
                    i += 1
                    continue
                daily_data_unique.add(','.join(line))
        # Sort daily data based on IN TIME
        daily_data.sort(key=lambda x: x[4])
        # Add column name
        daily_data = [",".join(x)+"\n" for x in daily_data]
        daily_data_unique = ['REG ID,NAME,DATE'] + sorted(list(daily_data_unique))

        # save daily data
        np.savetxt(saving_dir_year_month + "/" + str(self.application_details['previous_session_date']) + ".csv", daily_data, delimiter=",", fmt='% s')

        unique_fr.write("\n".join(daily_data_unique))
        unique_fr.close()
        print("unique records saved ")
        # Empty the inside_cache and daily_cache for next day
        cache = dict()
        np.save("./cache/inside_cache.npy", cache, allow_pickle=True)
        daily_cache_fr = open('./cache/daily_cache.csv', 'w')
        daily_cache_fr.write('')
        daily_cache_fr.close()
        self.capacity.set(self.application_details['capacity'])
        # Update the window
        self.window.update()

    # Update the data
    def updateData(self):
        # if password is Not set then update the information in installation mode
        if self.application_details['password'] is None:
            # Call the update window
            update_window = update.UpdateApplicationData(installation=True)
            # Update all the values for this window
            self.application_details = update_window.getUpdatedApplicationDetails()
            self.capacity.set(self.application_details['capacity'])
            self.endTime.set(self.getFormattedEndTime())
            self.loadRecords()
        # Ask for password, if correct open the update window else display incorrect password
        elif askstring('Password',
                       '\n                         Enter password:                         \n',
                       show="*") == self.application_details['password']:
            update_window = update.UpdateApplicationData()
            self.application_details = update_window.getUpdatedApplicationDetails()
            self.capacity.set(self.application_details['capacity'])
            self.endTime.set(self.getFormattedEndTime())
            self.loadRecords()
        else:
            messagebox.showerror('Incorrect Password', 'Please enter the correct password')
        # Update the window
        self.window.update()


# Get the month name to make te folder of that month
def getMonthName(month):
    if month == 1:
        return "January"
    elif month == 2:
        return "February"
    elif month == 3:
        return "March"
    elif month == 4:
        return "April"
    elif month == 5:
        return "May"
    elif month == 6:
        return "June"
    elif month == 7:
        return "July"
    elif month == 8:
        return "August"
    elif month == 9:
        return "September"
    elif month == 10:
        return "October"
    elif month == 11:
        return "November"
    else:
        return "December"
