import importlib.metadata

try:
    __version__ = importlib.metadata.version(__package__ or __name__)
except ImportError:
    __version__ = None
