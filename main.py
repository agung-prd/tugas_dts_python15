from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import argparse
import os

def pie_chart(listcom, save_file):
    y = np.array(listcom)
    labels = ['resizer', 'reducer', 'inverter']
    # explode = (0.1, 0, 0)
    plt.pie(y, labels=labels, autopct='%1.1f%%',) # explode=explode)
    plt.savefig(save_file)

def resizer(name_file, newsize, new_file):
    img = Image.open(name_file)
    newimg = img.resize(newsize)
    newimg.save(new_file)
    print(f"Done resizing {name_file} to {new_file}")

def inverter(name_file, new_file):
    img = Image.open(name_file)
    arr = np.array(img)
    inverse_arr = 255 - arr # inverting image
    Image.fromarray(inverse_arr).save(new_file)
    print(f"Done inverting {name_file} to {new_file}")

def reduce_color(name_file, fr, new_file):
    img = Image.open(name_file)
    arr = np.array(img)
    reduce_arr = arr // fr * fr # reducing color image to factor fr
    Image.fromarray(reduce_arr).save(new_file)
    print(f"Done reducing {name_file} to {new_file} in factor {fr}")

def batchcommand(csv_file):
    '''
        csv_file must consist: source directory, name_file, destination directory, new_file
                               command, newsize, fr 
    '''
    dataset = pd.read_csv(csv_file)
    com_resizer = list(dataset['com']).count('resizer') * 100 / len(dataset)
    com_reducer = list(dataset['com']).count('reducer') * 100 / len(dataset)
    com_inverter = list(dataset['com']).count('inverter') * 100 / len(dataset)
    list_com = [com_resizer, com_reducer, com_inverter]
    pie_chart(list_com, f"{csv_file[:-4]}.jpg")
    for row in range(len(dataset)):
        command = dataset['com'][row]
        src = dataset['src'][row]
        name = dataset['name'][row]
        dest = dataset['dest'][row]
        new_file = dataset['new_file'][row]
        try:
            size = int(dataset['size'][row])
        except:
            pass
        try:
            fr = int(dataset['fr'][row])
        except:
            pass
        if command == "resizer":
            resizer(os.path.join(src, name), (size, size), os.path.join(dest, new_file))
        elif command == "reducer":
            reduce_color(os.path.join(src, name), fr, os.path.join(dest, new_file))
        else:
            inverter(os.path.join(src, name), os.path.join(dest, new_file))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', type=str, help='command option: batch, reducer, resizer, inverter')
    parser.add_argument('--input', type=str, help='input image file name')
    parser.add_argument('--size', type=int, default=100, help='output size')
    parser.add_argument('--fr', type=int, help='factor reducer')
    parser.add_argument('--output', type=str, help='output image file name')
    opt = parser.parse_args()

    if opt.command == "resizer":
        resizer(opt.input, (opt.size, opt.size), opt.output)
    elif opt.command == "reducer":
        reduce_color(opt.input, opt.fr, opt.output)
    elif opt.command == "batch":
        if opt.input[-3:] == "csv":
            csv_file = opt.input
            batchcommand(csv_file)
        else:
            raise TypeError("Please use csv format for batch command!")
    else:
        inverter(opt.input, opt.output)


