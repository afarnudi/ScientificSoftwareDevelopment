from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="helloWorld", #what you write after $ pip install
    version="0.0.1", # 0.0.x generaly means it is nstable
    description="Say hello!", # usually one liner
    long_description=long_description,
    long_description_content_type="text/x-rst",
    py_modulies=["helloWorld"], # list of actual python modules (code) 
    package_dir={"": "src"},
    
    url="https://github.com/...",
    auther="name surname",
    auther_email="user@example.com",

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
	    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "numpy ~=1.7",
    ],
    extras_require = {
        "dev":[
            "pytest>=3.7",
        ],
    },
)



