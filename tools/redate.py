"""Pennsylvania, wave 3: re-date the first build's five acts (Constitution, Titles 13, 15, 18, 68) append-only.

The first build dated each act by its file's "revised" stamp, a compilation date that can fall before an amendment's
in-force day. corpus.json (parse_all.py) now dates them by that build's retrieval day, 2026-10-30. append.py cannot move
a held version later (it has no base version on or before the held day), so this script uses append.py's own writer,
trailer check, docs and check_corrected to append, onto origin/main:

1. per act, one labelled correction commit (In-force: <stamp>; Corrects: <act> <stamp>..2026-10-29; Supersedes: the
   start commit; Reason; Act-path; one Files: line per file) whose tree lacks the act's files, so readers hold no text
   for the act on those days;
2. per act, its start commit for the version in force from 2026-10-30, as build.py writes it (the same text);
3. a documentation commit, as append.py writes it.

    python -X utf8 redate.py --repo <clone at origin/main> --docs-date YYYY-MM-DD [--dry-run]
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'gitlaw_common'))
import append as A  # noqa: E402

B = A.B
FIVE = ['constitution', 'title-13-commercial-code', 'title-15-corporations', 'title-18-crimes', 'title-68-property']
REASON = ('dated by a compilation stamp, not an in-force day: under the wave 3 rule the text is first recorded on the '
          'retrieval day, 2026-10-30')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--docs-date', required=True)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    repo, docs_date = Path(a.repo), a.docs_date
    c, raw = B.load(HERE)
    errs = B.validate(c)
    if errs:
        raise SystemExit('corpus has problems: ' + '; '.join(errs[:20]))
    c['_docs_date'] = docs_date
    git = lambda *x: A.git(repo, *x)  # noqa: E731
    if git('status', '--porcelain', '--untracked-files=no').strip():
        raise SystemExit('uncommitted changes')
    head = git('rev-parse', 'main').strip()
    if head != git('rev-parse', 'origin/main').strip():
        raise SystemExit('main is not origin/main')
    head_ct, head_tz = git('log', '-1', '--format=%ct %ci', 'main').split()[0::3]
    co = c['country']
    committer = ('Lexifina', f'{co["slug"]}-law@lexifina.com')
    clock = B.Clock(co['tz'])
    acts = {x['slug']: x for x in c['acts']}
    new_day = acts[FIVE[0]]['versions'][0]['from']
    fixes, starts = [], []
    for s in FIVE:
        act = acts[s]
        if len(act['versions']) != 1 or act['versions'][0]['from'] != new_day:
            raise SystemExit(f'{s}: expected one version from {new_day}')
        shas = [h for h in git('log', '--format=%H', 'main', '--', f'{s}/').split()
                if 'In-force: ' in git('log', '-1', '--format=%B', h)]
        if len(shas) != 1:
            raise SystemExit(f'{s}: expected one published commit, found {len(shas)} (already re-dated?)')
        sup = shas[0]
        body = git('log', '-1', '--format=%B', sup)
        old = next(l.split(': ', 1)[1].strip() for l in body.splitlines() if l.startswith('In-force: '))
        subj = git('log', '-1', '--format=%s', sup).strip()
        held = set(git('ls-tree', '-r', '--name-only', 'main', '--', f'{s}/').split())
        paths = sorted(A.unit_oids(s, act['versions'][0]))   # the act's unit files (not its README)
        if not set(paths) <= held:
            raise SystemExit(f'{s}: main lacks {len(set(paths) - held)} unit files')
        to = A.day_before(new_day)
        msg = [B.short_subject(f'Correction: {act["short"]}, no version recorded from {old} to {to}'), '']
        msg += B.wrap(f'{act["title"]}: main dated its oldest available text from {old}, the "revised" stamp of the '
                      f'publisher\'s file. That stamp is a compilation date, not an in-force day, so the current wording '
                      f'could read as in force before its latest amendment took effect. Under the wave 3 dating rule the '
                      f'text is dated by the day it was retrieved, {new_day}, credited to the publisher.') + ['']
        msg += B.wrap(f'This commit removes the act\'s {len(paths)} files for the days {old} to {to}: no version is '
                      f'recorded for them. The next commit publishes the same text as the version in force from '
                      f'{new_day}. The history is not re-sorted: the commit before keeps its text as first published, '
                      f'and readers apply this commit to the days in its Corrects range. It supersedes {sup[:12]} '
                      f'("{subj}").') + ['']
        trailers = ['Kind: correction', f'In-force: {old}', f'Corrects: {s} {old}..{to}', f'Supersedes: {sup}',
                    f'Reason: {REASON}', f'Act-path: {s}'] + [f'Files: {p}' for p in paths]
        B.check_trailers(trailers)
        fixes.append({'day': old, 'slug': s, 'text': '\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n',
                      'files': {p: None for p in paths}})
    fixes.sort(key=lambda x: (x['day'], x['slug']))
    sub = {**c, 'acts': [acts[s] for s in FIVE]}
    for x in B.plan(sub):
        if x['kind'] != 'start':
            raise SystemExit('unexpected plan kind ' + x['kind'])
        author, msg, trailers = B.start_message(c, x)
        B.check_trailers(trailers)
        starts.append({'x': x, 'author': author, 'files': B.act_files(x['act'], x['version']['units'], None),
                       'text': '\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n'})
    print({'head': head, 'corrections': [(f['slug'], f['day'], len(f['files'])) for f in fixes],
           'starts': [(e['x']['act']['slug'], e['x']['day']) for e in starts]})
    if a.dry_run:
        return
    existing = set(git('tag', '--list').split())
    w = A.Appender(repo, head, int(head_ct), head_tz)
    log, tags = [], {}
    for f in fixes:
        w.commit(committer, clock.stamp(f['day']), committer, f['text'], f['files'])
        log.append({'day': f['day'], 'kind': 'correction', 'law': None, 'acts': [f['slug']], 'units': len(f['files']),
                    'branch': 'main', 'clamped': False})
    for e in starts:
        x = e['x']
        mark = w.commit(e['author'], clock.stamp(x['day']), committer, e['text'], e['files'])
        tags.setdefault(f'{x["act"]["slug"]}/{x["day"]}', mark)
        log.append({'day': x['day'], 'kind': 'start', 'law': x['act'].get('first_law'), 'acts': [x['act']['slug']],
                    'units': len(e['files']), 'branch': 'main', 'clamped': False})
    full_log = A.published_log(repo) + log
    all_tags = {t: 0 for t in existing} | tags
    docs = B.docs_files(c, HERE, raw, full_log, all_tags, docs_date)
    docs['tools/append.py'] = Path(A.__file__).read_text(encoding='utf-8').replace('\r\n', '\n')
    ts, tz = clock.stamp(docs_date).split()
    w.commit(committer, f'{min(int(ts), int(time.time()))} {tz}', committer,
             f'Documentation, tables, tools and REPRODUCE.md\n\nAppended {len(log)} commits to {head[:12]} '
             f'({len(fixes)} of them corrections, re-dating five acts to {new_day}); corpus sha256 '
             f'{B.hashlib.sha256(raw).hexdigest()}, data retrieved {docs_date}.\n', docs)
    for name, mark in sorted(tags.items()):
        if name not in existing:
            w.tag(name, mark)
    w.finish()
    git('-c', 'checkout.workers=0', 'checkout', '-q', '-f', 'main')
    new = git('rev-parse', 'main').strip()
    if subprocess.run(['git', 'merge-base', '--is-ancestor', head, new], cwd=repo).returncode:
        raise SystemExit('internal: head is not an ancestor')
    res = A.check_corrected(repo, c, docs_date)
    print({'main': new, **res})


if __name__ == '__main__':
    main()
