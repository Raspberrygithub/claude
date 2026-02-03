#!/usr/bin/env python3
"""
Catawba Digital Economic Zone (CDEZ) Research Visualizations
Generates charts and graphs for the fintech analysis report
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Create output directory
output_dir = '/home/user/claude/cdez_graphs'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# Graph 1: Global Fintech VC Investment Timeline
# ============================================================
def create_fintech_investment_timeline():
    years = ['2019', '2020', '2021', '2022', '2023', '2024']
    investments = [216.8, 124, 229, 150, 118.2, 130]  # in billions

    fig, ax = plt.subplots(figsize=(12, 7))

    colors = ['#2E86AB' if year not in ['2022', '2023'] else '#E94F37' for year in years]
    bars = ax.bar(years, investments, color=colors, edgecolor='black', linewidth=1.2)

    # Add CDEZ launch annotation
    ax.annotate('CDEZ Launches\n(Late 2022)',
                xy=(3, 150), xytext=(3.5, 190),
                fontsize=11, ha='center',
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

    # Add value labels on bars
    for bar, val in zip(bars, investments):
        height = bar.get_height()
        ax.annotate(f'${val}B',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Investment (Billions USD)', fontsize=12)
    ax.set_title('Global Fintech VC Investment Timeline\nCDEZ Launched During Market Decline', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 260)

    # Legend
    legend_elements = [mpatches.Patch(facecolor='#2E86AB', edgecolor='black', label='Normal Market'),
                       mpatches.Patch(facecolor='#E94F37', edgecolor='black', label='Decline Period (CDEZ Launch)')]
    ax.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_fintech_investment_timeline.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: 01_fintech_investment_timeline.png")

# ============================================================
# Graph 2: Wyoming DAO Registrations Growth
# ============================================================
def create_wyoming_dao_growth():
    dates = ['Jul 2021\n(Law Effective)', 'Dec 2021', 'Oct 2022', 'Mar 2023']
    registrations = [0, 130, 500, 800]

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(dates, registrations, marker='o', markersize=12, linewidth=3,
            color='#2E86AB', markerfacecolor='#E94F37', markeredgewidth=2)

    # Fill area under curve
    ax.fill_between(range(len(dates)), registrations, alpha=0.3, color='#2E86AB')

    # Add CDEZ comparison annotation
    ax.annotate('CDEZ Launches\n(No public data\navailable)',
                xy=(2, 500), xytext=(2.5, 650),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', alpha=0.7))

    # Add value labels
    for i, (date, val) in enumerate(zip(dates, registrations)):
        ax.annotate(f'{val}', xy=(i, val), xytext=(0, 10),
                    textcoords="offset points", ha='center', fontsize=12, fontweight='bold')

    ax.set_ylabel('Number of DAO Registrations', fontsize=12)
    ax.set_title('Wyoming DAO Registrations Growth\n(Benchmark Comparison for CDEZ)', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 900)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_wyoming_dao_growth.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: 02_wyoming_dao_growth.png")

# ============================================================
# Graph 3: DAO Formation Cost Comparison
# ============================================================
def create_cost_comparison():
    jurisdictions = ['Marshall Islands', 'Wyoming', 'Tennessee', 'Vermont', 'CDEZ']
    costs = [5000, 500, 500, 500, 250]

    fig, ax = plt.subplots(figsize=(12, 7))

    colors = ['#E94F37', '#2E86AB', '#2E86AB', '#2E86AB', '#28A745']
    bars = ax.barh(jurisdictions, costs, color=colors, edgecolor='black', linewidth=1.2)

    # Add value labels
    for bar, cost in zip(bars, costs):
        width = bar.get_width()
        ax.annotate(f'${cost:,}',
                    xy=(width, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=12, fontweight='bold')

    ax.set_xlabel('Formation Cost (USD)', fontsize=12)
    ax.set_title('DAO/LLC Formation Cost Comparison\nCDEZ Offers Most Competitive Pricing', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 6000)

    # Legend
    legend_elements = [mpatches.Patch(facecolor='#28A745', edgecolor='black', label='CDEZ (Most Competitive)'),
                       mpatches.Patch(facecolor='#2E86AB', edgecolor='black', label='US State Jurisdictions'),
                       mpatches.Patch(facecolor='#E94F37', edgecolor='black', label='International (Highest Cost)')]
    ax.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_cost_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: 03_cost_comparison.png")

# ============================================================
# Graph 4: CDEZ Regulatory Milestone Timeline
# ============================================================
def create_regulatory_timeline():
    fig, ax = plt.subplots(figsize=(14, 8))

    milestones = [
        ('Feb 2022', 'Commercial Code\nEnacted', 0),
        ('Aug 2022', 'First Academic\nPaper Published', 1),
        ('Nov 2022', 'Incorporation\nPlatform Launch', 2),
        ('Dec 2022', 'CDEZ Officially\nLaunches', 3),
        ('Apr 2023', 'Banking Code\nPassed', 4),
        ('Jul 2023', 'Second Academic\nPaper Published', 5),
        ('Feb 2024', 'Banking Commission\nAppointed', 6),
    ]

    # Timeline
    ax.axhline(y=0.5, color='#2E86AB', linewidth=4, alpha=0.7)

    for date, event, i in milestones:
        y_offset = 0.7 if i % 2 == 0 else 0.3
        color = '#E94F37' if 'Banking' in event else '#2E86AB'

        ax.scatter(i, 0.5, s=200, color=color, zorder=5, edgecolor='black', linewidth=2)
        ax.annotate(f'{date}\n{event}',
                    xy=(i, 0.5), xytext=(i, y_offset),
                    ha='center', va='center' if y_offset > 0.5 else 'top',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8),
                    arrowprops=dict(arrowstyle='-', color='gray', lw=1))

    ax.set_xlim(-0.5, 7)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('CDEZ Regulatory Development Timeline\n(Key Milestones 2022-2024)', fontsize=14, fontweight='bold', y=1.02)

    # Legend
    legend_elements = [mpatches.Patch(facecolor='#E94F37', edgecolor='black', label='Banking Milestones'),
                       mpatches.Patch(facecolor='#2E86AB', edgecolor='black', label='General Milestones')]
    ax.legend(handles=legend_elements, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.05))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_regulatory_timeline.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: 04_regulatory_timeline.png")

# ============================================================
# Graph 5: Catawba Nation Economic Diversification
# ============================================================
def create_economic_diversification():
    fig, ax = plt.subplots(figsize=(12, 7))

    categories = ['Two Kings Casino\n(Investment)', 'Charlottesville Angel\nNetwork Investment\n(Estimated)',
                  'CDEZ Annual Fees\n(Theoretical 100 entities)']
    values = [1000, 0.2, 0.01]  # in millions

    colors = ['#2E86AB', '#28A745', '#FFC107']
    bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)

    ax.set_ylabel('Investment/Revenue (Millions USD)', fontsize=12)
    ax.set_title('Catawba Nation Economic Initiatives Scale Comparison\n(Logarithmic Scale)', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.set_ylim(0.001, 2000)

    # Add value labels
    for bar, val in zip(bars, values):
        height = bar.get_height()
        label = f'${val*1000:,.0f}K' if val < 1 else f'${val:,.0f}M'
        ax.annotate(label,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_economic_diversification.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: 05_economic_diversification.png")

# ============================================================
# Graph 6: Data Availability Assessment
# ============================================================
def create_data_availability():
    fig, ax = plt.subplots(figsize=(12, 8))

    categories = [
        'Academic Papers',
        'Regulatory Framework',
        'Fee Structure',
        'Leadership Info',
        'Investment Amounts',
        'Registered Companies',
        'Revenue Data',
        'Success Metrics',
        'Bank Charter Apps'
    ]

    # 0 = Not Available, 1 = Partial, 2 = Available
    availability = [2, 2, 2, 2, 1, 0, 0, 0, 0]

    colors = ['#28A745' if v == 2 else '#FFC107' if v == 1 else '#E94F37' for v in availability]

    bars = ax.barh(categories, availability, color=colors, edgecolor='black', linewidth=1.2)

    ax.set_xlabel('Data Availability', fontsize=12)
    ax.set_title('CDEZ Public Data Availability Assessment\nSignificant Transparency Gaps Identified', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 2.5)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['Not Available', 'Partial', 'Available'])

    # Legend
    legend_elements = [mpatches.Patch(facecolor='#28A745', edgecolor='black', label='Available'),
                       mpatches.Patch(facecolor='#FFC107', edgecolor='black', label='Partial'),
                       mpatches.Patch(facecolor='#E94F37', edgecolor='black', label='Not Available')]
    ax.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/06_data_availability.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: 06_data_availability.png")

# ============================================================
# Graph 7: Jurisdictional Feature Comparison
# ============================================================
def create_feature_comparison():
    fig, ax = plt.subplots(figsize=(14, 9))

    features = ['DAO\nSupport', 'Bank\nCharters', 'Crypto\nHolding', 'Fast\nRegulation', 'Federal\nCertainty', 'Cost\nAdvantage']

    # Scores out of 5
    cdez_scores = [5, 4, 5, 5, 2, 5]
    wyoming_scores = [5, 3, 4, 2, 5, 3]
    delaware_scores = [1, 5, 2, 2, 5, 2]

    x = np.arange(len(features))
    width = 0.25

    bars1 = ax.bar(x - width, cdez_scores, width, label='CDEZ', color='#28A745', edgecolor='black')
    bars2 = ax.bar(x, wyoming_scores, width, label='Wyoming', color='#2E86AB', edgecolor='black')
    bars3 = ax.bar(x + width, delaware_scores, width, label='Delaware', color='#FFC107', edgecolor='black')

    ax.set_ylabel('Score (1-5)', fontsize=12)
    ax.set_title('Jurisdictional Feature Comparison\nCDEZ vs. Established Competitors', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(features)
    ax.set_ylim(0, 6)
    ax.legend(loc='upper right')

    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_feature_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: 07_feature_comparison.png")

# ============================================================
# Graph 8: US Fintech Market Context
# ============================================================
def create_us_fintech_context():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Pie chart - Regional distribution
    regions = ['North America', 'Europe', 'Asia Pacific', 'Rest of World']
    sizes = [36.75, 28, 25, 10.25]
    colors = ['#2E86AB', '#28A745', '#FFC107', '#E94F37']
    explode = (0.1, 0, 0, 0)

    ax1.pie(sizes, explode=explode, labels=regions, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.set_title('Global Fintech Deal Distribution\n(US Leads with 36.75%)', fontsize=12, fontweight='bold')

    # Bar chart - Company counts
    regions2 = ['North\nAmerica', 'Europe', 'Asia\nPacific', 'Latin\nAmerica']
    companies = [12000, 9000, 7500, 3000]

    bars = ax2.bar(regions2, companies, color=['#2E86AB', '#28A745', '#FFC107', '#E94F37'], edgecolor='black')
    ax2.set_ylabel('Number of Fintech Companies', fontsize=12)
    ax2.set_title('Fintech Companies by Region\n(North America: 12,000+)', fontsize=12, fontweight='bold')

    for bar, val in zip(bars, companies):
        height = bar.get_height()
        ax2.annotate(f'{val:,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/08_us_fintech_context.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: 08_us_fintech_context.png")

# ============================================================
# Main execution
# ============================================================
if __name__ == '__main__':
    print("Generating CDEZ Research Visualizations...")
    print("=" * 50)

    create_fintech_investment_timeline()
    create_wyoming_dao_growth()
    create_cost_comparison()
    create_regulatory_timeline()
    create_economic_diversification()
    create_data_availability()
    create_feature_comparison()
    create_us_fintech_context()

    print("=" * 50)
    print(f"All graphs saved to: {output_dir}/")
    print("\nGraphs generated:")
    for f in sorted(os.listdir(output_dir)):
        print(f"  - {f}")
