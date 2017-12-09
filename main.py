from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfiles


# Placeholder function
# TODO: remove this function
def donothing():
    return None


# Küsib kasutajalt .csv failid, avab neid ja tagastab nende objektid listina
def open_file():
    global files
    files = askopenfiles(filetypes=[("CSV file", ".csv")],
                           title="Choose a file."
                           )
    print(files) # Only for debugging purpoces
                 # TODO: remove when finished
    return files


# Kasutab argumendina csv objetide listi funktsioonist open_file()
# Tagastab listi tudengite nimidega
def tudengite_nimekiri(csv_files):
    global nimekiri
    nimekiri = []
    for file in csv_files:
        for rida in file:
            osad = rida.strip().split(",")
            if osad[0] not in nimekiri:
                nimekiri.append(osad[0])
    return nimekiri


def student_singleWork():
    return None




################################################################################
################################################################################

# Global variables
global files
global nimekiri


################################################################################
################################################################################


main_window = Tk() # Creates main application window
main_window.title("Project") # TODO: change main window title
#main_window.geometry("400x400") # TODO: remove when obsolete

# Loob menu'riba
main_menu = Menu(main_window)

#  Loome file-menu
filemenu = Menu(main_menu)
filemenu.add_command(label="Open", command=open_file)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=main_window.quit)
main_menu.add_cascade(label="File", menu=filemenu)

# Loome statistics-menu
statistics_menu = Menu(main_menu)

# Loome student-menu
student_menu = Menu(statistics_menu)
student_menu.add_command(label="Single work", command=donothing)
student_menu.add_command(label="Semester", command=donothing)

statistics_menu.add_cascade(label="Student", menu=student_menu)

main_menu.add_cascade(label="Statistics", menu=statistics_menu)

# Loome group-menu
group_menu = Menu(statistics_menu)
group_menu.add_command(label="Single work", command=donothing)
group_menu.add_command(label="Semester", command=donothing)

statistics_menu.add_cascade(label="Group", menu=group_menu)

# Loome course_menu
course_menu = Menu(statistics_menu)
course_menu.add_command(label="Single work", command=donothing)
course_menu.add_command(label="Semester", command=donothing)

statistics_menu.add_cascade(label="Course", menu=group_menu)



# Loome message_menu
message_menu = Menu(main_menu)
message_menu.add_command(label="Send message", command=donothing)

main_menu.add_cascade(label="Message", menu=message_menu)


main_window.config(menu=main_menu)
main_window.mainloop()
