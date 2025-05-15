# Ansible Role: asdf

[![CI](https://github.com/1000Bulbs/ansible-role-asdf/actions/workflows/ci.yml/badge.svg)](https://github.com/1000Bulbs/ansible-role-asdf/actions/workflows/ci.yml)

This role installs and manages [asdf](https://asdf-vm.com/) — the extendable version manager — on Linux (Ubuntu 22.04+) systems.

It handles:

- **Binary installation** of the Go‑based asdf CLI from GitHub releases
- Auto‑detecting OS (Linux) and CPU architecture (amd64 vs arm64)
- Installing global system dependencies via `apt` and plugin‑specific dependencies
- Managing asdf **plugins** and their **installed** and **default** versions
- Uninstalling specified versions
- Configuring asdf for all users via (`/etc/profile.d/asdf.sh`)
- Enabling bash completions for all users via `/etc/bash.bashrc`

---

## ✅ Requirements

- Ansible 2.13+
- Python 3.9+ (for Molecule + testinfra)
- Tested on Ubuntu 22.04+

---

## ⚙️ Role Variables

All defaults live in `defaults/main.yml` and `vars/main.yml`.

### Defaults (`defaults/main.yml`)

```yaml
asdf_version: 0.16.7                                  # asdf release to install
asdf_user: deploy                                     # default user account
asdf_bin_dir: /usr/local/bin                          # where to put the binary
asdf_bin_path: "{{ asdf_bin_dir }}/asdf"              # full path to asdf executable
asdf_apt_optional_dependencies: []                    # apt packages before plugin adds
asdf_legacy_version_file: yes                         # manage legacy .tool-versions handling
```

### Variables (`vars/main.yml`)

```yaml
apt_cache_valid_time: 86400                           # seconds before apt cache refresh
remote_package_retries: 5                             # apt retry count
asdf_script_file: /etc/profile.d/asdf.sh              # system‑wide asdf loader script
asdf_global_dependencies:                             # packages needed by language builds
  - autoconf
  - automake
  - binutils
  - bison
  - curl
  - g++
  - gcc
  - git
  - libreadline-dev
  - libtool
  - make
  - patch
  - pkg-config
  - unzip
asdf_ruby_dependencies:                               # packages needed by ruby builds
  - libdb-dev
  - libffi-dev
  - libgdbm-dev
  - libgmp-dev
  - libmysqlclient-dev
  - libncurses-dev
  - libpq-dev
  - libreadline-dev
  - libssl-dev
  - libyaml-dev
  - patch
  - rustc
  - uuid-dev
  - zlib1g-dev
```

### Plugin Management (`asdf_plugins`)

Define a list of plugins and what versions to install, set default, or uninstall.

```yaml
asdf_plugins:
  - name: ruby
    install:
      - 3.4.3

  - name: nodejs
    install:
      - 23.11.0
      - 22.15.0
    default: 23.11.0         # default, if not specified, first install version

  - name: act
    uninstall:
      - 0.2.77               # version(s) to remove
```

Each item supports:

| Key         | Type          | Description                                                |
| ----------- | ------------- | ---------------------------------------------------------- |
| `name`      | string        | Plugin name (`nodejs`, `python`, `ruby`, etc.)             |
| `install`   | list          | Versions to install                                        |
| `default`   | string (opt.) | Version to set as default (defaults to first install entry) |
| `uninstall` | list (opt.)   | Versions to remove                                         |

---

## 📦 Dependencies

No external roles or collections required.

---

## 📥 Installing the Role

To include this role in your project using a `requirements.yml` file:

```yaml
roles:
  - name: okb.asdf
    src: git@github.com:1000bulbs/ansible-role-asdf.git
    scm: git
    version: master
```

Then install it with:

```bash
ansible-galaxy role install -r requirements.yml
```

---

## 💡 Example Playbook

```yaml
- name: My Playbook
  hosts: all
  become: true
  vars:
    asdf_plugins:
      - name: ruby
        install: ["3.4.3"]
      - name: nodejs
        install: ["23.11.0", "22.15.0"]
        default: "23.11.0"
      - name: act
        uninstall: ["0.2.77"]
  roles:
    - role: okb.asdf
```

---

## 🧪 Testing

This role uses a `Makefile` for linting and formatting, and [Molecule](https://molecule.readthedocs.io/) with
`pytest-testinfra` for integration testing.

### Run tests locally

#### Lint and Format

```bash
# Run all checks (linting and formatting)
make check

# Run linting tools manually (ruff, yamllint, ansible-lint)
make lint

# Run Python formatting tools manually (ruff)

make format
```

#### Integration Tests

Install dependencies

```bash
pip install -r requirements.txt
```

Run Molecule integration tests

```bash
molecule test
```

---

## 🪝 Git Hooks

This project includes [pre-commit](https://pre-commit.com/) integration via Git hooks to automatically run formatting and linting checks **before each commit**.

These hooks help catch errors early and keep the codebase consistent across contributors.

### Install Git Hooks

```bash
make install-hooks
```

This will:

- Install pre-commit (if not already installed)
- Register a Git hook in .git/hooks/pre-commit
- Automatically run checks like:
- Code formatting with black and isort
- Linting with ruff, yamllint, and ansible-lint

### Remove Git Hooks

```bash
make uninstall-hooks
```

This removes the Git pre-commit hook and disables automatic checks.

💡 Even with hooks uninstalled, you can still run the same checks manually with `make test`.

Why Use Git Hooks?

- Ensures consistency across contributors
- Catches syntax and style issues before they hit CI
- Prevents accidental commits of broken or misformatted files
- Integrates seamlessly with your local workflow
