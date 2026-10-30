import { chainConvert, chartRows, currencyOptions, dollarsToday, fmtAmount, fmtRate, fmtUsd, log10, parseAmount, thenConvert, zerosOf } from "./engine.js";

const [table, countries, rates, history] = await Promise.all([
  fetch("data/redenominations.json").then((r) => r.json()),
  fetch("data/countries.json").then((r) => r.json()),
  fetch("data/rates.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
  fetch("data/history.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
]);

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const chainOf = (iso) => countries.countries.find((x) => x.iso === iso);

// ---------- shareable state in the URL ----------
// #c=BR.0.1000000&t=IND.1980.1000  (country.currencyIndex.amount / country.year.amount)
const urlState = Object.fromEntries(location.hash.replace(/^#/, "").split("&").filter(Boolean).map((kv) => kv.split("=")));
let hashTimer;
function writeState() {
  const c = `${cCountry.value}.${cFrom.value}.${parseAmount(cAmount.value) || 0}`;
  const t = history ? `${$("#t-country").value}.${$("#t-year").value}.${parseAmount($("#t-amount").value) || 0}` : "";
  clearTimeout(hashTimer);
  hashTimer = setTimeout(() => history_replace(`#c=${c}${t ? `&t=${t}` : ""}`), 150);
}
function history_replace(hash) { if (location.hash !== hash) window.history.replaceState(null, "", hash); }

// ---------- coverage ----------
$("#coverage").innerHTML = `${table.rows.filter((r) => r.year >= 1945).length} reforms since 1945 in the table, ` +
  `${table.count} in all · <b>${countries.verified} countries</b> with a fully cited chain from 1945, ` +
  `${countries.partial} partial · ${countries.countries.length} of roughly 195 countries covered so far`;

// ---------- converter ----------
const cCountry = $("#c-country"), cFrom = $("#c-from"), cAmount = $("#c-amount");
for (const c of countries.countries) {
  const o = document.createElement("option");
  o.value = c.iso; o.textContent = `${c.name}${c.status === "partial" ? " (partial)" : ""}`;
  cCountry.append(o);
}
function fillCurrencies(selectIdx = 0) {
  const c = chainOf(cCountry.value);
  cFrom.innerHTML = "";
  for (const cur of currencyOptions(c)) {
    const o = document.createElement("option");
    o.value = cur.idx; o.textContent = `${cur.name} (${cur.from}${cur.idx === c.steps.length ? " – today" : ""})`;
    cFrom.append(o);
  }
  cFrom.value = String(Math.min(selectIdx, c.steps.length));
  convert();
}
function convert() {
  const c = chainOf(cCountry.value);
  const amount = parseAmount(cAmount.value);
  const stepsEl = $("#c-steps"), out = $("#c-result");
  if (!Number.isFinite(amount)) { out.textContent = "Enter an amount."; stepsEl.innerHTML = ""; return; }
  const r = chainConvert(c, Number(cFrom.value), amount);
  stepsEl.innerHTML = r.trail.map(({ step: s, applied }) => applied
    ? `<li>${s.year}: ${esc(s.old)} → ${esc(s.new)} <span class="rate">÷ ${fmtRate(s.rate)}</span>${s.source ? "" : ' <span class="uncited">(not yet cited)</span>'}</li>`
    : `<li class="uncited">${s.year}: ${esc(s.old)} → ${esc(s.new)} — no fixed conversion; the chain stops here.</li>`).join("");
  if (r.noop) { out.innerHTML = `${fmtAmount(amount)} ${esc(r.from)} is already the current unit.` + usdHtml(c, r); writeState(); return; }
  out.innerHTML = `${fmtAmount(amount)} ${esc(r.from)} ${r.broken ? "was last convertible as" : "="}<span class="big">${fmtAmount(r.value)} ${esc(r.unit)}</span>` +
    `<span class="zeros">${r.zeros ? `${Number.isInteger(r.zeros) ? r.zeros : r.zeros.toFixed(2)} zeros removed over ${r.applied} reform${r.applied === 1 ? "" : "s"}` : "no zeros removed"}` +
    `${r.uncited ? " · includes a step that is not yet cited" : ""}${r.broken ? " · the chain has no fixed rate past this point" : ""}</span>`;
  out.innerHTML += usdHtml(c, r);
  writeState();
}
function usdHtml(c, r) {
  const d = dollarsToday(c, r, rates);
  if (d) {
    return `<div class="usd">≈ <b>${fmtUsd(d.usd)}</b> at the rate of ${esc(d.date)} (${d.perUsd.toLocaleString("en-US", { maximumFractionDigits: 4 })} ${d.code} per US dollar). ` +
      `One dollar today buys ${fmtAmount(d.oneDollarBuys)} ${esc(r.from)}.` +
      `${["VES", "ARS", "BOB"].includes(d.code) ? " This is the published rate; a parallel street rate may differ." : ""}` +
      ` <a href="${esc(d.source.url)}">Rate source</a>.</div>`;
  }
  return "";
}
cCountry.addEventListener("change", () => fillCurrencies());
cFrom.addEventListener("change", convert);
cAmount.addEventListener("input", convert);
$("#convert-form").addEventListener("submit", (e) => e.preventDefault());
{
  const [iso, idx, amt] = (urlState.c ?? "").split(".");
  cCountry.value = chainOf(iso) ? iso : "BR";
  if (amt && Number.isFinite(+amt)) cAmount.value = (+amt).toLocaleString("en-US", { maximumFractionDigits: 6 });
  fillCurrencies(Number(idx) || 0);
}

// ---------- chart ----------
const DECADES = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020];
const DECADE_COLOURS = { 1940: "#5b4a2f", 1950: "#8a6d3b", 1960: "#b8860b", 1970: "#c2651a", 1980: "#9b2d20", 1990: "#7b4b94", 2000: "#1f5f8b", 2010: "#2f6b3a", 2020: "#3f7f7f" };
let chartShowAll = false, chartSort = "zeros";
function chart() {
  let rows = chartRows(countries.countries);
  if (chartSort === "recent") rows = [...rows].sort((a, b) => b.segs[b.segs.length - 1].step.year - a.segs[a.segs.length - 1].step.year);
  if (chartSort === "name") rows = [...rows].sort((a, b) => a.c.name.localeCompare(b.c.name));
  const shown = chartShowAll ? rows : rows.slice(0, 20);
  const maxZ = Math.ceil(Math.max(...rows.map((r) => r.total)) / 5) * 5;
  const ticks = [];
  for (let z = 0; z <= maxZ; z += 5) ticks.push(`<span style="left:${(z / maxZ) * 100}%">${z}</span>`);
  let html = `<div class="bars" role="img" aria-label="Zeros removed per country since 1945, one segment per reform">` +
    `<div class="bar-row axis-row"><span class="bar-name"></span><span class="bar-track axis">${ticks.join("")}</span><span class="bar-total">zeros</span></div>`;
  for (const r of shown) {
    const label = r.c.name.replace(/ \(.*\)/, "");
    let segs = "";
    for (const sg of r.segs) {
      const decade = Math.floor(sg.step.year / 10) * 10;
      const tip = `${r.c.name} — ${sg.step.year}: ${sg.step.old} → ${sg.step.new}, ÷ ${sg.step.rate.toLocaleString("en-US")} (${sg.z % 1 ? sg.z.toFixed(2) : sg.z} zeros)${sg.uncited ? " · not yet cited" : ""}`;
      if (sg.z === 0) { segs += `<i class="tick" data-tip="${esc(tip)} — at par" title="${esc(tip)} — at par"></i>`; continue; }
      segs += `<i class="seg${sg.uncited ? " uncited" : ""}" style="width:${(sg.z / maxZ) * 100}%;background:${DECADE_COLOURS[decade] ?? "#888"}" data-tip="${esc(tip)}" title="${esc(tip)}"></i>`;
    }
    html += `<div class="bar-row"><span class="bar-name" title="${esc(r.c.name)}">${esc(label)}</span><span class="bar-track" style="background-size:${100 / (maxZ / 5)}% 100%">${segs}</span>` +
      `<span class="bar-total">${r.total % 1 ? r.total.toFixed(1) : r.total}${r.c.status === "partial" ? " ·" : ""}</span></div>`;
  }
  html += "</div>";
  html += `<div class="legend">${DECADES.filter((d) => shown.some((r) => r.segs.some((sg) => Math.floor(sg.step.year / 10) * 10 === d)))
    .map((d) => `<span><i style="background:${DECADE_COLOURS[d]}"></i>${d}s</span>`).join("")}<span><i style="border:1px dashed var(--red)"></i>not yet cited</span><span>· partial chain</span></div>`;
  $("#chart").innerHTML = html;
  $("#chart-more").textContent = chartShowAll ? "Show the top 20" : `Show all ${rows.length} countries`;
}
chart();
$("#chart-more").addEventListener("click", () => { chartShowAll = !chartShowAll; chart(); });
$("#chart-sort").addEventListener("change", (e) => { chartSort = e.target.value; chart(); });
{
  const tip = $("#tip");
  $("#chart").addEventListener("pointerover", (e) => {
    const t = e.target.closest("[data-tip]"); if (!t) return;
    tip.textContent = t.dataset.tip; tip.hidden = false;
  });
  $("#chart").addEventListener("pointermove", (e) => { tip.style.left = `${Math.min(e.clientX + 12, innerWidth - 300)}px`; tip.style.top = `${e.clientY + 14}px`; });
  $("#chart").addEventListener("pointerout", () => { tip.hidden = true; });
}

// ---------- table ----------
let tableSort = { key: "year", dir: 1 };
function renderTable() {
  const q = $("#filter").value.trim().toLowerCase();
  const all = $("#all-years").checked;
  const rows = table.rows.filter((r) => (all || r.year >= 1945) && (!q || `${r.country} ${r.old} ${r.new}`.toLowerCase().includes(q)));
  const k = tableSort.key;
  rows.sort((a, b) => (k === "rate" ? a.rate - b.rate : k === "year" ? a.year - b.year || a.country.localeCompare(b.country) : String(a[k]).localeCompare(String(b[k]))) * tableSort.dir);
  const maxZ = 30;
  $("#table tbody").innerHTML = rows.map((r) => {
    const z = zerosOf(r.rate);
    return `<tr class="${r.year < 1945 ? "old" : ""}"><td>${r.year}</td><td>${esc(r.country)}</td><td>${esc(r.old)}</td><td>${esc(r.new)}</td>` +
      `<td class="num">${r.approximate ? "≈ " : ""}${r.at_par ? "at par" : fmtRate(r.rate)}</td>` +
      `<td class="num"><span class="zeros-bar" style="width:${(z / maxZ) * 60}px"></span>${z ? (Number.isInteger(z) ? z : z.toFixed(1)) : "–"}</td></tr>`;
  }).join("");
  $("#table-count").textContent = `${rows.length} reform${rows.length === 1 ? "" : "s"}`;
  for (const th of document.querySelectorAll("#table th[data-sort]")) {
    th.setAttribute("aria-sort", th.dataset.sort === k ? (tableSort.dir > 0 ? "ascending" : "descending") : "none");
  }
}
$("#filter").addEventListener("input", renderTable);
$("#all-years").addEventListener("change", renderTable);
$("#table thead").addEventListener("click", (e) => {
  const th = e.target.closest("th[data-sort]"); if (!th) return;
  const key = th.dataset.sort;
  tableSort = { key, dir: tableSort.key === key ? -tableSort.dir : (key === "rate" ? -1 : 1) };
  renderTable();
});
renderTable();

// ---------- chains ----------
function renderChains() {
  const q = $("#chain-filter").value.trim().toLowerCase();
  const list = countries.countries.filter((c) => !q || c.name.toLowerCase().includes(q) || c.steps.some((s) => `${s.old} ${s.new}`.toLowerCase().includes(q)));
  $("#chain-count").textContent = `${list.length} of ${countries.countries.length} · ${countries.verified} verified`;
  $("#chains").innerHTML = list.map((c) => `
  <details class="chain" id="chain-${c.iso}">
    <summary><h3>${esc(c.name)}</h3><span class="badge ${c.status}">${c.status}</span>
      <span class="factor">${c.steps.length ? `${c.steps.length} step${c.steps.length === 1 ? "" : "s"}` : "no change"}${c.total_factor > 1 ? ` · ${Math.round(log10(c.total_factor))} zeros` : ""}</span></summary>
    <ol>${c.steps.map((s) => `<li>${s.year}: ${esc(s.old)} → ${esc(s.new)}, ${s.rate ? (s.rate === 1 ? "at par" : `${fmtRate(s.rate)} old per new`) : "no fixed rate"}` +
      `${s.note ? `<div class="note">${esc(s.note)}</div>` : ""}` +
      `<div>${s.source ? `<cite>Source: <a href="${esc(s.source.url)}">${esc(s.source.title)}</a></cite>` : `<cite class="uncited" style="color:var(--red)">Not yet cited</cite>`}</div></li>`).join("")}</ol>
    ${c.steps.length ? "" : `<p>The ${esc(c.currency)} has been the currency since ${c.start}, with no change of unit.${c.basis ? ` <cite>Source: <a href="${esc(c.basis.url)}">${esc(c.basis.title)}</a></cite>` : ""}</p>`}
    ${c.gap ? `<p class="gap">${esc(c.gap)}</p>` : ""}
    <p class="chain-links"><a href="#c=${c.iso}.0.1000000">Convert from this country</a></p>
  </details>`).join("");
}
$("#chain-filter").addEventListener("input", renderChains);
renderChains();
// Apply a "#c=…" or "#t=…" state (from an example link, a pasted link or the back button).
function applyState(part, scroll) {
  const amount = (a) => (+a).toLocaleString("en-US", { maximumFractionDigits: 6 });
  if (part.startsWith("c=")) {
    const [iso, idx, amt] = part.slice(2).split(".");
    if (!chainOf(iso)) return;
    cCountry.value = iso;
    if (amt && Number.isFinite(+amt)) cAmount.value = amount(amt);
    fillCurrencies(Number(idx) || 0);
    if (scroll) $("#converter").scrollIntoView({ behavior: "smooth", block: "start" });
  } else if (part.startsWith("t=") && history) {
    const [iso, year, amt] = part.slice(2).split(".");
    if (!history.countries[iso]) return;
    $("#t-country").value = iso;
    if (year && Number.isFinite(+year)) $("#t-year").value = year;
    if (amt && Number.isFinite(+amt)) $("#t-amount").value = amount(amt);
    $("#t-country").dispatchEvent(new Event("change"));
    if (scroll) $("#then").scrollIntoView({ behavior: "smooth", block: "start" });
  }
}
document.addEventListener("click", (e) => {
  const a = e.target.closest("a[href^='#c='], a[href^='#t=']"); if (!a) return;
  e.preventDefault();
  applyState(a.getAttribute("href").slice(1), true);
});
// replaceState (used by writeState) does not fire hashchange, so this only runs on real navigation.
window.addEventListener("hashchange", () => {
  const parts = location.hash.replace(/^#/, "").split("&").filter(Boolean);
  parts.forEach((p, i) => applyState(p, i === parts.length - 1 && parts.length === 1));
});

// ---------- at the time ----------
if (history) {
  const tCountry = $("#t-country"), tYear = $("#t-year"), tAmount = $("#t-amount");
  const chainByWb = Object.fromEntries(countries.countries.filter((c) => c.wb).map((c) => [c.wb, c]));
  const list = Object.entries(history.countries).map(([iso, c]) => ({ iso, name: c.name })).sort((a, b) => a.name.localeCompare(b.name));
  for (const c of list) { const o = document.createElement("option"); o.value = c.iso; o.textContent = c.name; tCountry.append(o); }
  const cpiLatest = Math.max(...Object.keys(history.us_cpi).map(Number));
  tYear.max = String(cpiLatest + 2);

  function renderThen() {
    const iso = tCountry.value, year = Math.round(Number(tYear.value));
    const r = thenConvert({ history, chain: chainByWb[iso], tableRows: table.rows }, iso, year, parseAmount(tAmount.value));
    const out = $("#t-result");
    $("#t-unit").textContent = r.unit && r.unit.name !== "local currency" ? `in ${r.unit.name}` : "";
    if (!r.ok) {
      out.innerHTML = `${esc(r.reason)}${r.detail ? `<span class="fine">${esc(r.detail)}</span>` : ""}`;
      writeState();
      return;
    }
    out.innerHTML = `${fmtAmount(parseAmount(tAmount.value))} ${esc(r.unitLabel)} in ${year} =` +
      `<span class="big">${fmtUsd(r.usdThen)} in ${year} dollars</span>` +
      `<span class="zeros">about <b>${fmtUsd(r.usdNow)}</b> in ${r.cpiLatest} dollars (US consumer prices rose ${r.inflation.toFixed(1)}× since ${year})` +
      ` · average official rate in ${year}: ${r.rate >= 0.01 ? r.rate.toLocaleString("en-US", { maximumFractionDigits: 4 }) : r.rate.toExponential(3)} ${chainByWb[iso] ? "current units" : "local units"} per dollar</span>` +
      `<span class="fine">${r.warnings.map(esc).join(" ")} <a href="${esc(history.source.url)}">Source</a>, fetched ${esc(history.fetched)}.</span>`;
    writeState();
  }
  tCountry.addEventListener("change", renderThen);
  tYear.addEventListener("input", renderThen);
  tAmount.addEventListener("input", renderThen);
  $("#then-form").addEventListener("submit", (e) => e.preventDefault());
  const [iso, year, amt] = (urlState.t ?? "").split(".");
  tCountry.value = history.countries[iso] ? iso : "IND";
  if (year && Number.isFinite(+year)) tYear.value = year;
  if (amt && Number.isFinite(+amt)) tAmount.value = (+amt).toLocaleString("en-US", { maximumFractionDigits: 6 });
  renderThen();
  if (urlState.t && !urlState.c) $("#then").scrollIntoView();
}
