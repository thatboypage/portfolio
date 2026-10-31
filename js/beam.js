// Cantilever beam vibrating in its first three bending modes.
// Mode shapes are the exact Euler-Bernoulli cantilever solutions; the
// frequencies in the labels are BeamTwin's FEM results for a 1 m steel beam.
(function () {
  const svg = document.getElementById("beam");
  if (!svg) return;
  const path = svg.querySelector(".shape");
  const sensors = Array.from(svg.querySelectorAll(".sensor"));
  const label = document.getElementById("mode-label");
  const buttons = Array.from(document.querySelectorAll(".mode-picker button"));

  const MODES = [
    { bl: 1.8751, s: 0.7341, hz: "8.15 Hz", speed: 1.0 },
    { bl: 4.6941, s: 1.0185, hz: "51.10 Hz", speed: 1.6 },
    { bl: 7.8548, s: 0.9992, hz: "143.08 Hz", speed: 2.2 },
  ];
  const X0 = 60, X1 = 1060, Y0 = 130, AMP = 70, N = 120;
  let mode = 0, t0 = performance.now();

  function shape(m, u) {
    const b = m.bl * u;
    return Math.cosh(b) - Math.cos(b) - m.s * (Math.sinh(b) - Math.sin(b));
  }
  function norm(m) { return Math.abs(shape(m, 1)); }

  function draw(phase) {
    const m = MODES[mode], k = AMP / norm(m) * phase;
    let d = "";
    for (let i = 0; i <= N; i++) {
      const u = i / N;
      d += (i ? "L" : "M") + (X0 + u * (X1 - X0)).toFixed(1) + " " + (Y0 - k * shape(m, u)).toFixed(1);
    }
    path.setAttribute("d", d);
    sensors.forEach((c, i) => {
      const u = (i + 1) / sensors.length;
      c.setAttribute("cy", (Y0 - k * shape(m, u)).toFixed(1));
    });
  }

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function tick(now) {
    const m = MODES[mode];
    draw(Math.sin((now - t0) / 1000 * 2 * Math.PI * 0.45 * m.speed));
    requestAnimationFrame(tick);
  }

  function setMode(i) {
    mode = i;
    buttons.forEach((b, j) => b.setAttribute("aria-pressed", String(j === i)));
    if (label) label.textContent = MODES[i].hz;
    if (reduce) draw(1);
  }

  buttons.forEach((b, i) => b.addEventListener("click", () => setMode(i)));
  setMode(0);
  if (reduce) draw(1); else requestAnimationFrame(tick);
})();
