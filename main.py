import tkinter as tk
from random import shuffle, randint

# -- Variables --

TAILLEX, TAILLEY = 2400, 1080
NB_LINES = 1000
SPEED = 1

OPTIONS = [
"Bulle",
"Insertion",
"Cocktail",
"Comb",
"Selection"
]



# -- Logic --

def gen_gradient(start, stop, steps):
    r = start[0]
    g = start[1]
    b = start[2]

    sr = abs(start[0] - stop[0]) / steps
    sg = abs(start[1] - stop[1]) / steps
    sb = abs(start[2] - stop[2]) / steps

    res = []
    for i in range(steps):
        r = r - sr if start[0] > stop[0] else r + sr
        g = g - sg if start[1] > stop[1] else g + sg
        b = r - sb if start[2] > stop[2] else b + sb
        res.append([(int(r), int(g), int(b)), i])

    return res

def rgbToHex(rgb):
    return "#" + f"{hex(rgb[0]).lstrip("0x"):>02}" + f"{hex(rgb[1]).lstrip("0x"):>02}" + f"{hex(rgb[2]).lstrip("0x"):>02}"

def displayList(frame, colors, sx, sy):
    size = len(colors)


    for i in range(size):
        frame.create_rectangle(i * sx / size, 0, (i + 1) * (sx / size), sy, fill=rgbToHex(colors[i][0]), outline=rgbToHex(colors[i][0]))

    return None

def etapeTriBulle():
    n = len(col)
    swapped = False

    for i in range(n - 1):
        if col[i][1] < col[i + 1][1]:
            col[i], col[i + 1] = col[i + 1], col[i]
            swapped = True

    return swapped

def etapeTriInsertion(i):
    global col
    if i >= len(col):
        return

    key = col[i]
    j = i - 1

    while j >= 0 and col[j][1] < key[1]:
        col[j + 1] = col[j]
        j -= 1

    col[j + 1] = key

def etapeTriCocktail(start, end):
    swapped = False

    for i in range(start, end):
        if col[i][1] < col[i + 1][1]:
            col[i], col[i + 1] = col[i + 1], col[i]
            swapped = True

    if not swapped:
        return False

    for i in range(end, start, -1):
        if col[i][1] > col[i - 1][1]:
            col[i], col[i - 1] = col[i - 1], col[i]
            swapped = True

    return swapped

def etapeTriComb(gap):
    swapped = False
    n = len(col)

    for i in range(n - gap):
        if col[i][1] < col[i + gap][1]:
            col[i], col[i + gap] = col[i + gap], col[i]
            swapped = True

    return swapped

def etapeTriSelection(start):
    n = len(col)
    min_index = start

    for i in range(start + 1, n):
        if col[i][1] > col[min_index][1]:
            min_index = i

    if min_index != start:
        col[start], col[min_index] = col[min_index], col[start]

    return col

def update(start=0, end=None, gap=None):
    if end is None:
        end = len(col) - 1
    if gap is None:
        gap = len(col) // 1.3

    mainFrame.delete('all')
    displayList(mainFrame, col, TAILLEX, TAILLEY)

    if variable.get() == "Bulle":
        if etapeTriBulle():
            root.after(SPEED, lambda: update())
    elif variable.get() == "Insertion":
        if start < len(col):
            etapeTriInsertion(start)
            root.after(SPEED, lambda: update(start + 1, end, gap))
    elif variable.get() == "Cocktail":
        if etapeTriCocktail(start, end):
            root.after(SPEED, lambda: update(start, end, gap))
    elif variable.get() == "Comb":
        if etapeTriComb(int(gap)):
            root.after(SPEED, lambda: update(start, end, gap))
        else:
            gap = max(1, int(gap / 1.3))
            if gap > 1:
                root.after(SPEED, lambda: update(start, end, gap))
    elif variable.get() == "Selection":
        if start < len(col):
            etapeTriSelection(start)
            root.after(SPEED, lambda: update(start + 1, end, gap))

def reset():
    global col
    col = gen_gradient((randint(0, 255), randint(0, 255), randint(0, 255)), (randint(0, 255), randint(0, 255), randint(0, 255)), NB_LINES)
    shuffle(col)
    displayList(mainFrame, col, TAILLEX, TAILLEY)

def start():
    update()


# -- Display --

root = tk.Tk()
controlBar = tk.Frame(root)
variable = tk.StringVar(controlBar)
sortChoice = tk.OptionMenu(controlBar, variable, *OPTIONS)
bstart = tk.Button(controlBar, text="Start", command=start)
breset = tk.Button(controlBar, text="reset", command=reset)
mainFrame = tk.Canvas(root, width=TAILLEX, height=TAILLEY)

root.resizable(False, False)
variable.set(OPTIONS[0])
sortChoice.pack(side=tk.LEFT)
bstart.pack(side=tk.LEFT)
breset.pack(side=tk.LEFT)
controlBar.pack()
mainFrame.pack()
reset()
tk.mainloop()
