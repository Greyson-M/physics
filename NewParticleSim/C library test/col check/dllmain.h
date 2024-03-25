#ifndef _DLL_MAIN_H_
#define _DLL_MAIN_H_
#include <iostream>

#if defined DLL_EXPORT
#define DECLDIR __declspec(dllexport)
#else
#define DECLDIR __declspec(dllimport)
#endif

typedef struct Vector;

extern "C"
{
	DECLDIR float distance(float x1, float y1, float x2, float y2);
	DECLDIR int add(int a, int b);
	DECLDIR int check(Vector *p, int size);
}

#endif