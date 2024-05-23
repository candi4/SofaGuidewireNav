from SofaGuidewireNav import SimController
from SofaGuidewireNav import utils

sim = SimController(timeout=10)
sim.open()
for i in range(500):
    if i == 1:
        sim.reset()
    sim.action(translation=1, rotation=0.1)
    sim.step(realtime=False)
    image = sim.GetImage()
    utils.SaveImage(image=image, filename=f'image/image_{i}.jpg')
sim.close()
