from os import getcwd
from os.path import join
from GenView.classes import Source, Layout


sources_ini_path = join(getcwd(), 'test_files', 'sources.ini')
sources = Source.decode_sources(sources_ini_path)

print(sources)
for source in sources:
    print(source.Ratio)

layouts_ini_path = join(getcwd(), 'test_files', 'template.ini')


layouts = Layout.decode_layouts(layouts_ini_path, sources)
print(layouts)