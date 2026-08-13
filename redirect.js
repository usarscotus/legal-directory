(() => {
  const legacyBase = "/legal-directory";
  const destinationBase = "https://nationalarchivesusar.github.io/courts";

  function destinationFor(currentLocation) {
    const pathname = String(currentLocation.pathname || "");
    let suffix = "/";

    if (pathname === legacyBase || pathname === `${legacyBase}/`) {
      suffix = "/";
    } else if (pathname.startsWith(`${legacyBase}/`)) {
      suffix = pathname.slice(legacyBase.length);
    }

    const target = new URL(`${destinationBase}${suffix}`);
    target.search = currentLocation.search || "";
    target.hash = currentLocation.hash || "";
    return target;
  }

  const target = destinationFor(window.location);
  const fallback = document.getElementById("redirect-link");
  const canonical = document.getElementById("canonical-link");
  if (fallback) fallback.href = target.href;
  if (canonical) canonical.href = target.href;

  window.location.replace(target.href);
})();

