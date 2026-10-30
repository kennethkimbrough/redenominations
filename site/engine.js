/**
 * The arithmetic behind the page, with no DOM: chain conversion, the
 * at-the-time conversion against the World Bank series, and number formatting.
 * Imported by app.js in the browser and by tests/engine.test.mjs in Node.
 */

export const log10 = (x) => Math.log10(x);

/** Number of zeros a rate removes: log10, rounded to 2 places; 0 for rates ≤ 1. */
export const zerosOf = (r) => (r >= 1 ? Math.round(log10(r) * 100) / 100 : 0);

/** A rate for display, as HTML: 10<sup>n</sup> for a million and up, else a plain number. */
export function fmtRate(r) {
  if (r >= 1e6) {
    const e = Math.floor(log10(r)), m = r / 10 ** e;
    return (Math.abs(m - 1) < 1e-9 ? "" : `${+m.toFixed(2)} × `) + `10<sup>${e}</sup>`;
  }
  return r.toLocaleString("en-US", { maximumFractionDigits: 6 });
}

/** A dollar amount for display, as HTML. */
export function fmtUsd(x) {
  if (x >= 0.01) return "$" + x.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  if (x >= 1e-6) return "$" + x.toLocaleString("en-US", { maximumFractionDigits: 8 });
  return "$" + x.toExponential(2).replace(/e\+?(-?\d+)/, " × 10<sup>$1</sup>");
}

/** Any amount for display, as HTML: scientific outside 1e-6..1e15. */
export function fmtAmount(x) {
  if (!Number.isFinite(x)) return "—";
  if (x === 0) return "0";
  const a = Math.abs(x);
  if (a >= 1e15 || a < 1e-6) return x.toExponential(3).replace(/e\+?(-?\d+)/, " × 10<sup>$1</sup>");
  return x.toLocaleString("en-US", { maximumFractionDigits: a < 1 ? 10 : a < 1000 ? 4 : 2 });
}

/** "1,000,000" or "1e6" or "1 000 000" -> 1000000; NaN when unreadable. */
export const parseAmount = (text) => parseFloat(String(text).replace(/[,\s_]/g, ""));

/** The currencies of a chain in order: the first step's old currency, then each new one. */
export function currencyOptions(chain) {
  const list = [{ name: chain.currency ?? chain.steps[0].old, from: chain.start, idx: 0 }];
  chain.steps.forEach((s, i) => list.push({ name: s.new, from: s.year, idx: i + 1 }));
  return list;
}

/**
 * Convert `amount` of the chain's currency number `idx` through every later step.
 * Returns the value in the last reachable unit plus what happened on the way.
 */
export function chainConvert(chain, idx, amount) {
  const steps = chain.steps.slice(idx);
  const from = currencyOptions(chain)[idx].name;
  let value = amount, broken = false, uncited = false, applied = 0;
  const trail = [];
  for (const s of steps) {
    if (!s.rate) { broken = true; trail.push({ step: s, applied: false }); break; }
    value /= s.rate;
    applied += 1;
    if (!s.source) uncited = true;
    trail.push({ step: s, applied: true });
  }
  const last = steps.length ? steps[steps.length - 1] : null;
  const unit = broken ? trail[trail.length - 1].step.old : (chain.steps.length ? chain.steps[chain.steps.length - 1].new : from);
  const totalRate = steps.filter((s) => s.rate).reduce((p, s) => p * s.rate, 1);
  return { from, unit, value, totalRate, zeros: zerosOf(totalRate), applied, broken, uncited, trail, noop: steps.length === 0, last };
}

/** Today's dollar figure for a chain conversion, or null when there is no usable rate. */
export function dollarsToday(chain, result, rates) {
  const code = rates?.units?.[chain.iso];
  let perUsd = code && rates.rates?.[code];
  if (result.broken || !perUsd) return null;
  // The source may still quote the pre-reform unit (Syria after 2026); see RATE_OLD_UNIT.
  const fix = chain.rate_old_unit;
  if (fix && perUsd > fix.above) perUsd /= fix.divisor;
  return { code, perUsd, usd: result.value / perUsd, oneDollarBuys: perUsd * result.totalRate, date: rates.date, source: rates.source };
}

