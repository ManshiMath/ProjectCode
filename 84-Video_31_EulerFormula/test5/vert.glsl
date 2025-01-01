#version 330 core

// layout (location = 0) in vec3 point;
// layout (location = 1) in vec4 color;

in vec3 point;
in vec4 color;

out vec4 out_color;
out float x;

void main()
{
    gl_Position = vec4(point, 1.0);
    out_color = color;
    x = point.x;
}