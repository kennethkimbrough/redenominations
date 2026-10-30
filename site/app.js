const [table, countries, rates, history] = await Promise.all([
  fetch("data/redenominations.json").then((r) => r.json()),
  fetch("data/countries.json").then((r) => r.json()),
  fetch("data/rates.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
  fetch("data/history.json").then((r) => (r.ok ? r.json() : null)).catch(() => null),
]);

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const log10 = (x) => Math.log10(x);
const fmtRate = (r) => {
  if (r >= 1e6) {
    const e = Math.floor(log10(r)), m = r / 10 ** e;
    return (Math.abs(m - 1) < 1e-9 ? "" : `${+m.toFixed(2)} × `) + `10<sup>${e}</sup>`;
  }
  return r.toLocaleString("en-US", { maximumFractionDigits: 6 });
};
const zerosOf = (r) => (r >= 1 ? Math.round(log10(r) * 100) / 100 : 0);
const fmtUsd = (x) => {
  if (x >= 0.01) return "$" + x.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  if (x >= 1e-6) return "$" + x.toLocaleString("en-US", { maximumFractionDigits: 8 });
  return "$" + x.toExponential(2).replace(/e\+?(-?\d+)/, " × 10<sup>$1</sup>");
};
const fmtAmount = (x) => {
  if (!Number.isFinite(x)) return "—";
  if (x === 0) return "0";
  const a = Math.abs(x);
  if (a >= 1e15 || a < 1e-6) return x.toExponential(3).replace(/e\+?(-?\d+)/, " × 10<sup>$1</sup>");
  return x.toLocaleString("en-US", { maximumFractionDigits: a < 1 ? 10 : a < 1000 ? 4 : 2 });
};

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
function currencyOptions(c) {
  // The chain's currencies in order: the first step's old currency, then each new one.
  const list = [{ name: c.steps[0].old, from: c.start, idx: 0 }];
  c.steps.forEach((s, i) => list.push({ name: s.new, from: s.year, idx: i + 1 }));
  return list;
}
function fillCurrencies() {
  const c = countries.countries.find((x) => x.iso === cCountry.value);
  cFrom.innerHTML = "";
  for (const cur of currencyOptions(c)) {
    const o = document.createElement("option");
    o.value = cur.idx; o.textContent = `${cur.name} (${cur.from}${cur.idx === c.steps.length ? " – today" : ""})`;
    cFrom.append(o);
  }
  convert();
}
function convert() {
  const c = countries.countries.find((x) => x.iso === cCountry.value);
  const idx = Number(cFrom.value);
  const amount = parseFloat(cAmount.value.replace(/[,\s_]/g, ""));
  const steps = c.steps.slice(idx);
  const stepsEl = $("#c-steps");
  if (!Number.isFinite(amount)) { $("#c-result").textContent = "Enter an amount."; stepsEl.innerHTML = ""; return; }
  let value = amount, broken = false, uncited = false;
  const lines = [];
  for (const s of steps) {
    if (!s.rate) { broken = true; lines.push(`<li class="uncited">${s.year}: ${esc(s.old)} → ${esc(s.new)} — no fixed conversion; the chain stops here.</li>`); break; }
    value /= s.rate;
    if (!s.source) uncited = true;
    lines.push(`<li>${s.year}: ${esc(s.old)} → ${esc(s.new)} <span class="rate">÷ ${fmtRate(s.rate)}</span>${s.source ? "" : ' <span class="uncited">(not yet cited)</span>'}</li>`);
  }
  const from = currencyOptions(c)[idx].name;
  const last = steps.length ? steps[steps.length - 1] : null;
  const unit = broken ? (last ? last.old : from) : (c.steps.length ? c.steps[c.steps.length - 1].new : from);
  const totalRate = steps.filter((s) => s.rate).reduce((p, s) => p * s.rate, 1);
  const zeros = zerosOf(totalRate);
  $("#c-result").innerHTML = steps.length === 0
    ? `${fmtAmount(amount)} ${esc(from)} is already the current unit.`
    : `${fmtAmount(amount)} ${esc(from)} ${broken ? "was last convertible as" : "="}<span class="big">${fmtAmount(value)} ${esc(unit)}</span>` +
      `<span class="zeros">${zeros ? `${Number.isInteger(zeros) ? zeros : zeros.toFixed(2)} zeros removed over ${steps.filter((s) => s.rate).length} reform${steps.length === 1 ? "" : "s"}` : "no zeros removed"}` +
      `${uncited ? " · includes a step that is not yet cited" : ""}${broken ? " · the chain has no fixed rate past this point" : ""}</span>`;
  // Dollars today: only when the chain reaches the country's current unit and a rate exists.
  const code = rates?.units?.[c.iso];
  const perUsd = code && rates.rates[code];
  if (!broken && perUsd && steps.length) {
    const usd = value / perUsd;
    const oneDollar = perUsd * totalRate;
    $("#c-result").innerHTML += `<div class="usd">≈ <b>${fmtUsd(usd)}</b> at the rate of ${esc(rates.date)} (${perUsd.toLocaleString("en-US", { maximumFractionDigits: 4 })} ${code} per US dollar). ` +
      `One dollar today buys ${fmtAmount(oneDollar)} ${esc(from)}.` +
      `${["VES", "ARS", "BOB"].includes(code) ? " This is the published rate; a parallel street rate may differ." : ""}` +
      ` <a href="${esc(rates.source.url)}">Rate source</a>.</div>`;
  }
  stepsEl.innerHTML = lines.join("");
}
cCountry.addEventListener("change", fillCurrencies);
cFrom.addEventListener("change", convert);
cAmount.addEventListener("input", convert);
$("#convert-form").addEventListener("submit", (e) => e.preventDefault());
cCountry.value = "BR";
fillCurrencies();

// ---------- chart ----------
function chart() {
  const W = 860, H = 460, L = 56, R = 150, T = 16, B = 36;
  const x0 = 1945, x1 = 2026;
  const series = countries.countries
    .map((c) => {
      let f = 1; const pts = [{ year: x0, f: 1, label: `${c.steps[0].old}` }];
      for (const s of c.steps) {
        if (!s.rate) break;
        pts.push({ year: s.year, f, label: `${s.year}: ${s.old} → ${s.new}, ÷ ${s.rate.toLocaleString("en-US")}`, before: true });
        f *= s.rate;
        pts.push({ year: s.year, f, label: `${s.year}: ${s.old} → ${s.new}, ÷ ${s.rate.toLocaleString("en-US")}` });
      }
      pts.push({ year: x1, f, label: c.unit });
      return { c, pts, total: f };
    })
    .filter((s) => s.total > 1);
  const maxLog = Math.ceil(Math.max(...series.map((s) => log10(s.total))));
  const X = (y) => L + ((y - x0) / (x1 - x0)) * (W - L - R);
  const Y = (f) => T + (1 - log10(f) / maxLog) * (H - T - B);
  const colours = ["#b8860b", "#9b2d20", "#2f6b3a", "#1f5f8b", "#7b4b94", "#c2651a", "#3f7f7f", "#8a6d3b"];
  let svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Cumulative zeros removed per country since 1945, log scale">`;
  for (let z = 0; z <= maxLog; z += 5) {
    svg += `<line class="grid" x1="${L}" x2="${W - R}" y1="${Y(10 ** z)}" y2="${Y(10 ** z)}"/><text class="axis" x="${L - 6}" y="${Y(10 ** z) + 4}" text-anchor="end">10<tspan baseline-shift="super" font-size="9">${z}</tspan></text>`;
  }
  for (let y = 1950; y <= 2020; y += 10) svg += `<text class="axis" x="${X(y)}" y="${H - 12}" text-anchor="middle">${y}</text>`;
  const labels = [];
  series.forEach((s, i) => {
    const col = colours[i % colours.length];
    const d = s.pts.map((p, j) => `${j ? "L" : "M"}${X(p.year).toFixed(1)},${Y(p.f).toFixed(1)}`).join(" ");
    svg += `<path class="series ${s.c.status}" stroke="${col}" d="${d}"/>`;
    s.pts.filter((p) => !p.before && p.year !== x0 && p.year !== x1).forEach((p) => {
      svg += `<circle class="pt" r="4" cx="${X(p.year)}" cy="${Y(p.f)}" fill="${col}" data-tip="${esc(s.c.name)} — ${esc(p.label)}"/>`;
    });
    labels.push({ y: Y(s.total), text: `${s.c.name.replace(/ \(.*\)/, "")} · ${Math.round(log10(s.total))}`, col });
  });
  // Spread the right-hand labels so they don't overlap.
  labels.sort((a, b) => a.y - b.y);
  for (let i = 1; i < labels.length; i++) if (labels[i].y - labels[i - 1].y < 13) labels[i].y = labels[i - 1].y + 13;
  for (const l of labels) svg += `<text class="name" x="${W - R + 8}" y="${l.y + 4}" fill="${l.col}">${esc(l.text)}</text>`;
  svg += `</svg><div class="legend"><span><i style="background:var(--ink-2)"></i>solid: verified chain</span><span><i style="background:repeating-linear-gradient(90deg,var(--ink-2) 0 4px,transparent 4px 7px)"></i>dashed: has an uncited step</span><span>label: country · zeros removed in total</span></div>`;
  $("#chart").innerHTML = svg;
  const tip = $("#tip");
  $("#chart").addEventListener("pointerover", (e) => {
    const t = e.target.closest("[data-tip]"); if (!t) return;
    tip.textContent = t.dataset.tip; tip.hidden = false;
  });
  $("#chart").addEventListener("pointermove", (e) => { tip.style.left = `${Math.min(e.clientX + 12, innerWidth - 300)}px`; tip.style.top = `${e.clientY + 14}px`; });
  $("#chart").addEventListener("pointerout", () => { tip.hidden = true; });
}
chart();

// ---------- table ----------
function renderTable() {
  const q = $("#filter").value.trim().toLowerCase();
  const all = $("#all-years").checked;
  const rows = table.rows.filter((r) => (all || r.year >= 1945) && (!q || `${r.country} ${r.old} ${r.new}`.toLowerCase().includes(q)));
  const maxZ = 30;
  $("#table tbody").innerHTML = rows.map((r) => {
    const z = zerosOf(r.rate);
    return `<tr class="${r.year < 1945 ? "old" : ""}"><td>${r.year}</td><td>${esc(r.country)}</td><td>${esc(r.old)}</td><td>${esc(r.new)}</td>` +
      `<td class="num">${r.approximate ? "≈ " : ""}${r.at_par ? "at par" : fmtRate(r.rate)}</td>` +
      `<td class="num"><span class="zeros-bar" style="width:${(z / maxZ) * 60}px"></span>${z ? (Number.isInteger(z) ? z : z.toFixed(1)) : "–"}</td></tr>`;
  }).join("");
  $("#table-count").textContent = `${rows.length} reform${rows.length === 1 ? "" : "s"}`;
}
$("#filter").addEventListener("input", renderTable);
$("#all-years").addEventListener("change", renderTable);
renderTable();

// ---------- chains ----------
$("#chains").innerHTML = countries.countries.map((c) => `
  <details class="chain">
    <summary><h3>${esc(c.name)}</h3><span class="badge ${c.status}">${c.status}</span>
      <span class="factor">${c.steps.length} step${c.steps.length === 1 ? "" : "s"}${c.total_factor > 1 ? ` · ${Math.round(log10(c.total_factor))} zeros` : ""}</span></summary>
    <ol>${c.steps.map((s) => `<li>${s.year}: ${esc(s.old)} → ${esc(s.new)}, ${s.rate ? (s.rate === 1 ? "at par" : `${fmtRate(s.rate)} old per new`) : "no fixed rate"}` +
      `${s.note ? `<div class="note">${esc(s.note)}</div>` : ""}` +
      `<div>${s.source ? `<cite>Source: <a href="${esc(s.source.url)}">${esc(s.source.title)}</a></cite>` : `<cite class="uncited" style="color:var(--red)">Not yet cited</cite>`}</div></li>`).join("")}</ol>
    ${c.gap ? `<p class="gap">${esc(c.gap)}</p>` : ""}
  </details>`).join("");


// ---------- at the time ----------
if (history) {
  const tCountry = $("#t-country"), tYear = $("#t-year"), tAmount = $("#t-amount");
  const chainByWb = Object.fromEntries(countries.countries.filter((c) => c.wb).map((c) => [c.wb, c]));
  const list = Object.entries(history.countries).map(([iso, c]) => ({ iso, name: c.name })).sort((a, b) => a.name.localeCompare(b.name));
  for (const c of list) { const o = document.createElement("option"); o.value = c.iso; o.textContent = c.name; tCountry.append(o); }
  const cpiYears = Object.keys(history.us_cpi).map(Number);
  const cpiLatest = Math.max(...cpiYears);
  tYear.max = String(cpiLatest + 2);

  /** Name of the currency a chain country used in `year`, and the factor from that unit to the World Bank's unit. */
  function unitFor(chain, year) {
    const cutoff = chain.wb_unit_year ?? Infinity;
    let name = chain.steps[0].old, factor = 1;
    for (const s of chain.steps) {
      if (s.year <= year) name = s.new;
      else if (s.year <= cutoff && s.new !== "Euro" && s.rate) factor *= s.rate;
      else if (s.year <= cutoff && s.new !== "Euro" && !s.rate) return { name, factor: null };
    }
    return { name, factor };
  }

  function thenConvert() {
    const iso = tCountry.value, year = Math.round(Number(tYear.value));
    const amount = parseFloat(tAmount.value.replace(/[,\s_]/g, ""));
    const c = history.countries[iso];
    const chain = chainByWb[iso];
    const out = $("#t-result"), note = $("#t-note");
    const unit = chain ? unitFor(chain, year) : { name: c.currency ? c.currency.name : "local currency", factor: 1, current: true };
    $("#t-unit").textContent = `in ${unit.name}`;
    if (!Number.isFinite(amount) || !Number.isFinite(year)) { out.textContent = "Enter a year and an amount."; note.textContent = ""; return; }
    const rate = c.rates[year];
    if (chain?.wb_unsupported) { out.textContent = `No reliable series for ${c.name}.`; note.textContent = chain.wb_unsupported; return; }
    if (!rate) {
      const have = Object.keys(c.rates).map(Number);
      out.textContent = `No exchange rate for ${c.name} in ${year}.`;
      note.textContent = have.length ? `The World Bank series for ${c.name} covers ${Math.min(...have)}–${Math.max(...have)}, with gaps.` : "";
      return;
    }
    if (unit.factor === null) { out.textContent = `${c.name}'s chain has no fixed rate between ${year} and the World Bank's unit.`; note.textContent = ""; return; }
    const usdThen = amount / unit.factor / rate;
    const cpiYear = history.us_cpi[Math.min(Math.max(year, Math.min(...cpiYears)), cpiLatest)];
    const usdNow = usdThen * history.us_cpi[cpiLatest] / cpiYear;
    const unitLabel = unit.current && unit.name === "local currency" ? `${c.name} local currency` : unit.name;
    out.innerHTML = `${fmtAmount(amount)} ${esc(unitLabel)} in ${year} =` +
      `<span class="big">${fmtUsd(usdThen)} in ${year} dollars</span>` +
      `<span class="zeros">about <b>${fmtUsd(usdNow)}</b> in ${cpiLatest} dollars (US consumer prices rose ${(history.us_cpi[cpiLatest] / cpiYear).toFixed(1)}× since ${year})` +
      ` · average official rate in ${year}: ${rate >= 0.01 ? rate.toLocaleString("en-US", { maximumFractionDigits: 4 }) : rate.toExponential(3)} ${chain ? "current units" : "local units"} per dollar</span>`;
    const later = table.rows.filter((r) => r.country === c.name && r.year > year);
    const warn = [];
    if (!chain && later.length) warn.push(`${c.name} redenominated in ${later.map((r) => r.year).join(", ")}; the amount is read in today's ${unit.name}, because the World Bank restates earlier years in it. In the currency of ${year} the figure would differ by a factor of ${later.map((r) => fmtRate(r.rate).replace(/<[^>]+>/g, "^")).join(" × ")}.`);
    if (chain && chain.status === "partial") warn.push(`${chain.name}'s chain has an uncited step; the conversion to the current unit may be off.`);
    if (["VEN", "ARG", "BOL", "ZWE"].includes(iso)) warn.push("Official rate; a parallel street rate existed for much of this period.");
    note.innerHTML = warn.map(esc).join(" ") + ` <a href="${esc(history.source.url)}">Source</a>, fetched ${esc(history.fetched)}.`;
  }
  tCountry.addEventListener("change", thenConvert);
  tYear.addEventListener("input", thenConvert);
  tAmount.addEventListener("input", thenConvert);
  $("#then-form").addEventListener("submit", (e) => e.preventDefault());
  tCountry.value = "IND";
  thenConvert();
}
