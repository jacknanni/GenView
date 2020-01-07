from os import listdir
from os.path import join


class Source(object):
    def __init__(self,
                 alias=None,
                 log_number=None,
                 resolution=None,
                 rectangle=None,
                 crossbar=None,
                 censoring=None,
                 grayscale=False):
        self.Alias = alias
        self.LogNumber = log_number
        self.Resolution = resolution
        self.Rectangle = rectangle
        self.Crossbar = crossbar
        self.Censoring = censoring
        self.Grayscale = grayscale

    def __repr__(self):
        return "Source instance with alias '{}'".format(self.Alias)

    @property
    def X_Width(self):
        if self.Rectangle is None:
            return int(self.Resolution.split('x')[0])
        else:
            return int(self.Rectangle.split(',')[2])

    @property
    def Y_Width(self):
        if self.Rectangle is None:
            return int(self.Resolution.split('x')[1])
        else:
            return int(self.Rectangle.split(',')[3])

    @property
    def Ratio(self):
        if self.X_Width / self.Y_Width * 9 == 16:
            return '16:9'
        elif self.X_Width / self.Y_Width * 3 == 4:
            return '4:3'
        else:
            return '1:1'

    @staticmethod
    def decode_sources(sources_ini_path):
        # pre-allocating sources list
        sources = []

        # reading sources.ini file lines
        with open(sources_ini_path) as f:
            lines = f.readlines()

        # deleting blank rows
        # (this will speed up the algorithm)
        lines = list(filter(lambda x: x != '\n', lines))

        # pre-allocating current source
        current_source = None

        # main cycle
        for line in lines:
            # removing the \n character:
            line = line.rstrip()

            # if first line char is '[' a new source was found
            if line[0] == '[':
                # if current_source is not blank...
                if current_source is not None:
                    # ...appending current_source to sources list
                    sources.append(current_source)

                # creating a new source instance with a brand new alias
                alias = line.replace('[', '').replace(']', '').replace(' ', '')
                current_source = Source(alias=alias)
            else:
                # getting current property name & value
                current_property_name, current_property_value = line.split('=')
                if current_property_value == 'None':
                    current_property_value = None

                # storing property value
                setattr(
                    current_source,
                    current_property_name,
                    current_property_value
                )

        # at the end of file, if there is a not blank source...
        if current_source is not None:
            # ...appending current_source to sources list
            sources.append(current_source)

        # at the very end, return sources
        return sources


