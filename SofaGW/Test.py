from SofaGW import SimController, example_vessel
from SofaGW.utils import SaveImage, root_dir

def test_installation():
    sim = SimController(timeout=10,
                        vessel_filename=example_vessel)

    errclose = False
    for i in range(2000):
        sim.action(translation=1, rotation=0.1)
        errclose = sim.step(realtime=False)
        if errclose:
            sim.reset()
    sim.close()