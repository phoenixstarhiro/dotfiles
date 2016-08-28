#!/usr/bin/python

import argparse
import errno
import os
import re
import shutil
import subprocess


# ABS Path to the src/ directory.
_SRC_DIR = os.path.abspath(os.path.normpath(os.path.join(
    os.path.dirname(__file__), 'src')))

# Git repo for Google style guide.
_GOOGLE_STYLE_GIT = 'https://github.com/google/styleguide.git'


def _makedirs(name, mode=0o777, exist_ok=False):
    """Poor backport of Python3 os.makedirs for exist_ok"""
    try:
        os.makedirs(name, mode)
    except OSError as e:
        if not exist_ok or e.errno != errno.EEXIST or not os.path.isdir(name):
            raise


def _backup_file(path):
    if not os.path.exists(path):
        return
    m = re.search(r'^(.*)\.(\d+)$', path)
    if m:
        backup = '%s.%d' % (m.group(1), int(m.group(2)) + 1)
    else:
        backup = path + '.1'

    # Rotate the file.
    _backup_file(backup)
    os.rename(path, backup)


def _copy_file(src, dest, backup=False):
    """Copy files from src to dest.

    If |backup| is set to True, the original file at |dest| will be backup
    with numbered suffix.
    """
    if backup:
        _backup_file(dest)
    shutil.copy2(src, dest)


def _maybe_install_google_style(google_style_dir):
    """Installs google-style at |google_style_dir| if necessary."""
    if not google_style_dir:
        return

    # Sanity check.
    if os.path.exists(google_style_dir) and os.listdir(google_style_dir):
        # The google style dir is non empty. We assume it is google style's
        # git repo. Do nothing, then.
        return

    _makedirs(google_style_dir, exist_ok=True)
    subprocess.check_call(['git', 'clone', _GOOGLE_STYLE_GIT],
                          cwd=google_style_dir, close_fds=True)


def _install_screen_config(home, backup=False):
    """Installs screen config file.

    Args:
       home: Path to the home directory.
       backup: (Optional) if True, existing file is back-up.
    """
    _copy_file(os.path.join(_SRC_DIR, 'screen', 'screenrc'),
               os.path.join(home, '.screenrc'),
               backup=backup)


def _install_bash_config(home, backup=False):
    """Installs bash config files.

    Args:
       home: Path to the home directory.
       backup: (Optional) if True, existing file is back-up.
    """
    _copy_file(os.path.join(_SRC_DIR, 'bash', 'bashrc'),
               os.path.join(home, '.bashrc'),
               backup=backup)


def _install_input_config(home, backup=False):
    """Installs input config files.

    Args:
       home: Path to the home directory.
       backup: (Optional) if True, existing file is back-up.
    """
    _copy_file(os.path.join(_SRC_DIR, 'input', 'inputrc'),
               os.path.join(home, '.inputrc'),
               backup=backup)


def _install_emacs_config(home, google_style_dir, backup=False):
    """Installs emacs config files.

    Args:
       home: Path to the home directory.
       google_style_dir: (Optional) Path to the google-style repository.
       backup: (Optional) if True, existing file is back-up.
    """
    _makedirs(os.path.join(home, '.emacs.d'), exist_ok=True)
    _copy_file(os.path.join(_SRC_DIR, 'emacs', 'init.el'),
               os.path.join(home, '.emacs.d', 'init.el'),
               backup=backup)
    if google_style_dir:
        dest = os.path.join(home, '.emacs.d', 'google-c-style.el')
        if backup:
            _backup_file(dest)
        os.symlink(
            os.path.abspath(os.path.join(
                google_style_dir, 'styleguide', 'google-c-style.el')),
            dest)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--google-style-dir',
                        help='Path to google style repository')
    parser.add_argument('--home', default=os.environ['HOME'],
                        help='Path to the home directory.')
    parser.add_argument('--backup', type=bool, default=True,
                        help='If True, the existing files will be backup.')
    return parser.parse_args()


def main():
    args = _parse_args()
    _maybe_install_google_style(args.google_style_dir)

    _install_screen_config(args.home, args.backup)
    _install_bash_config(args.home, args.backup)
    _install_input_config(args.home, args.backup)
    _install_emacs_config(args.home, args.google_style_dir, args.backup)


if __name__ == '__main__':
    main()
