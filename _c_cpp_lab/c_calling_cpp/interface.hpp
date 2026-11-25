#ifndef INTERFACE_HPP
#define INTERFACE_HPP

class MyInterface {
public:
    virtual ~MyInterface() = default;
    virtual void do_something() = 0;
};

#endif
