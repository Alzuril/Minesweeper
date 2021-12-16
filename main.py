from tkinter import *
import configparser, random, os, tkinter.messagebox, tkinter.simpledialog, pickle

window = Tk()
window.title("Сапёр")

selectwindow = Toplevel(window, pady=20, padx=20)
selectwindow.title("Авторизация")
selectwindow.geometry("300x350")
selectwindow.grab_set()
greatingwindow = Toplevel(window, pady=20, padx=20)
greatingwindow.title("Добро пожаловать")
greatingwindow.geometry("300x100")
selectwindow.lift(window)
greatingwindow.lift(window)

rows = 10
cols = 10
mines = 10
isCliced = False

field = []
buttons = []

colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']

gameover = False
qr = True
customsizes = []
resultsArr = []

def get_name():
    f = open("Current_Player.txt", "r")
    a = f.read()
    f.seek(0)
    f.close()
    return a


def saveResults(didWin):
    global resultsArr
    playerName = get_name()
    if os.path.getsize((playerName + "Res.txt")) != 0:
        res_file = open((playerName + "Res.txt"), "rb")
        r = pickle.load(res_file)
        res_file.close()
        if didWin:
            results = "1"
            r.append(results)
        elif not didWin:
            results = "0"
            r.append(results)
        res1_file = open((playerName + "Res.txt"), "wb")
        pickle.dump(r, res1_file)
        res1_file.close()
    else:
        if didWin:
            resultsArr.append("1")
        elif not didWin:
            resultsArr.append("0")
        res_file = open((playerName + "Res.txt"), "wb")
        pickle.dump(resultsArr, res_file)
        res_file.close()


def calculateRating(name):
    if os.path.getsize((name + "Res.txt")) != 0:
        res_file = open((name + "Res.txt"), "rb")
        resultsArr = pickle.load(res_file)
        res_file.close()
        quantity = len(resultsArr)
        totalWins = 0
        for x in resultsArr:
            if x == "1":
                totalWins +=1
        calcResult = (totalWins * 100) / quantity
    else:
        calcResult = 0
    return round(calcResult, 2)

def quitApp():
    selectwindow.destroy()
    greatingwindow.destroy()
    window.destroy()

def start_menu():
    rbtn = Button(selectwindow, text="Регистрация", command=lambda: registration())
    rbtn.pack()
    lbtn = Button(selectwindow, text="Вход", command=lambda: login())
    lbtn.pack()
    btn1 = Button(selectwindow, text="Выйти", command=lambda: quitApp())
    btn1.pack(side=BOTTOM)

def registration():
    name_label = Label(selectwindow, text="Введите имя:")
    name_entry = Entry(selectwindow)
    password_label = Label(selectwindow, text="Введите пароль:")
    password_entry = Entry(selectwindow)
    name_label.pack()
    name_entry.pack()
    password_label.pack()
    password_entry.pack()
    btn = Button(selectwindow, text="Регистрация", command=lambda: save())
    btn.pack()

    def save():
        password_save = {}
        password_save[name_entry.get()] = password_entry.get()
        login_file = open((name_entry.get() + "SaveLog.txt"), "wb")
        pickle.dump(password_save, login_file)
        login_file.close()
        players_file = open("All_Players.txt", "a")
        players_file.write(name_entry.get())
        players_file.write(" ")
        players_file.close()
        with open((name_entry.get() + "Res.txt"), 'tw', encoding='utf-8') as f:
            pass
        login()


def login():
    name_login_label = Label(selectwindow, text="Введите имя:")
    name_login_entry = Entry(selectwindow)
    password_login_label = Label(selectwindow, text="Введите пароль:")
    password_login_entry = Entry(selectwindow, show="*")
    name_login_label.pack()
    name_login_entry.pack()
    password_login_label.pack()
    password_login_entry.pack()
    btn2 = Button(selectwindow, text="Войти", command=lambda: logining())
    btn2.pack()

    def logining():
        f = open("Current_Player.txt", "w")
        f.write(name_login_entry.get())
        f.close()
        f = open("Current_Player.txt", "r")
        a = f.read()
        f.close()
        try:
            login_file = open((name_login_entry.get() + "SaveLog.txt"), "rb")
            log = pickle.load(login_file)
            login_file.close()
            if password_login_entry.get() == log[name_login_entry.get()]:
                quitLogin()
                createGratingMenu()
            else:
                tkinter.messagebox.showerror("Ошибка", "Неверный пароль")
        except:
            tkinter.messagebox.showerror("Ошибка", "Неверное имя или пароль")


def startGame():
    with open((get_name() + "Save.bin"), 'tw', encoding='utf-8') as savecf:
        pass
    createMenu()
    prepareWindow()
    prepareGame()
    greatingwindow.grab_release()
    greatingwindow.destroy()


