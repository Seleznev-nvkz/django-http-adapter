from os.path import join, dirname

from setuptools import setup

LONG_DESCRIPTION = open(join(dirname(__file__), 'README.md')).read()

CLASSIFIERS = [
    'License :: Freeware',
    'Environment :: Web Environment',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
    'Framework :: Django :: 1.11',
    'Framework :: Django :: 2.0',
    'Framework :: Django :: 2.1',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

setup(
    name='django_http_adapter',
    version='1.0.0',  # When changing this, remember to change it in __init__.py
    packages=['django_http_adapter'],
    author='Konstantin Seleznev',
    author_email='seleznev.nvkz@gmail.com',
    url='https://github.com/Seleznev-nvkz/django-http-adapter',
    license='Unlicense',
    description="Simple third-party application for communicating back-end systems on Django using HTTP",
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
    install_requires=["django>=1.11", "requests>=2.19"],
)