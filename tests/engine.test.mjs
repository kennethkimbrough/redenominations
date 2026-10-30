import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { chainConvert, chartRows, currencyOptions, dollarsToday, fmtAmount, fmtRate, fmtUsd, parseAmount, thenConvert, unitFor, zerosOf } from "../site/engine.js";

const countries = JSON.parse(readFileSync(new URL("../data/countries.json", import.meta.url)));
const table = JSON.parse(readFileSync(new URL("../data/redenominations.json", import.meta.url)));
const chain = (iso) => countries.countries.find((c) => c.iso === iso);

test("zerosOf counts powers of ten and ignores rates below one", () => {
  assert.equal(zerosOf(1000), 3);
  assert.equal(zerosOf(2750), 3.44);
  assert.equal(zerosOf(4e29), 29.6);
  assert.equal(zerosOf(1), 0);
  assert.equal(zerosOf(0.1), 0);
});

test("formatting", () => {
  assert.equal(fmtRate(1000), "1,000");
  assert.equal(fmtRate(1e6), "10<sup>6</sup>");
  assert.equal(fmtRate(4e29), "4 × 10<sup>29</sup>");
  assert.equal(fmtUsd(127.18), "$127.18");
  assert.equal(fmtUsd(0.00001234), "$0.00001234");
  assert.equal(fmtUsd(6.8e-12), "$6.80 × 10<sup>-12</sup>");
  assert.equal(fmtAmount(1e6), "1,000,000");
  assert.equal(fmtAmount(3.636e-10), "3.636 × 10<sup>-10</sup>");
  assert.equal(parseAmount("1,000,000"), 1e6);
  assert.equal(parseAmount("1 000"), 1000);
  assert.ok(Number.isNaN(parseAmount("abc")));
});

test("Brazil: a million 1945 cruzeiros become 3.636e-10 reais over six reforms", () => {
  const r = chainConvert(chain("BR"), 0, 1e6);
  assert.equal(r.from, "Cruzeiro (antigo)");
  assert.equal(r.unit, "Real");
  assert.ok(Math.abs(r.value - 1e6 / (1000 ** 4 * 2750)) < 1e-25);
  assert.equal(r.applied, 6);
  assert.equal(r.zeros, 15.44);
  assert.equal(r.broken, false);
  assert.equal(r.uncited, false);
});

test("starting later in a chain applies only the later steps", () => {
  const opts = currencyOptions(chain("BR"));
  assert.equal(opts[1].name, "Cruzeiro (novo)");
  assert.equal(opts[1].from, 1967);
  const r = chainConvert(chain("BR"), 1, 100);
  assert.equal(r.applied, 5);
  const last = chainConvert(chain("BR"), opts.length - 1, 5);
  assert.equal(last.noop, true);
  assert.equal(last.value, 5);
});

test("Zimbabwe: the chain stops where there is no fixed rate", () => {
  const r = chainConvert(chain("ZW"), 0, 1e6);
  assert.equal(r.broken, true);
  assert.equal(r.unit, "Zimbabwean dollar (4th)");
  assert.equal(r.applied, 3);
  assert.equal(r.zeros, 25);
  assert.equal(dollarsToday(chain("ZW"), r, { units: { ZW: "ZWG" }, rates: { ZWG: 26.8 } }), null);
});

test("an uncited step is flagged but still applied", () => {
  const by = chain("BY");
  assert.equal(chainConvert(by, 0, 1).uncited, false);
  const steps = by.steps.map((s, i) => (i === by.steps.length - 2 ? { ...s, source: null } : s));
  const r = chainConvert({ ...by, steps }, 0, 1);
  assert.equal(r.uncited, true);
  assert.equal(r.applied, by.steps.length);
});

test("dollars today", () => {
  const r = chainConvert(chain("HU"), 0, 1e6);
  const d = dollarsToday(chain("HU"), r, { units: { HU: "HUF" }, rates: { HUF: 329.25 }, date: "2026-10-29", source: { url: "x" } });
  assert.equal(d.code, "HUF");
  assert.ok(Math.abs(d.usd - 1e6 / 4e29 / 329.25) < 1e-40);
  assert.ok(Math.abs(d.oneDollarBuys - 329.25 * 4e29) < 1e18);
});

