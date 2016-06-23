all:
	gcc cross.c -O3 -shared -fpic -o lib_cross.so
	gcc face.c -O3 -shared -fpic -o lib_face.so

