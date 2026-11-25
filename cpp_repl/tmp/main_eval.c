
        #include <decls.h>

        void _main_eval(Context* context) {
            
        {
            void* eval_handle = dlopen("././c_repl/tmp/a.so", RTLD_LOCAL | RTLD_LAZY);
            RuntimeEntry* runtime_entry = makeRuntimeEntry(strdup("././c_repl/tmp/a.so"), eval_handle);

            runtime_entry->vars[0] = dlsym(eval_handle, "a");

            arrpush(context->runtime_entries, runtime_entry);
        }
        
        }
        