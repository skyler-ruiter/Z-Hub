# Z-Hub

Z-Hub is an open, machine-readable registry of scientific and general-purpose
compression techniques. It separates reusable algorithm **modules** from concrete
compressor **compositions**, and also catalogs ecosystem tools and benchmark datasets.

The site is a research index, not a benchmark leaderboard or a guarantee that every
entry is correct. Records without an explicit `verification` block are unreviewed by
default; follow their papers, repositories, and implementation links for authoritative
details.

## Machine-readable catalogs

The static JSON files are intentionally usable without the Vue interface:

- `public/modules.json` — general algorithm families and known implementations
- `public/compositions.json` — concrete pipelines from software and literature
- `public/ecosystem.json` — libraries, interfaces, integrations, and applications
- `public/datasets.json` — community-submitted dataset metadata
- `public/sdrbench-datasets.json` — SDRBench-oriented dataset metadata

Their consistent JSON structure makes the catalogs suitable for search, knowledge graphs,
reproducible tooling, and future research tools. Consumers should treat missing verification
metadata as `unverified`/`low` and preserve links to primary sources.

## Development

Requires Node.js 18 or newer.

```sh
npm install
npm run dev
```

Quality checks:

```sh
npm run lint
npm run build
```

The production base path defaults to `/Z-Hub/`. Override it for another deployment:

```sh
VITE_BASE_PATH=/ npm run build
```

## Contributing

Module and composition buttons open curated GitHub issue forms. Maintainers translate
those proposals into schema-valid records because taxonomy and source mapping require
review.

Dataset submissions use a GitHub Issues + Actions workflow:

1. “Submit a community dataset” opens the dataset issue form.
2. The ingestion workflow parses issues labeled `dataset`.
3. It opens or updates a pull request changing `public/datasets.json`.
4. After maintainer review and merge, the Datasets page displays approved records from
   that file at runtime. Records marked `example` remain as fixtures and are not displayed.

Submission buttons always target the canonical `guoxiliu/Z-Hub` repository, including
when the site is built from a development fork. Submitted files remain externally hosted;
Z-Hub stores links and metadata only.

## Attribution and rights

Z-Hub summarizes factual and technical material in original wording and links readers to
primary sources. Citations do not themselves grant permission to reproduce copyrighted
expression, so contributions must not copy abstracts, documentation, figures, tables, or
other substantial source text.

The MIT license covers the repository's original software and original project-authored
documentation. Third-party publications, software, datasets, names, and linked materials
remain subject to their own licenses and terms.
