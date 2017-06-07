#version 120

in vec2 pos;
uniform vec2 offset = vec2(-0.5, -0.5);
uniform vec2 scale  = vec2(2.0, 2.0);
void main()
{
	gl_FrontColor = gl_Color;
	gl_Position = vec4(scale * (pos + offset), 0.0, 1.0);
}
