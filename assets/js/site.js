(function () {
  var root = document.documentElement;  // saved theme is applied early by an inline snippet in <head>
  document.getElementById("theme").addEventListener("click", function () {
    var dark = root.dataset.theme
      ? root.dataset.theme === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("theme", root.dataset.theme); } catch (e) {}
  });

  var clock = document.getElementById("clock");
  function tick() {
    clock.textContent = new Intl.DateTimeFormat("de-CH", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Zurich" }).format(new Date());
  }
  tick(); setInterval(tick, 30000);
  document.getElementById("year").textContent = new Date().getFullYear();

  /* ---------- Avatar: eyes follow, blink, duck, curious brows ---------- */
  var svg = document.getElementById("avatar");
  var irises = Array.prototype.slice.call(svg.querySelectorAll(".iris"));
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var MAX_X = 9, MAX_Y = 3;
  var target = { x: 0, y: 0 }, cur = { x: 0, y: 0 }, lastInput = 0;

  function aimAt(clientX, clientY) {
    var ctm = svg.getScreenCTM(); if (!ctm) return;
    // midpoint between both eyes, in screen coords
    var cx = 200 * ctm.a + 257 * ctm.c + ctm.e, cy = 200 * ctm.b + 257 * ctm.d + ctm.f;
    var dx = clientX - cx, dy = clientY - cy;
    var dist = Math.hypot(dx, dy) || 1;
    var f = Math.min(dist / 220, 1);
    target.x = dx / dist * MAX_X * f;
    target.y = dy / dist * MAX_Y * f;
    lastInput = performance.now();
  }
  addEventListener("pointermove", function (e) { aimAt(e.clientX, e.clientY); }, { passive: true });
  addEventListener("touchstart", function (e) { var t = e.touches[0]; aimAt(t.clientX, t.clientY); }, { passive: true });

  // look around on its own when nobody is moving the mouse
  setInterval(function () {
    if (reduce || performance.now() - lastInput < 4000) return;
    var a = Math.random() * Math.PI * 2, r = Math.random() < .3 ? 0 : 1;
    target.x = Math.cos(a) * MAX_X * r; target.y = Math.sin(a) * MAX_Y * r;
  }, 2200);

  (function loop() {
    var k = reduce ? 1 : .18;
    cur.x += (target.x - cur.x) * k; cur.y += (target.y - cur.y) * k;
    // snap to whole pixels: pupils sit left, centre or right (2 art pixels = 10 units)
    var px = cur.x > 3 ? 10 : cur.x < -3 ? -10 : 0;
    var t = "translate(" + px + " 0)";
    irises.forEach(function (el) { el.setAttribute("transform", t); });
    requestAnimationFrame(loop);
  })();

  // blink every few seconds, sometimes twice
  function blink(again) {
    svg.classList.add("blink");
    setTimeout(function () {
      svg.classList.remove("blink");
      if (again) setTimeout(function () { blink(false); }, 160);
    }, 130);
  }
  (function scheduleBlink() {
    setTimeout(function () {
      if (!reduce && !svg.classList.contains("ducked")) blink(Math.random() < .25);
      scheduleBlink();
    }, 2500 + Math.random() * 3500);
  })();

  // hover (or tap) the illustration: duck behind the laptop
  var popTimer;
  svg.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") svg.classList.add("ducked"); });
  svg.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") svg.classList.remove("ducked"); });
  svg.addEventListener("click", function (e) {
    if (e.pointerType === "mouse") return;
    svg.classList.add("ducked");
    clearTimeout(popTimer);
    popTimer = setTimeout(function () { svg.classList.remove("ducked"); }, 1200);
  });

  // raise eyebrows when a link is hovered or focused
  document.querySelectorAll(".links a").forEach(function (a) {
    a.addEventListener("pointerenter", function () { svg.classList.add("curious"); });
    a.addEventListener("pointerleave", function () { svg.classList.remove("curious"); });
    a.addEventListener("focus", function () { svg.classList.add("curious"); });
    a.addEventListener("blur", function () { svg.classList.remove("curious"); });
  });
})();
