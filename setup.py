from setuptools import setup, find_packages

version = '2.1'

setup(
    name='slc.smtp2zope',
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
    url='https://github.com/syslabcom/slc.smtp2zope',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir = {'' : 'src'},
    namespace_packages=['slc'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points="""
        [console_scripts]
        smtp2zope = slc.smtp2zope:main
    """,
    setup_requires=[],
    paster_plugins = ["ZopeSkel"],
    )
