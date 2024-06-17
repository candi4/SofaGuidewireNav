from SofaGW.simulation.SimServer import SimController
from SofaGW.utils import SaveImage

sim = SimController(timeout=10,
                    vessel_filename='vessel/phantom.obj')

errclose = False
for i in range(2000):
    sim.action(translation=1, rotation=0.1)
    errclose = sim.step(realtime=False)
    print("errclose",errclose)
    if errclose:
        sim.reset()
    image = sim.GetImage()
    SaveImage(image=image, filename=f'image/image_{i}.jpg')
sim.close()
