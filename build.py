#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin
from pybuilder.core import init
from pybuilder.core import Author

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin('python.install_dependencies')
use_plugin("python.flake8")
use_plugin("python.coverage")
# use_plugin("python.distutils")


name = 'pybuilder-radon'
authors = [
    Author('Emilio Reyes', 'soda480@gmail.com')
]
summary = 'Pybuilder plugin for radon'
url = 'https://github.com/soda480/pybuilder-radon'
version = '0.0.1'
default_task = [
    'clean',
    'analyze'
]
license = 'Apache License, Version 2.0'
description = summary


@init
def set_properties(project):
    project.set_property('unittest_module_glob', 'test_*.py')
    project.set_property('coverage_break_build', False)
    project.set_property('flake8_max_line_length', 120)
    project.set_property('flake8_verbose_output', True)
    project.set_property('flake8_break_build', True)
    project.set_property('flake8_include_scripts', True)
    project.set_property('flake8_include_test_sources', True)
    # project.set_property('flake8_ignore', 'E501, W503, F401')
    project.build_depends_on_requirements('requirements-build.txt')
    project.depends_on_requirements('requirements.txt')
    # project.set_property('distutils_readme_description', True)
    # project.set_property('distutils_description_overwrite', True)
    # project.set_property('distutils_upload_skip_existing', True)
