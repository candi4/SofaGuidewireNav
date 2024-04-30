from Package.scene import SOFA, SaveImage

sofa = SOFA()


for i in range(10000):
    sofa.action(translation=1,rotation=0.1)
    sofa.step()
    image = sofa.GetImage()
    SaveImage(image, f'image/screen{i%10}.jpg')


