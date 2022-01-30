from setuptools import find_packages, setup
from clavis.version import title, description, url, version, author, author_email, license

# From https://github.com/pypa/pip/issues/3610#issuecomment-356687173
def install_deps():
    with open("requirements.txt", "r") as f:
        packages = f.readlines()
        new_pkgs = []
        links = []
        for resource in packages:
            if "git+https" in resource:
                pkg = resource.split("#")[-1]
                links.append(resource.strip() + "-9876543210")
                new_pkgs.append(pkg.replace("egg=", "").rstrip())
            else:
                new_pkgs.append(resource.strip())
        return new_pkgs, links


pkgs, new_links = install_deps()

setup(
    name=title,
    description=description,
    long_description=url,
    url=url,
    version=version,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=[],
    keywords="kubernetes secrets",
    py_modules=["clavis"],
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    dependency_links=new_links,
    install_requires=pkgs,
    entry_points={
        "console_scripts": [
            "clavis=clavis.cli:cli"
        ],
    },
)