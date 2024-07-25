import SofaGW.utils as utils
from SofaGW.simulation.SimServer import SimController

example_vessel = utils.root_dir + '/vessel/phantom.obj'

from SofaGW.Test import test_installation

__all__ = ["utils", 'SimController', 'test_installation']

