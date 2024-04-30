from Package.scene import SOFA, SaveImage

sofa = SOFA()


for i in range(10000):
    sofa.action(1,0.01)
    sofa.step()
    image = sofa.GetImage()
    SaveImage(image, f'image/screen{i%10}.jpg')


