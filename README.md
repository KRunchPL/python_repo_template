# My Project

[Project description]

## Additional documentation

[Development documentation](README-DEV.md)

[Changelog](CHANGELOG.md)

## Repo template

[Remove the 'Repo template' section once you set up all the files]

This is a template I am using for my Python projects. I will be force pushing to `master`, so that the repo always contains single commit. After creating a repo from this template I amend the commit with the changes described below.

### README.md

- [ ] change default name of project in `README.md` file
- [ ] fill in the description in `README.md` file
- [ ] remove the checklist when all the points are checked in `README.md`

### Project metadata

- [ ] fill in the project name in `pyproject.toml` file
- [ ] fill in the project description in `pyproject.toml` file
- [ ] fill in the project authors in `pyproject.toml` file
- [ ] fill in the project repository URLs in `pyproject.toml` file

### Python version

- [ ] update minimal Python version in `pyproject.toml` file
- [ ] update required Python version in `README-dev.md` file
- [ ] update tested Python versions in `.github\workflows\pr-checker.yml` file

### Package name

- [ ] rename `my_project` folder
- [ ] change package name in `pyproject.toml` (`tool.poetry.packages`)
- [ ] change folder name to count coverage from in `pytest.ini` (`--cov` param)
- [ ] change import in `test_dummy.py` file
