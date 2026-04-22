from setuptools import setup, find_packages  # finds packages in the project
from typing import List  # type hinting

def get_requirements() -> List[str]:
    """Read requirement.txt and return as a list of strings."""
    requirements: List[str] = []## Initialize an empty list to hold the requirements
    try:
        with open("requirement.txt", "r") as f:
            # Read the contents of the file
            lines = f.readlines()
            for line in lines:
                req = line.strip() # Remove leading/trailing whitespace and newline characters
                # Skip empty lines and accidental '.e'
                if req and req != "-e .":
                    requirements.append(req)
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
    return requirements

setup(
    name="network_security",
    version="0.0.1",
    author="YASHARTH YASH",
    description="Short description of your package",
    packages=find_packages(),
    install_requires=get_requirements(),
)