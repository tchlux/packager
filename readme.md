|             |                |
|-------------|----------------|
|**TITLE:**   | packager       |
|**PURPOSE:** | An easy way to create and manage a `pip` Python package. |
|**AUTHOR:**  | Thomas C.H. Lux  |
|**EMAIL:**   | thomas.ch.lux@gmail.com |


## INSTALLATION:

    $ pip install git+https://github.com/tchlux/packager.git
%    $ pip install https://github.com/tchlux/template/archive/0.0.0.zip

## USAGE:

### Python

    > import packager  
    > packager.create(<path_to_project>)
    > packager.push(<path_to_project>)

  Descriptions of the `create` and `push` functions follow.

### Command line

    $ python -m packager <project> [create] [push] [push comments]

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


## VERSION HISTORY:


## UPCOMING

- [x] Make this project even more usable.
- [ ] Think more about this project.

### Known Bugs

- [ ] Find all the bugs.

### Usability Issues

- [ ] Make it all more usable.

### Staged Improvements

- [ ] Come up with improvements.