class Layout(object):
    def __init__(self, sources=None, layout_index=None):
        self.LayoutIndex = layout_index

        # pre-allocating properties
        self.Aliases = []
        self.Sources = []
        self.Resolutions = []
        self.Rectangles = []
        self.Crossbars = []
        self.Censorings = []
        self.Grayscales = []
        self.X_Widths = []
        self.Y_Widths = []
        self.Ratios = []

        # cycling on sources list to fill properties
        for source in sources:
            self.Aliases.append(source.Alias)
            self.Sources.append(source.LogNumber)
            self.Resolutions.append(source.Resolution)
            self.Rectangles.append(source.Rectangle)
            self.Crossbars.append(source.Crossbar)
            self.Censorings.append(source.Censoring)
            self.Grayscales.append(source.Grayscale)
            self.X_Widths.append(source.X_Width)
            self.Y_Widths.append(source.Y_Width)
            self.Ratios.append(source.Ratio)

    def __repr__(self):
        return "Layout instance with sources '" + self.Name + "'"

    @property
    def n_sources(self):
        return len(self.Aliases)

    @property
    def Name(self):
        if self.LayoutIndex is None:
            name = ''
        else:
            name = '{}: '.format(self.LayoutIndex)
        for index, alias in enumerate(self.Aliases):
            name += alias
            if index != self.n_sources - 1:
                name += ' + '
        return name

    @property
    def Text(self):
        # pre-allocating
        text = ''

        # Info
        text += '[Info]\n'
        text += 'Name=' + self.Name + '\n'
        text += 'AudioSourceName=VoiceMeeter Output\n'
        text += "BackgroundBitMap='OVX_Background_1280_720_black.jpg'\n"
        text += '\n'

        # Sources
        text += '[Sources]\n'
        for index, value in enumerate(self.Sources):
            text += 'Area{}={}\n'.format(index + 1, value)

        # Grayscales
        for index, value in enumerate(self.Grayscales):
            if bool(value) is not False:
                text += 'Grayscale{}={}\n'.format(index+1, 'True')
        text += '\n'

        # Resolutions
        text += '[Resolutions]\n'
        for index, value in enumerate(self.Resolutions):
            text += 'Resolution{}={}\n'.format(index+1, value)
        text += '\n'

        # Censoring
        if not all(x is None for x in self.Censorings):
            text += '[Censoring]\n'
            for index, value in enumerate(self.Censorings):
                if value is not None:
                    text += 'Area{}={}\n'.format(index + 1, value)
            text += '\n'

        # Crossbar
        if not all(x is None for x in self.Crossbars):
            text += '[Crossbar]\n'
            for index, value in enumerate(self.Crossbars):
                if value is not None:
                    text += 'Input{}={}\n'.format(index + 1, value)
                    text += 'Output{}=0\n'.format(index + 1)
            text += '\n'

        # Views
        text += '[Views]\n'
        text += 'View='
        for index in range(1, self.n_sources + 1):
            text += 'View{}'.format(index)
            if index == self.n_sources:
                text += '\n'
            else:
                text += ','
        text += '\n'

        # every View in details
        for view_index in range(self.n_sources):
            # [ViewX]
            text += '[View{}]\n'.format(view_index + 1)
            text += 'Name=\n'
            text += 'Locations={}\n'.format(self.n_sources)
            if self.Layouts[view_index] is not None:
                text += self.Layouts[view_index] + '\n'
            for source_index in range(self.n_sources):
                text += 'Location{}={}\n'.format(
                    source_index + 1,
                    self.Locations[view_index][source_index]
                )
                if self.Rectangles[source_index] is not None:
                    text += 'Rectangle{}={}\n'.format(
                        source_index + 1,
                        self.Rectangles[source_index]
                    )
                text += 'Ratio{}={}\n'.format(
                    source_index + 1,
                    self.Ratios[source_index]
                )
            text += '\n'

        # returning full layout text
        return text

    @property
    def Locations(self):
        if self.n_sources == 1:
            return [[1]]
        if self.n_sources == 2:
            # TODO: insert here some smart routine
            return [[1, 2], [1, 2]]
        if self.n_sources == 3:
            # TODO: insert here some smart routine
            return [[1, 2, 3], [2, 1, 3], [2, 3, 1]]
        if self.n_sources == 4:
            # TODO: insert here some smart routine
            return [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]

    @property
    def Layouts(self):
        if self.n_sources == 1:
            return [None]
        if self.n_sources == 2:
            # TODO: insert here some smart routine
            return ['Layout2=1', 'Layout2=1']
        if self.n_sources == 3:
            # TODO: insert here some smart routine
            return ['Layout3=2', 'Layout3=2', 'Layout3=1']
        if self.n_sources == 4:
            # TODO: insert here some smart routine
            return [None]

    @staticmethod
    def decode_layouts(layouts_txt_path, sources):
        # pre-allocating layouts list
        layouts = []

        # reading layouts.txt file lines
        with open(layouts_txt_path) as f:
            lines = f.readlines()

        # deleting blank rows
        # (this will speed up the algorithm)
        lines = list(filter(lambda x: x != '\n', lines))

        for index, line in enumerate(lines):
            # removing the \n character:
            line = line.rstrip()

            # removing spaces
            line = line.replace(" ", "")

            # splitting to get aliases
            aliases = line.split('+')

            # looking for right source instances with aliases
            current_sources = Layout.get_sources_from_aliases(
                sources=sources,
                aliases=aliases
            )

            # appending current layout instance
            layouts.append(
                Layout(
                    sources=current_sources,
                    layout_index=index + 1
                )
            )
        # at the very end, return the layouts list
        return layouts

    @staticmethod
    def get_sources_from_aliases(sources, aliases):
        output = []
        for alias in aliases:
            for source in sources:
                if source.Alias == alias:
                    output.append(source)
        return output

    @staticmethod
    def layout_finder():
        file_list = []
        path_list = []
        for file in listdir('C:\\OneViewX'):
            if file.endswith('.ini') and file.startswith('Layout'):
                file_list.append(file)
                path_list.append(join('C:\\OneViewX', file))
        return file_list, path_list
