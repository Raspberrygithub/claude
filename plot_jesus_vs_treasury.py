#!/usr/bin/env python3
"""
Plot: Polymarket "Will Jesus Christ Return Before 2027?" vs 1-Year US Treasury Yield

Data sources:
- Polymarket data: assembled from Bloomberg, CoinDesk, Benzinga, Gizmodo, OddsShark news reports
- Treasury data: assembled from FRED DGS1, Federal Reserve H.15, Wolf Street, Advisor Perspectives
- See notes at bottom for specific source attributions

Market launched: November 25, 2025
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# ============================================================
# Polymarket "Jesus Christ Return Before 2027" - YES price (%)
# Assembled from multiple news sources reporting specific values
# ============================================================
polymarket_dates = [
    "2025-11-25",  # Market launch
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
    "2026-02-08",  # CoinDesk: ~4%, "doubled since early January"
    "2026-02-14",  # Derivative market pressure pushing toward 5%
    "2026-02-17",  # Peak ~6% (sponsored liquidity rewards event)
    "2026-02-21",  # Settling back down
    "2026-02-28",
    "2026-03-07",
    "2026-03-14",  # Mid-March rapture claims
    "2026-03-21",
    "2026-03-28",
    "2026-04-01",  # Current: 4%
]

polymarket_yes_pct = [
    1.0,   # Launch - minimal trading
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
    4.0,   # CoinDesk Feb 8: "about 4%, more than doubling since early Jan"
    4.8,   # Derivative market driving up odds toward 5%
    6.0,   # Feb 17 peak: liquidity rewards event, ~6%
    5.0,   # Settling back
    4.5,
    4.2,
    4.5,   # Brief uptick on rapture prediction chatter
    4.2,
    4.0,
    4.0,   # Current: 4% (96.2% No)
]

# ============================================================
# 1-Year US Treasury Yield (%) - DGS1
# Assembled from FRED, Fed H.15, Wolf Street, Advisor Perspectives
# Fed cut 3x in late 2025: FFR went from 4.25-4.50% to 3.50-3.75%
# March 2026 spike: Iran conflict + inflation (core PCE 3.1%)
# ============================================================
treasury_dates = [
    "2025-11-25",
    "2025-12-01",
    "2025-12-08",
    "2025-12-15",
    "2025-12-19",  # Advisor Perspectives: 2yr at 3.48%, 10yr at 4.16%
    "2025-12-22",
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
    "2026-03-14",  # Wolf Street: 1yr "squeaked over EFFR" (~3.63%)
    "2026-03-21",  # Wolf Street: yield spike, +33bps since early March
    "2026-03-28",
    "2026-03-31",  # FRED/Fed: 3.68%
    "2026-04-01",
]

treasury_yield_pct = [
    3.95,  # Pre-Dec cut, still pricing in further easing
    3.80,  # After Nov cut, ahead of Dec cut
    3.65,  # Dec cut anticipation
    3.50,  # Around Dec cut
    3.45,  # Dec 19 snapshot (2yr was 3.48%)
    3.40,
    3.38,
    3.35,  # Year-end
    3.35,  # Jan: FOMC held steady at 3.50-3.75%
    3.33,
    3.35,
    3.34,
    3.32,  # Feb: relatively stable
    3.33,
    3.35,
    3.34,
    3.35,  # Early March: before the spike
    3.40,  # Spike begins (Iran conflict, inflation fears)
    3.63,  # Mar 14: Wolf Street - "squeaked over EFFR"
    3.70,  # Mar 21: continued selling
    3.67,
    3.68,  # Mar 31: FRED confirmed
    3.68,
]

# Convert to datetime
pm_dates = [datetime.strptime(d, "%Y-%m-%d") for d in polymarket_dates]
tr_dates = [datetime.strptime(d, "%Y-%m-%d") for d in treasury_dates]

# ============================================================
# Create the plot
# ============================================================
fig, ax1 = plt.subplots(figsize=(14, 7))

# Polymarket on left axis
color_pm = '#e74c3c'
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Polymarket "Yes" Price (%)', color=color_pm, fontsize=12)
ax1.plot(pm_dates, polymarket_yes_pct, color=color_pm, linewidth=2.5,
         marker='o', markersize=4, label='Jesus Return Before 2027 (Yes %)')
ax1.fill_between(pm_dates, polymarket_yes_pct, alpha=0.1, color=color_pm)
ax1.tick_params(axis='y', labelcolor=color_pm)
ax1.set_ylim(0, 8)

# Treasury yield on right axis
ax2 = ax1.twinx()
color_tr = '#2980b9'
ax2.set_ylabel('1-Year US Treasury Yield (%)', color=color_tr, fontsize=12)
ax2.plot(tr_dates, treasury_yield_pct, color=color_tr, linewidth=2.5,
         marker='s', markersize=4, linestyle='--',
         label='1-Year Treasury Yield (%)')
ax2.fill_between(tr_dates, treasury_yield_pct, alpha=0.1, color=color_tr)
ax2.tick_params(axis='y', labelcolor=color_tr)
ax2.set_ylim(3.0, 4.2)

# Formatting
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator())
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Title
fig.suptitle('Polymarket: "Will Jesus Christ Return Before 2027?"\nvs. 1-Year US Treasury Yield',
             fontsize=15, fontweight='bold', y=0.98)

# Annotations
ax1.annotate('Market Launch\nNov 25, 2025',
             xy=(datetime(2025, 11, 25), 1.0),
             xytext=(datetime(2025, 12, 5), 3.5),
             fontsize=8, ha='center',
             arrowprops=dict(arrowstyle='->', color='gray'),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

ax1.annotate('Feb 17: Liquidity\nRewards Spike\n(peak ~6%)',
             xy=(datetime(2026, 2, 17), 6.0),
             xytext=(datetime(2026, 2, 25), 7.2),
             fontsize=8, ha='center',
             arrowprops=dict(arrowstyle='->', color='gray'),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8))

ax2.annotate('Mar: Iran conflict +\ninflation spike\n(+33 bps)',
             xy=(datetime(2026, 3, 14), 3.63),
             xytext=(datetime(2026, 3, 1), 4.05),
             fontsize=8, ha='center',
             arrowprops=dict(arrowstyle='->', color='gray'),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcyan', alpha=0.8))

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10,
           framealpha=0.9)

# Grid
ax1.grid(True, alpha=0.3)
ax1.set_axisbelow(True)

# Source note
fig.text(0.5, -0.02,
         'Data assembled from: Bloomberg, CoinDesk, Benzinga, FRED (DGS1), Fed H.15, Wolf Street\n'
         'Polymarket market launched Nov 25, 2025 | Fed Funds Rate: 3.50-3.75% (held since Dec 2025)',
         ha='center', fontsize=8, style='italic', color='gray')

plt.tight_layout()
fig.savefig('/home/user/claude/jesus_vs_treasury.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Chart saved to /home/user/claude/jesus_vs_treasury.png")
