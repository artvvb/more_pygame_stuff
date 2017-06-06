[[vertex-program]]
#version 120
void main()
{
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}

[[fragment-program]]
#version 120
void main()
{
	gl_FragColor = vec4(1,0,0,1);
}
