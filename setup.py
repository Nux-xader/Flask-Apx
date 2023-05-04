from setuptools import setup


setup(
    name="apx", 
    url="https://github.com/Nux-xader/Apx", 
    author="Nux xader A.K.A Satria Rahmat", 
    python_requires=">=3.7, <4", 
    version="1.0.0", 
    description="The API helper for Flask", 
    packages=["apx"], 
    install_requires=[
        "Flask==2.3.2"
    ]
)
