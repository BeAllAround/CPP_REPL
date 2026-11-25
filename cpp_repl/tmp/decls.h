#ifndef DL_DECLS

#define DL_DECLS

#include <stddef.h>

#include <stdint.h>

#include <stdio.h>

#include <stdlib.h>


#include <string.h>

#include <assert.h>

#include <dlfcn.h>


#define STB_DS_IMPLEMENTATION
#include "stb_ds.h"

// #undef STB_DS_IMPLEMENTATION

#define decl_assign_var(type, var_index, value) ({type v = vars[var_index] = (type)malloc(sizeof(type)); *v = value; })
#define decl_var(type, var_index) ({type v = vars[var_index] = (type)malloc(sizeof(type)); })

#define deref_var(cast_type, context, inx) ( *(cast_type((context->runtime_entries[inx])->vars[0])) )


#define cast(type, ptr) ((type)(ptr))


#define assertm(msg, exp) assert((exp) && msg)


#define ATTACH_CONTEXT(dest_context, src_context) (*((Context**)dest_context)) = (src_context)

typedef struct {
  void* dl_handle;
  char* dl_name;
  void** vars;
} RuntimeEntry;

typedef struct {
  RuntimeEntry** runtime_entries;

} Context;


RuntimeEntry* makeRuntimeEntry(char* dl_name, void* dl_handle) {
  RuntimeEntry* runtime_entry = malloc(sizeof(RuntimeEntry));

  runtime_entry->dl_name = dl_name;
  runtime_entry->dl_handle = dl_handle;

  runtime_entry->vars = NULL; // malloc(sizeof(void*) * 10); // FIXED LEN FOR TESTING

  // SET DEFAULT ARRAY CAPACITY
  // For vars, the capacity is always 1 as we resolve one symbol per dl handle
  arrsetcap(runtime_entry->vars, 10);

  return runtime_entry;
}

Context makeContext() {
  Context context = {};

  context.runtime_entries = NULL; // malloc(sizeof(RuntimeEntry*) * 10); // FIXED LEN FOR TESTING

  // SET DEFAULT ARRAY CAPACITY
  arrsetcap(context.runtime_entries, 10);

  return context;
}




#endif
