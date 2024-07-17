import pyglet
from pyglet import gl
import numpy as np
from PIL import Image

# Define width and height for the off-screen rendering
width, height = 800, 600

# Create a hidden window
config = pyglet.gl.Config(double_buffer=False)
window = pyglet.window.Window(width=width, height=height, config=config, visible=False)

# Make the context current
window.switch_to()
gl.glViewport(0, 0, width, height)
gl.glClearColor(0.0, 1.0, 0.0, 1.0)
gl.glClear(gl.GL_COLOR_BUFFER_BIT)

# Read the buffer
buffer = (gl.GLubyte * (width * height * 4))(0)
gl.glReadPixels(0, 0, width, height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, buffer)

# Convert the buffer to a numpy array
image = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
image = np.flipud(image)  # Flip the image vertically

# Save the image
image = Image.fromarray(image)
image.save("offscreen_render.png")

# Clean up and close the window
window.close()