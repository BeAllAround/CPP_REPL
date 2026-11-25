#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


// TODO: DO THIS FOR ALL the C-headers for C++ but is there a need for that really is the question? Can we not just include the C style header.
#if __GNUG__
#include <cassert>
#else
#include <assert.h>
#endif

/*
// TODO: Only use the ones needed
// TODO: Predefine a macro to add them at compile time
#include <ctype.h>
#include <regex.h>
#include <errno.h>
#include <assert.h>
#include <stdarg.h>
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
#include <unistd.h>
#include <math.h>
*/

static int __c  = 0;

// g++ -fpic -shared debug.cpp -Iinclude -o libdebug.so
// g++ test_debug.cpp -o out.out --std=c++11 -O3 -I./  -Iinclude -L./ -ldebug
// runtime: export LD_LIBRARY_PATH="/home/alex/Project/LITTLE_API" && ./out.out

extern void __pause();

#define newLine printf("\n");
#define BREAK printf("---LINE: %d - BREAK %d---", __LINE__, ++__c); \
		newLine; \
		__pause();
#define _print(s) printf(s); \
		newLine;

#define RESET __c = 0


#define start_time clock_t s_t_a_r_t = clock();

#if __GNUG__
#define end_time printf("[Cpu_time_used: %f]\n", static_cast<double>(clock() - s_t_a_r_t) / CLOCKS_PER_SEC);
#else
#define end_time printf("[Cpu_time_used: %f]\n", ((double) (clock() - s_t_a_r_t)) / CLOCKS_PER_SEC);
#endif

void __pause() {
	char s[2];
	_print("PAUSED");
	if(fgets(s, sizeof s, stdin)) {}
}


