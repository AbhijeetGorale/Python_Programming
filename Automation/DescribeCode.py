#!/usr/bin/env python3
"""
Code Explainer
--------------
Accepts a source file (.c, .cpp, .java, or .py) and prints a
line-by-line, plain-English explanation of what the code does.

Usage:
    python explain_code.py <filename>
    (or just run it and enter the filename when prompted)
"""

import os
import re
import sys


# --------------------------------------------------------------------
# 1. Language detection
# --------------------------------------------------------------------
def detect_language(filename):
    ext = os.path.splitext(filename)[1].lower()
    mapping = {
        ".c": "C",
        ".cpp": "C++",
        ".cc": "C++",
        ".cxx": "C++",
        ".h": "C/C++ header",
        ".hpp": "C++ header",
        ".java": "Java",
        ".py": "Python",
    }
    return mapping.get(ext, None)


# --------------------------------------------------------------------
# 2. Explanation rules
#    Each rule = (regex pattern, function that builds explanation text)
# --------------------------------------------------------------------
BRACE_LANG_RULES = [
    (r'^\s*#\s*include\s*[<"](.+)[>"]', lambda m: f"Includes the '{m.group(1)}' library so its functions can be used."),
    (r'^\s*import\s+(.+);', lambda m: f"Imports the '{m.group(1).strip()}' package/class."),
    (r'^\s*package\s+(.+);', lambda m: f"Declares that this file belongs to the '{m.group(1)}' package."),
    (r'^\s*//(.*)', lambda m: f"Comment: {m.group(1).strip()}"),
    (r'^\s*/\*(.*)', lambda m: f"Start of a block comment: {m.group(1).strip()}"),
    (r'.*\*/\s*$', lambda m: "End of block comment."),
    (r'^\s*(public\s+|private\s+|protected\s+)?(static\s+)?(final\s+)?class\s+(\w+)', 
        lambda m: f"Defines a class named '{m.group(4)}'."),
    (r'^\s*struct\s+(\w+)', lambda m: f"Defines a structure named '{m.group(1)}' to group related data."),
    (r'^\s*typedef\s+(.+);', lambda m: f"Creates a type alias: {m.group(1).strip()}."),
    (r'^\s*(public\s+|private\s+|protected\s+)?(static\s+)?\w[\w<>\[\]]*\s+main\s*\(', 
        lambda m: "This is the main function — the program's entry point; execution starts here."),
    (r'^\s*(public\s+|private\s+|protected\s+)?(static\s+)?(final\s+)?[\w<>\[\],\s]+?\s+(?!if\b|for\b|while\b|switch\b|else\b|return\b|do\b|catch\b)(\w+)\s*\([^;]*\)\s*\{?\s*$',
        lambda m: f"Defines a function/method named '{m.group(4)}'."),
    (r'^\s*for\s*\((.*)\)', lambda m: f"A 'for' loop — repeats a block of code based on: {m.group(1).strip()}."),
    (r'^\s*while\s*\((.*)\)', lambda m: f"A 'while' loop — repeats as long as the condition ({m.group(1).strip()}) is true."),
    (r'^\s*do\s*\{', lambda m: "Start of a 'do-while' loop — the block runs at least once before checking the condition."),
    (r'^\s*if\s*\((.*)\)', lambda m: f"An 'if' condition checks: {m.group(1).strip()}."),
    (r'^\s*else\s+if\s*\((.*)\)', lambda m: f"An 'else if' branch checks: {m.group(1).strip()}."),
    (r'^\s*else\b', lambda m: "The 'else' branch — runs when the earlier condition(s) were false."),
    (r'^\s*switch\s*\((.*)\)', lambda m: f"A 'switch' statement branches based on the value of: {m.group(1).strip()}."),
    (r'^\s*case\s+(.+):', lambda m: f"Case for when the switch value equals {m.group(1).strip()}."),
    (r'^\s*break;', lambda m: "Breaks out of the current loop or switch statement."),
    (r'^\s*continue;', lambda m: "Skips to the next iteration of the loop."),
    (r'^\s*return\s*(.*);', lambda m: f"Returns {m.group(1).strip() if m.group(1).strip() else 'from the function (no value)'} to the caller."),
    (r'^\s*(int|float|double|char|long|short|unsigned|bool|BOOL)\s+\**\s*\w+\s*(\[\s*\d*\s*\])?\s*(=\s*(.+))?;',
        lambda m: f"Declares a variable" + (f" and initializes it to {m.group(4).strip()}." if m.group(4) else ".")),
    (r'^\s*malloc\s*\(', lambda m: "Allocates a block of memory dynamically (heap memory)."),
    (r'\bfree\s*\(', lambda m: "Frees previously allocated dynamic memory."),
    (r'^\s*printf\s*\(', lambda m: "Prints formatted output to the console (C)."),
    (r'^\s*scanf\s*\(', lambda m: "Reads formatted input from the user (C). Remember: variables need '&' unless they're pointers/arrays."),
    (r'std::cout\s*<<|^\s*cout\s*<<', lambda m: "Prints output to the console (C++)."),
    (r'std::cin\s*>>|^\s*cin\s*>>', lambda m: "Reads input from the user (C++)."),
    (r'System\.out\.println?\s*\(', lambda m: "Prints output to the console (Java)."),
    (r'Scanner\s*\(', lambda m: "Creates a Scanner object to read user input (Java)."),
    (r'^\s*\w+\s*=\s*.+;', lambda m: "Assigns a new value to a variable."),
    (r'&\s*\w+', lambda m: None),  # placeholder, avoid duplicate matches
    (r'.*[&|^~]{1}.*;', lambda m: "Performs a bitwise operation (AND '&', OR '|', XOR '^', NOT '~', or shifts)."),
]

