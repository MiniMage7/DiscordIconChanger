from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, UnidentifiedImageError
import os


# Ask user for the path to Discord.exe
def getDiscordPath():
    # Open file explorer for user input
    newDiscordDirectory = filedialog.askopenfilename(filetypes=[('Discord', 'Discord.exe')])
    if os.path.exists(newDiscordDirectory) and newDiscordDirectory.endswith('Discord.exe'):
        discordDirectory.set(newDiscordDirectory)


# Ask user for the path to the image
def getImagePath():
    # Get possible file extensions
    exts = Image.registered_extensions()
    supported_extensions = []
    for ex in exts:
        if exts[ex] in Image.OPEN:
            supported_extensions.append(('Image', ex))

    # Open file explorer for user input
    newImageDirectory = filedialog.askopenfilename(filetypes=supported_extensions)
    if os.path.exists(newImageDirectory) and newImageDirectory != '':
        try:
            Image.open(newImageDirectory)
            imageDirectory.set(newImageDirectory)
        except UnidentifiedImageError:
            imageDirectory.set('Invalid image file')


def updateIcos():
    # Load the image
    img = None
    try:
        img = Image.open(imageDirectory.get())
    except FileNotFoundError:
        imageDirectory.set('The image doesn\'t exist')
        return
    except UnidentifiedImageError:
        imageDirectory.set('This file type is not supported')
        return

    # Account for both slash types
    if discordDirectory.get().index('/') > -1:
        pathSplit = discordDirectory.get().split('/')
    else:
        pathSplit = discordDirectory.get().split('\\')

    # Save the ico in both ico spots
    img.save('/'.join(pathSplit[0:-1]) + '/app.ico')
    img.save('/'.join(pathSplit[0:-2]) + '/app.ico')

    quit()


if __name__ == '__main__':
    # Check for OS
    if os.name != 'nt':
        print('This currently only works for windows.')
        quit()

    # Make Window Structure
    root = Tk()
    root.title("Discord Icon Changer")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky='NESW')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Discord Directory Box
    discordDirectory = StringVar()
    discordEntry = ttk.Entry(mainframe, width=70, textvariable=discordDirectory)
    discordEntry.grid(column=1, row=1, sticky='WE')
    discordDirectory.set('C:/Users/77jam/AppData/Local/Discord/app-1.0.9021/Discord.exe')

    # Discord Directory Browse Button
    ttk.Button(mainframe, text='Browse', command=getDiscordPath).grid(column=2, row=1, sticky='WE')

    # Image Directory Box
    imageDirectory = StringVar()
    imageEntry = ttk.Entry(mainframe, width=70, textvariable=imageDirectory)
    imageEntry.grid(column=1, row=2, sticky='WE')
    imageDirectory.set('Path to Image')

    # Image Directory Browse Button
    ttk.Button(mainframe, text='Browse', command=getImagePath).grid(column=2, row=2, sticky='WE')

    # Run Button
    ttk.Button(mainframe, text='Update Icon', command=updateIcos).grid(column=1, row=3, columnspan=2)
    # Add some padding
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
