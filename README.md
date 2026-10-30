# Pennsylvania: law history in git

The Constitution of the Commonwealth of Pennsylvania and four titles of the Pennsylvania Consolidated Statutes as a git repository: one file per section, committed with the Pennsylvania General Assembly as its publisher. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `united-states/pennsylvania/`.

**What is in it now**

| Folder | Act | Sections | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of the Commonwealth of Pennsylvania (1968, as amended), with its schedules | 237 | One version: the publisher's file stamped 7 March 2022 |
| `title-18-crimes/` | 18 Pa.C.S., Crimes and Offenses | 729 | One version: the file stamped 31 August 2026 |
| `title-13-commercial-code/` | 13 Pa.C.S., Commercial Code | 634 | One version: the file stamped 1 December 2025 |
| `title-15-corporations/` | 15 Pa.C.S., Corporations and Unincorporated Associations | 1,045 | One version: the file stamped 28 July 2026 |
| `title-68-property/` | 68 Pa.C.S., Real and Personal Property | 332 | One version: the file stamped 28 July 2026 |

That is all the law this repository holds today. This is a first build: the other Consolidated Statutes titles, the unconsolidated statutes (acts not yet codified in Pa.C.S.), regulations and court decisions are not in it, and it has no amendment history yet.

## Where the text comes from

The Pennsylvania General Assembly's Legislative Data Processing Center publishes each Consolidated Statutes title as one file at palegis.us. This build takes the text of each section from those files and nothing else. It leaves out the Source parentheticals, cross references, editor's notes and annotations that follow each section. The unofficial annotated Purdon's Pennsylvania Statutes published by West are a separate copyrighted work and are not used.

## Dates

- Each title has a single version, dated by the stamp the publisher puts in its file (its `revised` field). That stamp is the date the compiled file was produced, not necessarily the date the newest amendment took effect, and the site offers no earlier editions. Each first commit is credited to the publisher as "oldest version available".
- The Constitution file is stamped 7 March 2022. It may not show amendments adopted after that stamp.
- The Constitution's preamble is not in the publisher's file and is not in this repository.

## What it does not show

- Any amendment history: which act changed which section and when. The publisher's Source notes list them, but past texts are not online, so no earlier versions can be built yet.
- The Source notes themselves, cross references and annotations.
- Nothing here is an official publication.

## How it is checked

- Every unit is read back from git on its day and compared with the corpus (`tools/check_repo.py`; results in `REPRODUCE.md`).
- The source of each version is identified by its sha256 in `data/versions.json`.
