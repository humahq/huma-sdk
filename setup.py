"""Setup.py for Huma SDK"""

from setuptools import setup, find_packages

# Pull in the package info
package_name = 'huma_sdk'
author = 'Huma AI'
email = 'support@humaai.com'
version = '1.0'

setup(
    name=package_name,
    version=version,
    description='Huma SDK',
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask[async]',
        'requests',
        'bson',
        'nose2==0.13.0',
        'nose2[coverage_plugin]',
        'python-dotenv',
        'pygments',
        'uvicorn',
        'werkzeug',
        'pydantic',
        'websocket-client'
    ],
    license='Proprietary',
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Proprietary',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)