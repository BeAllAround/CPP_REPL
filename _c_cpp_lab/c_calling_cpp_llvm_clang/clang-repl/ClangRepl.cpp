
//===--- tools/clang-repl/ClangRepl.cpp - clang-repl - the Clang REPL -----===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
//  This file implements a REPL tool on top of clang.
//
//===----------------------------------------------------------------------===//

#include "clang/Basic/Diagnostic.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Frontend/FrontendDiagnostic.h"
#include "clang/Interpreter/CodeCompletion.h"
#include "clang/Interpreter/Interpreter.h"
#include "clang/Lex/Preprocessor.h"
#include "clang/Sema/Sema.h"

#include "clang/Frontend/TextDiagnosticPrinter.h"



#include "llvm/ExecutionEngine/Orc/LLJIT.h"
#include "llvm/LineEditor/LineEditor.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/ManagedStatic.h" // llvm_shutdown
#include "llvm/Support/Signals.h"
#include "llvm/Support/TargetSelect.h"

#include "llvm/ExecutionEngine/Orc/ExecutionUtils.h"


#include <iostream>
#include <vector>
#include <optional>


// Disable LSan for this test.
// FIXME: Re-enable once we can assume GCC 13.2 or higher.
// https://llvm.org/github.com/llvm/llvm-project/issues/67586.
#if LLVM_ADDRESS_SANITIZER_BUILD || LLVM_HWADDRESS_SANITIZER_BUILD
#include <sanitizer/lsan_interface.h>
LLVM_ATTRIBUTE_USED int __lsan_is_turned_off() { return 1; }
#endif



static void LLVMErrorHandler(void *UserData, const char *Message,
                             bool GenCrashDiag) {
  
  std::cout << "START: LLVMErrorHandler" << std::endl;
  auto &Diags = *static_cast<clang::DiagnosticsEngine *>(UserData);

  Diags.Report(clang::diag::err_fe_error_backend) << Message;

  // Run the interrupt handlers to make sure any special cleanups get done, in
  // particular that we remove files registered with RemoveFileOnSignal.
  llvm::sys::RunInterruptHandlers();

  // We cannot recover from llvm errors.  When reporting a fatal error, exit
  // with status 70 to generate crash diagnostics.  For BSD systems this is
  // defined as an internal software error. Otherwise, exit with status 1.

  exit(GenCrashDiag ? 70 : 1);
}

// If we are running with -verify a reported has to be returned as unsuccess.
// This is relevant especially for the test suite.
static int checkDiagErrors(const clang::CompilerInstance *CI, bool HasError) {
  unsigned Errs = CI->getDiagnostics().getClient()->getNumErrors();
  if (CI->getDiagnosticOpts().VerifyDiagnostics) {
    // If there was an error that came from the verifier we must return 1 as
    // an exit code for the process. This will make the test fail as expected.
    clang::DiagnosticConsumer *Client = CI->getDiagnostics().getClient();
    Client->EndSourceFile();
    Errs = Client->getNumErrors();

    // The interpreter expects BeginSourceFile/EndSourceFiles to be balanced.
    Client->BeginSourceFile(CI->getLangOpts(), &CI->getPreprocessor());
  }
  return (Errs || HasError) ? EXIT_FAILURE : EXIT_SUCCESS;
}

