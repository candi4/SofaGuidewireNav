from Package.scene import SOFA, SaveImage

sofa = SOFA()


for i in range(10000):
    if i%50 == 0: sofa.reset()
    sofa.action(translation=1,rotation=0.1)
    sofa.step()
    image = sofa.GetImage()
    SaveImage(image, f'image/screen{i%50}.jpg')


