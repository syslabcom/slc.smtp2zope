from setuptools import setup, find_packages

version = '0.1'

setup(
    name='slc.mailrouter.scripts',
    version=version,
    description="Provides smtp2zope integration script for slc.mailrouter.",
    long_description=open("README.txt").read(),
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        ],
    keywords='smtp2zope',
    author='Izak Burger, Syslab.com GmbH',
    author_email='isburger@gmail.com',
    url='https://github.com/syslabcom/slc.mailrouter.scripts',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir = {'' : 'src'},
    namespace_packages=['slc', 'slc.mailrouter'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points="""
        [console_scripts]
        smtp2zope = slc.mailrouter.scripts.smtp2zope:main
    """,
    setup_requires=["PasteScript"],
    paster_plugins = ["ZopeSkel"],
    )
