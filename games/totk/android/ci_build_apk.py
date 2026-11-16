#!/usr/bin/env python3
"""Build a debuggable, no-Turnip APK for GitHub Actions from source only."""
import argparse
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_release  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ndk', type=Path, required=True)
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--key', type=Path, required=True, help='PEM containing a private key and its certificate')
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()

    if not args.key.is_file():
        parser.error(f'no signing key at {args.key}; configure the TOTK_SIGNING_KEY_PEM Actions secret')
    run_number = int(os.environ.get('GITHUB_RUN_NUMBER', '1'))
    logs = args.work / 'logs'
    build_release.app(
        work=args.work,
        ndk=args.ndk,
        logs=logs,
        out=args.out,
        key=args.key,
        release=False,
        turnip=None,
        android_sdk=args.sdk,
        version_code=100000 + run_number,
        version_name=f'{build_release.APP_VERSION}-ci.{run_number}',
        package_id='com.aure.totk.codextest',
        jobs=os.cpu_count() or 2,
    )
    print(f'APK ready: {args.out} (package com.aure.totk.codextest)')


if __name__ == '__main__':
    main()
