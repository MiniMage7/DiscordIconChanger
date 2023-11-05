import os
import numpy as np
from PIL import Image, ImageDraw, UnidentifiedImageError


# Takes an image file and makes it circular
def roundImage(image):
    # Function inspired from:
    # stackoverflow.com/questions/51486297/cropping-an-image-in-a-circular-way-using-python
    npImage = np.array(image)
    h, w = image.size

    # TODO: Square/Center image

    # Create same size alpha layer with circle
    alpha = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice(((0, 0), (h, w)), 0, 360, fill=255)

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
    # TODO: Make this point at Discord.exe for smarter future dev
    user = os.environ.get('USERNAME')
    discordDirectory = 'C:\\Users\\' + user + '\\AppData\\Local\\Discord'

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
    filenames = os.listdir(discordDirectory)
    for filename in filenames:
        if filename.find('app-') >= 0:
            img.save(discordDirectory + '\\' + filename + '\\app.ico')
            break

    img.save(discordDirectory + '\\app.ico')