/*

struct ReplListCompleter {
  clang::IncrementalCompilerBuilder &CB;
  clang::Interpreter &MainInterp;
  ReplListCompleter(clang::IncrementalCompilerBuilder &CB,
                    clang::Interpreter &Interp)
      : CB(CB), MainInterp(Interp){};

  std::vector<llvm::LineEditor::Completion> operator()(llvm::StringRef Buffer,
                                                       size_t Pos) const;
  std::vector<llvm::LineEditor::Completion>
  operator()(llvm::StringRef Buffer, size_t Pos, llvm::Error &ErrRes) const;
};

std::vector<llvm::LineEditor::Completion>
ReplListCompleter::operator()(llvm::StringRef Buffer, size_t Pos) const {
  auto Err = llvm::Error::success();
  auto res = (*this)(Buffer, Pos, Err);
  if (Err)
    llvm::logAllUnhandledErrors(std::move(Err), llvm::errs(), "error: ");
  return res;
}

std::vector<llvm::LineEditor::Completion>
ReplListCompleter::operator()(llvm::StringRef Buffer, size_t Pos,
                              llvm::Error &ErrRes) const {
  std::vector<llvm::LineEditor::Completion> Comps;
  std::vector<std::string> Results;

  auto CI = CB.CreateCpp();
  if (auto Err = CI.takeError()) {
    ErrRes = std::move(Err);
    return {};
  }

  size_t Lines =
      std::count(Buffer.begin(), std::next(Buffer.begin(), Pos), '\n') + 1;
  auto Interp = clang::Interpreter::create(std::move(*CI));

  if (auto Err = Interp.takeError()) {
    // log the error and returns an empty vector;
    ErrRes = std::move(Err);

    return {};
  }
  auto *MainCI = (*Interp)->getCompilerInstance();
  auto CC = clang::ReplCodeCompleter();
  CC.codeComplete(MainCI, Buffer, Lines, Pos + 1,
                  MainInterp.getCompilerInstance(), Results);
  for (auto c : Results) {
    if (c.find(CC.Prefix) == 0)
      Comps.push_back(
          llvm::LineEditor::Completion(c.substr(CC.Prefix.size()), c));
  }
  return Comps;
}
*/



// See: https://clang.llvm.org/doxygen/CompilerInstance_8cpp_source.html and search for "createDiagnostics" and "getDiagnosticOpts"
// See:
// - https://clang.llvm.org/doxygen/classclang_1_1TextDiagnosticPrinter.html
// - https://clang.llvm.org/doxygen/classclang_1_1DiagnosticOptions.html
// - https://clang.llvm.org/doxygen/TextDiagnosticPrinter_8cpp_source.html
class MyCustomDiagConsumer : public clang::TextDiagnosticPrinter {
public:

    MyCustomDiagConsumer(clang::DiagnosticOptions &Opts) : TextDiagnosticPrinter(llvm::errs(), &Opts) {
    }

    void HandleDiagnostic(clang::DiagnosticsEngine::Level DiagLevel,
                          const clang::Diagnostic &Info) override {

        // Call the default handler to keep standard behavior
        TextDiagnosticPrinter::HandleDiagnostic(DiagLevel, Info);

    }

    void clear() override {
      Msgs.clear();
      Errors.clear();
      TextDiagnosticPrinter::clear();
    }

    std::vector<llvm::SmallString<32>> Msgs;
    std::vector<llvm::SmallString<32>> Errors;
};


/*
class MyCustomDiagConsumer : public clang::DiagnosticConsumer {
public:
    MyCustomDiagConsumer(clang::DiagnosticOptions &Opts) {
    }

    void HandleDiagnostic(clang::DiagnosticsEngine::Level DiagLevel,
                          const clang::Diagnostic &Info) override {

        // Optionally call the default handler to keep standard behavior
        // DiagnosticConsumer::HandleDiagnostic(DiagLevel, Info);
        // const auto& OS = llvm::errs();
        // std::cout << OS.tell() << std::endl;


        // Info.getLocation();
        // Info.getRanges();
        // Info.getFixItHints();
        // FullSourceLoc(Info.getLocation(), Info.getSourceManager())

        llvm::SmallString<100> OutStr;
        Info.FormatDiagnostic(OutStr);



        if (DiagLevel >= clang::DiagnosticsEngine::Error) {
            std::cerr << "Parser/Compiler Error: " << OutStr.str().str() << "\n";
        }
        else if(DiagLevel == clang::DiagnosticsEngine::Warning) {
            std::cout << "Parser/Compiler Warning: " << OutStr.str().str() << "\n";
        }
    }

    void clear() override {
      Msgs.clear();
      Errors.clear();
      DiagnosticConsumer::clear();
    }

    std::vector<llvm::SmallString<32>> Msgs;
    std::vector<llvm::SmallString<32>> Errors;
};
*/

