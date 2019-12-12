import sys
from shutil import move
from os.path import join
from tkinter import Tk
from tkinter import messagebox
from GenView.utils import touch_dir
from GenView.utils import current_date_time
from GenView.classes import Source, Layout

# creating window root for tkinter
# (this will hide useless window)
root = Tk()
Tk.withdraw(root)

# noinspection PyBroadException
try:
    # setting OneViewX directory
    ovx_dir = 'C:\\OneViewX'

    # computing backup directory
    backup_dir = join(ovx_dir, 'Backups', current_date_time())
    touch_dir(backup_dir)

    # making backup of layout and configuration files
    ini_files, ini_paths = Layout.layout_finder()
    for ini_file, ini_path in zip(ini_files, ini_paths):
        new_path = join(backup_dir, ini_file)
        move(ini_path, new_path)

    # computing sources.ini and layouts.txt path
    sources_ini_path = join(ovx_dir, 'sources.ini')
    layouts_txt_path = join(ovx_dir, 'layouts.txt')

    # creating a list of source instances from the sources.ini file
    sources = Source.decode_sources(sources_ini_path=sources_ini_path)

    # creating a list of layout instances from the layouts.ini file
    layouts = Layout.decode_layouts(
        layouts_txt_path=layouts_txt_path,
        sources=sources
    )

    # creating layout files
    for layout in layouts:
        # computing current LayoutX.ini path
        layout_path = join(ovx_dir, 'Layout{}.ini'.format(layout.LayoutIndex))

        # opening the file in write mode
        layout_file = open(layout_path, 'w')

        # writing lines
        layout_file.writelines(layout.Text)

    # giving a feedback to the user
    messagebox.showinfo(
        title='Success',
        message='{} new Layout(s) successfully created.'.format(len(layouts)))
except:
    error_type, value, _ = sys.exc_info()
    messagebox.showerror(
        title='Ops... we got an error!!',
        message='Error type: {}\n{}'.format(error_type, value)
    )
