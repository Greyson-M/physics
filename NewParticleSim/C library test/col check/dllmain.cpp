// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
#include "dllmain.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#define DLL_EXPORT

typedef struct Vector {
    float x;
    float y;
} Vector;

extern "C" {
    float distance(float x1, float y1, float x2, float y2) {
        float xd = x2 - x1;
        float yd = y2 - y1;
        return sqrt(xd * xd + yd * yd);
    }

    int add(int a, int b) {
		return a + b;
	}


    int check(Vector *p, int size) {

        //float * result = (float*)malloc(size * sizeof(float));

        int found = 0;

        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (i == j) {
					continue;
				}

                float d = distance(p[i].x, p[i].y, p[j].x, p[j].y);
                if (d < 1.0)
                {
                    return j;
                }

			}
        }
        return -1;
        
	}

}


BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

