/* Hall da Fama — person page v1. person.html?id=<slug> */

const $ = (s) => document.querySelector(s);
const MEDAL = { gold: "Ouro", silver: "Prata", bronze: "Bronze", "honorable-mention": "Menção honrosa" };
const NOTE = {
  "no-award": { text: "—", label: "Sem medalha (confirmado)" },
  "inferred-no-award": { text: "—", label: "Sem medalha (inferido da contagem oficial)" },
  unknown: { text: "", label: "Medalha ainda não atribuída individualmente" },
  pending: { text: "pendente", label: "Evento ainda não realizado / resultado pendente" },
};
const plural = (n, s, p) => `${n} ${n === 1 ? s : p}`;

function resultText(x) {
  if (x.medal) return MEDAL[x.medal];
  const n = NOTE[x.medalNote] || NOTE["no-award"];
  return n.text ? `<span class="muted" title="${n.label}">${n.text}</span>` : "";
}

async function boot() {
  const id = new URLSearchParams(location.search).get("id");
  let DATA, OL, SRC;
  try {
    [DATA, OL, SRC] = await Promise.all([
      fetch("data/people.json").then((r) => r.json()),
      fetch("data/olympiads.json").then((r) => r.json()),
      fetch("data/sources.json").then((r) => r.json()).catch(() => ({})),
    ]);
  } catch {
    $("#p-name").textContent = "Erro ao carregar os dados.";
    return;
  }
  const person = DATA.people.find((p) => p.id === id);
  if (!person) {
    $("#p-name").textContent = "Estudante não encontrado";
    $("#p-summary").textContent = "Verifique o endereço ou volte para a tabela.";
    return;
  }
  document.title = `${person.name} — Hall da Fama`;
  $("#p-name").textContent = person.name;
  if (person.nameVariants.length) {
    $("#p-variants").hidden = false;
    $("#p-variants").textContent = `grafias nas fontes: ${person.nameVariants.join(" · ")}`;
  }

  // summary
  const counts = { gold: 0, silver: 0, bronze: 0, "honorable-mention": 0 };
  for (const x of person.participations) if (x.medal) counts[x.medal]++;
  const years = person.participations.map((x) => x.year);
  const span = Math.min(...years) === Math.max(...years) ? `${years[0]}` : `${Math.min(...years)}–${Math.max(...years)}`;
  const medalBits = [
    counts.gold && plural(counts.gold, "ouro", "ouros"),
    counts.silver && plural(counts.silver, "prata", "pratas"),
    counts.bronze && plural(counts.bronze, "bronze", "bronzes"),
    counts["honorable-mention"] && plural(counts["honorable-mention"], "menção honrosa", "menções honrosas"),
  ].filter(Boolean).join(", ");
  const nOls = new Set(person.participations.map((x) => x.olympiad)).size;
  $("#p-summary").textContent =
    `${plural(person.participations.length, "participação", "participações")} · ` +
    `${plural(nOls, "olimpíada", "olimpíadas")} · ${span}` + (medalBits ? ` · ${medalBits}` : "");

  // teammate index: (olympiad|year) -> [people]
  const teamIdx = new Map();
  for (const p of DATA.people)
    for (const x of p.participations) {
      const k = `${x.olympiad}|${x.year}`;
      if (!teamIdx.has(k)) teamIdx.set(k, []);
      teamIdx.get(k).push(p);
    }

  $("#tbody").innerHTML = person.participations.map((x) => {
    const o = OL.olympiads[x.olympiad];
    const mates = (teamIdx.get(`${x.olympiad}|${x.year}`) || [])
      .filter((p) => p.id !== person.id)
      .sort((a, b) => a.searchKey.localeCompare(b.searchKey))
      .map((p) => `<a href="person.html?id=${p.id}">${p.name}</a>`)
      .join('<span class="sep"> · </span>');
    return `<tr>
      <td class="num">${x.year}</td>
      <td><span class="ols">${o.code}</span> <span class="muted olname">${o.name}</span></td>
      <td>${resultText(x)}</td>
      <td class="team">${mates}</td>
    </tr>`;
  }).join("");

  // Fontes section: per participation, the corroborating URLs for that edition
  const lines = [];
  const datasetLevel = new Map(); // olympiad -> entries (fallback "*")
  for (const x of person.participations) {
    const forOl = SRC[x.olympiad];
    if (!forOl) continue;
    if (forOl["*"]) { datasetLevel.set(x.olympiad, forOl["*"]); continue; }
    const entries = forOl[String(x.year)];
    if (!entries || !entries.length) continue;
    const links = entries
      .map((s) => `<a href="${s.u}" target="_blank" rel="noopener" title="${(s.c || "").replace(/"/g, "&quot;")}">${s.d}</a>`)
      .join('<span class="sep"> · </span>');
    lines.push(`<p><span class="src-key">${x.year} ${OL.olympiads[x.olympiad].code}</span> ${links}</p>`);
  }
  for (const [ol, entries] of datasetLevel) {
    const links = entries
      .map((s) => `<a href="${s.u}" target="_blank" rel="noopener" title="${(s.c || "").replace(/"/g, "&quot;")}">${s.d}</a>`)
      .join('<span class="sep"> · </span>');
    lines.push(`<p><span class="src-key">${OL.olympiads[ol].code}</span> ${links}</p>`);
  }
  if (lines.length) {
    $("#p-sources").hidden = false;
    $("#p-sources-list").innerHTML = lines.join("");
  }

}
boot();
