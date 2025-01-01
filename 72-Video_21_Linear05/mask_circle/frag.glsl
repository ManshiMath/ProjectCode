#version 330

uniform sampler2D Texture;
uniform float mask_radius;
uniform vec3 mask_center;

in vec3 v_point;
in vec2 v_im_coords;
in float v_opacity;

out vec4 frag_color;

void main() {
    if (length(v_point - mask_center) > mask_radius) discard;
    frag_color = texture(Texture, v_im_coords);
    frag_color.a *= v_opacity;
}