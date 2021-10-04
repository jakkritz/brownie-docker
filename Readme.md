# Brownie Macos Fix
```sh
vim /root/.local/pipx/venvs/eth-brownie/lib/python3.9/site-packages/brownie/project/scripts.py
```
- replace _import_from_path method in above file.
```py
def _import_from_path(path: Path) -> ModuleType:
    # Imports a module from the given path
    
    import_str = "/" + "/".join(path.parts[1:-1] + (path.stem,))+'.py'
    
    if import_str in _import_cache:
        importlib.reload(_import_cache[import_str])
    else:
        spec = importlib.util.spec_from_file_location('.'+path.stem,import_str)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _import_cache[import_str] = module
    return _import_cache[import_str]
```