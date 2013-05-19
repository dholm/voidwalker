VERSION = (0, 2, 99, 'dev')
__version__ = ''.join(['-.' [type(x) == int] + str(x) for x in VERSION])[1:]
