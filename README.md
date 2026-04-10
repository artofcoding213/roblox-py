## roblox-py <i>(artofcoding213's fork)</i>

.py -> .luau transpiler\
this is a fork of [roblox-compilers/roblox-py](https://github.com/roblox-compilers/roblox-py), notably adding:
- class inheritence (w/ `super()`, proper `issubclass()` & `isinstance()` impls)
- `luau()` macro
- kwargs support! (including `**` operator)
- proper Rojo support for `client`, `server`, & `shared` import targets (this includes `from [...] import *`)
- matrix multiplication operator (`@`)
- walrus operator or named expression (`:=`)
- slicing
- a **LOT** of bug fixes including:
  - generators
  - list comprehensions
  - lists
  - etc...

## original [roblox-py](https://github.com/roblox-compilers/roblox-py) contributors
(thank you for your amazing work, this project saved me so much time!)

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AsynchronousAI"><img src="https://avatars.githubusercontent.com/u/72946059?v=4?s=100" width="100px;" alt="aqzp"/><br /><sub><b>aqzp</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/commits?author=AsynchronousAI" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tututuana"><img src="https://avatars.githubusercontent.com/u/51187395?v=4?s=100" width="100px;" alt="tututuana"/><br /><sub><b>tututuana</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/commits?author=tututuana" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/BazirGames"><img src="https://avatars.githubusercontent.com/u/49544193?v=4?s=100" width="100px;" alt="BazirGames"/><br /><sub><b>BazirGames</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/issues?q=author%3ABazirGames" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://lawmixerscpf.tk/group"><img src="https://avatars.githubusercontent.com/u/53837083?v=4?s=100" width="100px;" alt="LawMixer"/><br /><sub><b>LawMixer</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/issues?q=author%3ALawMixer" title="Bug reports">🐛</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cataclysmic-dev"><img src="https://avatars.githubusercontent.com/u/141081747?v=4?s=100" width="100px;" alt="cataclysmic-dev"/><br /><sub><b>cataclysmic-dev</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/commits?author=cataclysmic-dev" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/luxkatana"><img src="https://avatars.githubusercontent.com/u/57036931?v=4?s=100" width="100px;" alt="luxkatana"/><br /><sub><b>luxkatana</b></sub></a><br /><a href="https://github.com/AsynchronousAI/roblox-pyc/issues?q=author%3Aluxkatana" title="Bug reports">🐛</a></td>
    </tr>
  </tbody>
</table>

## latest commit
> 4/10/26 (MM/DD/YY)

fix:
- `in` keyword not working on lists (tests passed because there were numbers in lists and it did [key] ~= nil)
- `isinstance()` throwing on non-class values

add:
- for-loop list expansion for list comprehensions
- forced opt-in to `--!native`

## using lune
this repo **requires** [`lune`](https://github.com/lune-org/lune) installed to use *some* features:
- `roblox-py test` run test cases
- `roblox-py repl` type in py code to run (translates it to luau then runs it)
> note: you can configure your Luau executor of choice in some variables in the code,
> i should use config files but these are very niche features

[`lune`](https://github.com/lune-org/lune) is a Luau executor capable of executing Luau code\
it has standard library functions that map exactly to roblox luau (i.e. `task.spawn()`)\
we do have to have *some* headers 

## working with rojo
we work exactly like roblox-ts!

### building a python project
`roblox-py build`

> note: python files are a LocalScript if they end in `.client.py` and a Server (Script?)
> if they end in `.server.py`. otherwise, they are a `ModuleScript`

required folders:
```
src/
  [PY_CODE HERE]
```
we output all code to `out/`. note that files in `out/` are never destroyed with `build`,
you may have to remove them manually

outputs to:
```
out/
  [LUAU_CODE_HERE]
```

### watching a python project
`roblox-py watch`\
this watches for file saves, moves, deletions, etc.\
this is the only superset of `build` that can delete files in `out/`, but only if you
subsequently delete a file in `src/`

in a nutshell, it just calls `roblox-py build` every time you change something in `src/`

</div>
