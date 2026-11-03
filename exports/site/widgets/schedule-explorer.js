/* schedule-explorer: renders periodic Pauli-measurement schedules from exported
   constructor data. It contains no entry-specific geometry or round logic. */
const ScheduleExplorer = (() => {
  "use strict";

  const COLORS = {
    X: "#c73737",
    Y: "#a26700",
    Z: "#2563a8",
    mixed: "#6b7280",
  };

  function fit(coords, width, height, pad) {
    const xs = coords.map(coord => coord[0]);
    const ys = coords.map(coord => coord[1]);
    const x0 = Math.min(...xs);
    const x1 = Math.max(...xs);
    const y0 = Math.min(...ys);
    const y1 = Math.max(...ys);
    const scale = Math.min(
      (width - 2 * pad) / Math.max(x1 - x0, 1e-9),
      (height - 2 * pad) / Math.max(y1 - y0, 1e-9)
    );
    return ([x, y]) => [
      pad + (x - x0) * scale,
      height - pad - (y - y0) * scale,
    ];
  }

  function centroid(points) {
    return [
      points.reduce((sum, point) => sum + point[0], 0) / points.length,
      points.reduce((sum, point) => sum + point[1], 0) / points.length,
    ];
  }

  function resizeCanvas(canvas) {
    const rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return false;
    if (!canvas.style.aspectRatio) {
      canvas.style.aspectRatio = `${canvas.width} / ${canvas.height}`;
    }
    const ratio = typeof window === "undefined"
      ? 1
      : Math.max(window.devicePixelRatio || 1, 1);
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

  function selectedRound(data, state) {
    const index = Math.max(0, Math.min(data.rounds.length - 1, state.round || 0));
    return data.rounds[index];
  }

  function visibleMeasurements(data, state) {
    return selectedRound(data, state).measurements.filter(measurement =>
      state.filter === "all" || measurement.type === state.filter
    );
  }

  function render(canvas, data, state) {
    resizeCanvas(canvas);
    const context = canvas.getContext("2d");
    const transform = fit(data.coords, canvas.width, canvas.height, 24);
    const measurements = selectedRound(data, state).measurements;
    context.clearRect(0, 0, canvas.width, canvas.height);

    measurements.forEach((measurement, index) => {
      if (state.filter !== "all" && measurement.type !== state.filter) return;
      const points = measurement.support.map(qubit => transform(data.coords[qubit]));
      if (!points.length) return;
      context.beginPath();
      context.moveTo(points[0][0], points[0][1]);
      points.slice(1).forEach(point => context.lineTo(point[0], point[1]));
      if (points.length > 2) context.closePath();
      context.strokeStyle = COLORS[measurement.type] || COLORS.mixed;
      context.lineWidth = state.highlight === index ? 5 : 3;
      context.globalAlpha = (
        state.highlight === null || state.highlight === undefined
        || state.highlight === index
      ) ? 1 : 0.2;
      context.stroke();
      context.globalAlpha = 1;
    });

    data.coords.forEach((coord, qubit) => {
      const [x, y] = transform(coord);
      context.beginPath();
      context.arc(x, y, 5, 0, 2 * Math.PI);
      context.fillStyle = "#20262b";
      context.fill();
      if (typeof context.fillText === "function") {
        context.fillStyle = "#4b5563";
        context.font = "11px ui-monospace, monospace";
        context.fillText(String(qubit), x + 7, y - 7);
      }
    });
  }

  function nearestMeasurement(canvas, data, state, mouseX, mouseY) {
    const transform = fit(data.coords, canvas.width, canvas.height, 24);
    const rect = canvas.getBoundingClientRect();
    const displayScale = rect.width && rect.height
      ? Math.max(canvas.width / rect.width, canvas.height / rect.height)
      : 1;
    let best = null;
    let bestDistance = (40 * displayScale) ** 2;
    selectedRound(data, state).measurements.forEach((measurement, index) => {
      if (state.filter !== "all" && measurement.type !== state.filter) return;
      const points = measurement.support.map(qubit => transform(data.coords[qubit]));
      if (!points.length) return;
      const [centerX, centerY] = centroid(points);
      const distance = (centerX - mouseX) ** 2 + (centerY - mouseY) ** 2;
      if (distance < bestDistance) {
        bestDistance = distance;
        best = index;
      }
    });
    return best;
  }

  function roundLabel(data, round) {
    const index = Math.max(0, Math.min(data.rounds.length - 1, round || 0));
    return (
      `Round ${index + 1} of ${data.rounds.length}`
      + ` · t mod ${data.rounds.length} = ${index}`
    );
  }

  function measurementDetail(data, state, measurementIndex) {
    if (measurementIndex === null || measurementIndex === undefined) {
      return "Hover a visible measurement edge to inspect its operator.";
    }
    const measurement = selectedRound(data, state).measurements[measurementIndex];
    if (!measurement) {
      return "Hover a visible measurement edge to inspect its operator.";
    }
    return (
      `${measurement.type} measurement ${measurement.index}; `
      + `qubits {${measurement.support.join(", ")}}; `
      + `operator ${measurement.pauli}.`
    );
  }

  function init() {
    const canvas = document.querySelector("[data-schedule-canvas]");
    if (
      !canvas
      || typeof ENTRY_DATA === "undefined"
      || !ENTRY_DATA.schedule
      || !ENTRY_DATA.schedule.rounds.length
    ) return;

    const data = ENTRY_DATA.schedule;
    const state = {round: 0, filter: "all", highlight: null};
    const roundInput = document.querySelector("[data-schedule-round]");
    const roundOutput = document.querySelector("[data-schedule-round-label]");
    const detail = document.querySelector("[data-schedule-detail]");

    function updateControls() {
      if (roundInput) {
        roundInput.min = "0";
        roundInput.max = String(data.rounds.length - 1);
        roundInput.step = "1";
        roundInput.value = String(state.round);
        roundInput.setAttribute("aria-valuetext", roundLabel(data, state.round));
      }
      if (roundOutput) roundOutput.textContent = roundLabel(data, state.round);
      if (detail) {
        detail.textContent = measurementDetail(data, state, state.highlight);
      }
      document.querySelectorAll("[data-schedule-filter]").forEach(button => {
        button.setAttribute(
          "aria-pressed",
          button.dataset.scheduleFilter === state.filter
        );
      });
    }

    function redraw() {
      render(canvas, data, state);
      updateControls();
    }

    function selectRound(round) {
      const period = data.rounds.length;
      state.round = ((round % period) + period) % period;
      state.highlight = null;
      redraw();
    }

    document.querySelectorAll("[data-schedule-filter]").forEach(button => {
      button.addEventListener("click", () => {
        state.filter = button.dataset.scheduleFilter;
        state.highlight = null;
        redraw();
      });
    });
    if (roundInput) {
      roundInput.addEventListener("input", () => {
        selectRound(Number.parseInt(roundInput.value, 10) || 0);
      });
    }
    const previous = document.querySelector("[data-schedule-prev]");
    const next = document.querySelector("[data-schedule-next]");
    if (previous) previous.addEventListener("click", () => selectRound(state.round - 1));
    if (next) next.addEventListener("click", () => selectRound(state.round + 1));
    canvas.addEventListener("mousemove", event => {
      const point = eventPoint(canvas, event);
      state.highlight = point === null
        ? null
        : nearestMeasurement(canvas, data, state, point[0], point[1]);
      redraw();
    });
    canvas.addEventListener("mouseleave", () => {
      state.highlight = null;
      redraw();
    });
    observeResize(canvas, () => {
      state.highlight = null;
      redraw();
    });

    redraw();
  }

  document.addEventListener("DOMContentLoaded", init);
  return {
    eventPoint,
    init,
    measurementDetail,
    nearestMeasurement,
    observeResize,
    render,
    resizeCanvas,
    roundLabel,
    visibleMeasurements,
  };
})();
