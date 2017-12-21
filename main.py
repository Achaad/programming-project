from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfiles
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy


################################################################################
################################################################################

# Global variables
global files
global nimekiri
nimekiri = []
tööd = []


#TODO: check if student has not done work
#TODO: change yscale

################################################################################
################################################################################

# Placeholder function
# TODO: remove this function
def donothing():
    return None


# Küsib kasutajalt .csv failid, avab neid ja tagastab nende objektid listina
# Lisaks täidab tööde ja nimede listi
def open_file():
    global files
    global nimekiri
    global tööd

    files = askopenfiles(filetypes=[("CSV file", ".csv")],
                         title="Choose a file."
                         )

    # Populates lists of works and students
    nimekiri = tudengite_nimekiri(files)
    tööd = tööde_nimed(files)

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
        file.seek(0)
    return nimekiri


# Tagastab listi, kus on erinevate tööde nimetused
def tööde_nimed(csv_files):
    global tööd
    tööd = []
    for e in csv_files:
        failinimi = e.name
        töönimi_foramtiga = failinimi.split("_")[1]
        töönimi = töönimi_foramtiga.split(".")[0]
        if "semester" not in töönimi and töönimi not in tööd:
            tööd.append(töönimi)
    return tööd


# Kontrollib, kas failid on avatud ja prindib veat, kui ei ole
def kontrolli_failid(command):
    global files

    if "files" not in globals():
        messagebox.showinfo(message="Failid ei ole avatud!")
    else:
        command()


def student_singleWork():
    global nimekiri
    global files
    global tööd

    def plot_single_work(inimese_nimi, töönimi):
        global files

        suurused = []
        numbrid = []

        # Saame kätte suurused graafiku joonistamiseks
        for f in files:
            if töönimi in f.name:
                for rida in f:
                    osad = rida.strip().split(",")
                    if inimese_nimi == osad[0]:
                        for i in range(len(osad)):
                            if i > 1:
                                suurused.append(float(osad[i]))
                                numbrid.append(i - 1)
                f.seek(
                    0)  # Tagastab faili algusele, et seda saaks kasutada uuesti

        print(suurused)
        print(numbrid)

        ax.clear()
        ax.bar(numbrid, suurused)
        ax.set_xticks(numbrid)
        ax.set_xlabel("Ülesanned")
        ax.set_ylabel("Ballid")
        graafiku_nimi = inimese_nimi + ", " + töönimi
        ax.set_title(graafiku_nimi)

        canvas.show()
        student_chooser.destroy()

    def get_student_name():
        valitud_nimi = nimekiri[options.curselection()[0]]
        options.delete(0, END)
        student_chooser.title("Choose a work.")
        for nimi in tööd:
            options.insert(END, nimi)
        select_name.configure(command=lambda: plot_single_work(
            valitud_nimi,
            tööd[options.curselection()[0]]
        )
                              )

    if nimekiri == []:
        nimekiri = tudengite_nimekiri(files)

    if tööd == []:
        tööd = tööde_nimed(files)

    student_chooser = Tk()
    student_chooser.title("Choose a student.")

    scroll = Scrollbar(student_chooser)

    options = Listbox(student_chooser, yscrollcommand=scroll.set)
    scroll.config(command=options.yview)

    for nimi in nimekiri:
        options.insert(END, nimi)

    options.pack(side=LEFT, fill=BOTH, expand=1)
    scroll.pack(side=LEFT, fill=Y)

    select_name = Button(student_chooser, text="OK",
                         command=get_student_name
                         )
    select_name.pack(fill=Y)

    student_chooser.mainloop()


