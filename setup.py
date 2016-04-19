# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python Dataflow SDK and Worker setup configuration."""

import os
import re
import setuptools

# Currently all compiled modules are optional  (for performance only).
# Cython is available on the workers, but we don't require it for development.
try:
  # pylint: disable=g-statement-before-imports,g-import-not-at-top
  from Cython.Build import cythonize
except ImportError:
  cythonize = lambda *args, **kwargs: []


# Configure the required packages and scripts to install.
REQUIRED_PACKAGES = [
    'dill>=0.2.5',
    'google-apitools>=0.5.2',
    # TODO(silviuc): Reenable api client package dependencies when we can
    # update the packages to the latest version without affecting previous
    # SDK releases.
    # 'google-apitools-bigquery-v2',
    # 'google-apitools-dataflow-v1b3>=0.4.20160217',
    # 'google-apitools-storage-v1',
    'httplib2>=0.8',
    'mock>=1.0.1',
    'oauth2client>=2.0.1',
    'protorpc>=0.9.1',
    'python-gflags>=2.0',
    'pyyaml>=3.10',
    ]

CONSOLE_SCRIPTS = [
    ]


def get_dataflow_version():
  global_names = {}
  execfile(os.path.normpath('./google/cloud/dataflow/version.py'),
           global_names)
  return global_names['__version__']


def get_dataflow_docstring():
  """Get docstring for Dataflow module and give it an rST title."""
  init_file_path = os.path.normpath('./google/cloud/dataflow/__init__.py')
  try:
    with open(init_file_path, 'r') as init_file:
      init_file_contents = init_file.read()
  except IOError:
    return None
  doc_match = re.search(r'"""(.*)"""', init_file_contents, flags=re.DOTALL)
  if not doc_match:
    return None
  docstring = doc_match.group(1).rstrip()
  title_match = re.match(r'(.*)\.\n\n', docstring)
  if title_match:
    # A module docstring has a first line that ends with a period and has a
    # blank line after it.  reStructuredText, the format used by setuptools
    # (and other Python API documentation tools), wants no trailing period
    # and a highlighting line of equal signs under the title line.
    # Convert by removing the period and adding a highlighting line.
    equalsigns_fill_format = '\n{:=^%d}\n' % title_match.end(1)
    title_underline = equalsigns_fill_format.format('=')
    docstring = re.sub(r'\.\n', title_underline, docstring, count=1)
  return docstring


_PYTHON_DATAFLOW_VERSION = get_dataflow_version()


def get_download_url():
  """Calculate a permanent download URL for this version."""
  return ('https://github.com/GoogleCloudPlatform/DataflowPythonSDK/'
          'archive/v%s.tar.gz' % _PYTHON_DATAFLOW_VERSION)


setuptools.setup(
    name='python_dataflow',
    version=_PYTHON_DATAFLOW_VERSION,
    description='Google Cloud Dataflow SDK for Python',
    long_description=get_dataflow_docstring(),
    url='https://cloud.google.com/dataflow/',
    download_url=get_download_url(),
    author='Google, Inc.',
    packages=setuptools.find_packages(),
    namespace_packages=['google', 'google.cloud'],
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS,
        },
    ext_modules=cythonize([
        '**/*.pyx',
        'google/cloud/dataflow/coders/coder_impl.py',
        'google/cloud/dataflow/runners/common.py',
        'google/cloud/dataflow/worker/executor.py',
        'google/cloud/dataflow/utils/counters.py',
    ]),
    setup_requires=['nose>=1.0'],
    install_requires=REQUIRED_PACKAGES,
    test_suite='nose.collector',
    zip_safe=False,
    # PyPI package information.
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    license='Apache 2.0',
    keywords='google cloud dataflow',
    )