def createGratingMenu():
    contbtn = Button(greatingwindow, text="Продолжить", command=lambda: loadSave())
    ngbtn = Button(greatingwindow, text="Новая игра", command=lambda: startGame())
    contbtn.pack()
    ngbtn.pack()



def quitLogin():
    selectwindow.grab_release()
    selectwindow.destroy()
    greatingwindow.grab_set()


def createMenu():
    menubar = Menu(window)
    menusize = Menu(window, tearoff=0)
    menusize.add_command(label="Новичок (9x9 и 10 мин)", command=lambda: setSize(9, 9, 10))
    menusize.add_command(label="Любитель (16x16 и 40 мин)", command=lambda: setSize(16, 16, 40))
    menusize.add_command(label="Профессионал (16x30 и 120 мин)", command=lambda: setSize(16, 30, 90))
    menubar.add_cascade(label="Сложность", menu=menusize)
    menubar.add_command(label="Рейтинг", command=lambda: show_rating())
    window.config(menu=menubar)

def show_rating():
    with open("All_Players.txt", "r") as players:
        all_names = players.read().split()
    ratingWindow = Toplevel(window, pady=20, padx=20)
    ratingWindow.title("Рейтинг")
    rat_lab = Label(ratingWindow, text="Ниже представлен рейтинг игроков:")
    ratingWindow.lift(window)
    rat_lab.pack()
    for name in all_names:
        player_namebtn = Button(ratingWindow, text=(name, "-", calculateRating(name)),
                                command=lambda name=name: showStats(name))
        player_namebtn.pack()


def showStats(namep):
    playerName = namep
    try:
        res_file = open((playerName + "Res.txt"), "rb")
        r = pickle.load(res_file)
        res_file.close()
        statsWindow = Toplevel(window, pady=20, padx=20)
        statsWindow.geometry("300x100")
        statsWindow.title("Статистика игрока")
        player_name = Label(statsWindow, text=("Имя:", playerName))
        player_games = Label(statsWindow, text=("Количество", "игр:", len(r)))
        player_r = Label(statsWindow, text=("Рейтинг:", calculateRating(playerName)))
        player_name.pack()
        player_games.pack()
        player_r.pack()
    except EOFError:
        statsWindow = Toplevel(window, pady=20, padx=20)
        statsWindow.geometry("300x100")
        statsWindow.title("Статистика игрока")
        player_name = Label(statsWindow, text=("Имя:", playerName))
        player_games = Label(statsWindow, text=("Количество", "игр:", "0"))
        player_r = Label(statsWindow, text=("Рейтинг:", "0"))
        player_name.pack()
        player_games.pack()
        player_r.pack()


def setSize(r, c, m):
    global rows, cols, mines
    rows = r
    cols = c
    mines = m
    saveConfig()
    restartGame()


def saveConfig():
    global rows, cols, mines
    config = configparser.ConfigParser()
    config.add_section("game")
    config.set("game", "rows", str(rows))
    config.set("game", "cols", str(cols))
    config.set("game", "mines", str(mines))
    config.add_section("sizes")
    config.set("sizes", "amount", str(min(5, len(customsizes))))
    for x in range(0, min(5, len(customsizes))):
        config.set("sizes", "row" + str(x), str(customsizes[x][0]))
        config.set("sizes", "cols" + str(x), str(customsizes[x][1]))
        config.set("sizes", "mines" + str(x), str(customsizes[x][2]))
    with open("config.ini", "w") as file:
        config.write(file)


def loadConfig():
    global rows, cols, mines, customsizes
    config = configparser.ConfigParser()
    config.read("config.ini")
    rows = config.getint("game", "rows")
    cols = config.getint("game", "cols")
    mines = config.getint("game", "mines")
    amountofsizes = config.getint("sizes", "amount")
    for x in range(0, amountofsizes):
        customsizes.append((config.getint("sizes", "row" + str(x)), config.getint("sizes", "cols" + str(x)),
                            config.getint("sizes", "mines" + str(x))))


def saveGame():
    global field, buttons, gameover
    openedCells = []
    playerName = get_name()
    save_file = open((playerName + "Save.bin"), "wb")
    pickle.dump(field, save_file)
    save_file.close()
    save_file = open((playerName + "Save.bin"), "rb")
    save = pickle.load(save_file)
    save_file.close()
    if not gameover:
        for buttonRow in buttons:
            for b in buttonRow:
                if b['state'] == 'disabled':
                    if b['text'] == "?":
                        openedCells.append(2)
                    else:
                        openedCells.append(1)
                else:
                    if b['text'] == " ":
                        openedCells.append(0)
        inClels = [openedCells[d:d+len(save[0])] for d in range(0, len(openedCells), len(save[0]))]
        cells = open((playerName + "CellsSave.bin"), "wb")
        pickle.dump(inClels, cells)
        cells.close()