/**
 * For a chain country: the currency in use in `year`, and the factor that takes
 * that unit to the unit the World Bank series is expressed in. Euro steps are
 * skipped because the World Bank keeps the national unit before adoption.
 * `factor` is null when a step without a fixed rate lies in between.
 */
export function unitFor(chain, year) {
  const cutoff = chain.wb_unit_year ?? Infinity;
  let name = chain.currency ?? chain.steps[0].old, factor = 1;
  for (const s of chain.steps) {
    if (s.year <= year) name = s.new;
    else if (s.year <= cutoff && s.new !== "Euro" && s.rate) factor *= s.rate;
    else if (s.year <= cutoff && s.new !== "Euro" && !s.rate) return { name, factor: null };
  }
  return { name, factor };
}

/**
 * Dollars at the time and in today's dollars for `amount` of `iso`'s currency in `year`.
 * `history` is data/history.json; `chain` is the matching entry from countries.json or null;
 * `tableRows` is the redenomination table, used to warn about restated series.
 * Returns {ok:false, reason} or {ok:true, ...}.
 */
export function thenConvert({ history, chain, tableRows }, iso, year, amount) {
  const c = history.countries[iso];
  if (!c) return { ok: false, reason: "Unknown country." };
  const cpiYears = Object.keys(history.us_cpi).map(Number);
  const cpiLatest = Math.max(...cpiYears), cpiFirst = Math.min(...cpiYears);
  const unit = chain ? unitFor(chain, year) : { name: c.currency ? c.currency.name : "local currency", factor: 1, current: true };
  if (!Number.isFinite(amount) || !Number.isFinite(year)) return { ok: false, reason: "Enter a year and an amount.", unit };
  if (chain?.wb_unsupported) return { ok: false, reason: `No reliable series for ${c.name}.`, detail: chain.wb_unsupported, unit };
  const rate = c.rates[year];
  if (!rate) {
    const have = Object.keys(c.rates).map(Number);
    return { ok: false, reason: `No exchange rate for ${c.name} in ${year}.`, unit,
      detail: have.length ? `The World Bank series for ${c.name} covers ${Math.min(...have)}–${Math.max(...have)}, with gaps.` : "" };
  }
  if (unit.factor === null) return { ok: false, reason: `${c.name}'s chain has no fixed rate between ${year} and the World Bank's unit.`, unit };
  const usdThen = amount / unit.factor / rate;
  const cpiYear = history.us_cpi[Math.min(Math.max(year, cpiFirst), cpiLatest)];
  const inflation = history.us_cpi[cpiLatest] / cpiYear;
  const later = tableRows.filter((r) => r.country === c.name && r.year > year);
  const warnings = [];
  if (!chain && later.length) {
    warnings.push(`${c.name} redenominated in ${later.map((r) => r.year).join(", ")}; the amount is read in today's ${unit.name}, because the World Bank restates earlier years in it. ` +
      `In the currency of ${year} the figure would differ by a factor of ${later.map((r) => fmtRate(r.rate).replace(/<[^>]+>/g, "^")).join(" × ")}.`);
  }
  if (chain && chain.status === "partial") warnings.push(`${chain.name}'s chain is partial (${chain.gap ?? "it has an uncited step"}), so the conversion to the current unit may be approximate.`);
  if (["VEN", "ARG", "BOL", "ZWE", "SYR", "IRN"].includes(iso)) warnings.push("Official rate; a parallel street rate existed for much of this period.");
  return { ok: true, country: c, unit, rate, usdThen, usdNow: usdThen * inflation, inflation, cpiLatest, warnings,
    unitLabel: unit.current && unit.name === "local currency" ? `${c.name} local currency` : unit.name };
}

/** Rows for the ranked chart: one per country with a segment per reform, sorted by zeros removed. */
export function chartRows(countries) {
  return countries
    .map((c) => {
      const segs = [];
      for (const st of c.steps) {
        if (!st.rate) break;
        segs.push({ z: zerosOf(st.rate), step: st, uncited: !st.source });
      }
      return { c, segs, total: segs.reduce((a, b) => a + b.z, 0) };
    })
    .filter((r) => r.total > 0)
    .sort((a, b) => b.total - a.total);
}
