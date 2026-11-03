from qeclib.checkmatrix import CheckMatrix
from qeclib.constructions import hgp, rep_parity

def _lattice(L, HX, HZ):
    coords = []
    for a in range(L):            # block 1: L*L "vertex" qubits at even coords
        for b in range(L):
            coords.append([2 * b, 2 * a])
    for a in range(L - 1):        # block 2: (L-1)^2 "face" qubits at odd coords
        for b in range(L - 1):
            coords.append([2 * b + 1, 2 * a + 1])
    checks = []
    for row in HX:
        checks.append({"type": "X", "support": [int(q) for q in row.nonzero()[0]]})
    for row in HZ:
        checks.append({"type": "Z", "support": [int(q) for q in row.nonzero()[0]]})
    return {"coords": coords, "checks": checks}

def build(L: int = 3):
    """Planar (unrotated) surface code as HGP(rep_L, rep_L): [[L^2+(L-1)^2, 1, L]]."""
    H = rep_parity(L)
    HX, HZ = hgp(H, H)
    cm = CheckMatrix.from_css(HX, HZ)
    cm.validate()
    return {"checkmatrix": cm, "lattice": _lattice(L, HX, HZ)}
