from setuptools import setup
import versioneer


project_name = 'multispot_utils'
long_description = """
Multispot Utils
===============

Various utilities for multispot data.

"""

setup(
    name=project_name,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Antonino Ingargiola',
    author_email='tritemio@gmail.com',
    url='https://github.com/multispot-software/multispot_utils',
    download_url='https://github.com/multispot-software/multispot_utils',
    license='MIT',
    description="Various utilities for multispot data.",
    long_description=long_description,
    platforms=('Windows', 'Linux', 'Mac OS X'),
    classifiers=['Intended Audience :: Science/Research',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Scientific/Engineering',
                 ],
    install_requires=['fretbursts', 'ipython', 'seaborn', 'pandas'],
    packages=['multispot_utils'],
)
