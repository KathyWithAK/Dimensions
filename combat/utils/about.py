def get_version_combat():
    """Display information about server or target"""

    string = """         |cEvennia|n MU* combat system
        |w Version|n: {version}
        |w Maintainer|n {maintainer}
    """.format(
        version="v2024.05.14",
        maintainer="(2023-) Katherine Bradford",
    )
    return string
