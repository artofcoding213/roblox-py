from translator import Translator, Config
import os
import subprocess

def repline():
    py = input(">>> ")
    luau_runner = "lune"
    tmp_file = "robloxpyrepltmp.luau"

    include_std = True
    export = True
    useRequire = False
    isLune = True

    translator = Translator(Config(".robloxpy.json"), show_ast=False)
    luau = translator.translate(
        py, include_std, False, export, False, useRequire, None,
        isLune
    )

    assert luau != None

    with open(tmp_file, "w") as f:
        f.write(luau)
        subprocess.run([luau_runner, "run", tmp_file])

    os.remove(tmp_file)

def repl():
    try:
        while True:
            try:
                repline()
            except Exception as e:
                print(f"repl error: {e}")
    except KeyboardInterrupt:
        pass