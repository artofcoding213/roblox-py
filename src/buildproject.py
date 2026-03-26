# writes all py files & dirs in src/ to out/
import os
import subprocess
import sys
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

build_lock = threading.Lock()

from translator import *
from rbxpy import check_pyright
from log import error

def splitpath(path):
    parts = []
    while True:
        path, tail = os.path.split(path)
        if tail:
            parts.append(tail)
        else:
            if path:
                parts.append(path)
            break
    return parts[::-1]

def joinpath(parts):
    return os.path.join(*parts)

def _buildfile(path: str):
    if not os.path.isfile(path):
        return
    
    _, ext = os.path.splitext(path)
    if ext != ".py":
        return
    
    lua_code: str | None = None
    with open(path, "r") as f:
        py = f.read()
        pyright = check_pyright()
        if pyright:
            def check():
                os.environ["PYRIGHT_PYTHON_FORCE_VERSION"] = "latest"
                success = (
                    subprocess.Popen(["pyright", path]).wait() == 0
                )

                if not success:
                    print(
                        "-----------------------------------------------------"
                    )
                    error("compilation failed")
                    sys.exit(1)

            threading.Thread(target=check, daemon=True).start()

        includeSTD = False
        export = True
        useRequire = False

        translator = Translator(Config(".robloxpy.json"), show_ast=ast)
        lua_code = translator.translate(
            py, includeSTD, False, export, False, useRequire, pyright
        )

    assert lua_code != None

    p = splitpath(path)
    if p[0] == 'src':
        p[0] = 'out'

    dirs = p.copy()
    dirs.pop()
    os.makedirs(joinpath(dirs), exist_ok=True)

    name = p[-1]
    base, ext = os.path.splitext(name)
    if base == "__init__":
        base = "init"

    p[-1] = base + ".luau"

    with open(joinpath(p), "w") as f:
        f.write(lua_code)

def buildfile(path: str):
    with build_lock:
        _buildfile(path)

def builddir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)

            print(f"build {fp}")
            buildfile(fp)

# the stuff below here is AI slop lol i did NOT want to figure out how to implement this

def src_to_out(path: str):
    p = splitpath(path)
    if not p:
        return None

    if p[0] == "src":
        p[0] = "out"

    if len(p) == 0:
        return None

    # change extension
    name = p[-1]
    base, ext = os.path.splitext(name)
    if ext != ".py":
        return None

    p[-1] = base + ".luau"
    return joinpath(p)

last_build = {}

def should_build(path, delay=0.2):
    now = time.time()
    if path in last_build and now - last_build[path] < delay:
        return False
    last_build[path] = now
    return True

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"create {event.src_path}")
        buildfile(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        
        if not should_build(event.src_path):
            return

        print(f"modify {event.src_path}")
        buildfile(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return

        out = src_to_out(event.src_path)
        if out and os.path.exists(out):
            print(f"[DELETE] {out}")
            os.remove(out)

    def on_moved(self, event):
        if event.is_directory:
            return

        old_out = src_to_out(event.src_path)
        new_out = src_to_out(event.dest_path)

        # delete old
        if old_out and os.path.exists(old_out):
            print(f"move-del {old_out}")
            os.remove(old_out)

        # rebuild new
        print(f"move-build {event.dest_path}")
        buildfile(event.dest_path)


def buildproject():
    builddir("src")

def watch():
    observer = Observer()
    handler = Handler()

    observer.schedule(handler, "src", recursive=True)
    observer.start()

    print("watching src/ ...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()