def student_semester():
    global nimekiri
    global files
    global tööd

    if nimekiri == []:
        nimekiri = tudengite_nimekiri(files)

    if tööd == []:
        tööd = tööde_nimed(files)

    def plot_single_semester(inimese_nimi):
        global files

        suurused = []
        numbrid = []

        # Saame kätte suurused graafiku joonistamiseks
        for f in files:
            if "semester" in f.name:
                for rida in f:
                    osad = rida.strip().split(",")
                    if inimese_nimi == osad[0]:
                        for i in range(len(osad)):
                            if i > 1:
                                suurused.append(float(osad[i]))
                                numbrid.append(i - 1)
                f.seek(
                    0)  # Tagastab faili algusele, et seda saaks kasutada uuesti

        print(suurused)
        print(numbrid)

        ax.clear()
        ax.plot(numbrid, suurused, "o-")
        ax.set_xticks(numbrid)
        ax.set_xlabel("Tööd")
        ax.set_ylabel("Ballid")

        graafiku_nimi = inimese_nimi + ", semester"
        ax.set_title(graafiku_nimi)

        canvas.show()
        student_chooser.destroy()

    student_chooser = Tk()
    student_chooser.title("Choose a student.")

    scroll = Scrollbar(student_chooser)

    options = Listbox(student_chooser, yscrollcommand=scroll.set)
    scroll.config(command=options.yview)

    for nimi in nimekiri:
        options.insert(END, nimi)

    options.pack(side=LEFT, fill=BOTH, expand=1)
    scroll.pack(side=LEFT, fill=Y)

    select_name = Button(student_chooser, text="OK",
                         command=lambda:
                         plot_single_semester(
                             nimekiri[options.curselection()[0]])
                         )
    select_name.pack(fill=Y)

    student_chooser.mainloop()


def group_single_work():
    global nimekiri
    global files
    global tööd

    rühmad = []

    def plot_course_work(töönimi, rühmanimi):
        global files

        ballid = []
        nimed = []
        numbrid = []

        # Saame kätte suurused graafiku joonistamiseks
        for f in files:
            if töönimi in f.name and rühmanimi in f.name:
                for rida in f:
                    osad = rida.strip().split(",")
                    nimed.append(osad[0])
                    ballid.append(osad[2:])

                f.seek(
                    0)  # Tagastab faili algusele, et seda saaks kasutada uuesti



        for i in range(len(ballid)):
            for e in range(len(ballid[i])):
                ballid[i][e] = float(ballid[i][e])


        for i in range(len(ballid[0])):
            numbrid.append(i + 1)
            for e in range(len(ballid[i])):
                ballid[i][e] = float(ballid[i][e])



        ballid = [list(x) for x in zip(*ballid)]

        ax.clear()
        ax.violinplot(ballid, showmeans=True)
        ax.set_xticks(numbrid)
        ax.set_xlabel("Ülesanned")
        ax.set_ylabel("Ballid")
        ax.legend()

        graafiku_nimi = rühmanimi + ", " + töönimi
        ax.set_title(graafiku_nimi)

        canvas.show()
        work_chooser.destroy()

    if nimekiri == []:
        nimekiri = tudengite_nimekiri(files)

    if tööd == []:
        tööd = tööde_nimed(files)

    work_chooser = Tk()
    work_chooser.title("Choose a group.")

    scroll = Scrollbar(work_chooser)

    options = Listbox(work_chooser, yscrollcommand=scroll.set)
    scroll.config(command=options.yview)

    for f in files:
        if "semester" not in f.name:
            tee_osad = f.name.split("/")
            rühma_nimi = tee_osad[-1].split("_")[0]
            if rühma_nimi not in rühmad:
                rühmad.append(rühma_nimi)
        f.seek(0)

    for rühm in rühmad:
        options.insert(END, rühm)

    options.pack(side=LEFT, fill=BOTH, expand=1)
    scroll.pack(side=LEFT, fill=Y)

    select_work = Button(work_chooser, text="OK",
                         command=lambda:
                         get_work_name(rühmad[options.curselection()[0]])
                         )
    select_work.pack(fill=Y)

    def get_work_name(rühmanimi):
        rühma_tööd = []
        for f in files:
            if rühmanimi in f.name and "semester" not in f.name:
                tee_osad = f.name.split("/")
                töö_nimi = tee_osad[-1].split("_")[1].split(".")[0]
                rühma_tööd.append(töö_nimi)
            f.seek(0)

        options.delete(0, END)
        work_chooser.title("Choose a work.")
        for töö in rühma_tööd:
            options.insert(END, töö)
        select_work.configure(command=lambda:
        plot_course_work(
            rühma_tööd[options.curselection()[0]], rühmanimi
        )
                              )

    work_chooser.mainloop()


