/* lattice-explorer: renders any entry's lattice from data alone (spec decision 18).
   Pure function of (data, state); no per-code logic may ever appear in this file. */
const LatticeExplorer = (() => {
  const COLORS = { X: "rgba(214, 39, 40, 0.35)", Z: "rgba(31, 119, 180, 0.35)" };
  const EDGE = { X: "#d62728", Z: "#1f77b4" };

  function fit(coords, w, h, pad) {
    const xs = coords.map(c => c[0]), ys = coords.map(c => c[1]);
    const [x0, x1] = [Math.min(...xs), Math.max(...xs)];
    const [y0, y1] = [Math.min(...ys), Math.max(...ys)];
    const s = Math.min((w - 2 * pad) / Math.max(x1 - x0, 1e-9),
                       (h - 2 * pad) / Math.max(y1 - y0, 1e-9));
    return ([x, y]) => [pad + (x - x0) * s, h - pad - (y - y0) * s];
  }

  function centroid(pts) {
    const n = pts.length;
    return [pts.reduce((a, p) => a + p[0], 0) / n, pts.reduce((a, p) => a + p[1], 0) / n];
  }

  function resizeCanvas(canvas) {
    const rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return false;
    if (!canvas.style.aspectRatio) {
      canvas.style.aspectRatio = `${canvas.width} / ${canvas.height}`;
    }
    const ratio = typeof window === "undefined" ? 1 : Math.max(window.devicePixelRatio || 1, 1);
    const width = Math.max(1, Math.round(rect.width * ratio));
    const height = Math.max(1, Math.round(rect.height * ratio));
    if (canvas.width === width && canvas.height === height) return false;
    canvas.width = width;
    canvas.height = height;
    return true;
  }

  function observeResize(canvas, redraw) {
    const onResize = () => {
      if (resizeCanvas(canvas)) redraw();
    };
    if (typeof ResizeObserver !== "undefined") {
      const observer = new ResizeObserver(onResize);
      observer.observe(canvas);
      return () => observer.disconnect();
    }
    if (typeof window !== "undefined") {
      window.addEventListener("resize", onResize);
      return () => window.removeEventListener("resize", onResize);
    }
    return () => {};
  }

  function eventPoint(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return null;
    return [
      (event.clientX - rect.left) * canvas.width / rect.width,
      (event.clientY - rect.top) * canvas.height / rect.height,
    ];
  }

  function render(canvas, data, state) {
    resizeCanvas(canvas);
    const ctx = canvas.getContext("2d");
    const T = fit(data.coords, canvas.width, canvas.height, 24);
    const dimAlpha = Number.isFinite(data.dimAlpha)
      ? Math.max(0, Math.min(1, data.dimAlpha))
      : 0.25;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    data.checks.forEach((ch, i) => {
      if (state.filter !== "all" && ch.type !== state.filter) return;
      const pts = ch.support.map(q => T(data.coords[q]));
      const [cx, cy] = centroid(pts);
      const ordered = pts.slice().sort((a, b) =>
        Math.atan2(a[1] - cy, a[0] - cx) - Math.atan2(b[1] - cy, b[0] - cx));
      ctx.beginPath();
      ordered.forEach((p, j) => (j ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])));
      ctx.closePath();
      ctx.fillStyle = COLORS[ch.type] || "rgba(128,128,128,0.3)";
      ctx.strokeStyle = EDGE[ch.type] || "#888";
      ctx.lineWidth = state.highlight === i ? 3 : 1;
      ctx.globalAlpha = state.highlight === null || state.highlight === i ? 1 : dimAlpha;
      ctx.fill();
      ctx.stroke();
      ctx.globalAlpha = 1;
    });
    data.coords.forEach(c => {
      const [x, y] = T(c);
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, 2 * Math.PI);
      ctx.fillStyle = "#222";
      ctx.fill();
    });
  }

  function nearestCheck(canvas, data, state, mx, my) {
    const T = fit(data.coords, canvas.width, canvas.height, 24);
    const rect = canvas.getBoundingClientRect();
    const displayScale = rect.width && rect.height
      ? Math.max(canvas.width / rect.width, canvas.height / rect.height)
      : 1;
    let best = null, bestD = (40 * displayScale) ** 2;
    data.checks.forEach((ch, i) => {
      if (state.filter !== "all" && ch.type !== state.filter) return;
      const [cx, cy] = centroid(ch.support.map(q => T(data.coords[q])));
      const d = (cx - mx) ** 2 + (cy - my) ** 2;
      if (d < bestD) { bestD = d; best = i; }
    });
    return best;
  }

  function configuredHighlight(data, filter) {
    const candidate = data.focusByFilter?.[filter]
      ?? (
        data.initialState?.filter === filter
          ? data.initialState.highlight
          : null
      );
    if (!Number.isInteger(candidate) || candidate < 0 || candidate >= data.checks.length) {
      return null;
    }
    const check = data.checks[candidate];
    return filter === "all" || check.type === filter ? candidate : null;
  }

  function visibleChecks(data, filter) {
    return data.checks
      .map((check, index) => ({check, index}))
      .filter(({check}) => filter === "all" || check.type === filter)
      .map(({index}) => index);
  }

  function checkDetail(data, index) {
    if (!Number.isInteger(index) || !data.checks[index]) {
      return "Point, tap, or focus the lattice and use arrow keys to inspect a check.";
    }
    const check = data.checks[index];
    return `${check.type}-check ${index}; support {${check.support.join(", ")}}.`;
  }

  function init() {
    const canvas = document.querySelector("[data-lattice-canvas]");
    if (!canvas || typeof ENTRY_DATA === "undefined" || !ENTRY_DATA.lattice) return;
    const data = ENTRY_DATA.lattice;
    const detail = document.querySelector("[data-lattice-detail]");
    const requestedFilter = data.initialState?.filter;
    const filter = ["all", "X", "Z"].includes(requestedFilter)
      ? requestedFilter
      : "all";
    const state = {
      highlight: configuredHighlight(data, filter),
      filter,
      hover: null,
      selected: null,
    };

    const updateFilters = () => {
      document.querySelectorAll("[data-lattice-filter]").forEach(button => {
        button.setAttribute("aria-pressed", button.dataset.latticeFilter === state.filter);
      });
    };

    const activeHighlight = () => (
      state.hover
      ?? state.selected
      ?? configuredHighlight(data, state.filter)
    );
    const redraw = () => {
      state.highlight = activeHighlight();
      render(canvas, data, state);
      if (detail) detail.textContent = checkDetail(data, state.highlight);
    };
    const itemAtEvent = event => {
      const point = eventPoint(canvas, event);
      return point === null
        ? null
        : nearestCheck(canvas, data, state, point[0], point[1]);
    };
    const selectRelative = delta => {
      const indices = visibleChecks(data, state.filter);
      if (!indices.length) return;
      const current = state.selected ?? state.highlight;
      const position = indices.indexOf(current);
      const next = position < 0
        ? (delta < 0 ? indices.length - 1 : 0)
        : (position + delta + indices.length) % indices.length;
      state.selected = indices[next];
      state.hover = null;
      redraw();
    };

    redraw();
    updateFilters();
    canvas.addEventListener("mousemove", e => {
      state.hover = itemAtEvent(e);
      redraw();
    });
    canvas.addEventListener("mouseleave", () => {
      state.hover = null;
      redraw();
    });
    canvas.addEventListener("pointerup", e => {
      const nearest = itemAtEvent(e);
      if (nearest === null) return;
      state.selected = nearest;
      state.hover = null;
      redraw();
      canvas.focus();
    });
    canvas.addEventListener("focus", () => {
      if (state.highlight === null) {
        state.selected = visibleChecks(data, state.filter)[0] ?? null;
      }
      redraw();
    });
    canvas.addEventListener("keydown", e => {
      if (e.key === "ArrowRight" || e.key === "ArrowDown") {
        e.preventDefault();
        selectRelative(1);
      } else if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
        e.preventDefault();
        selectRelative(-1);
      } else if (e.key === "Home" || e.key === "End") {
        e.preventDefault();
        const indices = visibleChecks(data, state.filter);
        state.selected = e.key === "Home"
          ? (indices[0] ?? null)
          : (indices[indices.length - 1] ?? null);
        state.hover = null;
        redraw();
      } else if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        state.selected = state.highlight;
        state.hover = null;
        redraw();
      } else if (e.key === "Escape") {
        state.selected = null;
        state.hover = null;
        redraw();
      }
    });
    document.querySelectorAll("[data-lattice-filter]").forEach(btn =>
      btn.addEventListener("click", () => {
        state.filter = btn.dataset.latticeFilter;
        state.hover = null;
        state.selected = null;
        updateFilters();
        redraw();
      }));
    observeResize(canvas, () => {
      redraw();
    });
  }

  document.addEventListener("DOMContentLoaded", init);
  return {
    configuredHighlight,
    checkDetail,
    eventPoint,
    init,
    nearestCheck,
    observeResize,
    render,
    resizeCanvas,
    visibleChecks,
  };
})();
