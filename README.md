# QEC-Bank

QEC-Bank is a machine-checked dataset of quantum error-correcting codes. Each
entry records a code family, its concrete instances, their parameters, and
where every number comes from.

**Browse the data:** https://a85tract.github.io/QEC-Bank/

## What is in this release

| | count |
|---|---|
| code entries | 185 (166 at T1, 12 at T2, 6 at T3, 1 gold) |
| instances in the parameter table | 393 |
| entries in the full corpus (T2 and above) | 19 |
| QEC-Eval examples | 210, split into train, validation, and test by entry |

Every quantitative claim carries one of three origins.

- `verified` means the value was recomputed from the code's construction.
- `bounded` means only an upper or lower bound has been computed.
- `claimed(ref)` means the value comes from the cited reference and has not
  been recomputed.

Tiers describe how complete an entry is. A T1 entry has a verified formal core,
and the facets nobody has researched yet are marked as such. T2 entries are
researched. T3 entries cover the full reader packet (intuition, derivation,
reproduction, and a guided tour). Only the maintainers can mark an entry gold.

## Layout

| path | contents |
|---|---|
| `exports/formal-catalog-v2.jsonl` | one record per entry (185), with the card, instances, claims, and certificate ids |
| `exports/corpus-v3.jsonl` | the full corpus records for T2+ entries |
| `exports/graph-v2.json` | 37 typed relations between the 185 entries (special case of, product of, gauge fixes to, and others) |
| `exports/qec-eval-v2.json` | QEC-Eval, with tasks for formal-claim retrieval, rate calculation, and quantum Singleton checks |
| `exports/site-data-v2.jsonl`, `exports/site-routes-v2.json` | the data behind the site |
| `exports/comparison-v2.md` | the `[[n, k, d]]` table for all instances |
| `exports/site/` | the static site, deployed to GitHub Pages |
| `schemas/` | JSON Schemas for the records above |
| `registry/` | controlled vocabularies: categories, circuits, decoders, noise models, and references |

Each export is wrapped in a consumer envelope that names its schema and its
verification status. Schema and contract ids use the `qec-atlas-` prefix of the
tool that generates the data.

## License

The data are released under CC BY 4.0. Records bound to the
[Error Correction Zoo](https://errorcorrectionzoo.org) carry an `eczoo` source
binding, and the material taken or adapted from the Zoo stays under
CC BY-SA 4.0. See [LICENSE](LICENSE).

## Authors

Yuliang Xiong, Yicheng Guang, Xun Gao, Yueqi Chen