void logLLVMError(llvm::Error&& err, const std::string& err_message = "logLLVMError: ") {
   llvm::logAllUnhandledErrors(std::move(err), llvm::errs(), err_message);
}

// TODO: READ THE DOCS ON THIS ONE
llvm::ExitOnError ExitOnErr;

// clang::Interpreter: https://clang.llvm.org/doxygen/Interpreter_8cpp_source.html

// https://github.com/llvm/llvm-project/blob/main/clang/lib/Frontend/CompilerInstance.cpp

// https://llvm.org/docs/CommandLine.html

// https://clang.llvm.org/docs/RAVFrontendAction.html, https://clang.llvm.org/doxygen/structclang_1_1PartialTranslationUnit.html

// https://clang.llvm.org/doxygen/classclang_1_1TranslationUnitDecl.html

// Class Hierarchy: https://clang.llvm.org/doxygen/inherits.html, https://clang.llvm.org/doxygen/dir_7c3366c0dfc05dfe1380b9a1e2bf7190.html

// TODO: LLVM DOCS: TODO: Building a JIT: Remote-JITing – Process Isolation and Laziness at a Distance


/*
// AST Visiting and Dumping
* https://clang.llvm.org/docs/LibClang.html
* https://clang.llvm.org/docs/RAVFrontendAction.html
* https://clang.llvm.org/doxygen/classclang_1_1CompilerInstance.html
* https://clang.llvm.org/doxygen/classclang_1_1CompilerInstance.html#a5283524cfb9615ef55e431892684dce0
* https://clang.llvm.org/doxygen/classclang_1_1RecursiveASTVisitor.html
* https://stackoverflow.com/questions/71318084/how-visitnameddecl-and-visitcxxrecorddecl-are-called-by-recursiveastvisitor
*/

std::string getASTString(const clang::PartialTranslationUnit &PTU) {
  std::string ASTString;
  llvm::raw_string_ostream OS(ASTString);
  
  if (PTU.TUPart != nullptr) {
    // Dump the TranslationUnitDecl and its children to the stream
    PTU.TUPart->dump(OS);
  }
  
  return OS.str();
}


// Pointer Globals
// clang::CompilerInstance* CI = nullptr;
clang::IncrementalCompilerBuilder* CB = nullptr;
clang::Interpreter* Interp = nullptr;

std::vector<const char *>* ClangArgv = nullptr;

