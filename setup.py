from setuptools import setup

setup(
        name = 'vgapi',
        version='1.0',
        packages = ['vgapi'],
        include_package_data = True,
        zip_safe=False,
        long_description='Video Games DB Demo REST API',
        install_requires = ['flask',],
)