def loadSave():
    global rows, cols, mines, field, buttons
    try:
        playerName = get_name()
        if os.path.getsize((playerName + "Save.bin")) != 0:
            f = open((playerName + "Save.bin"), "rb")
            save = pickle.load(f)
            f.close()
            field = save
        greatingwindow.grab_release()
        greatingwindow.destroy()
        createMenu()
        prepareWindow()
        f = open((playerName + "CellsSave.bin"), "rb")
        cells = pickle.load(f)
        f.close()
        for x, cellRow in enumerate(cells):
            for y, cell in enumerate(cellRow):
                if cell == 0:
                    buttons[x][y]['state'] = 'normal'
                    buttons[x][y]['relief'] = 'raised'
                elif cell == 2:
                    buttons[x][y]['text'] = "?"
                    buttons[x][y]['state'] = 'disabled'
                else:
                    clickOn(x, y)
    except:
        tkinter.messagebox.showerror("Ошибка", "У Вас нету сохранённой игры")


def prepareGame():
    global rows, cols, mines, field
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, cols):
            field[x].append(0)
    for _ in range(0, mines):
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        while field[x][y] == -1:
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)
        field[x][y] = -1
        if x != 0:
            if y != 0:
                if field[x - 1][y - 1] != -1:
                    field[x - 1][y - 1] += 1
            if field[x - 1][y] != -1:
                field[x - 1][y] += 1
            if y != cols - 1:
                if field[x - 1][y + 1] != -1:
                    field[x - 1][y + 1] += 1
        if y != 0:
            if field[x][y - 1] != -1:
                field[x][y - 1] += 1
        if y != cols - 1:
            if field[x][y + 1] != -1:
                field[x][y + 1] += 1
        if x != rows - 1:
            if y != 0:
                if field[x + 1][y - 1] != -1:
                    field[x + 1][y - 1] += 1
            if field[x + 1][y] != -1:
                field[x + 1][y] += 1
            if y != cols - 1:
                if field[x + 1][y + 1] != -1:
                    field[x + 1][y + 1] += 1
    saveGame()


