import os
import subprocess

from translator import Translator, Config
from rbxpy import check_pyright

def dotests():
    tests_folder = "tests/"
    out_folder = tests_folder + "out/"
    luau_runner = "lune" # https://github.com/lune-org/lune

    def testfile(fp):
        with open(fp, "r") as f:
            py = f.read()

            include_std = True
            export = True
            useRequire = False
            isLune = True

            translator = Translator(Config(".robloxpy.json"), show_ast=True)
            luau = translator.translate(
                py, include_std, False, export, False, useRequire, None,
                isLune
            )

            assert luau != None

            base, _ = os.path.splitext(fp)
            out_path = out_folder + os.path.basename(base) + ".luau"

            with open(out_path, "w") as of:
                of.write(luau)
            
            subprocess.run([luau_runner, "run", out_path], check=True)

    passed = 0
    failed = 0

    for root, dirs, files in os.walk(tests_folder):
        for f in files:
            fp = os.path.join(root, f)
            if 'out' in fp:
                break

            try:
                testfile(fp)
                passed += 1
                print(f"{fp}: PASS")
            except Exception as e:
                failed += 1
                print(f"{fp}: FAIL:\n{e}")

    print(f"{passed} PASS, {failed} FAIL")