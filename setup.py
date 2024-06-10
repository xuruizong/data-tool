import setuptools

package_metadata: dict = {}
with open("./src/doristool/__init__.py") as fp:
    exec(fp.read(), package_metadata)

setuptools.setup(
    name=package_metadata["__package_name__"],
    version=package_metadata["__version__"],
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="./src"),
    install_requires=[
        "pymysql==1.1.1",
        "SQLAlchemy>=2.0.30",
        "sqlalchemy-doris[pymysql]>=0.2.2",
        "click>=8.1.7"
    ],
    entry_points={
        "console_scripts": ["doristool = doristool.entrypoints:main"],
    }
)