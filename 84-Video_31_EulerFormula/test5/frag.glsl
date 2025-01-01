#version 330 core
out vec4 frag_color;

uniform float opacity;
uniform float center;

in float x;

void main()
{
    float color = 0.2f*(x+1-center)/2;
    
    frag_color = vec4(color, color, color, opacity);
}