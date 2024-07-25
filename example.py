from SofaGW import SimController, example_vessel
from SofaGW.utils import SaveImage

sim = SimController(timeout=10,
                    vessel_filename=example_vessel)

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
