"""Python to lua translator class"""

import ast
import sys
from config import Config
from nodevisitor import NodeVisitor
from log import error
from const import HEADER
from lib import *
import lib

DEPEND = lib.DEPENDENCY


class Translator:
    """Python to lua main class translator"""

    def __init__(self, config=None, show_ast=False):
        self.config = config if config is not None else Config()
        self.show_ast = show_ast

        self.output = []

    @staticmethod
    def reset_dependencies():
        global DEPEND
        DEPEND = lib.DEPENDENCY
    def translate(
        self,
        pycode,
        fn,
        isAPI=False,
        export=True,
        reqfile=False,
        useRequire=False,
        pyRight=False,
        isLune=False,
    ):
        """Translate python code to lua code"""
        Translator.reset_dependencies()

        loc_header = ""
        lune_header = ""

        global DEPEND
        if isLune:
            DEPEND = ""
            lune_header = "-- lune header:\nlocal task = require('@lune/task')\n--end\n"

        if not reqfile:
            if isAPI:
                py_ast_tree = ast.parse(pycode)
            else:
                try:
                    # code that uses ast
                    py_ast_tree = ast.parse(pycode)
                except SyntaxError as err:
                    sys.stderr.write(
                        "\033[1;31m" + "syntax error: " + "\033[0m" + str(err) + "\n"
                    )
                    sys.exit(1)

            visitor = NodeVisitor(config=self.config)
            visitor.exports = [] # i dunno why this works but it makes sure we don't try to export like a class we removed from the original source code
            visitor.tl_decls = [] # same issue with this one... weird

            if self.show_ast:
                print(ast.dump(py_ast_tree))

            visitor.visit(py_ast_tree)

            for tl in visitor.get_tldecls():
                loc_header += f"local {tl};"

            loc_header += "\n"

            self.output = visitor.output

            # Remove duplicates from dependencies (list)
            dependencies = list(set(visitor.get_dependencies()))

            exports = list(set(visitor.get_exports()))

            if fn:
                dependencies.append("fn")
            if export and len(exports) > 0:
                FOOTER = "\n\n--> exports\n"
                FOOTER += 'if (script ~= nil) and (not script:IsA("BaseScript")) then\n\treturn {\n'
                for export in exports:
                    FOOTER += f'\t\t["{export}"] = {export},\n'
                FOOTER += "\t}\nend"
            else:
                FOOTER = ""

        if reqfile:
            dependencies = [
                "class",
                "dict",
                "kwargs",
                "fn",
                "complex",
            ]
            DEPEND = ""
        if not useRequire:
            for depend in dependencies:
                if depend == "complex":
                    DEPEND += COMPLEX
                elif depend == "dict":
                    DEPEND += DICT
                elif depend == "class":
                    DEPEND += CLASS
                elif depend == "fn":
                    DEPEND += FN
                elif depend == "generator":
                    DEPEND += GENERATOR
                elif depend == "kwargs":
                    DEPEND += KWARGS
                elif depend == "maths":
                    DEPEND += MATHS
                elif depend == "overloads":
                    DEPEND += OVERLOADS
                else:
                    error(
                        "Auto-generated dependency unhandled '{}', please report this issue on Discord or Github".format(
                            depend
                        )
                    )

        if reqfile:
            allDepends = ""
            for depend in lib.libs:
                allDepends += f'["{depend}"] = {depend},'
            DEPEND += "\n\nreturn {" + allDepends + "}\n"
            return DEPEND

        CODE = self.to_code()
        ERRS = "\n\n--> error handling\n"

        for i in errs:
            if ("error(" + i + "(") in CODE:
                ERRS += f"""function {i}(errorMessage)
    return ("[roblox-py] {i}: " .. errorMessage)
end
"""

        if not isLune:
            for i in lib.libs:
                if i in CODE:
                    DEPEND += f"\n{i} = py.{i}"

        DEPEND += "\n\n--> code start\n"

        return lune_header + HEADER + ERRS + DEPEND + loc_header + CODE + FOOTER

    def to_code(self, code=None, indent=0):
        """Create a lua code from the compiler output"""
        code = code if code is not None else self.output

        def add_indentation(line):
            """Add indentation to the given line"""
            indentation_width = 4
            indentation_space = " "

            indent_copy = max(indent, 0)

            return indentation_space * indentation_width * indent_copy + line

        lines = []
        for line in code:
            if isinstance(line, str):
                lines.append(add_indentation(line))
            elif isinstance(line, list):
                sub_code = self.to_code(line, indent + 1)
                lines.append(sub_code)

        return "\n".join(lines)

    @staticmethod
    def get_luainit():  # Return STDlib
        return """"""
