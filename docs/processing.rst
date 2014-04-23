Asset compilers and processors
==============================

The asset building process consists of multiple steps. At it's simplest,
only the directives are processed and dependencies are included into the
build files. The build process can do much more though, like compiling
less files with lessjs or compressing js files with uglifyjs.

Each build follows these fives steps that can be customized for your
environment.

1. Preprocess
2. Compile
3. Postprocess
4. Compress
5. Save to filesystem


1. Preprocess
-------------

The first step is where dependencies are managed. Gears looks for
directives within assets and includes them within the asset file. As
explained elsewhere, directives are simple comments in the header of
script or css files. For example::

    /*
     *= require jquery
     *= require underscore
     *= require backbone
    */

It's not common to change the preprocess step, but if you wish to do
so, this can be done by modifying the :setting:`GEARS_PREPROCESSORS`
setting.


2. Compile
----------

The second step compiles source files like CoffeeScript, Stylus, or Less
into javascript and css. Compilers are defined in the
:setting:`GEARS_COMPILERS` setting.

Various compilers are just a ``pip`` install away. You can browse plugins
that are available at the `Gears repositories github page`_. If you find
a compiler not supported, it's easy to create a plugin of your own.


3. Postprocess
--------------

The third step is where files are postprocessed. By default, Django Gears
runs the ``gears.processors.HexdigestPathsProcessor`` for css files. This
processor replaces ``url`` declarations in the css with fingerprinted
versions. Note, this processor only works if all paths in ``url``
declarations refer to local files.

The post processors can be modified with the :setting:`GEARS_POSTPROCESSORS`
setting.


4. Compress
-----------

The fourth step is where tools like SlimIt, UglifyJS, or clean-css are run.
These produce minified files and minimize bandwidth requirements.

For users of Python 2.X, Gears has built-in support for SlimIt and cssmin.

Other compilers are just a ``pip`` install away. You can browse plugins
that are available at the `Gears repositories github page`_.


5. Save to filesystem
---------------------

The fifth step is where processed files are saved to the file system.
The destination directory is controlled by the :setting:`GEARS_ROOT`
setting.

Unless :setting:`GEARS_FINGERPRINTING` is set to false, the asset will be
fingerprinted and added to the ``.manifest.json`` file.

During this step, the file can optionally be gzipped. This is controlled
by the :setting:`GEARS_GZIP` setting.


.. _gears repositories github page: https://github.com/gears/
