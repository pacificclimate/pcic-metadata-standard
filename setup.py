from setuptools import setup

__version__ = (0, 1, 0)

setup(
    name='pcic_metadata_standard',
    description='PCIC Climate Explorer Data Preparation',
    version='.'.join(str(d) for d in __version__),
    author='Rod Glover',
    author_email='rglover@uvic.ca',
    url='foo',
    keywords='science climate meteorology downscaling modelling climatology',
    zip_safe=True,
    install_requires='''
        PyYAML
    '''.split(),
    packages=['pcic_metadata_standard'],
    package_data = {
        'pcic_metadata_standard': [
            'data/*.csv',
            'tests/data/*.csv'
        ]
    },
    include_package_data=True,
    scripts='''
        scripts/pms
    '''.split(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

)
