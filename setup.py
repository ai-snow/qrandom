from setuptools import setup

setup(
   name='qrandom',
   version='1.0',
   description='A random number generator framework designed with testing in mind.',
   author='Sam Wehner',
   author_email='samcwehner@gmail.com',
   packages=['qrandom'],
   install_requires=['pytest']
)