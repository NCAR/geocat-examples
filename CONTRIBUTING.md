Porting NCL example scripts to Python
=====================================
0. Fork and clone this repository and create a conda environment containing all of the software necessary to build this examples gallery webpage: [installation instructions](INSTALLATION.md)

   Note that this repository uses a "git submodule" to store its data files in a separate GitHub repository. This submodule can be checked out as part of the clone process by using the `--recursive` flag:
```
git clone --recursive https://github.com/NCAR/GeoCAT-examples
```

   If you've already cloned the repository without the `--recursive` flag, you'll need to run the following command to clone the `data` submodule directory:
```
git submodule update --init
```

   If you ever notice that a file exists in the [GeoCAT-datafiles](https://github.com/NCAR/geocat-datafiles) repository, but it does not seem to exist in your local `data` subdirectory, please try running the following command to sync the contents of the submodule:
```
git submodule update --remote
git add data
git commit -m "Update data submodule tracking to latest commit"
```

1. Check the list of [Issues](https://github.com/NCAR/GeoCAT-examples/issues) for this repository to see if any of the existing to-do items are something you might be interested in working on. If so, please comment (or self-assign the issue if you have permissions to do so) indicating that you intend to work on it.

   Alternatively, if you are interested in porting a script that is not listed as an [issue](https://github.com/NCAR/GeoCAT-examples/issues), please check the `Plots` directory of this repository to ensure that the example you are about to work on has not been ported yet.

   For reference, NCL scripts to be ported can be found on the [NCL documentation website](http://ncl.ucar.edu/Applications/).

2. Determine if any critical NCL computational functions are missing. If so, please submit a new issue (or comment on an existing issue) on this repository's GitHub page containing the script name and function name, select a new NCL script, and start this process over.

3. Determine if any data files needed by your script are available in the [geocat-datafiles](https://github.com/NCAR/GeoCAT-datafiles) repository (which is included as a "git submodule" in this repository under the path `data`). If not, please submit a new issue (or comment on an existing issue) on this repository's GitHub page containing the name of the missing datafile(s).

4. Create a new Python script using the original NCL script's basename, but prepended with "NCL_". For example:
    `new_script_1.ncl` becomes `NCL_new_script_1.py`

    * Note that `template_script.py` at the root of this repository is a great starting point for a new script, so you may want to consider copying that to `NCL_new_script_1.py` instead of starting from scratch.


5. The general objective of this project is to identify any NCL plotting functionality that is missing from the popular Matplotlib + Cartopy toolchain, so each contributed script should contain a best-effort attempt at reproducing an NCL graphic as closely as possible without using NCL or PyNGL. In the future, PyNGL examples may be included in this repository as well, but the current goal is to see what *can't* be done with Matplotlib and Cartopy.

   That said, if you identify any NCL functionality in particular that does not seem to exist in Matplotlib/Cartopy, please create an issue on this repository's GitHub page with a link to the original NCL example page and list any NCL functions whose functionality is missing from Python.

6. When you have completed an example script, please try building the sphinx documentation from this repository using "make html" from the repository's root directory. Then open the HTML file located at `_build/html/auto_examples/index.html` and try to find your new example, ensuring that any output (text or graphical) matches what you expected.

7. Submit an Pull Request on this repository's GitHub page containing your new example. Please add a link to the original NCL script from the NCL documentation site. Also, please consider adding a brief summary of your experience porting the script. If it was easy, say so; if it was very hacky and required 7 times as many lines of code as the NCL script, please say that.