def prepareWindow():
    global rows, cols, buttons
    Button(window, text="Restart", command=restartGame).grid(row=0, column=0, columnspan=cols,
                                                             sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            b = Button(window, text=" ", width=2, command=lambda x=x, y=y: clickOn(x, y))
            b.bind("<Button-3>", lambda e, x=x, y=y: onRightClick(x, y))
            b.grid(row=x + 1, column=y, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            buttons[x].append(b)


def restartGame():
    global gameover, isCliced
    gameover = False
    isCliced = False
    for x in window.winfo_children():
        if type(x) != Menu:
            x.destroy()
    prepareWindow()
    prepareGame()


def despawnMine(x, y):
    global field, isCliced
    field[x][y] = 0
    if field[x] != 0 and field[x] != len(field):
        if field[y] != 0 and field[y] != len(field[x]):
            if y+1 < len(field[x]):
                try:
                    if field[x][y+1] > 0:
                        field[x][y+1] -= 1
                    else:
                        field[x][y] += 1
                except IndexError:
                    pass
            else:
                pass
            if y + 1 < len(field[x]) and x-1 >= 0:
                try:
                    if field[x-1][y+1] > 0:
                        field[x-1][y+1] -= 1
                    else:
                        field[x][y] += 1
                except IndexError:
                    pass
            else:
                pass
            if x-1 >= 0:
                try:
                    if field[x-1][y] > 0:
                        field[x-1][y] -= 1
                    else:
                        field[x][y] += 1
                except IndexError:
                    pass
            else:
                pass
            if x-1 >= 0 and y - 1 >= 0:
                try:
                    if field[x-1][y-1] > 0:
                        field[x-1][y-1] -= 1
                    else:
                        field[x][y] += 1
                except IndexError:
                    pass
            else:
                pass
            if y - 1 >= 0:
                try:
                    if field[x][y-1] > 0:
                        field[x][y-1] -= 1
                    else:
                        field[x][y] += 1
                except IndexError:
                    pass
            else:
                pass
            if x + 1 < len(field) and y - 1 >= 0:
                try:
                    if field[x+1][y-1] > 0:
                        field[x+1][y-1] -= 1
                    else:
                        field[x][y] += 1
                except IndexError:
                    pass
            else:
                pass
            if x + 1 < len(field):
                try:
                    if field[x+1][y] > 0:
                        field[x+1][y] -= 1
                    else:
                        field[x][y] += 1
                except IndexError:
                    pass
            else:
                pass
            if x + 1 < len(field) and y + 1 < len(field[x]):
                try:
                    if field[x+1][y+1] > 0:
                        field[x+1][y+1] -= 1
                    else:
                        field[x][y] += 1
                except IndexError:
                    pass
            else:
                pass
    t = random.randint(0, (len(field[x]) - 1))
    i = random.randint(0, (len(field) - 1))
    if t == y and i == x:
        t = random.randint(0, (len(field[x]) - 1))
        i = random.randint(0, (len(field) - 1))
    if field[i][t] != -1:
        if t != y:
            field[i][t] = -1
            if field[i] != 0 and field[i] != len(field):
                if field[t] != 0 and field[t] != len(field[x]):
                    if t + 1 < len(field[x]):
                        if field[i][t + 1] != -1:
                            field[i][t + 1] += 1
                        else: field[i][t] +=1
                    if i - 1 >= 0 and t + 1 < len(field[x]):
                        if field[i - 1][t + 1] != -1:
                            field[i - 1][t + 1] += 1
                        else:
                            field[i][t] += 1
                    if i - 1 >= 0:
                        if field[i - 1][t] != -1:
                            field[i - 1][t] += 1
                        else:
                            field[i][t] += 1
                    if i - 1 >= 0 and t - 1 >= 0:
                        if field[i - 1][t - 1] != -1:
                            field[i - 1][t - 1] += 1
                        else:
                            field[i][t] += 1
                    if t - 1 >= 0:
                        if field[i][t - 1] != -1:
                            field[i][t - 1] += 1
                        else:
                            field[i][t] += 1
                    if i + 1 < len(field) and t - 1 >= 0:
                        if field[i + 1][t - 1] != -1:
                            field[i + 1][t - 1] += 1
                        else:
                            field[i][t] += 1
                    if i + 1 < len(field):
                        if field[i + 1][t] != -1:
                            field[i + 1][t] += 1
                        else:
                            field[i][t] += 1
                    if i + 1 < len(field) and t + 1 < len(field[x]):
                        if field[i + 1][t + 1] != -1:
                            field[i + 1][t + 1] += 1
                        else:
                            field[i][t] += 1
    saveGame()
    isCliced = True


def clickOn(x, y):
    global field, buttons, colors, gameover, rows, cols, qr, isCliced
    if field[x][y] == -1 and isCliced == False:
        despawnMine(x, y)
    if field[x][y] != -1:
        isCliced = True
    if gameover:
        return
    buttons[x][y]["text"] = str(field[x][y])
    if field[x][y] == -1:
        buttons[x][y]["text"] = "*"
        buttons[x][y].config(background='red', disabledforeground='black')
        gameover = True
        qr = False
        saveResults(qr)
        tkinter.messagebox.showinfo("Game Over", "Вы проиграли")
        for _x in range(0, rows):
            for _y in range(cols):
                if field[_x][_y] == -1:
                    buttons[_x][_y]["text"] = "*"
    else:
        buttons[x][y].config(disabledforeground=colors[field[x][y]])
    if field[x][y] == 0:
        buttons[x][y]["text"] = " "
        autoClickOn(x, y)
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    saveGame()
    checkWin()


def autoClickOn(x, y):
    global field, buttons, colors, rows, cols
    if buttons[x][y]["state"] == "disabled":
        return
    if field[x][y] != 0:
        buttons[x][y]["text"] = str(field[x][y])
    else:
        buttons[x][y]["text"] = " "
    buttons[x][y].config(disabledforeground=colors[field[x][y]])
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    if field[x][y] == 0:
        if x != 0 and y != 0:
            autoClickOn(x - 1, y - 1)
        if x != 0:
            autoClickOn(x - 1, y)
        if x != 0 and y != cols - 1:
            autoClickOn(x - 1, y + 1)
        if y != 0:
            autoClickOn(x, y - 1)
        if y != cols - 1:
            autoClickOn(x, y + 1)
        if x != rows - 1 and y != 0:
            autoClickOn(x + 1, y - 1)
        if x != rows - 1:
            autoClickOn(x + 1, y)
        if x != rows - 1 and y != cols - 1:
            autoClickOn(x + 1, y + 1)
    saveGame()


def onRightClick(x, y):
    global buttons
    if gameover:
        return
    if buttons[x][y]["text"] == "?":
        buttons[x][y]["text"] = " "
        buttons[x][y]["state"] = "normal"
    elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        buttons[x][y]["text"] = "?"
        buttons[x][y]["state"] = "disabled"
    saveGame()


def checkWin():
    global buttons, field, rows, cols, gameover
    playerName = get_name()
    win = True
    for x in range(0, rows):
        for y in range(0, cols):
            if field[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        saveResults(win)
        calculateRating(playerName)
        gameover = True
        tkinter.messagebox.showinfo("Gave Over", "Вы выиграли")


if os.path.exists("config.ini"):
    loadConfig()
else:
    saveConfig()

start_menu()
window.mainloop()
