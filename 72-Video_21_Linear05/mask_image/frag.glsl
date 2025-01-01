#version 330

uniform sampler2D Texture;
uniform float trim_left;
uniform float trim_right;

in vec3 v_point;
in vec2 v_im_coords;
in float v_opacity;

out vec4 frag_color;

void main() {
    if (v_point.x < trim_left) discard;
    if (v_point.x > trim_right) discard;
    frag_color = texture(Texture, v_im_coords);
    frag_color.a *= v_opacity;
}