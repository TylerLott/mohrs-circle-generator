import tempfile
import shutil
import tkinter as tk
from tkinter import filedialog
import MohrsCircle as Mc
import os
from PIL import Image, ImageTk

tmpdir = tempfile.mkdtemp()
# print(tmpdir)


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Mechanics and Materials 2140")

        x = (self.master.winfo_screenwidth()) / 2
        y = (self.master.winfo_screenheight()) / 3
        self.master.geometry("+%d+%d" % (x, y))

        self.master.config(menu=tk.Menu(self.master))

        text_frame = tk.Frame(self)
        text_frame.grid(row=0, column=1, sticky='w')
        tk.Label(text_frame, text='Input information about area to create a Mohrs circle.').grid(row=1, column=0,
                                                                                                 columnspan=2,
                                                                                                 sticky='w')

        # formatting for all of the inputs and buttons in the interface
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

        tk.Label(text_frame, text='Units: ').grid(row=10, column=0, sticky='w')
        self.user_units = tk.Entry(text_frame, background='white', width=24)
        self.user_units.insert(0, 'kPa')
        self.user_units.grid(row=10, column=1, sticky='w')
        self.user_units.focus_set()

        tk.Label(text_frame, text='Show Principal Plane: ').grid(row=12, column=0, sticky='w')
        self.checkvar = tk.IntVar()
        self.checkvar.set(0)
        self.user_principal = tk.Checkbutton(text_frame, variable=self.checkvar, onvalue=1, offvalue=0, width=18)
        self.user_principal.grid(row=12, column=1, sticky='w')
        self.user_principal.focus_set()

        tk.Button(self, text='Create Mohrs circle', command=self.create_mohrs_circle).grid(row=14, column=1)

        pic_frame = tk.Frame(self)
        pic_frame.grid(row=16, column=0, rowspan=10, columnspan=10)

    # def show_image(self):
    #     load = Image.open('')
    #     render = ImageTk.PhotoImage(load)
    #
    #     img = Label(self, image=render)
    #     img.image = render
    #     img.place(x=0, y=0)


    def create_mohrs_circle(self):
        # toggle button for showing the principal plane
        if self.checkvar.get() == 0:
            show_prin = False
        if self.checkvar.get() == 1:
            show_prin = True

        # creates the mohrs circle
        circle = Mc.MohrsFindPrincipal(
                                         float(self.user_sigA.get()),
                                         float(self.user_sigB.get()),
                                         float(self.user_tau.get()),
                                         tmpdir,
                                         float(self.user_angle.get()),
                                         self.user_units.get(),
                                         show_principal=show_prin
                                         )
        circle.visualize()

        # button that allows to save picture in a file of the users choice
        tk.Button(self, text='Save Image As...', command=self.file_saver).grid(row=16, column=0)

        # finds the file saved in the temp directory and uses pillow to load the image then tkinter renders it
        path = os.path.join(tmpdir, 'mohrs.png')

        load = Image.open(path)
        render = ImageTk.PhotoImage(load)

        img = tk.Label(self, image=render)
        img.grid(row=24, column=1, sticky='e')
        img.image = render

    def file_saver(self):
        # method to allow user to search directories to save picture of the circle
        path = os.path.join(tmpdir, 'mohrs.png')
        save_image = Image.open(path)
        save = filedialog.asksaveasfilename(parent=self, title='choose file',
                                            defaultextension=".png",
                                            filetypes=(("png file", "*.png"),))
        save_image.save(save)
        # print(save)


if __name__ == '__main__':

    root = tk.Tk()
    app = App(root)

    # deletes the temp dir and everything in it on close
    def on_closing():
        shutil.rmtree(tmpdir)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()



