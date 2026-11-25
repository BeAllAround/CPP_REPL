#include <decls.h>


Context* context = NULL;

int is_loaded(void* handle) {
  int _loaded = handle != NULL;
  if(handle != NULL) {
    // NOTE: RTLD_NOLOAD, TOO, INCREMENTS THE REF COUNT SO MAKE SURE IT IS CLEANED UP
    dlclose(handle);
  }
  return _loaded;
}

void unload_all_dl_ref(const char* dl_name, void* dl_handle) {

  // https://man7.org/linux/man-pages/man3/dlerror.3.html
  // TODO: Error Handling dlerror
  while(is_loaded(dlopen(dl_name, RTLD_NOLOAD | RTLD_LAZY)) ) {
    dlclose(dl_handle);
  }

}

Context* get_context() {
  return context;
}


void init() {
  Context* _context = malloc(sizeof(Context));

  *_context = makeContext();

  context = _context;
}


int _eval() {
  printf("main_program START\n");


  // MAIN
  const char* main_shared = "./c_repl/tmp/main_eval.so";

  void* eval_handle = dlopen(main_shared, RTLD_LOCAL | RTLD_LAZY);

  printf("main_eval_handle: %p\n", eval_handle);

  __typeof__(void (*) (Context*) ) _main_as_void = dlsym(eval_handle, "_main_eval");


  _main_as_void(
    context);

  // printf("eval_handle %p\n", eval_handle);

  unload_all_dl_ref(main_shared, eval_handle);


  // MAIN EVAL
  // See: https://man7.org/linux/man-pages/man3/dlclose.3p.html

  printf("main_program END\n");

  return 0; // TODO: return 1 on error?
}

int clean_up() {
  // for(size_t i = 0; i < len(context.runtime_entries); i++)

  RuntimeEntry** runtime_entries = context->runtime_entries;

  for(size_t i = 0; i < arrlen(runtime_entries); i++) {
    RuntimeEntry* runtime_entry = runtime_entries[i];

    printf("Unloading dl_name %s\n", runtime_entry->dl_name);

    unload_all_dl_ref(runtime_entry->dl_name, runtime_entry->dl_handle);

    free(runtime_entry->dl_name);
    arrfree(runtime_entry->vars);

    free(runtime_entry);

  }

  arrfree(runtime_entries);

  free(context);
  // Dangling Ptr
  context = NULL;

  return 0;

}
