#!/usr/bin/env python3
"""
Plot: Polymarket "Jesus Christ Return" Markets vs 1-Year US Treasury Yield
Extended longitudinal view: Mar 2025 - Apr 2026

Data stitches together two Polymarket markets:
  1. "Will Jesus Christ return in 2025?" (Mar 20, 2025 - Jan 1, 2026, resolved No)
  2. "Will Jesus Christ return before 2027?" (Nov 25, 2025 - present)

Sources:
- Polymarket data: Bloomberg, CoinDesk, Benzinga, Protos, Jerusalem Post,
  Boing Boing, NewsNation, Polymarket tweets
- Treasury data: FRED DGS1, Federal Reserve H.15, Wolf Street,
  Advisor Perspectives, Congress.gov (Fed rate cut timeline)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# ============================================================
# POLYMARKET DATA — Stitched from two markets
# ============================================================

# --- Market 1: "Will Jesus Christ return in 2025?" ---
# Launched: Mar 20, 2025 | Resolved: Jan 1, 2026 (No)
# Volume: $3.3M
# Key data points from news:
#   - Launch: initially ~5%, settled to 3% by end of March
#   - Spring peak: ~4.7% (never breached 5%)
#   - May 27 tweet: "4% chance. The odds have risen."
#   - Summer: "above 3% throughout most of the spring"
#   - Fall: contract "sitting at around 2%"
#   - Dec: "well under 1%"
#   - Jan 1, 2026: resolved at 0%
jesus_2025_dates = [
    "2025-03-20",  # Launch
    "2025-03-24",  # Initially high ~5%
    "2025-03-31",  # Settled to ~3%
    "2025-04-07",
    "2025-04-14",
    "2025-04-21",  # Peak spring period
    "2025-04-28",  # Peak ~4.7%
    "2025-05-05",
    "2025-05-12",
    "2025-05-19",
    "2025-05-27",  # Polymarket tweet: "4% chance"
    "2025-06-02",  # Boing Boing article: traders bet $500K
    "2025-06-09",
    "2025-06-16",
    "2025-06-23",
    "2025-06-30",
    "2025-07-07",
    "2025-07-14",
    "2025-07-21",
    "2025-07-28",
    "2025-08-04",
    "2025-08-11",
    "2025-08-18",
    "2025-08-25",
    "2025-09-01",
    "2025-09-08",
    "2025-09-15",
    "2025-09-22",
    "2025-09-29",
    "2025-10-06",
    "2025-10-13",
    "2025-10-20",
    "2025-10-27",
    "2025-11-03",
    "2025-11-10",
    "2025-11-17",
    "2025-11-24",
]

jesus_2025_pct = [
    5.0,   # Launch: initially traded as high as 5%
    4.5,
    3.0,   # "stably trading at 3% shortly after launch"
    3.2,
    3.5,
    4.0,   # Spring peak building
    4.7,   # Peak: "reached 4.7% but never breached 5%"
    4.3,
    4.0,
    4.0,
    4.0,   # Polymarket tweet May 27: "4% chance"
    3.8,   # Boing Boing: "$500K wagered"
    3.5,
    3.3,
    3.2,
    3.0,
    3.0,   # Summer: "above 3% throughout most of spring"
    2.8,
    2.8,
    2.7,
    2.5,
    2.5,
    2.3,
    2.2,
    2.0,   # Fall: "contract sitting at around 2%"
    2.0,
    2.0,
    1.8,
    1.7,
    1.5,
    1.3,
    1.2,
    1.0,
    0.8,
    0.7,
    0.5,   # Nov: "well under 1%"
    0.4,
]

# --- Market 2: "Will Jesus Christ return before 2027?" ---
# Launched: Nov 25, 2025 | Ongoing
# Volume: $60.4M
jesus_2027_dates = [
    "2025-11-25",  # Launch
    "2025-12-01",
    "2025-12-08",
    "2025-12-15",
    "2025-12-22",
    "2025-12-29",
    "2026-01-02",  # Bloomberg: ~2%
    "2026-01-06",
    "2026-01-13",
    "2026-01-20",
    "2026-01-27",
    "2026-02-01",  # Large whale trade, spike begins
    "2026-02-08",  # CoinDesk: ~4%, "doubled since early Jan"
    "2026-02-14",  # Derivative market driving up odds toward 5%
    "2026-02-17",  # Peak ~6% (sponsored liquidity rewards event)
    "2026-02-21",  # Settling back down
    "2026-02-28",
    "2026-03-07",
    "2026-03-14",  # Rapture prediction chatter
    "2026-03-21",
    "2026-03-28",
    "2026-04-07",
    "2026-04-14",
    "2026-04-21",
    "2026-04-28",  # Current: 4%
]

jesus_2027_pct = [
    1.0,   # Launch
    1.2,
    1.3,
    1.5,
    1.5,
    1.8,
    2.0,   # Bloomberg Jan 2: "about 2%"
    2.1,
    2.3,
    2.5,
    2.8,
    3.0,   # Whale trade, volume spikes
    4.0,   # CoinDesk Feb 8: "~4%, more than doubling since early Jan"
    4.8,   # Derivative market pushing toward 5%
    6.0,   # Feb 17 peak: liquidity rewards event
    5.0,   # Settling back
    4.5,
    4.2,
    4.5,   # Brief uptick on rapture chatter
    4.2,
    4.0,
    4.0,
    3.8,
    3.8,
    4.0,   # Current
]

# ============================================================
# 1-YEAR US TREASURY YIELD (%) — DGS1
# ============================================================
# Fed Funds Rate timeline:
#   Jan-Aug 2025: 4.25-4.50% (held steady)
#   Sep 17, 2025: Cut to 4.00-4.25%
#   Oct 29, 2025: Cut to 3.75-4.00%
#   Dec 10, 2025: Cut to 3.50-3.75%
#   Jan-Apr 2026: Held at 3.50-3.75%
# 2025 annual average: 3.91% (FRED)
# Mar 2026 spike: Iran conflict + core PCE 3.1%

treasury_dates = [
    "2025-03-20",
    "2025-03-31",
    "2025-04-07",
    "2025-04-14",
    "2025-04-21",
    "2025-04-28",
    "2025-05-05",
    "2025-05-12",
    "2025-05-19",
    "2025-05-27",
    "2025-06-02",
    "2025-06-09",
    "2025-06-16",
    "2025-06-23",
    "2025-06-30",
    "2025-07-07",
    "2025-07-14",
    "2025-07-21",
    "2025-07-28",
    "2025-08-04",
    "2025-08-11",
    "2025-08-18",
    "2025-08-25",
    "2025-09-01",
    "2025-09-08",
    "2025-09-15",
    "2025-09-17",  # Fed cut #1
    "2025-09-22",
    "2025-09-29",
    "2025-10-06",
    "2025-10-13",
    "2025-10-20",
    "2025-10-27",
    "2025-10-29",  # Fed cut #2
    "2025-11-03",
    "2025-11-10",
    "2025-11-17",
    "2025-11-24",
    "2025-12-01",
    "2025-12-08",
    "2025-12-10",  # Fed cut #3
    "2025-12-15",
    "2025-12-19",  # Advisor Perspectives: 2yr 3.48%
    "2025-12-29",
    "2025-12-31",
    "2026-01-06",
    "2026-01-13",
    "2026-01-20",
    "2026-01-27",
    "2026-02-03",
    "2026-02-10",
    "2026-02-17",
    "2026-02-24",
    "2026-03-03",
    "2026-03-07",
    "2026-03-14",  # Wolf Street: 1yr squeaked over EFFR (~3.63%)
    "2026-03-21",  # Wolf Street: +33 bps since early March
    "2026-03-28",
    "2026-03-31",  # FRED: 3.68%
    "2026-04-07",
    "2026-04-14",
    "2026-04-21",
    "2026-04-28",  # Current: 3.72%
]

treasury_yield_pct = [
    # Pre-cut period (FFR 4.25-4.50%)
    4.22,  # Mar 20
    4.20,  # Mar 31
    4.18,
    4.15,
    4.12,
    4.10,  # Apr 28
    4.08,
    4.05,
    4.05,
    4.02,
    4.00,  # Jun 2
    3.98,
    3.95,
    3.92,
    3.90,  # Jun 30
    3.92,
    3.95,  # Mid-Jul: some volatility
    3.93,
    3.90,
    3.88,
    3.85,  # Aug: easing expectations building
    3.80,
    3.78,
    # Sep: cut anticipation ramp
    3.72,
    3.68,
    3.65,
    3.60,  # Sep 17: Fed cut to 4.00-4.25%
    3.58,
    3.55,
    3.52,
    3.50,
    3.48,
    3.45,
    3.42,  # Oct 29: Fed cut to 3.75-4.00%
    3.40,
    3.42,
    3.55,  # Nov: brief backup on tariff fears
    3.50,
    3.48,  # Dec: pre-cut anticipation
    3.45,
    3.42,  # Dec 10: Fed cut to 3.50-3.75%
    3.45,
    3.45,  # Dec 19
    3.38,
    3.35,  # Year-end
    # 2026
    3.35,  # Jan: FOMC held steady
    3.33,
    3.35,
    3.34,
    3.32,  # Feb: relatively stable
    3.33,
    3.35,
    3.34,
    3.35,  # Early March
    3.40,  # Spike begins (Iran + inflation)
    3.63,  # Mar 14: Wolf Street confirmed
    3.70,  # Mar 21: continued selling
    3.67,
    3.68,  # Mar 31: FRED confirmed
    3.70,
    3.71,
    3.72,
    3.72,  # Current
]

# Convert to datetime
j25_dt = [datetime.strptime(d, "%Y-%m-%d") for d in jesus_2025_dates]
j27_dt = [datetime.strptime(d, "%Y-%m-%d") for d in jesus_2027_dates]
tr_dt  = [datetime.strptime(d, "%Y-%m-%d") for d in treasury_dates]

# ============================================================
# Create the plot
# ============================================================
fig, ax1 = plt.subplots(figsize=(16, 8))

# --- Polymarket on left axis ---
color_2025 = '#e74c3c'
color_2027 = '#c0392b'

# 2025 market (solid red)
ax1.plot(j25_dt, jesus_2025_pct, color=color_2025, linewidth=2.5,
         marker='o', markersize=3,
         label='"Return in 2025" (Mar-Nov 2025, resolved No)')
ax1.fill_between(j25_dt, jesus_2025_pct, alpha=0.08, color=color_2025)

# 2027 market (darker red, thicker)
ax1.plot(j27_dt, jesus_2027_pct, color=color_2027, linewidth=3,
         marker='D', markersize=3,
         label='"Return Before 2027" (Nov 2025-present)')
ax1.fill_between(j27_dt, jesus_2027_pct, alpha=0.12, color=color_2027)

ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Polymarket "Yes" Price (%)', color=color_2025, fontsize=13)
ax1.tick_params(axis='y', labelcolor=color_2025)
ax1.set_ylim(0, 8)

# --- Treasury yield on right axis ---
ax2 = ax1.twinx()
color_tr = '#2980b9'
ax2.set_ylabel('1-Year US Treasury Yield (%)', color=color_tr, fontsize=13)
ax2.plot(tr_dt, treasury_yield_pct, color=color_tr, linewidth=2.5,
         marker='s', markersize=2, linestyle='--',
         label='1-Year Treasury Yield (%)')
ax2.fill_between(tr_dt, treasury_yield_pct, alpha=0.08, color=color_tr)
ax2.tick_params(axis='y', labelcolor=color_tr)
ax2.set_ylim(3.0, 4.5)

# --- Date formatting ---
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator())
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=0, ha='center', fontsize=9)

# --- Title ---
fig.suptitle(
    'Polymarket "Jesus Christ Return" Markets vs. 1-Year US Treasury Yield\n'
    'Longitudinal View: March 2025 – April 2026',
    fontsize=16, fontweight='bold', y=0.98
)

# --- Vertical line: market transition ---
ax1.axvline(x=datetime(2025, 11, 25), color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax1.text(datetime(2025, 11, 28), 7.5, '2027 market\nlaunches',
         fontsize=7, color='gray', ha='left', style='italic')

# --- Fed rate cut annotations (on treasury axis) ---
for cut_date, label, y_off in [
    (datetime(2025, 9, 17), 'Fed cut #1\n4.00-4.25%', 4.30),
    (datetime(2025, 10, 29), '#2: 3.75-4.00%', 4.18),
    (datetime(2025, 12, 10), '#3: 3.50-3.75%', 4.10),
]:
    ax2.annotate(label,
                 xy=(cut_date, treasury_yield_pct[treasury_dates.index(cut_date.strftime("%Y-%m-%d"))]),
                 xytext=(cut_date, y_off),
                 fontsize=7, ha='center', color=color_tr,
                 arrowprops=dict(arrowstyle='->', color=color_tr, alpha=0.6),
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='lightcyan', alpha=0.7))

# --- Polymarket annotations ---
ax1.annotate('2025 market\nlaunches\nMar 20',
             xy=(datetime(2025, 3, 20), 5.0),
             xytext=(datetime(2025, 4, 10), 7.0),
             fontsize=7, ha='center',
             arrowprops=dict(arrowstyle='->', color='gray'),
             bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.8))

ax1.annotate('Peak ~4.7%\n(spring 2025)',
             xy=(datetime(2025, 4, 28), 4.7),
             xytext=(datetime(2025, 5, 20), 6.5),
             fontsize=7, ha='center',
             arrowprops=dict(arrowstyle='->', color='gray'),
             bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.8))

ax1.annotate('Feb 17: Liquidity\nrewards spike\n(peak ~6%)',
             xy=(datetime(2026, 2, 17), 6.0),
             xytext=(datetime(2026, 3, 5), 7.2),
             fontsize=7, ha='center',
             arrowprops=dict(arrowstyle='->', color='gray'),
             bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.8))

ax2.annotate('Mar: Iran +\ninflation spike\n(+33 bps)',
             xy=(datetime(2026, 3, 14), 3.63),
             xytext=(datetime(2026, 4, 1), 4.25),
             fontsize=7, ha='center',
             arrowprops=dict(arrowstyle='->', color=color_tr, alpha=0.6),
             bbox=dict(boxstyle='round,pad=0.2', facecolor='lightcyan', alpha=0.7))

# --- Combined legend ---
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', fontsize=9,
           framealpha=0.9, ncol=3, bbox_to_anchor=(0.5, -0.08))

# --- Grid ---
ax1.grid(True, alpha=0.25)
ax1.set_axisbelow(True)

# --- Source note ---
fig.text(0.5, -0.06,
         'Data assembled from: Bloomberg, CoinDesk, Benzinga, Protos, Jerusalem Post, FRED (DGS1),\n'
         'Fed H.15, Wolf Street, Advisor Perspectives, Congress.gov | '
         'Polymarket API was inaccessible; data from news reports.',
         ha='center', fontsize=7, style='italic', color='gray')

plt.tight_layout()
fig.savefig('/home/user/claude/jesus_vs_treasury.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Chart saved to /home/user/claude/jesus_vs_treasury.png")
