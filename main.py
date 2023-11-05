import os
import numpy as np
from PIL import Image, ImageDraw, UnidentifiedImageError


# Takes an image file and makes it circular
def roundImage(image):
    # Function inspired from:
    # stackoverflow.com/questions/51486297/cropping-an-image-in-a-circular-way-using-python
    image = image.convert("RGB")
    w, h = image.size

    # If the image isn't a square
    if h > w:
        image = image.crop((0, (h - w) / 2, w, h - (h - w) / 2))
        w, h = image.size
    elif w > h:
        image = image.crop(((w - h) / 2, 0, w - (w - h) / 2, h))
        w, h = image.size

    npImage = np.array(image)

    # Create same size alpha layer with circle
    alpha = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice(((0, 0), (w, h)), 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)

    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Save with alpha
    return Image.fromarray(npImage)


# Main
if __name__ == '__main__':
    # Check for OS
    if os.name != 'nt':
        print('This currently only works for windows.')
        quit()

    # Find the Discord directory (currently default)
    user = os.environ.get('USERNAME')
    discordDirectory = 'C:\\Users\\' + user + '\\AppData\\Local\\Discord'

    if os.path.exists(discordDirectory):
        filenames = os.listdir(discordDirectory)
        for filename in filenames:
            if filename.find('app-') >= 0:
                discordDirectory += '\\' + filename + '\\Discord.exe'
                break

    # If discord wasn't found, ask user for discord.exe location
    while not (os.path.exists(discordDirectory) and discordDirectory.endswith('\\Discord.exe')):
        print('\nDiscord was not at the default location.')
        discordDirectory = input('Please paste the filepath to Discord.exe\n>')

        # In case the user just pasted the path to the folder that Discord is in
        # Check if the pasted path is a folder with Discord.exe in it
        if os.path.exists(discordDirectory) and os.path.isdir(discordDirectory):
            for filename in os.listdir(discordDirectory):
                if filename == 'Discord.exe':
                    discordDirectory += '\\Discord.exe'

    # Get the image to make into the icon
    img = None
    pathToNewIcon = ''
    while img is None:
        try:
            pathToNewIcon = input('\nWhat is the image name?\n>')
            img = Image.open(pathToNewIcon)
        except FileNotFoundError as e:
            print('The image doesn\'t exist. Is it in the same directory as this program?')
        except UnidentifiedImageError as e:
            print('This file type is not supported')

    # Handle rounding the image
    if input('\nWould you like to round the image? [Y/n]\n>').lower() != 'n':
        img = roundImage(img)

    # Save image in the 2 ico spots
    pathSplit = discordDirectory.split('\\')
    img.save('\\'.join(pathSplit[0:-1]) + '\\app.ico')
    img.save('\\'.join(pathSplit[0:-2]) + '\\app.ico')
