# My Project

[Project description]

## Repo template checklist

[Remove the 'Repo template checklist' part once you set up all the files]

When using this template:

### README.md

- [ ] change default name of project in `README.md` file
- [ ] fill in the description in `README.md` file
- [ ] remove the checklist when all the points are checked in `README.md`

### pyproject.toml

- [ ] fill in the project name in `pyproject.toml` file
- [ ] fill in the project description in `pyproject.toml` file
- [ ] fill in the project repository URLs in `pyproject.toml` file

### Python version

- [ ] update minimal Python version in `pyproject.toml` file
- [ ] update required Python version in `README-dev.md` file
- [ ] update tested Python versions in `.github\workflows\pr-checker.yml` file

### Update package name

- [ ] rename `my_project` folder
- [ ] change package name in `pyproject.toml` (`tool.poetry.packages`)
- [ ] change folder name to count coverage from in `pyproject.toml` (`--cov` param)
- [ ] change import in `test_dummy.py` file

## Additional documentation

[Development documentation](README-DEV.md)

[Changelog](CHANGELOG.md)
