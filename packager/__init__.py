# Get the version number from the setup file
import os

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ABOUT_DIR = os.path.join(DIRECTORY, "about")
__version__ = open(os.path.join(ABOUT_DIR,"version.txt")).read().strip()


# Function for creating a project.
def create(project):
    import shutil
    src = os.path.dirname(DIRECTORY)
    print("Copying '"+src+"' to '"+project+"'.")
    shutil.copytree(src, project)
    project_name = os.path.basename(project)
    shutil.move(os.path.join(project, "packager"),
                os.path.join(project, project_name))
    # Write a file called "package_name.txt" to have the name of the package.
    with open(os.path.join(project, "package_name.txt"),"w") as f:
        print(project_name, file=f)

# Function for pushing an update of a package.
def push(package_path, dry_run=False, clean_before=True, clean_after=None,
         manifest=True, manifest_exclude=(".git", ".gitignore"),
         update_history=None, git_commit=None, git_release=None,
         pypi_build=None, pypi_release=None):
    import os, sys, datetime, subprocess

    class MissingAbout(Exception): pass
    class CommandError(Exception): pass
    class MissingProject(Exception): pass
    class NotEnoughArguments(Exception): pass

    # Check to make sure the project exists.
    if not os.path.exists(package_path):
        raise(MissingProject("No project exists at '"+package_path+"'."))

    # Change directories into the package.
    starting_dir = os.curdir
    os.chdir(package_path)
    # Construct the name of the package and locate it's about directory.
    package = os.path.basename(package_path)
    package_about = os.path.join(package_path, package, "about")
    if not os.path.exists(package_about):
        raise(MissingAbout("The directory '"+package_about+"' must exist."))

    # Function for reading about information from this packages
    # "about" file. It is defined here so "package" can be inferred.
    def read(f_name, processed=True, empty_lines=False):
        text = []
        with open(os.path.join(package_about, f_name)) as f:
            if processed:
                for line in f:
                    line = line.strip("\n")
                    if (not empty_lines) and (len(line.strip()) == 0): continue
                    if (len(line) > 0) and (line[0] == "%"): continue
                    text.append(line)
            else:
                text = f.read()
        return text

    # Execute a blocking command with a subprocess, raise errors if any
    # are encountered, otherwiser print standard output and return. This
    # should work across both Python2.7 and Python3.x as well as cross-platform.
    #  INPUT:
    #   command -- A list of strings or string (space separated) describing
    #              a standard command as would be given to subprocess.Popen
    def run(command, **popen_kwargs):
        print("  $", " ".join(command))
        # For Python3.x ensure that the outputs are strings
        if sys.version_info >= (3,6):
            popen_kwargs.update( dict(encoding="UTF-8") )
        # print("'%s'"%(" ".join(command)))
        # return
        proc = subprocess.Popen(command, cwd=package_path, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, **popen_kwargs)
        stdout, stderr = proc.communicate()
        if stdout: stdout = stdout.replace("\r","").split("\n")
        else:      stdout = ""
        if stderr: stderr = stderr.replace("\r","").split("\n")
        else:      stderr = ""
        if (proc.returncode != 0) or (len(stderr) > 0):
            raise(CommandError("\n\n%s"%("\n".join(stderr))))
        elif (len(stdout) > 0):
            print("\n".join(stdout))

    # Infer the unprovided parameters based on whether or not this is
    # a dry run of the "push" operation.
    if (type(update_history) == type(None)):
        update_history = not dry_run
    if (type(git_commit) == type(None)):
        git_commit = not dry_run
    if (type(git_release) == type(None)):
        git_release = not dry_run
    if (type(pypi_build) == type(None)):
        pypi_build = ("t" in read("on_pypi.txt")[0].lower())
    if (type(pypi_release) == type(None)):
        pypi_release = pypi_build and (not dry_run)

    # Get the version of this package.
    version = read("version.txt")[0]

    if clean_before:
        #      Remove all of the wheel generated files     
        # =================================================
        dist_dir = os.path.join(package_path,"dist")
        build_dir = os.path.join(package_path, "build")
        egg_file = os.path.join(package_path, )
        run(["rm", "-rf", "dist", "build", package+".egg-info"])
        # Remove any pyc files that are hidden away     
        run(["find", ".", "-name", '*.pyc', "-delete"])
        run(["find", ".", "-name", '__pycache__', "-delete"])

    if (update_history or git_commit or git_release):
        # Make sure the user provided the correct number of arguments
        if len(sys.argv) >= 2:
            notes = sys.argv[1]
        else:
            raise(NotEnoughArguments("Provide update notes as command line argument."))

    if update_history:
        #     Update the history with the notes for this update     
        # ==========================================================
        max_comment_length = 52
        formatted_comment = notes.split()
        start = 0
        curr = 1
        while (curr < len(formatted_comment)):
            if len(" ".join(formatted_comment[start:curr+1])) > max_comment_length:
                formatted_comment.insert(curr, "<br>")
                start = curr+1
            curr += 1
        formatted_comment = " ".join(formatted_comment)

        # Get the month and the year to add to the "updates" record.
        month = datetime.datetime.now().strftime("%B")
        year = datetime.datetime.now().strftime("%Y")
        time = version +"<br>"+ month +" "+ year

        # Update the version history file
        with open(os.path.join(package_about,"version_history.md"), "a") as f:
            print("| %s | %s |"%(time, formatted_comment), file=f)


    # Generate an all-inclusive manifest
    if manifest:
        with open(os.path.join(package_path,"MANIFEST.in"), "w") as f:
            for name in os.listdir(package_path):
                if name not in manifest_exclude:
                    if os.path.isdir(name):
                        print("recursive-include",name,"*", file=f)
                    else:
                        print("include",name, file=f)

    if git_commit:
        #      Upload current version with git     
        # =========================================
        run(["git", "add", "*"])
        run(["git", "commit", "-a", "-m", notes])
        run(["git", "push", "origin", "master"])

    if git_release:
        #      Upload to github with version tag     
        # ===========================================
        run(["git", "tag", "-a", version, "-m", notes])
        run(["git", "push", "--tags", package])

    if pypi_build:
        #      Setup the python package as a universal wheel     
        # =======================================================
        run([sys.executable, "setup.py", "sdist"])
        # run([sys.executable, "setup.py", "bdist_wheel"])

        #      Remove any pyc files that are hidden away     
        # ===================================================
        run(["find", ".", "-name", '*.pyc', "-delete"])
        run(["find", ".", "-name", '__pycache__', "-delete"])

    if pypi_release:
        #      Use twine to upload the package to PyPI     
        # =================================================
        run(["twine", "upload", "dist/*"])

    if clean_after:
        #      Remove all of the wheel generated files     
        # =================================================
        run(["rm", "-rf", "dist", "build", package+".egg-info", "MANIFEST.in"])

    # Update the version file so the next will not conflict
    if not dry_run:
        next_version = list(map(int,version.split(".")))
        next_version[-1] += 1
        with open(os.path.join(package_about,"version.txt"), "w") as f:
            print(".".join(list(map(str,next_version))), file=f)


    # Change directories back to the starting directory.
    os.chdir(starting_dir)