extern "C" {

int setUp() {

  ExitOnErr.setBanner("clang-repl: ");

  // NOTE: NOT NEEDED AS THIS "TRANSINIONS/FORWARDS" LLVM COMMANDS ONTO OUR MAIN PROGRAM
  // llvm::cl::ParseCommandLineOptions(argc, argv);

  // llvm::llvm_shutdown_obj Y; // Call llvm_shutdown() on exit.

  // Set Default Commands
  ClangArgv = new std::vector<const char *>({
    "-O0",
    "--gcc-install-dir=/usr/lib/gcc/x86_64-linux-gnu/14",
    "--std=c++17",
    // "-emit-llvm",
  });


  {
    // Initialize all targets (required for device offloading)
    llvm::InitializeAllTargetInfos();
    llvm::InitializeAllTargets();
    llvm::InitializeAllTargetMCs();
    llvm::InitializeAllAsmPrinters();
  }

  CB = new clang::IncrementalCompilerBuilder();

  CB->SetCompilerArgs(*ClangArgv);


  // FIXME: Investigate if we could use runToolOnCodeWithArgs from tooling. It
  // can replace the boilerplate code for creation of the compiler instance.
  std::unique_ptr<clang::CompilerInstance> _CI = ExitOnErr(CB->CreateCpp());


  // Set an error handler, so that any LLVM backend diagnostics go through our
  // error handler.
  // TODO:
  llvm::install_fatal_error_handler(LLVMErrorHandler,
                                    static_cast<void *>(&_CI->getDiagnostics()));
  // Load any requested plugins.
  _CI->LoadRequestedPlugins();
  _CI->createDiagnostics(new MyCustomDiagConsumer(_CI->getDiagnosticOpts()), /*ShouldOwnClient=*/true);

  // _CI->createDiagnostics(); // Default


  std::unique_ptr<clang::Interpreter> _Interp = ExitOnErr(clang::Interpreter::create(std::move(_CI)));
  /*
{
    auto EE = _Interp->getExecutionEngine();
    if (EE) {
      std::cout << "EEEEEE" << std::endl;
      auto Generator =
          llvm::orc::DynamicLibrarySearchGenerator::GetForCurrentProcess(
              EE->getDataLayout().getGlobalPrefix());

      if (!Generator) {
        llvm::logAllUnhandledErrors(Generator.takeError(), llvm::errs(),
                                    "Failed to create symbol generator: ");
        exit(0);
      } else {
        EE->getMainJITDylib().addGenerator(std::move(*Generator));
      }
    }
  }
  */

  
  // Ready to release once these are used and are no further required
  {
    Interp = _Interp.release();
  }

  /*
  for (const std::string &input : OptInputs) {
    if (auto Err = Interp->ParseAndExecute(input))
      llvm::logAllUnhandledErrors(std::move(Err), llvm::errs(), "error: ");
  }
  */


  // Create The Executor
  // if(auto err = Interp->CreateExecutor()) { // 'CreateExecutor' is a private member of 'clang::Interpreter'
  //  logLLVMError(std::move(err));
  // }

  clang::CompilerInstance* compilerinstance = Interp->getCompilerInstance();

  bool HasError = false;

  std::initializer_list<const char*> includes = {
    "#include <iostream>",
    "#include <vector>",
  };

  for(const char* include : includes) {
    llvm::Error Err = Interp->ParseAndExecute(include);

    if(Err) {
      llvm::logAllUnhandledErrors(std::move(Err), llvm::errs(), "my error format: ");
      return 1;
    }
  }

  #ifdef CPP_REPL_VERBOSE
  std::cout << "SETUP DONE" << std::endl;
  #endif


  return 0;

}


int parseAndExecute(const char* input) {
    std::string Input = input;

    llvm::Expected<clang::PartialTranslationUnit&> translation_unit = Interp->Parse(Input); 
    // auto Err = Interp->ParseAndExecute(Input); 

    if(auto E = translation_unit.takeError()) {
      llvm::logAllUnhandledErrors(std::move(E), llvm::errs(), "my error format: ");
      return 1;
    } else {
      // std::cout << getASTString(translation_unit.get()) << std::endl;
      llvm::Error Err = Interp->Execute(translation_unit.get());
    }
    /*
    if(Err) {
      llvm::logAllUnhandledErrors(std::move(Err), llvm::errs(), "my error format: ");
      HasError = true;
    }
    */

    return 0;
}

}

/*
int main(int argc, const char **argv) {

    setUp();


  // TODO: Handle Err


    llvm::LineEditor LE("");
    std::string Input;

    // LE.setListCompleter(ReplListCompleter(CB, *Interp));


    while (std::optional<std::string> Line = LE.readLine()) {
      llvm::StringRef L = *Line;
      L = L.trim();
      if (L.ends_with("\\")) {
        // FIXME: Support #ifdef X \ ...
        Input += L.drop_back(1);
        LE.setPrompt("clang-repl...   ");
        continue;
      }

      Input += L;

      parseAndExecute(Input.c_str());



      Input = "";
      // LE.setPrompt("clang-repl> ");
    }

  // Our error handler depends on the Diagnostics object, which we're
  // potentially about to delete. Uninstall the handler now so that any
  // later errors use the default handling behavior instead.
  
  // llvm::remove_fatal_error_handler();

  // return checkDiagErrors(Interp->getCompilerInstance(), HasError);
  return 0;
}
*/
