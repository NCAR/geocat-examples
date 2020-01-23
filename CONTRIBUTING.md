Porting NCL example scripts to Python
=====================================
0. Clone this repository and create a conda environment containing all of the software necessary to build this examples gallery webpage: [installation instructions](INSTALLATION.md)

1. Select an NCL script from the NCL documentation website: http://ncl.ucar.edu/Applications/

   Check the `Plots` directory of this repository to ensure the example you are about to work on has not been ported yet.

2. Determine if any critical NCL computational functions are missing. If so, please submit an issue on this repository's GitHub page containing the script name and function name, select a new NCL script, and start this process over.

3. Create a new Python script using the original NCL script's basename, but prepended with "NCL_". For example:
    `new_script_1.ncl` becomes `NCL_new_script_1.py`

    * Note that `template_script.py` at the root of this repository is a great starting point for a new script, so you may want to consider copying that to `NCL_new_script_1.py` instead of starting from scratch.


4. The general objective of this project is to identify any NCL plotting functionality that is missing from the popular Matplotlib + Cartopy toolchain, so each contributed script should contain a best-effort attempt at reproducing an NCL graphic as closely as possible without using NCL or PyNGL. In the future, PyNGL examples may be included in this repository as well, but the current goal is to see what *can't* be done with Matplotlib and Cartopy.

   That said, if you identify any NCL functionality in particular that does not seem to exist in Matplotlib/Cartopy, please create an issue on this repository's GitHub page with a link to the original NCL example page and list any NCL functions whose functionality is missing from Python.

5. When you have completed an example script, please try building the sphinx documentation from this repository using "make html" from the repository's root directory. Then open the HTML file located at `_build/html/auto_examples/index.html` and try to find your new example, ensuring that any output (text or graphical) matches what you expected.

6. Submit an Pull Request on this repository's GitHub page containing your new example. Please add a link to the original NCL script from the NCL documentation site. Also, please consider adding a brief summary of your experience porting the script. If it was easy, say so; if it was very hacky and required 7 times as many lines of code as the NCL script, please say that.

https://github.com/Unidata/python-training/blob/master/pages/contributing.md
