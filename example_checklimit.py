from SofaGW.utils import SaveImage
from SofaGW.simulation.scene import SOFA

sim = SOFA(vessel_filename='vessel/phantom.obj')
for i in range(2000):
    print("i",i)
    print("sim.root.InstrumentCombined.m_ircontroller.findData('xtip').value",sim.root.InstrumentCombined.m_ircontroller.findData('xtip').value)
    print("sim.root.InstrumentCombined.m_ircontroller.findData('rotationInstrument').value",sim.root.InstrumentCombined.m_ircontroller.findData('rotationInstrument').value)
    sim.action(translation=1, rotation=0.1)
    sim.step(realtime=False)
    image = sim.GetImage()
    SaveImage(image=image, filename=f'image/image_{i}.jpg')
