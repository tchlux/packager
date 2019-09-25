import sys, os
from . import DIRECTORY, create, push

# Function for printing the help message.
def print_help_message():
    print("""

packager -- An easy way to create and manage a `pip` Python package.

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

    """)

# If no arguments were provided, give the usage.
if len(sys.argv) <= 2:
    print_help_message()
    exit()

# Get the project directory in absolute path.
project = os.path.abspath(sys.argv[1])

# Create the project
if "create" in sys.argv:
    create(project)
# Perform a push operation.
elif "push" in sys.argv:
    # Pop out the package name from the command line argument list.
    sys.argv.pop(1)
    # Pop out the "push" command from the command line argument list.
    sys.argv.pop(sys.argv.index("push"))
    # Remove that extra "dry_run" argument if necessary.
    dry_run = ("-test" in sys.argv)
    if dry_run: sys.argv.pop(sys.argv.index("-test"))
    # Execut the push.
    push(project, dry_run=dry_run)
# Improper usage.
else:
    print_help_message()