PYTHON_RULES = [
    (r'^\s*#(.*)', lambda m: f"Comment: {m.group(1).strip()}"),
    (r'^\s*import\s+(.+)', lambda m: f"Imports the '{m.group(1).strip()}' module."),
    (r'^\s*from\s+(\S+)\s+import\s+(.+)', lambda m: f"Imports {m.group(2).strip()} from the '{m.group(1)}' module."),
    (r'^\s*def\s+(\w+)\s*\((.*)\)\s*:', lambda m: f"Defines a function named '{m.group(1)}'" + (f" that takes parameters: {m.group(2)}." if m.group(2).strip() else " with no parameters.")),
    (r'^\s*class\s+(\w+)', lambda m: f"Defines a class named '{m.group(1)}'."),
    (r'^\s*if\s+(.*):', lambda m: f"An 'if' condition checks: {m.group(1).strip()}."),
    (r'^\s*elif\s+(.*):', lambda m: f"An 'elif' branch checks: {m.group(1).strip()}."),
    (r'^\s*else\s*:', lambda m: "The 'else' branch — runs when earlier conditions were false."),
    (r'^\s*for\s+(\w+)\s+in\s+(.*):', lambda m: f"A 'for' loop — iterates variable '{m.group(1)}' over: {m.group(2).strip()}."),
    (r'^\s*while\s+(.*):', lambda m: f"A 'while' loop — repeats as long as: {m.group(1).strip()}."),
    (r'^\s*return\s*(.*)', lambda m: f"Returns {m.group(1).strip() if m.group(1).strip() else '(nothing)'} to the caller."),
    (r'^\s*print\s*\(', lambda m: "Prints output to the console."),
    (r'^\s*try\s*:', lambda m: "Starts a 'try' block to catch potential errors."),
    (r'^\s*except(.*):', lambda m: f"Catches an exception: {m.group(1).strip() if m.group(1).strip() else '(any error)'}."),
    (r'^\s*with\s+(.*):', lambda m: f"Opens a managed context (e.g. a file): {m.group(1).strip()}."),
    (r'^\s*\w+\s*=\s*.+', lambda m: "Assigns a value to a variable."),
]


def explain_line(line, language):
    rules = PYTHON_RULES if language == "Python" else BRACE_LANG_RULES
    for pattern, builder in rules:
        m = re.search(pattern, line)
        if m:
            result = builder(m)
            if result:
                return result
    stripped = line.strip()
    if stripped in ("{", "}"):
        return "Marks the start/end of a code block."
    if stripped == "":
        return None
    return None  # no rule matched


