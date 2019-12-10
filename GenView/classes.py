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
    def decode_sources(ini_path):
        # pre-allocating sources list
        sources = []

        # reading sources.ini file lines
        with open(ini_path) as f:
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
    def __init__(self,
                 sources=None):
        self.Sources = sources

    def __repr__(self):
        return "Layout instance with sources '{}'".format(self.Sources)

    @staticmethod
    def decode_layouts(ini_path, sources_list):
        # pre-allocating sources list
        layouts = []

        # reading template.ini file lines
        with open(ini_path) as f:
            lines = f.readlines()

        for line in lines:
            # removing the \n character:
            line = line.rstrip()

            # removing spaces
            line = line.replace(" ", "")

            #splitting the strings
            line = line.split('+')

            #appending the line to var layouts
            layouts.append(line)

        #layouts = Layout()
        return layouts

    def gen_sources(ini_path, layouts):
