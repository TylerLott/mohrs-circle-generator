import tempfile
import shutil
import tkinter as tk
from tkinter import filedialog
import Mohrs_Circle as mc
import os
from PIL import Image, ImageTk

tmpdir = tempfile.mkdtemp()
print(tmpdir)
class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Mechanics and Materials 2140")

        x = (self.master.winfo_screenwidth()) / 2
        y = (self.master.winfo_screenheight()) / 3
        self.master.geometry("+%d+%d" % (x,y))

        self.master.config(menu=tk.Menu(self.master))

        text_frame = tk.Frame(self)
        text_frame.grid(row=0, column=1, sticky='w')
        tk.Label(text_frame, text='Input information about area to create a Mohrs circle.').grid(row=1, column=0,
                                                                                                 columnspan=2,
                                                                                                 sticky='w')

        tk.Label(text_frame, text='Normal Stress in X: ').grid(row=2, column=0, sticky='w')
        self.user_sigA = tk.Entry(text_frame, background='white', width=24)
        self.user_sigA.grid(row=2, column=1, sticky='w')
        self.user_sigA.focus_set()

        tk.Label(text_frame, text='Normal Stress in Y: ').grid(row=4, column=0, sticky='w')
        self.user_sigB = tk.Entry(text_frame, background='white', width=24)
        self.user_sigB.grid(row=4, column=1, sticky='w')
        self.user_sigB.focus_set()

        tk.Label(text_frame, text='Shear Stress: ').grid(row=6, column=0, sticky='w')
        self.user_tau = tk.Entry(text_frame, background='white', width=24)
        self.user_tau.grid(row=6, column=1, sticky='w')
        self.user_tau.focus_set()

        tk.Label(text_frame, text='Angle of rotation: ').grid(row=8, column=0, sticky='w')
        self.user_angle = tk.Entry(text_frame, background='white', width=24)
        self.user_angle.insert(0, '0')
        self.user_angle.grid(row=8, column=1, sticky='w')
        self.user_angle.focus_set()

        tk.Button(self, text='Create Mohrs circle', command=self.create_mohrs_circle).grid(row=10, column=1)

        pic_frame = tk.Frame(self)
        pic_frame.grid(row=12, column=0, rowspan=10, columnspan=10)


    # def show_image(self):
    #     load = Image.open('')
    #     render = ImageTk.PhotoImage(load)
    #
    #     img = Label(self, image=render)
    #     img.image = render
    #     img.place(x=0, y=0)


    def create_mohrs_circle(self):
        circle = mc.Mohrs_Find_Principal(
                                         float(self.user_sigA.get()),
                                         float(self.user_sigB.get()),
                                         float(self.user_tau.get()),
                                         tmpdir,
                                         float(self.user_angle.get())
                                         )
        circle.visualize()

        tk.Button(self, text='Save Image As...', command=self.file_saver).grid(row=16, column=0)

        path = os.path.join(tmpdir, 'mohrs.png')

        load = Image.open(path)
        render = ImageTk.PhotoImage(load)

        img = tk.Label(self, image=render)
        img.grid(row=24, column=1, sticky='e')
        img.image = render

    def file_saver(self):

        path = os.path.join(tmpdir, 'mohrs.png')
        save_image = Image.open(path)
        save = filedialog.asksaveasfilename(parent=self, title='choose file',
                                            defaultextension=".png",
                                            filetypes=(("png file", "*.png"),))
        save_image.save(save)
        print(save)


if __name__ == '__main__':

    root = tk.Tk()
    app = App(root)

    def on_closing():
        shutil.rmtree(tmpdir)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()



