all:
	gcc render_face.c -O3 -shared -fpic -o lib_render_face.so `pkg-config --cflags glfw3` `pkg-config --static --libs glfw3` -lGL
	gcc cross.c -O3 -shared -fpic -o lib_cross.so

