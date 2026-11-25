#include <iostream>
#include <typeinfo>
#include <memory>
#include <string>

// Include cxxabi.h only for GCC/Clang compilers
// #ifndef _MSC_VER
#include <cxxabi.h>
// #endif

struct MyClass {};

std::string demangle(const char* mangled_name) {
    std::cout << mangled_name << std::endl;

    int status = 0;
    // abi::__cxa_demangle allocates memory via malloc
    std::unique_ptr<char, void(*)(void*)> demangled(
        abi::__cxa_demangle(mangled_name, nullptr, nullptr, &status),
        std::free
    );
    
    // status == 0 means successful demangling
    if(status == 0) {
      return demangled.get(); 
    }
   
    return  mangled_name;
}

template<typename T>
void print_type(const T& var) {
    std::cout << demangle(typeid(var).name()) << "\n";
}

int main() {
    std::string text = "Hello";
    int i = 1;

    MyClass my_class;

    print_type(text); // Prints: std::string (or its full std::__cxx11... template instantiation)
                      //
    print_type(i);
    print_type(my_class);

    return 0;
}
