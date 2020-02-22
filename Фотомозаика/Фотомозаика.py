#!/usr/bin/env python3
import os
import sys
import PIL
import json

import tkinter as tk

from tkinter import filedialog
# from tkinter import ttk
from PIL import Image

# original_background = Image.open(r'C:\Users\Admin\Desktop\background\1346678072_more.jpg')
# original_image1 = Image.open(r'C:\Users\Admin\Desktop\images\first.jpg')
# original_image2 = Image.open(r'C:\Users\Admin\Desktop\images\second.jpg')
# original_image3 = Image.open(r'C:\Users\Admin\Desktop\images\third.jpg')
# original_image4 = Image.open(r'C:\Users\Admin\Desktop\images\fourth.jpg')

# images = [image, image1]


class Main(tk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.toolbar = tk.Frame(bg="#FFFFFF", bd=2)
        self.toolbar.pack(fill="both", side="top", expand=True)
        self.label_images_directory = tk.Label(self.toolbar, bg="white", justify=tk.LEFT, text=text_for_images_label + directories['images_directory'])
        self.label_background_directory = tk.Label(self.toolbar, bg="white", justify=tk.LEFT, text=text_for_background_label + directories['background_directory'])
        self.label_output_images_directory = tk.Label(self.toolbar, bg="white", justify=tk.LEFT, text=text_for_output_label + directories['output_images_directory'])
        self.init_main()

    def init_main(self):
        # упаковка кнопок
        btn_images_directory = tk.Button(self.toolbar, text="Папка с фото",
                                         command=lambda: self.open_filedialog(dialog_to_open="images",
                                                                              valuable_directory="images_directory",
                                                                              title='Choose the directory of the input original_images.',
                                                                              text=text_for_images_label,
                                                                              label=self.label_images_directory,
                                                                              must_exist=True),
                                         bg="#FFCFFF", compound=tk.TOP, width=13)
        btn_images_directory.pack()  # side=tk.LEFT)
        btn_images_directory.place(relx=0.001, rely=0.01)

        btn_background_directory = tk.Button(self.toolbar, text="Выбрать фон",
                                             command=lambda: self.open_filedialog(dialog_to_open="background",
                                                                                  valuable_directory="background_directory",
                                                                                  title='Choose the background.',
                                                                                  text=text_for_background_label,
                                                                                  label=self.label_background_directory),
                                             bg="#FFCFFF", compound=tk.TOP, width=13)
        btn_background_directory.pack()  # side=tk.LEFT)
        btn_background_directory.place(relx=0.001, rely=0.16)

        btn_output_images_directory = tk.Button(self.toolbar, text="Конечная папка",
                                                command=lambda: self.open_filedialog(dialog_to_open="output",
                                                                                     valuable_directory="output_images_directory",
                                                                                     title='Choose the output directory',
                                                                                     text=text_for_output_label,
                                                                                     label=self.label_output_images_directory,
                                                                                     must_exist=True),
                                                bg="#FFCFFF", compound=tk.TOP, width=13)
        btn_output_images_directory.pack()  # side=tk.LEFT)
        btn_output_images_directory.place(relx=0.001, rely=0.31)

        # TODO сделать сначала проверку, что все выбранные пути существуют (отдельный метод)
        btn_initialize_operations = tk.Button(self.toolbar, text="Склеить фото",
                                              # TODO сделать проверку, что операции с фоном уже выполнялись ->
                                              #  не надо трогать кусок фона (мб его удалять/перемещать куда-то)
                                              command=lambda: ImageChanger.image_merging(),
                                              bg="#CFCFFF", compound=tk.TOP, width=13)
        btn_initialize_operations.pack()  # side=tk.LEFT)
        btn_initialize_operations.place(relx=0.7, rely=0.85)

        # упакова лейблов, где будет отображаться путь, до выбранных файлов
        self.label_images_directory.pack()
        self.label_images_directory.place(relx=0.25, rely=0)
        self.label_background_directory.pack()
        self.label_background_directory.place(relx=0.25, rely=0.145)
        self.label_output_images_directory.pack()
        self.label_output_images_directory.place(relx=0.25, rely=0.295)

    @staticmethod
    def open_filedialog(dialog_to_open, valuable_directory, title="", text="", must_exist=False, label=None):
        # если путь раньше выбирался, то окно выбора директории откроется на папке, где лежит конечный файл пути
        if directories[valuable_directory]:
            init_dir = directories[valuable_directory]
            init_dir = init_dir.rsplit(r'/', 1)
            init_dir = init_dir[0]
        else:
            init_dir = r"C:\Users\Admin\Desktop"
        if dialog_to_open == "images" and label:
            directory = filedialog.askdirectory(mustexist=must_exist,
                                                initialdir=init_dir,
                                                title=title)
        elif dialog_to_open == "output" and label:
            directory = filedialog.askdirectory(mustexist=must_exist,
                                                initialdir=init_dir,
                                                title=title)
        else:
            directory = filedialog.askopenfilename(initialdir=init_dir,
                                                   title=title)

        if directory and label:
            directories.update({valuable_directory: directory})
            ImageChanger.json_upd(json_path, directories)
            if dialog_to_open == "images":
                Main.images_list_appender(directory)
            label.config(text=text + directory)
            print(directories[valuable_directory])

    @staticmethod
    def images_list_appender(directory):
        global original_images
        original_images = []
        for file in os.listdir(directory):
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                original_images.append(directory + r"/" + file)
        print("Images list: \n", original_images, "\n")

    @staticmethod
    def directories_upd_at_start():
        global directories
        global json_exists

        if json_exists:
            with open(json_path, "r", encoding="utf-8") as json_file:
                not_existing_directory = []
                directories = json_file.read()
                if directories:
                    directories = json.loads(directories)

                # проверка, все ли пути из старой json существуют; если есть несуществующий путь, заменяем пустым
                for key in directories.keys():
                    if directories[key]:
                        if not os.path.exists(directories[key]):
                            not_existing_directory.append(key)
                if not_existing_directory:
                    for old_directory in not_existing_directory:
                        directories.update({old_directory: ""})
                    ImageChanger.json_upd(json_path, directories)

                if directories["images_directory"]:
                    Main.images_list_appender(directories["images_directory"])
                print("Actualized directories:\n", directories, "\n")
        else:
            directories.update({"images_directory": "", "background_directory": "", "output_images_directory": ""})
            ImageChanger.json_upd(json_path, directories)
            json_exists = True


class ImageChanger:
    def __init__(self):
        pass

    @staticmethod
    def resize_image(old_image, size):
        # with open(old_image) as f:
        #     for line in f:
        #         line = line.rstrip()
        #         if line:
        # TODO сделать возможность объединять изменяемые фото с рамкой, которую скинула Света
        old_image = Image.open(open(old_image, "rb"))
        old_width, old_height = old_image.size
        print('The original image size is {wide} wide x {height} '
              'high'.format(wide=old_width, height=old_height))
        resized_image = old_image.resize(size)
        new_width, new_height = resized_image.size
        print('The resized image size is {wide} wide x {height} '
              'high'.format(wide=new_width, height=new_height))
        return resized_image

    @staticmethod
    def path_creator(path, new_folder):
        new_path = path + r"/" + new_folder
        if os.path.exists(new_path):
            for file in os.listdir(new_path):
                os.remove(new_path + r"/" + file)
        else:
            os.mkdir(path=new_path, mode=0o777)
        return new_path

    @staticmethod
    def json_upd(path, new_json):
        with open(path, "w", encoding="utf-8") as edited_file:
            edited_file.write(str(new_json).replace("'", '"'))

    @staticmethod
    def image_merging():
        # TODO сделать понятный читаемый код
        # TODO сделать отдельно метод склеивания картинок и метод делающий две картинки в одной
        # new_background = r'C:\Users\Admin\Desktop\background\1346678072_more.jpg'
        dst_path = ImageChanger.path_creator(path=directories["output_images_directory"], new_folder="sliced_background")
        new_background = ImageChanger.resize_image(old_image=directories["background_directory"], size=(320, 240))
        new_background_path = r'C:\Users\Admin\Desktop\background\new_background.jpg'
        new_background.save(new_background_path)
        backgrounds = []
        if not os.path.exists(dst_path) or not os.path.isfile(new_background_path):
            print('Not exists', dst_path, new_background_path)
            sys.exit(1)
        w, h = int(160), int(120)
        im = Image.open(new_background_path)
        im_w, im_h = im.size
        print('Image width:%d height:%d  will split into (%d %d) ' % (im_w, im_h, w, h))
        w_num, h_num = im_w // w, im_h // h
        number = 1
        for hi in range(0, h_num):
            for wi in range(0, w_num):
                box = (wi * w, hi * h, (wi + 1) * w, (hi + 1) * h)
                piece = im.crop(box)
                tmp_img = Image.new("RGB", (w, h))
                tmp_img.paste(piece)
                img_path = os.path.join(dst_path, "%d.png" % number)
                tmp_img.save(img_path)
                number += 1
                backgrounds.append(tmp_img)
        for i in range(len(original_images)):
            original_images[i] = ImageChanger.resize_image(old_image=original_images[i], size=(160, 120))
        print(original_images)
        w, h = original_images[0].size
        first_picture_transparency = 0.6
        second_picture_transparency = 0.8
        for i in range(len(original_images)):
            for x in range(w):
                for y in range(h):
                    try:
                        pix_coord = (x, y)
                        if type(backgrounds[i]) != PIL.Image.Image:
                            print(type(backgrounds[i]))
                        r, g, b = backgrounds[i].getpixel(pix_coord)
                        if type(original_images[i]) != PIL.Image.Image:
                            print(type(original_images[i]))
                        r1, g1, b1 = original_images[i].getpixel(pix_coord)
                        new_col = (int(first_picture_transparency * r + second_picture_transparency * r1),
                                   int(first_picture_transparency * g + second_picture_transparency * g1),
                                   int(first_picture_transparency * b + second_picture_transparency * b1))
                        backgrounds[i].putpixel(pix_coord, new_col)
                    except TypeError:
                        continue
            backgrounds[i].save(directories["output_images_directory"] + "/" + '%d.jpg' % i)


if __name__ == '__main__':
    # константные значения
    json_name = "Фотомозаика.json"
    json_path = os.getcwd() + r"/" + json_name
    text_for_images_label = "Путь до папки с фотографиями:\n"
    text_for_background_label = "Путь до фонового изображения:\n"
    text_for_output_label = "Путь до конечной папки:\n"
    json_exists = os.path.isfile(json_path)

    # изображения
    original_images = []
    directories = {}
    Main.directories_upd_at_start()

    #
    root = tk.Tk()
    app = Main(root)
    root.title("Фотомозаика")
    root.geometry("450x300+300+200")
    root.resizable(False, False)
    root.mainloop()
