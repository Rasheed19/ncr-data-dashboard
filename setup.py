from setuptools import setup, find_packages

setup(
    name="ncr-dashboard",
    version="0.0.1",
    author="Rasheed Ibraheem",
    author_email="ibraheem.abdulrasheed@gmai.com",
    maintainer="Rasheed Ibraheem",
    maintainer_email="ibraheem.abdulrasheed@gmai.com",
    description="This dashboard showcases the distribution of chargepoints in the UK.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
)
