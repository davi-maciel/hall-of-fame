(async function () {
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const [cov, ols] = await Promise.all([
    fetch("data/coverage.json").then((r) => r.json()),
    fetch("data/olympiads.json").then((r) => r.json()),
  ]);
  // olympiads flagged "hidden" in olympiads.json are held back from the site
  const shown = cov.olympiads.filter((o) => !(ols.olympiads[o.id] || {}).hidden);
  const withGaps = shown.filter((o) => o.gaps.length || o.caveat);
  const clean = shown.filter((o) => !o.gaps.length && !o.caveat);
  const fieldLabel = (f) => (ols.fields[f] && ols.fields[f].label) || f;
  let html = "";
  let lastField = null;
  for (const o of withGaps) {
    if (o.field !== lastField) {
      html += `<h2>${esc(fieldLabel(o.field))}</h2>`;
      lastField = o.field;
    }
    const gaps = o.gaps.map((g) => `<li>${g.year ? `<span class="num">${g.year}:</span> ` : ""}${esc(g.label)}</li>`).join("");
    html += `<section class="ol">
      <h3>${esc(o.code)} <span class="oname">${esc(o.name)}</span></h3>
      <p class="sub">${o.attended} ${o.attended === 1 ? "edição" : "edições"} (${esc(o.span)}) · ${o.complete} completa${o.complete === 1 ? "" : "s"}</p>
      ${gaps ? `<ul class="gaps">${gaps}</ul>` : ""}
      ${o.caveat ? `<p class="caveat">${esc(o.caveat)}</p>` : ""}
    </section>`;
  }
  if (clean.length) {
    html += `<h2>Sem lacunas conhecidas</h2><p class="sub">${clean.map((o) => `<a href="./?ols=${encodeURIComponent(o.id)}">${esc(o.code)}</a>`).join(" · ")}</p>`;
  }
  html += `<p class="sub foot">Atualizado em ${esc(cov.generatedAt)}. Encontrou uma fonte que preenche uma dessas lacunas? Me avise abrindo uma issue no <a href="https://github.com/davi-maciel/hall-of-fame/issues" target="_blank" rel="noopener">repositório</a>.</p>`;
  $("#coverage").innerHTML = html;
})();
