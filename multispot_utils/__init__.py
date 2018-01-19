from .heatmap import heatmap48, spotsh, spotsv
from .utils import info_html

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
