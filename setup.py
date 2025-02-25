from setuptools import setup

setup(
    name="swd2",
    version="1.0.0",
    packages=["swd2"],
    install_requires=[
        'Click',
        'pyfiglet',
        'parameterized',
        # tests
        # 'jsonpath-ng',
        # 'jsonpath-python'
        # 'requests'
    ],
    entry_points={
        'console_scripts': ['swd2 = swd2.__main__:main']
    }
)