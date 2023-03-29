import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np

# Define the vertex shader
vertex_shader_source = """

layout (location = 0) in vec2 position;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    gl_PointSize = 1.0;
}
"""

# Define the fragment shader
fragment_shader_source = """

out vec4 color;

void main()
{
    color = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW initialization failed")

# Create a window
window = glfw.create_window(640, 480, "My OpenGL Window", None, None)
if not window:
    glfw.terminate()
    raise Exception("Window creation failed")

# Make the window's context current
glfw.make_context_current(window)

# Set the viewport size
glViewport(0, 0, 640, 480)

# Compile the shaders and link them into a program
vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
program = compileProgram(vertex_shader, fragment_shader)

# Define the points to be rendered
points = np.array([
    [0.0, 0.0],
    [0.1, 0.2],
    [-0.3, 0.4],
    [0.5, -0.6]
], dtype=np.float32)

# Create a vertex buffer object (VBO) and bind it
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)

# Upload the points to the VBO
glBufferData(GL_ARRAY_BUFFER, points.nbytes, points, GL_STATIC_DRAW)

# Enable the vertex attribute array for the position
position_location = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(position_location)

# Specify the vertex attribute array for the position
glVertexAttribPointer(position_location, 2, GL_FLOAT, GL_FALSE, 0, None)

# Main loop
while not glfw.window_should_close(window):
    # Clear the screen to black
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Use the shader program
    glUseProgram(program)

    # Draw the points
    glDrawArrays(GL_POINTS, 0, 4)

    # Swap buffers
    glfw.swap_buffers(window)

    # Poll for events
    glfw.poll_events()

# Terminate GLFW
glfw.terminate()