def group_semester():
    global nimekiri
    global files
    global tööd

    if nimekiri == []:
        nimekiri = tudengite_nimekiri(files)

    if tööd == []:
        tööd = tööde_nimed(files)

    def plot_group_semester(rühma_nimi):
        global files

        ballid = []
        nimed = []
        numbrid = []

        # Saame kätte suurused graafiku joonistamiseks
        for f in files:
            if rühma_nimi in f.name and "semester" in f.name:
                for rida in f:
                    osad = rida.strip().split(",")
                    nimed.append(osad[0])
                    ballid.append(osad[2:])

                f.seek(
                    0)  # Tagastab faili algusele, et seda saaks kasutada uuesti

        for i in range(len(ballid)):
            for e in range(len(ballid[i])):
                ballid[i][e] = float(ballid[i][e])

        for n in range(len(ballid[0])):
            numbrid.append(n + 1)

        ballid = [list(x) for x in zip(*ballid)]


        ax.clear()
        ax.violinplot(ballid, showmeans=True)
        ax.set_xticks(numbrid)
        ax.set_xlabel("Tööd")
        ax.set_ylabel("Ballid")
        ax.legend()

        graafiku_nimi = rühma_nimi + ", semester"
        ax.set_title(graafiku_nimi)

        canvas.show()
        group_chooser.destroy()

    group_chooser = Tk()
    group_chooser.title("Choose a group.")

    scroll = Scrollbar(group_chooser)

    options = Listbox(group_chooser, yscrollcommand=scroll.set)
    scroll.config(command=options.yview)

    rühmad = []
    for f in files:
        if "semester" in f.name:
            tee_osad = f.name.split("/")
            rühma_nimi = tee_osad[-1].split("_")[0]
            if rühma_nimi not in rühmad:
                rühmad.append(rühma_nimi)
        f.seek(0)

    for rühm in rühmad:
        options.insert(END, rühm)

    options.pack(side=LEFT, fill=BOTH, expand=1)
    scroll.pack(side=LEFT, fill=Y)

    select_name = Button(group_chooser, text="OK",
                         command=lambda:
                         plot_group_semester(
                             rühmad[options.curselection()[0]])
                         )
    select_name.pack(fill=Y)

    group_chooser.mainloop()


def course_single_work():
    global nimekiri
    global files
    global tööd

    def plot_semester_single_work(töönimi):
        global files

        ballid = []
        nimed = []
        numbrid = []

        # Saame kätte suurused graafiku joonistamiseks
        for f in files:
            if töönimi in f.name:
                for rida in f:
                    osad = rida.strip().split(",")
                    nimed.append(osad[0])
                    ballid.append(osad[2:])

                f.seek(
                    0)  # Tagastab faili algusele, et seda saaks kasutada uuesti

        for i in range(len(ballid[0])):
            numbrid.append(i + 1)

        for i in range(len(ballid)):
            for e in range(len(ballid[i])):
                ballid[i][e] = float(ballid[i][e])

        # List, kus on iga ülesanne kohta tema keskmine ball
        keskmised_ballid = []

        # List selleks, et seadistada xticks
        kõik_ballid = []

        # List, kus on iga ülesanne ballid
        ülesanned = []

        for i in ballid[0]:
            ülesanned.append([])
            keskmised_ballid.append([])

        for student in ballid:
            for i in range(len(student)):
                ülesanned[i].append(student[i])

        for i in range(len(ülesanned)):
            summa = 0
            for ball in ülesanned[i]:
                summa += ball
                kõik_ballid.append(ball)
            keskmised_ballid[i] = summa / len(ülesanned[i])

        graafiku_nimi = töönimi.capitalize() + ", kursus"

        ax.clear()
        ax.set_yticks(numpy.arange(0, len(kõik_ballid), 0.1))
        ax.set_xticks(numbrid)
        ax.set_xlabel("Ülesanned")
        ax.set_ylabel("Ballid")
        ax.violinplot(ülesanned, showmeans=True)
        ax.set_title(graafiku_nimi)

        canvas.show()
        work_chooser.destroy()

    if nimekiri == []:
        nimekiri = tudengite_nimekiri(files)

    if tööd == []:
        tööd = tööde_nimed(files)

    work_chooser = Tk()
    work_chooser.title("Choose a work.")

    scroll = Scrollbar(work_chooser)

    options = Listbox(work_chooser, yscrollcommand=scroll.set)
    scroll.config(command=options.yview)

    for töö in tööd:
        options.insert(END, töö)

    options.pack(side=LEFT, fill=BOTH, expand=1)
    scroll.pack(side=LEFT, fill=Y)

    select_work = Button(work_chooser, text="OK",
                         command=lambda:
                         plot_semester_single_work(
                             tööd[options.curselection()[0]])
                         )
    select_work.pack(fill=Y)

    work_chooser.mainloop()


