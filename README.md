# My Project

[Project description]

## Additional documentation

[Development documentation](README-DEV.md)

[Changelog](CHANGELOG.md)

## Repo template

[Remove the 'Repo template' section once you set up all the files]

This is a template I am using for my Python projects. I will be force pushing to `master`, so that the repo always contains single commit. After creating a repo from this template I amend the commit with the changes described below.

### Project metadata

- [ ] fill in the project name in `pyproject.toml` file
- [ ] fill in the project description in `pyproject.toml` file
- [ ] fill in the project authors in `pyproject.toml` file
- [ ] fill in the project URLs in `pyproject.toml` file

### Python version

- [ ] update required Python version in `pyproject.toml` file
- [ ] update required Python version in `README-dev.md` file
- [ ] update tested/release Python versions in `.github\workflows\pr-checker.yml` and `.github\workflows\release.yml` files
- [ ] update `target-version` option in `ruff.toml`

### Package name

- [ ] rename `src/my_project` folder
- [ ] rename `tests/my_project` folder
- [ ] change package name in `pyproject.toml` (`tool.hatch.build.targets.wheel.packages`)
- [ ] change script name and path in `pyproject.toml` (`project.scripts`)
- [ ] change imports in files from `tests` and `src` folder

### README.md

- [ ] change default name of project in `README.md` file
- [ ] fill in the description in `README.md` file
- [ ] remove the checklist when all the points are checked in `README.md`

### Release pipeline

- [ ] update the environment URL to point to proper pypi project
- [ ] create a `pypi` environment in you GitHub repo
- [ ] add a trusted publisher in PyPI for your GitHub repository
