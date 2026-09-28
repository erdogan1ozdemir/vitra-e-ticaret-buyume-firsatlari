# -*- coding: utf-8 -*-
"""Ozdilek raporundan uyarlanan ek bilesenler: koyu hero, KPI karolari, bulgu kartlari, metrik kartlari, not kutusu."""
CSS_EK = """
.hero.dark{color:#fff;position:relative;overflow:hidden;border:0;border-radius:14px;margin:4px 0 30px;padding:26px 28px 24px;
  background:radial-gradient(900px 480px at 88% -14%,rgba(255,123,82,.30),transparent 58%),
  radial-gradient(680px 420px at -8% 112%,rgba(127,200,174,.13),transparent 62%),
  linear-gradient(140deg,#0B221E 0%,#10332F 52%,#174A41 100%)}
.hero.dark .ring{position:absolute;right:-150px;top:-150px;width:460px;height:460px;border:50px solid rgba(255,123,82,.13);border-radius:50%;pointer-events:none}
.hero.dark .eyebrow{color:#FFB399}
.hero.dark h1{color:#fff;font-size:clamp(26px,3.2vw,38px);font-weight:760;line-height:1.12;max-width:820px}
.hero.dark h1 .hl{color:#FFB399}
.hero.dark .sub{color:rgba(255,255,255,.88);max-width:780px;font-size:14.5px}
.hero.dark .chips{display:flex;flex-wrap:wrap;gap:7px;margin:16px 0 0}
.hero.dark .chip{display:inline-flex;align-items:center;font-size:11px;font-weight:600;padding:4px 11px;border-radius:999px;
  border:1px solid rgba(255,255,255,.28);color:rgba(255,255,255,.9);background:rgba(255,255,255,.06)}
.hero.dark .chip.f{background:#FF7B52;border-color:#FF7B52;color:#10332F}
.hero.dark .kpis{margin:22px 0 0;position:relative;z-index:2}
.hero.dark .kpi{border:0;box-shadow:0 12px 32px rgba(0,0,0,.22);text-align:center;color:var(--ink)}
.hero.dark .kpi .v{color:var(--teal);font-size:clamp(24px,2.4vw,32px);font-weight:760}
.hero.dark .kpi .v.up{color:var(--green)}.hero.dark .kpi .v.dn{color:var(--red)}
.hero.dark .kpi .k{color:var(--ink-2)}
.hero.dark .kpi .tag{display:inline-block;margin-top:8px;font-size:10.5px;font-weight:600;padding:2.5px 11px;border-radius:999px;background:var(--coral-tint);color:var(--coral-deep)}
:root[data-theme="dark"] .hero.dark .kpi{background:#12211F}
:root[data-theme="dark"] .hero.dark .kpi .v{color:#EDEAE4}
/* bulgu kartlari */
.fnotes{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:0 0 20px}
.fnote{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px 14px}
.fnote .fc{font-size:10.5px;letter-spacing:.14em;color:var(--coral-deep);font-weight:700}
.fnote h3{margin:6px 0 8px;font-size:15px;line-height:1.3}
.fnote ul{margin:0;padding-left:17px;font-size:13.5px}
.fnote li{margin:0 0 5px;color:var(--ink-2)}
.fnote li b{color:var(--ink)}
/* metrik / tanim kartlari */
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(225px,1fr));gap:13px;margin:0 0 20px}
.metric{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:15px 17px}
.metric .mk{font-size:10.5px;letter-spacing:.14em;color:var(--muted);font-weight:700}
.metric .mv{font-size:27px;font-weight:760;color:var(--teal);margin-top:7px;line-height:1.1;letter-spacing:-.01em}
.metric .mv small{font-size:.44em;font-weight:600;color:var(--muted)}
.metric .md{font-size:12.5px;color:var(--ink-2);margin-top:7px;line-height:1.5}
:root[data-theme="dark"] .metric .mv{color:#EDEAE4}
/* not kutusu */
.note{background:var(--coral-tint);border-radius:12px;padding:15px 19px;margin:0 0 20px}
.note .nt{font-size:10.5px;letter-spacing:.1em;color:var(--coral-deep);font-weight:700;margin-bottom:5px}
.note p{margin:0;color:var(--ink)}
.note p+p{margin-top:8px}
.note.mint{background:var(--green-wash)}.note.mint .nt{color:var(--green)}
:root[data-theme="dark"] .note{background:#3A241D}
:root[data-theme="dark"] .note.mint{background:#1F3A24}
/* siralama listesi (etiket + zeminli cubuk + deger) */
.rank{list-style:none;margin:0 0 18px;padding:0;display:grid;gap:7px}
.rank li{display:grid;grid-template-columns:26px minmax(120px,1.1fr) minmax(0,2fr) 92px;gap:10px;align-items:center;font-size:13px}
.rank li .rn{color:var(--muted);font-weight:700;font-variant-numeric:tabular-nums}
.rank li .rv{text-align:right;font-weight:650;font-variant-numeric:tabular-nums;white-space:nowrap}
.rank li .rl{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rank li.you .rl{color:var(--coral-deep);font-weight:650}
.rank li.you .bar-mini{background:var(--coral-deep)}
@media(max-width:520px){.rank li{grid-template-columns:22px minmax(90px,1fr) minmax(0,1.4fr) 74px;gap:7px;font-size:12px}}
/* iki sutunlu metin + yan panel */
.split{display:grid;grid-template-columns:1.15fr 1fr;gap:18px;align-items:start;margin:0 0 18px}
.split>*{min-width:0}
.split .box{margin:0}
@media(max-width:940px){.split{grid-template-columns:1fr}}
/* strateji kartlari */
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:0 0 18px}
.step{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.step .sn{display:inline-flex;width:26px;height:26px;border-radius:7px;background:var(--teal);color:#fff;align-items:center;justify-content:center;font-weight:700;font-size:12px}
.step h4{margin:9px 0 5px;font-size:14px}
.step p{margin:0;font-size:12.8px;color:var(--ink-2)}
:root[data-theme="dark"] .step .sn{background:var(--coral-deep)}
"""
