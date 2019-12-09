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
        return "Source instance with Alias '{}'".format(self.Alias)

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

        # adding a blank space at the end
        # (this will speed up the decoding algorithm)
        lines.append('\n')

        # pre-allocating current source
        current_source = None

        # main cycle
        for line in lines:
            # if firs line char is '[' a new source was found
            if line[0] == '[':
                # removing the \n character:
                line = line.rstrip()

                # creating a new source instance
                alias = line.replace('[', '').replace(']', '')
                current_source = Source(alias=alias)
            # else if line is blank
            elif line == '\n':
                # if current_source is blank as well, nothing happens
                if current_source is None:
                    pass
                else:
                    # closing this source and storing it
                    sources.append(current_source)
                    current_source = None
            # else:
            else:
                # removing the \n character:
                line = line.rstrip()

                # getting current property name & value
                current_property_name, current_property_value = line.split('=')
                if current_property_value == 'None':
                    current_property_value = None

                # storing property value
                setattr(current_source, current_property_name, current_property_value)

        # at the very end, return sources
        return sources
