> **Warning**
>    This version of the gallery uses experimental features from [geocat-viz](https://github.com/NCAR/geocat-viz>). We advise against using this version of the gallery to learn how to make visualizations, as it will be minimally maintained for plotting accuracy. However, we still want to provide it as a sneak peak for the GeoCAT user community. To see the latest stable version of the gallery, switch to the `main` branch.

Please first refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for overall
contribution guidelines (such as detailed description of GeoCAT structure, forking, repository cloning,
branching, etc.). Once you determine that a function should be contributed under this repo, please refer to the
following contribution guidelines:


# Adding new plotting scripts to the Geocat-examples repo

1. Please check the followings to ensure that the example you are about to work on has not been ported yet:

    - [GeoCAT-Examples Gallery](https://geocat-examples.readthedocs.io/en/latest/) or
    the `Gallery` as well as `GeoCAT-comp-examples` directories of this repo,

    - The list of [Issues](https://github.com/NCAR/GeoCAT-examples/issues) for this repo to see if any of
    the existing to-do items are something you might be interested in working on.

        - If so, please comment (or self-assign the issue if you have permissions to do so) indicating that
        you intend to work on it.

        - Otherwise, you may create and self-assign an issue that describes need for the plot you are planning
        to contribute.

    - For reference, NCL scripts can be seen as well: [NCL applications](http://ncl.ucar.edu/Applications/).

2. Determine if any critical computational functions are missing.

    - If so, please submit a new issue (or comment on an existing issue) on this repository's GitHub page
    containing the script name and explanation of the need for computational function(s).

3. Determine if any data files needed by your script are available in the
[GeoCAT-datafiles](https://github.com/NCAR/GeoCAT-datafiles) repo:

    - If not,

        - Submit a new issue (or comment on an existing issue) on this repository's GitHub page containing
        the name of the missing datafile(s), or

        - Check [GeoCAT-datafiles contributing documentation](https://github.com/NCAR/geocat-datafiles/blob/contribuotr_updates/CONTRIBUTING.md)
        to see if you can contribute to the [GeoCAT-datafiles](https://github.com/NCAR/geocat-datafiles) by
        uploading your own file.

4. Create a new Python script:

    - [template_script.py](https://github.com/NCAR/GeoCAT-examples/blob/master/template_script.py)
    (at the root of this repo) could be a great starting point for a new script, so you may want to
    consider copying that to `NCL_new_script_1.py` instead of starting from scratch.

    - If this script originates from an NCL example, use the original NCL script's basename,
     but prepended with "NCL_". For example: `new_script_1.ncl` becomes `NCL_new_script_1.py`.

5. When you complete an example script, please try building the
[Sphinx](https://www.sphinx-doc.org/en/master/)-generated documentation (i.e. html files)
from this repo by running the following commands from within the `/docs` directory:

   ```bash
   make html
   ```

   - This is particularly important to see the final look of a plotting example on
   [GeoCAT-Examples Gallery](https://geocat-examples.readthedocs.io) as varying IDEs or local development set up of
   developers preferences would generate different plotting results from each other.

   - Note: Please follow the [installation instructions](https://github.com/NCAR/geocat-examples/INSTALLATION.md)
   beforehand to ensure an accurate conda environment is installed and activated for GeoCAT-examples, including
   [Sphinx](https://www.sphinx-doc.org/en/master/).

   - The generated HTML file can be viewed under `$GEOCAT_EXAMPLES/_build/html/gallery/` to ensure that
   any output (text or graphical) matches what you expected. The complete list of the plotting examples can be
   viewed by running the following command as well:

     ```bash
     open _build/html/gallery/index.html
     ```
