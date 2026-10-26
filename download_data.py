"""Download and restore this repository's complete research dataset (Python 3)."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
import urllib.parse
import urllib.request

BLOCK = 8 * 1024 * 1024


def sha256(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(BLOCK), b''):
            value.update(block)
    return value.hexdigest()


def matches(path, item):
    return path.is_file() and path.stat().st_size == item['bytes'] and sha256(path) == item['sha256']


def download(opener, url, path, item):
    if matches(path, item):
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + '.partial')
    for attempt in range(5):
        try:
            offset = partial.stat().st_size if partial.exists() else 0
            if offset > item['bytes']:
                partial.unlink()
                offset = 0
            if offset < item['bytes']:
                headers = {'User-Agent': 'intersection-resilience-data/1.0'}
                if offset:
                    headers['Range'] = f'bytes={offset}-'
                with opener.open(urllib.request.Request(url, headers=headers), timeout=120) as response:
                    append = offset > 0 and response.status == 206
                    with partial.open('ab' if append else 'wb') as output:
                        shutil.copyfileobj(response, output, BLOCK)
            if not matches(partial, item):
                partial.unlink(missing_ok=True)
                raise ValueError('Size or SHA-256 verification failed')
            os.replace(partial, path)
            return
        except Exception:
            if attempt == 4:
                raise
            time.sleep(min(2 ** attempt, 10))


def restore_file(entry, assets, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + '.partial')
    value = hashlib.sha256()
    size = 0
    try:
        with temporary.open('wb') as output:
            for asset in entry['assets']:
                path = assets / asset['name']
                if not matches(path, asset):
                    raise ValueError(f"Asset verification failed: {asset['name']}")
                source = gzip.open(path, 'rb') if entry['compression'] == 'gzip' else path.open('rb')
                with source:
                    for block in iter(lambda: source.read(BLOCK), b''):
                        value.update(block)
                        size += len(block)
                        output.write(block)
        if size != entry['bytes'] or value.hexdigest() != entry['sha256']:
            raise ValueError(f"Restored file verification failed: {entry['path']}")
        os.replace(temporary, destination)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true', help='Verify all restored dataset files without downloading')
    parser.add_argument('--assets-dir', type=Path, help='Use release attachments already downloaded into this directory')
    parser.add_argument('--no-proxy', action='store_true', help='Ignore HTTP_PROXY and HTTPS_PROXY for this run')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'data-manifest.json').read_text(encoding='utf-8'))
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if args.no_proxy else urllib.request.build_opener()
    cache = args.assets_dir.resolve() if args.assets_dir else root / '.data-downloads'
    base = f"https://github.com/{manifest['repository']}/releases/download/{manifest['release_tag']}/"
    missing = []
    for entry in manifest['files']:
        relative = Path(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe path in manifest')
        target = root / relative
        if matches(target, entry):
            print(f"OK: {entry['path']}", flush=True)
            continue
        if args.verify_only:
            missing.append(entry['path'])
            continue
        print(f"Restoring: {entry['path']}", flush=True)
        if entry['storage'] == 'git':
            url = f"https://raw.githubusercontent.com/{manifest['repository']}/{manifest['release_tag']}/" + urllib.parse.quote(entry['path'], safe='/')
            download(opener, url, target, entry)
        else:
            for asset in entry['assets']:
                path = cache / asset['name']
                if args.assets_dir:
                    if not matches(path, asset):
                        raise ValueError(f"Missing or invalid local attachment: {asset['name']}")
                else:
                    download(opener, base + urllib.parse.quote(asset['name']), path, asset)
            restore_file(entry, cache, target)
    if missing:
        raise SystemExit('Missing or invalid files:\n' + '\n'.join(missing))
    print(f"All {len(manifest['files'])} dataset files verified.")


if __name__ == '__main__':
    main()
