cmake_minimum_required(VERSION 3.16)


# NOTE: DISCOURGED FOR PORTABILITY REASONS!
# gcc, g++
set(CMAKE_C_COMPILER "gcc") # "clang"
set(CMAKE_CXX_COMPILER "g++") # "clang++"

project(MyProject)

find_package(LLVM REQUIRED CONFIG)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")


set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Disable RTTI and exceptions
add_compile_options(-fno-rtti -fno-exceptions)

# Get llvm-config flags
# execute_process(
	#    COMMAND llvm-config-18 --cxxflags
    #    OUTPUT_VARIABLE LLVM_CXXFLAGS
    #    OUTPUT_STRIP_TRAILING_WHITESPACE
    #)

#execute_process(
	#    COMMAND llvm-config-18 --ldflags --libs
    #    OUTPUT_VARIABLE LLVM_LDFLAGS
    #    OUTPUT_STRIP_TRAILING_WHITESPACE
    #)

# execute_process(
#    COMMAND llvm-config-18 --libs all
#    OUTPUT_VARIABLE LLVM_ALL_LIBS
#    OUTPUT_STRIP_TRAILING_WHITESPACE
#)

# string(STRIP "${MY_LIBRARIES}" LLVM_ALL_LIBS_STRIPPED)
# string(STRIP "${LLVM_LDFLAGS}" LLVM_LDFLAGS_STRIPPED)


message(STATUS "LLMV_INCLUDE_DIRS ${LLVM_INCLUDE_DIRS}")
message(STATUS "LLVM DEFINITIONS ${LLVM_DEFINITIONS}")
message(STATUS "LLMV_LIBRARY_DIRS ${LLVM_LIBRARY_DIRS}")
message(STATUS "LLVM_TARGETS_TO_BUILD ${LLVM_TARGETS_TO_BUILD}")
message(STATUS "LLVM_LINK_COMPONENTS ${LLVM_LINK_COMPONENTS}")


# Convert flags into lists
# separate_arguments(LLVM_CXXFLAGS)
# separate_arguments(LLVM_LDFLAGS)
# separate_arguments(LLVM_ALL_LIBS_STRIPPED)

add_executable(out.out ClangRepl.cpp)

# Include directories
target_include_directories(out.out PRIVATE ${LLVM_INCLUDE_DIRS})

# Apply compile flags
# target_compile_options(out.out PRIVATE ${LLVM_CXXFLAGS})

# Link directories
# link_directories(/usr/lib/llvm-18/lib)

target_link_directories(out.out PRIVATE ${LLVM_LIBRARY_DIRS})


# NOTE THAT THE CLANG++ COMPILATION BREAKS WITH GNU/GCC 16 LIBRARIES GIVEN THAT CLANG PICKS THE LATEST VERSION ON YOUR SYSTEM
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --gcc-install-dir=/usr/lib/gcc/x86_64-linux-gnu/14")

# Link libraries
target_link_libraries(out.out PRIVATE
    LLVM-18
    clangBasic
    clangFrontend
    clangAST
    clangInterpreter
    clang-cpp
)
