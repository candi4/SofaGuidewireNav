from SofaGW import SimController
from SofaGW.utils import SaveImage, root_dir

def test():
    sim = SimController(timeout=10,
                        vessel_filename=root_dir+'/vessel/phantom.obj')

    errclose = False
    for i in range(2000):
        sim.action(translation=1, rotation=0.1)
        errclose = sim.step(realtime=False)
        if errclose:
            sim.reset()
    sim.close()