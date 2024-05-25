from SofaGW import SimController
from SofaGW.utils import SaveImage

vessel_filename = 'vessel/phantom.obj'

sim = SimController(timeout=10,
                    vessel_filename=vessel_filename)
for i in range(500):
    if i == 1:
        sim.reset()
    sim.action(translation=1, rotation=0.1)
    sim.step(realtime=False)
    image = sim.GetImage()
    SaveImage(image=image, filename=f'image/image_{i}.jpg')
sim.close()
