[[vertex-program]]
#version 120

in vec2 pos;
uniform vec2 offset = vec2(0.5, 0.5);
uniform vec2 scale  = vec2(0.5, 0.5);
out vec4 outPosition;
void main()
{
	outPosition = vec4(scale * (pos + offset), 0.0, 1.0);
}
