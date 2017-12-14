from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfiles

################################################################################
################################################################################

# Global variables
global files
global nimekiri
nimekiri = []
tööd = []


################################################################################
################################################################################


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


def plot_singlework_student(nimi):
    return None

def tööde_nimed(csv_files):
    global tööd
    tööd = []
    for e in csv_files:
        failinimi = e.name
        töönimi = failinimi.split("_")[1]
        if "semester" not in töönimi:
            tööd.append(töönimi.split(".")[0])
    return tööd

def plot_work(inimese_nimi, töönimi):
    print(inimese_nimi, töönimi)

def student_singleWork():

    global nimekiri
    global files
    global tööd
    global plot_work


    def get_student_name():
        valitud_nimi = nimekiri[options.curselection()[0]]
        options.delete(0, END)
        student_chooser.title("Choose a work.")
        for nimi in tööd:
            options.insert(END, nimi)
        select_name.configure(command=lambda: plot_work(valitud_nimi,
                                                        tööd[options.curselection()[0]]))


    def get_name(options):
        global nimekiri
        number = options.curselection()
        nimi = nimekiri[number]

    # TODO: check if nimekiri is not already filled
    nimekiri = tudengite_nimekiri(files)

    #TODO: check if tööd is not already filled
    tööd = tööde_nimed(files)

    student_chooser = Tk()
    student_chooser.title("Choose a student.")

    scroll = Scrollbar(student_chooser)

    options = Listbox(student_chooser, yscrollcommand=scroll.set)
    scroll.config(command=options.yview)

    for nimi in nimekiri:
        options.insert(END, nimi)

    options.pack(side=LEFT, fill=BOTH, expand=1)
    scroll.pack(side=LEFT,fill=Y)

    select_name = Button(student_chooser, text="OK",
                         command=get_student_name
                        )
    select_name.pack(fill=Y)


    student_chooser.mainloop()
    return None



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
student_menu.add_command(label="Single work",
                         command=student_singleWork
                         )
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