test("unitFor names the year's currency and the factor to the World Bank unit", () => {
  // after 1980: 1986, 1989, 1993 at 1000 each, 1990 at par, 1994 at 2750
  assert.deepEqual(unitFor(chain("BR"), 1980), { name: "Cruzeiro (novo)", factor: 1000 ** 3 * 2750 });
  assert.deepEqual(unitFor(chain("BR"), 1995), { name: "Real", factor: 1 });
  // Euro steps do not count: the World Bank keeps francs before 1999.
  assert.deepEqual(unitFor(chain("FR"), 1980), { name: "New French Franc", factor: 1 });
  assert.deepEqual(unitFor(chain("FR"), 1955), { name: "French Franc", factor: 100 });
  // Venezuela's series is restated only to the 2008 unit.
  assert.deepEqual(unitFor(chain("VE"), 1980), { name: "(old) Bolivar", factor: 1000 });
  assert.equal(unitFor(chain("ZW"), 2000).factor, null);
});

test("thenConvert: 1,000 rupees in 1980 at 7.8629 per dollar, 3.8x US inflation since", () => {
  const history = { source: { url: "x" }, fetched: "2026-10-30", us_cpi: { 1980: 37.9, 2024: 143.86 },
    countries: { IND: { name: "India", currency: { code: "INR", name: "Indian rupee" }, rates: { 1980: 7.8629 } } } };
  const r = thenConvert({ history, chain: null, tableRows: table.rows }, "IND", 1980, 1000);
  assert.equal(r.ok, true);
  assert.ok(Math.abs(r.usdThen - 127.18) < 0.01);
  assert.ok(Math.abs(r.inflation - 3.796) < 0.01);
  assert.equal(r.unitLabel, "Indian rupee");
  assert.deepEqual(r.warnings, []);
  assert.equal(thenConvert({ history, chain: null, tableRows: table.rows }, "IND", 1970, 1000).ok, false);
});

test("thenConvert applies the chain factor for restated series and warns for unchained ones", () => {
  const history = { source: { url: "x" }, fetched: "d", us_cpi: { 1980: 37.9, 2024: 143.86 },
    countries: { BRA: { name: "Brazil", rates: { 1980: 2.28123189244443e-11 } }, MEX: { name: "Mexico", currency: { name: "Mexican peso" }, rates: { 1985: 0.2569 } } } };
  const br = thenConvert({ history, chain: chain("BR"), tableRows: table.rows }, "BRA", 1980, 1e6);
  assert.equal(br.unit.name, "Cruzeiro (novo)");
  assert.ok(Math.abs(br.usdThen - 15940) < 5, String(br.usdThen));
  const mx = thenConvert({ history, chain: null, tableRows: table.rows }, "MEX", 1985, 1000);
  assert.equal(mx.ok, true);
  assert.match(mx.warnings[0], /Mexico redenominated in 1993/);
});

test("chart rows are sorted by zeros removed and skip countries with none", () => {
  const rows = chartRows(countries.countries);
  assert.equal(rows[0].c.iso, "HU");
  assert.ok(rows.every((r, i) => i === 0 || rows[i - 1].total >= r.total));
  assert.ok(rows.every((r) => r.total > 0));
});

test("a country with no currency change converts to itself and still gets dollars", () => {
  const c = { iso: "XX", start: 1945, currency: "Test dollar", steps: [] };
  const opts = currencyOptions(c);
  assert.deepEqual(opts.map((o) => o.name), ["Test dollar"]);
  const r = chainConvert(c, 0, 50);
  assert.equal(r.noop, true);
  assert.equal(r.value, 50);
  const d = dollarsToday(c, r, { units: { XX: "XXD" }, rates: { XXD: 2 }, date: "d", source: { url: "x" } });
  assert.equal(d.usd, 25);
  assert.equal(unitFor(c, 1980).name, "Test dollar");
});
