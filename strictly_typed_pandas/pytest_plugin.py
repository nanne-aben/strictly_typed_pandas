import sys
from typing import List

from ._vendor.typeguard.importhook import install_import_hook

try:
    import typeguard

    del typeguard
    TYPEGUARD_INSTALLED = True
except ImportError:
    TYPEGUARD_INSTALLED = False


def pytest_addoption(parser):
    group = parser.getgroup("stp_typeguard")
    group.addoption(
        "--stp-typeguard-packages",
        action="store",
        help=(
            "comma separated name list of packages and modules to "
            "instrument for type checking by strictly typed pandas"
        ),
    )
    if not TYPEGUARD_INSTALLED:
        group = parser.getgroup("typeguard")
        group.addoption(
            "--typeguard-packages",
            action="store",
            help=(
                "comma separated name list of packages and modules to "
                "instrument for type checking"
            ),
        )


def _parse_packages(val: str) -> List[str]:
    if val is None or not val.strip():
        return []
    return [pkg.strip() for pkg in val.split(",")]


def pytest_configure(config):
    packages = _parse_packages(config.getoption("stp_typeguard_packages"))
    typeguard_packages = _parse_packages(config.getoption("typeguard_packages"))

    packages_in_both = set(packages) & set(typeguard_packages)
    if packages_in_both:
        raise RuntimeError(
            "If you are going to use both --stp-typeguard-packages "
            "and --typeguard-packages at the same time, "
            "please don't list the same package in both options: "
            f"{', '.join(packages_in_both)}"
        )

    if not TYPEGUARD_INSTALLED:
        packages.extend(typeguard_packages)

    if not packages:
        return

    already_imported_packages = sorted(p for p in packages if p in sys.modules)
    if already_imported_packages:
        message = (
            "strictly_typed_pandas cannot check these packages because "
            "they are already imported: {}"
        )
        raise RuntimeError(message.format(", ".join(already_imported_packages)))

    install_import_hook(packages=packages)
