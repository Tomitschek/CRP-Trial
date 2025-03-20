from setuptools import setup, find_packages

setup(
    name="crptrial",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "statsmodels>=0.14.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "tabulate>=0.8.10",
        "lxml>=4.9.0",
        "openpyxl>=3.0.0",
    ],
    entry_points={
        'console_scripts': [
            'crptrial=crptrial.cli:main',
        ],
    },
    author="Tomitschek",
    description="A tool for CRP data analysis",
)
