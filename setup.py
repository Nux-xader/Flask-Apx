from setuptools import setup


with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("README.rst") as f:
    readme = f.read()

github_url = "https://github.com/Nux-xader/Flask-Apx"


setup(
    name="FlaskApx", 
    url=github_url, 
    project_urls={
        "Github": github_url
    },
    author="Nux xader A.K.A Satria Rahmat", 
    python_requires=">=3.7, <4", 
    version="1.0.0", 
    keywords=["flask helper", "flask", "API heler", "API Toolkit", "API warper"], 
    description="The helper for Flask", 
    long_description=readme, 
    packages=["apx"], 
    install_requires=requirements
)
