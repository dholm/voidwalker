import gdb
import tempfile

from ..ui.terminal import Terminal


class GdbTerminal(Terminal):
    def _get_depth(self):
        tf = tempfile.NamedTemporaryFile(delete=True)
        gdb.execute('shell tput colors >%s' % tf.name, False, True)
        tf.flush()
        try:
            return int(tf.read().strip())
        except ValueError:
            return Terminal.DEFAULT_DEPTH

    def __init__(self):
        width = gdb.parameter('width')
        height = gdb.parameter('height')
        depth = self._get_depth()
        super(GdbTerminal, self).__init__(width, height, depth)

    def write(self, string, dictionary=None):
        gdb.write(self.theme().write(string, dictionary))
