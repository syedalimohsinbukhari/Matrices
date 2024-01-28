from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
        name='umatrix',
        version='0.1.1',
        packages=find_packages(where="src"),
        url='https://github.com/syedalimohsinbukhari/Matrices',
        license='MIT',
        author='Syed Ali Mohsin Bukhari, Astrophysics and Python',
        author_email='syedali.b@outlook.com, astrophysicsandpython@gmail.com',
        description='',
        long_description=readme,
        long_description_content_type="text/markdown",
        python_requires=">=3.9",
        install_requires=["setuptools~=68.0.0"],
        include_package_data=True,
        classifiers=[
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3.11"],
        )
