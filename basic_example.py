from Package.simulation.SimServer import Server, SimController
from Package.utils import SaveImage

sim = SimController(timeout=10)
sim.run()
for i in range(250):
    if i%50 == 1:
        sim.reset()
    sim.action(translation=1, rotation=0.1)
    sim.step(realtime=False)
    image = sim.GetImage()
    SaveImage(image=image, filename=f'image/image_{i}.jpg')
sim.close()
