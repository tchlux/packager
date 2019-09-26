<p align="center">
  <h1 align="center">packager</h1>
</p>

An easy way to create and manage a `pip` Python package.

## INSTALLATION:

```bash
pip install git+https://github.com/tchlux/packager.git
```

## USAGE:

### Python

```python
import packager  
packager.create(<path_to_project>)
packager.push(<path_to_project>)
```

  Descriptions of the `create` and `push` functions follow.

### Command line

```bash
python -m packager <project> [create] [push] [push comments]
```

  Manage a python package project at provided directory.

  If `create` is specified, a project is initialized with
  default files for a package managed by this module.

  If `push` is specified, a git (and pypi if declared) update
  cycle is initiated. This includes a commit to the repository,
  version update, packaging, and commit to the PyPi servers.

## HOW IT WORKS:

  This module uses itself as a template to initialize a project
  directory, taking only the desired name to make necessary
  modifications to the internals of this project.

  When creating a push to PyPI, the following steps are taken:
  - The directory is cleaned of unnecessary files (.pyc, __pycache__)
  - The `version_history.md` file in the `about` directory is updated with the commit message.
  - A `MANIFEST.in` file is created specifying all files in the repository, to ensure all files are included on install.
  - Git commands `add *`, `commit -a`, and `push` are all executed.
  - Git commands `tag -a <version> -m <notes>` and `push --tags <package` are executed.
  - The `setup.py` file is executed with `sdist` argument to create a distribution.
  - `twine` is used to upload the distribution to PyPI.
  - All extra files created from the package build are deleted.
