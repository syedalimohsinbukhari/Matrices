from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='umatrix',
    version='0.1.3',
    packages=find_packages(where="src"),
    url='https://github.com/syedalimohsinbukhari/Matrices',
    license='MIT',
    author='Syed Ali Mohsin Bukhari',
    author_email='syedali.b@outlook.com',
    description='',
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    install_requires=["setuptools"],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"],
)
