# How this repository was made (Pennsylvania)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Pennsylvania General Assembly: Consolidated Statutes and Constitution (palegis.us) | <https://www.palegis.us/statutes/consolidated> | 2026-10-30 | No copyright claimed on the statute text. The site's Legal Notices say the information is an information service and not a replacement for official versions. Statute text of a state is not copyrightable (Georgia v. Public.Resource.Org, 590 U.S. 255 (2020)). The unofficial annotated Purdon's Pennsylvania Statutes (West) are a separate copyrighted work and are not used. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of the Commonwealth of Pennsylvania | 1 | 2022-03-07 to 2022-03-07 |
| `title-18-crimes` | Title 18 (Crimes and Offenses), Pennsylvania Consolidated Statutes | 1 | 2026-08-31 to 2026-08-31 |
| `title-13-commercial-code` | Title 13 (Commercial Code), Pennsylvania Consolidated Statutes | 1 | 2025-12-01 to 2025-12-01 |
| `title-15-corporations` | Title 15 (Corporations and Unincorporated Associations), Pennsylvania Consolidated Statutes | 1 | 2026-07-28 to 2026-07-28 |
| `title-68-property` | Title 68 (Real and Personal Property), Pennsylvania Consolidated Statutes | 1 | 2026-07-28 to 2026-07-28 |

The build made 5 commits:

| Commits | Kind |
| ---: | --- |
| 5 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 5 tags.

## Dates

Each commit is dated at noon (America/New_York) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Each file is the publisher's compilation of the law in force on the date it stamps on the file; the compilation date is used as the version date (oldest version available). https://www.palegis.us/statutes/consolidated

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `ec1963f4892f8f757e2f29a98642c24cea8b0d85d321223bce1dbb39ae094e20` (5668395 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Only the Constitution and four Consolidated Statutes titles (18 Crimes and Offenses, 13 Commercial Code, 15 Corporations and Unincorporated Associations, 68 Real and Personal Property) were taken for this first build; other titles and the unconsolidated statutes are not in it.
- Each title is one file on palegis.us that carries a "revised" stamp. That stamp is used as the date of the single version of the act (the oldest version available); the site offers no earlier editions. The Constitution file is stamped 2022-03-07 and may not show amendments adopted after that stamp.
- Only the text of each section is kept. The Source parentheticals, cross references, annotations and editor's notes that follow each section are left out.
- Unit keys are the section number with each run of digits padded to five places (Title 18 Sec. 301 is sec-00301; Sec. 3011.1 is sec-03011-00001). Constitution keys use the publisher's own section code (00c107 is sec-00107), and the label gives article and section.
- Typographic quotes and dashes were made plain, non-breaking spaces were made ordinary spaces and runs of spaces were collapsed; the publisher's wording and "--" run-in heading separators are kept.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
