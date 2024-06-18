def get_version_space():
    """Display information about server or target"""

    string = """         |cEvennia|n MU* space system
        |w Version|n: {version}
        |w Maintainer|n {maintainer}
    """.format(
        version="v2024.06.18",
        maintainer="(2019-) Katherine Bradford",
    )
    return string
