class Source(object):
    def __init__(self,
                 alias=None,
                 log_number=None,
                 resolution=None,
                 rectangle=None,
                 crossbar=None,
                 censoring=None):
        self.Alias = alias
        self.LogNumber = log_number
        self.Resolution = resolution
        self.Rectangle = rectangle
        self.Crossbar = crossbar
        self.Censoring = censoring

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
                alias = line.replace('[', '').replace(']', '')
                current_source = Source(alias=alias)
            else:
                # getting current property name & value
                current_property_name, current_property_value = line.split('=')
                if current_property_value == 'None':
                    current_property_value = None

                # storing property value
                setattr(current_source, current_property_name, current_property_value)

        # at the end of file, if there is a not blank source...
        if current_source is not None:
            # ...appending current_source to sources list
            sources.append(current_source)

        # at the very end, return sources
        return sources


class Layout(object):
    def __init__(self, sources=None):
        # pre-allocating properties
        self.Aliases = []
        self.Sources = []
        self.Resolutions = []
        self.Rectangles = []
        self.Crossbars = []
        self.Censorings = []
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
            self.X_Widths.append(source.X_Width)
            self.Y_Widths.append(source.Y_Width)
            self.Ratios.append(source.Ratio)

    def __repr__(self):
        return "Layout instance with sources '" + self.Name + "'"

    @property
    def Name(self):
        name = ''
        for index, alias in enumerate(self.Aliases):
            name += alias
            if index != len(self.Aliases) - 1:
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
        text += '\n'

        # Resolutions
        text += '[Resolutions]\n'
        for index, value in enumerate(self.Resolutions):
            text += 'Resolution{}={}\n'.format(index+1, value)
        text += '\n'

        # Censoring
        text += '[Censoring]\n'
        for index, value in enumerate(self.Censorings):
            text += 'Area{}={}\n'.format(index + 1, value)
        text += '\n'

        # Crossbar
        text += '[Crossbar]\n'
        for index, value in enumerate(self.Crossbars):
            if value is not None:
                text += 'Input{}={}\n'.format(index + 1, value)
                text += 'Output{}=0\n'.format(index + 1)
        text += '\n'

        # Views

        return text

    @staticmethod
    def decode_layouts(layouts_txt_path, sources):
        # pre-allocating layouts list
        layouts = []

        # reading layouts.txt file lines
        with open(layouts_txt_path) as f:
            lines = f.readlines()

        for line in lines:
            # removing the \n character:
            line = line.rstrip()

            # removing spaces
            line = line.replace(" ", "")

            # splitting to get aliases
            aliases = line.split('+')

            # looking for right source instances with aliases
            current_sources = Layout.get_sources_from_aliases(sources=sources, aliases=aliases)

            # appending current layout instance
            layouts.append(Layout(sources=current_sources))
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