# --------------------------------------------------------------------
# 2b. "Under the hood" deep-dive notes
#     These explain the underlying mechanics (memory, execution,
#     bit-level behavior) so students see WHY something works,
#     not just WHAT it does. Multiple notes can apply to one line.
# --------------------------------------------------------------------
def deep_dive(line, language):
    notes = []
    l = line.strip()

    if re.search(r'[^=!<>]&[^&=]', l) or re.search(r'&=', l):
        notes.append("Bitwise AND (&): compares each bit of both operands. A result bit is 1 only if BOTH "
                      "corresponding bits are 1. Commonly used to check or 'mask' specific bits (e.g. n & 1 checks the last bit).")
    if re.search(r'[^|]\|[^|=]', l) or re.search(r'\|=', l):
        notes.append("Bitwise OR (|): a result bit is 1 if EITHER corresponding bit is 1. Often used to 'set' a "
                      "specific bit to 1 without disturbing other bits.")
    if re.search(r'\^', l):
        notes.append("Bitwise XOR (^): a result bit is 1 only if the two corresponding bits are DIFFERENT. Used to "
                      "'toggle' bits (flip 0->1 or 1->0), and to compare bit patterns for equality (result 0 = identical).")
    if re.search(r'~', l):
        notes.append("Bitwise NOT (~): flips every bit — every 0 becomes 1 and every 1 becomes 0. Often combined "
                      "with '&' to clear a specific bit (n & ~mask).")
    if re.search(r'<<', l):
        notes.append("Left shift (<<): moves every bit left by n positions, filling with 0s on the right. Equivalent "
                      "to multiplying by 2^n, and the standard way to build a mask for bit position n (1 << n).")
    if re.search(r'>>', l):
        notes.append("Right shift (>>): moves every bit right by n positions. Equivalent to dividing by 2^n (for "
                      "unsigned/positive values). Used to 'read' a bit at a given position after masking.")

    if language in ("C", "C++") and re.search(r'\*\s*\w+', l) and 'printf' not in l and '/*' not in l:
        notes.append("The '*' here relates to a pointer: a variable that stores a memory ADDRESS rather than a "
                      "direct value. Dereferencing (*ptr) means 'go to that address and get/set the value stored there'.")
    if re.search(r'&\w+', l) and language in ("C", "C++"):
        notes.append("The '&' here means 'address-of' — it gets the memory address where a variable is stored "
                      "(this is why scanf needs &variable: it needs the address to write the input INTO, not the value).")

    if re.search(r'\bmalloc\s*\(', l) or re.search(r'\bcalloc\s*\(', l):
        notes.append("This allocates memory on the HEAP (not the stack). Heap memory persists until you explicitly "
                      "call free() — unlike local variables, which are destroyed automatically when the function returns.")
    if re.search(r'\bfree\s*\(', l):
        notes.append("Releases heap memory back to the system. Forgetting this causes a 'memory leak'; using the "
                      "pointer again after this is a 'dangling pointer' bug.")
    if language in ("C", "C++") and re.search(r'^\s*(int|float|double|char|long|short|unsigned|bool|BOOL)\s+\w+', l) and 'return' not in l:
        notes.append("This variable is created on the STACK — fast, automatically-managed memory that is reclaimed "
                      "the moment the function it belongs to returns.")

    if re.search(r'\[\s*\d*\s*\]', l) and language != "Python":
        notes.append("Arrays are stored as one CONTIGUOUS block of memory. Indexing starts at 0, so an array of "
                      "size N has valid indices 0 through N-1 — going beyond that reads/writes memory you don't own (undefined behavior).")

    if re.search(r'^\s*for\s*\(', l) and language != "Python":
        notes.append("Execution order inside for(init; condition; update): 1) init runs once, 2) condition is "
                      "checked — if false, the loop ends immediately, 3) if true, the body runs, 4) update runs, then it jumps back to step 2.")
    if re.search(r'^\s*for\s+\w+\s+in\s+', l) and language == "Python":
        notes.append("Python's for-loop pulls one item at a time from the iterable (list, range, string, etc.) and "
                      "binds it to the loop variable until the iterable is exhausted — no manual counter/condition to manage.")
    if re.search(r'^\s*while\s*[\(:]', l):
        notes.append("The condition is re-checked EVERY time before the loop body runs. If it's false the very "
                      "first time, the body never executes at all.")

    if re.search(r'^\s*(public|private|protected|static).*\(.*\)\s*\{?\s*$', l) or re.search(r'^\s*\w[\w<>\[\],\s]*\s+\w+\s*\([^;]*\)\s*\{\s*$', l):
        if language != "Python":
            notes.append("Calling this function pushes a new 'stack frame' onto the call stack, holding its local "
                          "variables and parameters. When it returns, that frame is popped and control resumes where it was called from.")

    if re.search(r'&&', l):
        notes.append("Logical AND (&&) short-circuits: if the left condition is false, the right side is never "
                      "even evaluated, since the overall result is already guaranteed false.")
    if re.search(r'\|\|', l):
        notes.append("Logical OR (||) short-circuits: if the left condition is true, the right side is never "
                      "evaluated, since the overall result is already guaranteed true.")

    return notes


# --------------------------------------------------------------------
# 3. Main driver
# --------------------------------------------------------------------
def explain_file(filename):
    language = detect_language(filename)
    if language is None:
        print(f"Sorry, I don't recognize the file type of '{filename}'.")
        print("Supported extensions: .c, .cpp, .cc, .h, .hpp, .java, .py")
        return

    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    print("=" * 70)
    print(f"File: {filename}")
    print(f"Detected language: {language}")
    print(f"Total lines: {len(lines)}")
    print("=" * 70)

    for i, raw_line in enumerate(lines, start=1):
        stripped = raw_line.rstrip("\n")
        if stripped.strip() == "":
            continue
        explanation = explain_line(stripped, language)
        notes = deep_dive(stripped, language)
        print(f"\nLine {i}: {stripped.strip()}")
        if explanation:
            print(f"   -> WHAT: {explanation}")
        else:
            print("   -> WHAT: (statement / expression, no specific rule matched)")
        for note in notes:
            print(f"   -> UNDER THE HOOD: {note}")

    print("\n" + "=" * 70)
    print("End of explanation.")
    print("=" * 70)


def main():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        filename = input("Enter the path/name of the .c, .cpp, .java or .py file: ").strip()

    explain_file(filename)


if __name__ == "__main__":
    main()