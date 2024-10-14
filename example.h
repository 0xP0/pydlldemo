// example.h
#ifndef EXAMPLE_H
#define EXAMPLE_H

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

EXPORT int add(int a, int b);

#ifdef __cplusplus
}
#endif

#endif // EXAMPLE_H