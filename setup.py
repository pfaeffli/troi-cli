from setuptools import setup, find_packages


# Function to parse requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


setup(
    name='troi-billing',
    version='0.1',
    py_modules=['troi-billing'],
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points='''
        [console_scripts]
        troi-billing=troi-billing:main
    ''',
)
