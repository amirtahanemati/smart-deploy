from setuptools import setup, find_packages

setup(
    name="smart-deploy",
    version="0.4.0",
    description="Zero-Config Automated CI/CD Tool for Developers",
    author="Amirtaha Nemati",
    packages=find_packages(),
    install_requires=[
        "typer",
        "fastapi",
        "uvicorn",
        "requests",
        "pydantic"
    ],
    entry_points={
        "console_scripts": [
            "smart-deploy=smart_deploy.cli:app",
        ],
    },
)