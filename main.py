from os import getcwd
from os.path import join
from GenView.classes import Source, Layout

# computing sources.ini and layouts.txt path
sources_ini_path = join(getcwd(), 'test_files', 'sources.ini')
layouts_txt_path = join(getcwd(), 'test_files', 'layouts.txt')

# creating a list of source instances from the sources.ini file
sources = Source.decode_sources(sources_ini_path=sources_ini_path)

# creating a list of layout instances from the layouts.ini file
layouts = Layout.decode_layouts(layouts_txt_path=layouts_txt_path,
                                sources=sources)
print(layouts)