import os
from StringIO import StringIO

# The context generator creates a line-by-line mapping of all files that are
# validated. It will then use that to help produce useful bits of code for
# errors, warnings, and the like.

class ContextGenerator:

    def __init__(self, data=None):
        if isinstance(data, StringIO):
            data = data.getvalue()
        
        self.data = data.split("\n")

    def get_context(self, line=1, column=0):
        "Returns a tuple containing the context for a line"
        
        line -= 1 # The line is one-based

        # If there is no data in the file, there can be no context.
        datalen = len(self.data)
        if datalen <= line:
            return None
        
        build = [self._format_line(line=line, column=column)]

        # Add surrounding lines if they're available.
        if line > 0:
            build.insert(0, self._format_line(line=line - 1, rel_line=0))
        if line < datalen - 1:
            build.append(self._format_line(line=line + 1, rel_line=2))

        for i in range(len(build)):
            # Truncate each line to 140-ish characters
            if len(build[i]) >= 140:
                
                build[i] = "%s ..." % build[i][:140]

        # Return the final output as a tuple.
        return tuple(build)

    def get_line(self, position):
        "Returns the line that the given string position would be found on"

        count = len(self.data[0])
        line = 1
        while count < position:
            count += len(self.data[line])
            line += 1

        return line

    def _format_line(self, line, column=0, rel_line=1):
        "Formats a line from the data to be the appropriate length"

        data = self.data[line].strip()

        line_length = len(data)
        if line_length >= 140:
            if rel_line == 0:
                # Trim from the beginning
                data = "... %s" % data[-140:]
            elif rel_line == 1:
                # Trim surrounding the error position
                
                if column < 70:
                    data = "%s ..." % data[:140]
                elif column > line_length - 70:
                    data = "... %s" % data[-140:]
                else:
                    data = "... %s ..." % data[column - 70:column + 70]

            elif rel_line == 2:
                # Trim from the end
                data = "%s ..." % data[:140]

        return data
