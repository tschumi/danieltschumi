(function () {
  /* ---------- Theme: no stored value = follow the system; "light"/"dark" = override ---------- */
  // the saved override is applied before first paint by an inline snippet in <head>
  var scheme = document.querySelector('meta[name="color-scheme"]');
  var themeColors = document.querySelectorAll('meta[name="theme-color"]');
  var lightBar = themeColors[0].content, darkBar = themeColors[1].content;
  var systemDark = matchMedia("(prefers-color-scheme: dark)");

  function applyTheme(override) {
    scheme.content = override || "light dark";
    // browser bar: pin both entries to the override, or restore the media-based pair
    themeColors[0].content = override === "dark" ? darkBar : lightBar;
    themeColors[1].content = override === "light" ? lightBar : darkBar;
  }
  applyTheme(scheme.content === "light dark" ? null : scheme.content);

  document.getElementById("theme").addEventListener("click", function () {
    var override = scheme.content === "light dark" ? null : scheme.content;
    var shownDark = override ? override === "dark" : systemDark.matches;
    var target = shownDark ? "light" : "dark";
    // flipping back to what the system shows anyway means "follow the system again", so forget the override
    if (target === (systemDark.matches ? "dark" : "light")) target = null;
    applyTheme(target);
    try { target ? localStorage.setItem("theme", target) : localStorage.removeItem("theme"); } catch (e) {}
  });
  // keep other open tabs in sync
  addEventListener("storage", function (e) { if (e.key === "theme") applyTheme(e.newValue); });

  var clock = document.getElementById("clock");
  function tick() {
    clock.textContent = new Intl.DateTimeFormat("de-CH", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Zurich" }).format(new Date());
  }
  tick(); setInterval(tick, 30000);
  document.getElementById("year").textContent = new Date().getFullYear();

  /* ---------- Avatar: eyes follow, blink, duck, curious brows ---------- */
  var svg = document.getElementById("avatar");
  var irises = Array.prototype.slice.call(svg.querySelectorAll(".iris"));
  // read live, so switching the OS setting while the page is open takes effect immediately
  var reduceMotion = matchMedia("(prefers-reduced-motion: reduce)");
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
    if (reduceMotion.matches || performance.now() - lastInput < 4000) return;
    var a = Math.random() * Math.PI * 2, r = Math.random() < .3 ? 0 : 1;
    target.x = Math.cos(a) * MAX_X * r; target.y = Math.sin(a) * MAX_Y * r;
  }, 2200);

  (function loop() {
    var k = reduceMotion.matches ? 1 : .18;
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
      if (!reduceMotion.matches && !svg.classList.contains("ducked")) blink(Math.random() < .25);
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
