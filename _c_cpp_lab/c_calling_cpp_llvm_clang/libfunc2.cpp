
#include <iostream>

#include <stdio.h>

#include <vector>
#include <initializer_list>

#include <memory>

/*

// NOTE: AVOID LIBRARIES THAT USE SYSTEM-LEVEL GLOBALS SUCH AS IOSTREAM AS VALGRIND MARKS THEM AS "STILL REACHABLE"
// SO TO REDUCE THE POSSIBLITY OF ANY SECURITY RISKS, USE printf and similar
// USING LIBRARIES THAT DON'T RELY ON GLOBAL STREAM OBJECTS ALSO SIMLIFIES DEBUGGING, ETC.
still reachable: 84,961 bytes in 18 blocks
HOWEVER, WE HAVE TO LIVE WITH THIS EITHER WAY AS THE USAGE OF OPERATOR DELETE ENFORCES THE INVOLVEMENT OF SOME GLOBAL OBJECTS.
SO THE WAY TO CALCULATE THE MEMORY LEAKS WILL BE:
 = default_base_global_memory_allocated_reachable_bytes - current_memory_reachable_bytes
*/


class MyClass {
  public:
  int i {0};

  MyClass() {
    printf("MyClass()\n");
  }

  ~MyClass() {
    printf("~MyClass()\n");
  }
};

class S {
  public:
  std::unique_ptr<MyClass> v;

  S() {
    v = std::unique_ptr<MyClass>(new MyClass());
  }

  void modify(const int i) { 
    printf("S::modify\n");

    MyClass* m = v.get();

    m->i = i;
  }

};

extern "C" {

  S* s = nullptr;

  void my_init() {
    printf("%s my_init() called.\n", __FILE__);

    s = new S();
  }


  void my_handle() {
    printf("%s my_handle() called.\n", __FILE__);

    s->modify(1);
  }

  void method_string(const char* s) {
    std::cout << "method_string() " << s << std::endl;
  }


  void my_clean_up() {
    printf("%s my_clean_up() called.\n", __FILE__);

    // s->~S();
    // ::operator delete(s);
    // s = nullptr;

    delete s;
    s = nullptr;
  }




}
