import os

from setuptools import setup, find_packages


# Function to parse requirements.txt with error handling and specified encoding
def parse_requirements(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


setup(
    name='troi-billing',
    author='Daniel Pfäffli',
    description='A simple CLI for TROI billing',
    version='0.1',
    py_modules=['troi_billing'],
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'troi-billing=troi_billing:cli',
        ],
    },
    data_files=[
        (os.path.expanduser('~/.config/troi_billing'), ['config.yaml.example'])
    ],
)
