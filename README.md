# QEC-Bank

QEC-Bank is a machine-checked dataset of quantum error-correcting codes. Each
entry records a code family, its concrete instances, their parameters, and
where every number comes from.

**Browse the data:** https://a85tract.github.io/QEC-Bank/

**Tutorials:** https://a85tract.github.io/QEC-Bank-Academy/ ([source](https://github.com/a85tract/QEC-Bank-Academy))

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

## Rebuilding a code

The constructors need Python 3.12 or later with `numpy`, `pyyaml`, and
`jsonschema`. From the repository root:

```python
import importlib.util, yaml
from qeclib.distance import exact_distance

spec = importlib.util.spec_from_file_location("surface", "codes/surface/constructor.py")
surface = importlib.util.module_from_spec(spec)
spec.loader.exec_module(surface)

cm = surface.build(L=3)["checkmatrix"]
print(cm.n, cm.k, exact_distance(cm)[0])   # 13 1 3
```

Each `codes/<id>/instances.yaml` lists the parameters of the recorded
instances and their claims, so every `verified` value of n, k, and d for these
codes can be recomputed this way.

## License

The data are released under CC BY 4.0, and the Python source code under
Apache-2.0 (see [LICENSE-APACHE](LICENSE-APACHE)). Records bound to the
[Error Correction Zoo](https://errorcorrectionzoo.org) carry an `eczoo` source
binding, and the material taken or adapted from the Zoo stays under
CC BY-SA 4.0. See [LICENSE](LICENSE).

## Authors

Yuliang Xiong, Yicheng Guang, Xun Gao, Yueqi Chen