def course_semester():
    global nimekiri
    global files
    global tööd

    if nimekiri == []:
        nimekiri = tudengite_nimekiri(files)

    if tööd == []:
        tööd = tööde_nimed(files)

    ballid = []
    nimed = []
    numbrid = []

    # Saame kätte suurused graafiku joonistamiseks
    for f in files:
        if "semester" in f.name:
            for rida in f:
                osad = rida.strip().split(",")
                nimed.append(osad[0])
                ballid.append(osad[2:])

            f.seek(
                0)  # Tagastab faili algusele, et seda saaks kasutada uuesti

    for i in range(len(ballid[0])):
        numbrid.append(i + 1)

    for i in range(len(ballid)):
        for e in range(len(ballid[i])):
            ballid[i][e] = float(ballid[i][e])

    # List, kus on iga ülesanne kohta tema keskmine ball
    keskmised_ballid = []

    # List selleks, et seadistada xticks
    kõik_ballid = []

    # List, kus on iga ülesanne ballid
    ülesanned = []

    for i in ballid[0]:
        ülesanned.append([])
        keskmised_ballid.append([])

    for student in ballid:
        for i in range(len(student)):
            ülesanned[i].append(student[i])

    for i in range(len(ülesanned)):
        summa = 0
        for ball in ülesanned[i]:
            summa += ball
            kõik_ballid.append(ball)
        keskmised_ballid[i] = summa / len(ülesanned[i])

    graafiku_nimi = "Semester, kursus"

    ax.clear()
    ax.set_yticks(numpy.arange(0, max(kõik_ballid), 1), minor=True)
    ax.set_xticks(numbrid)
    ax.set_xlabel("Tööd")
    ax.set_ylabel("Ballid")
    ax.violinplot(ülesanned, showmeans=True)
    ax.set_title(graafiku_nimi)

    canvas.show()


################################################################################
################################################################################


main_window = Tk()  # Creates main application window
main_window.title("Project")  # TODO: change main window title

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
                         command=lambda: kontrolli_failid(student_singleWork)
                         )
student_menu.add_command(label="Semester",
                         command=lambda: kontrolli_failid(student_semester)
                         )

statistics_menu.add_cascade(label="Student", menu=student_menu)

main_menu.add_cascade(label="Statistics", menu=statistics_menu)

# Loome group-menu
group_menu = Menu(statistics_menu)
group_menu.add_command(label="Single work",
                       command=lambda: kontrolli_failid(group_single_work)
                       )
group_menu.add_command(label="Semester",
                       command=lambda: kontrolli_failid(group_semester)
                       )

statistics_menu.add_cascade(label="Group", menu=group_menu)

# Loome course_menu
course_menu = Menu(statistics_menu)
course_menu.add_command(label="Single work",
                        command=lambda: kontrolli_failid(course_single_work)
                        )
course_menu.add_command(label="Semester",
                        command=lambda: kontrolli_failid(course_semester)
                        )

statistics_menu.add_cascade(label="Course", menu=course_menu)

# Loome message_menu
message_menu = Menu(main_menu)
message_menu.add_command(label="Send message", command=donothing)

main_menu.add_cascade(label="Message", menu=message_menu)

# Loome graafiku objektid ja vidinad
fig = Figure(dpi=150)
ax = fig.add_subplot(1, 1, 1)
fig.set_facecolor('white')

canvas = FigureCanvasTkAgg(fig, master=main_window)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky=N + W + E + S)

main_window.config(menu=main_menu)
main_window.mainloop()
