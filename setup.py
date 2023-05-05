from setuptools import setup


with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="apx", 
    url="https://github.com/Nux-xader/Apx", 
    author="Nux xader A.K.A Satria Rahmat", 
    python_requires=">=3.7, <4", 
    version="1.0.0", 
    keywords=["flask helper", "flask", "API heler", "API Toolkit", "API warper"], 
    description="The helper for Flask", 
    packages=["apx"], 
    install_requires=requirements
)
