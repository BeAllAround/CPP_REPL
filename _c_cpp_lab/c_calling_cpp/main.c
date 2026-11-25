#include <dlfcn.h>

#include <stdio.h>

#include <stdlib.h>

// #include <iostream>


// #define CAST_HANDLE(DLSYM) reinterpret_cast<typeof(void(*)())>(DLSYM)

#define CAST_HANDLE(DLSYM) (void(*)) (DLSYM)

int main() {
  const char* libfunc_dynamic = "./libfunc_dynamic.so";

  void* handle = dlopen(libfunc_dynamic, RTLD_LOCAL | RTLD_LAZY);

  /*
  using r_t = std::vector<int>;
  using args_type = std::initializer_list<int>;
  */

  typeof(void(*)()) my_init = CAST_HANDLE(dlsym(handle, "my_init"));
  typeof(void(*)()) my_handle = CAST_HANDLE(dlsym(handle, "my_handle"));
  typeof(void(*)()) my_clean_up = CAST_HANDLE(dlsym(handle, "my_clean_up"));

  my_init();

  my_clean_up();

  // function_type _handle = reinterpret_cast<function_type>(dlsym(handle, "my_handle"));

  // function_type _clean_up = reinterpret_cast<function_type>(dlsym(handle, "my_clean_up"));

  // dlclose(handle);

  dlclose(handle);



  /*
     void* _handle = dlopen("./libshared.so", RTLD_LOCAL | RTLD_LAZY);
     dlclose(_handle);
     */

  return 0;
}
