from setuptools import setup, find_packages

setup(
    name="devops-connect",
    version="2.1.4",
    description="Internal DevOps connection toolkit",
    author="Infra Team",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "pyyaml>=6.0",
        "requests>=2.28",
        "paramiko>=3.0",
        "sqlalchemy>=2.0",
        "cryptography>=41.0",
    ],
    entry_points={
        "console_scripts": [
            "devops-connect=devops_connect.cli:main",
        ],
    },
    python_requires=">=3.9",
)
