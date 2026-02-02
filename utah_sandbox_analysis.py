#!/usr/bin/env python3
"""
Utah Legal Regulatory Sandbox - Company Analysis and Visualization
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# =============================================================================
# DATA: Companies from 2022 Report (Pre-2022 Report Entities)
# =============================================================================

pre_2022_companies = {
    # Company Name: (Category, Valuation/Market Cap in millions, Status, Publicly Traded)
    "Rocket Lawyer": ("Legal Tech Platform", 288, "Exited Utah Sandbox (2024)", False),
    "LegalZoom (NASDAQ: LZ)": ("Legal Tech Platform", 1790, "Arizona ABS (Not Utah)", True),
    "1LAW": ("Access to Justice", None, "Active", False),
    "LawHQ": ("Consumer Legal Tech", 0.25, "Active", False),
    "LawGeex": ("AI Contract Review", 45, "Acquired 2023", False),
    "Hello Divorce": ("Family Law Tech", 8.5, "Active", False),
    "Estate Guru": ("Estate Planning", None, "Active", False),
    "Law on Call": ("General Legal Services", None, "Active", False),
    "LawPal": ("Document Automation", None, "Active", False),
    "Elysium Legal": ("Estate Planning", None, "Active", False),
    "Holy Cross Ministries": ("Nonprofit/Medical Debt", None, "Active (Nonprofit)", False),
    "Timpanogos Legal Center": ("Nonprofit/Domestic Violence", None, "Active (Nonprofit)", False),
    "Blue Bee Bankruptcy Law": ("Bankruptcy Law", None, "Active", False),
    "Rasa Legal": ("Criminal Record Expungement", None, "Active", False),
    "Off the Record": ("Traffic Ticket Platform", None, "Unknown", False),
    "Xira Connect": ("Legal Marketplace", None, "Unknown", False),
}

# =============================================================================
# DATA: Companies Added Since 2022 Report
# =============================================================================

post_2022_companies = {
    # Company Name: (Category, Valuation/Market Cap in millions, Status, Publicly Traded)
    "Darrow AI": ("AI Legal Intelligence", 63, "Active (Approved Dec 2022)", False),
    "Superlegal": ("AI Contract Review", 5, "Active (LawGeex spinoff)", False),
}

# =============================================================================
# FIGURE 1: Companies by Category (Bar Chart)
# =============================================================================

def create_category_chart():
    categories = {}

    for company, data in {**pre_2022_companies, **post_2022_companies}.items():
        cat = data[0]
        if cat not in categories:
            categories[cat] = {'pre_2022': 0, 'post_2022': 0}

    for company, data in pre_2022_companies.items():
        categories[data[0]]['pre_2022'] += 1

    for company, data in post_2022_companies.items():
        categories[data[0]]['post_2022'] += 1

    cats = list(categories.keys())
    pre_counts = [categories[c]['pre_2022'] for c in cats]
    post_counts = [categories[c]['post_2022'] for c in cats]

    x = np.arange(len(cats))
    width = 0.35

    fig, ax = plt.subplots(figsize=(14, 8))
    bars1 = ax.bar(x - width/2, pre_counts, width, label='Pre-2022 Report', color='#2E86AB')
    bars2 = ax.bar(x + width/2, post_counts, width, label='Post-2022 Report', color='#F18F01')

    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Number of Companies', fontsize=12)
    ax.set_title('Utah Legal Sandbox Companies by Category\n(Pre vs Post March 2022 Pelican Report)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(cats, rotation=45, ha='right', fontsize=10)
    ax.legend()
    ax.set_ylim(0, max(max(pre_counts), max(post_counts)) + 1)

    # Add value labels on bars
    for bar in bars1:
        if bar.get_height() > 0:
            ax.annotate(f'{int(bar.get_height())}',
                       xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                       ha='center', va='bottom', fontsize=10)
    for bar in bars2:
        if bar.get_height() > 0:
            ax.annotate(f'{int(bar.get_height())}',
                       xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                       ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_categories.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_categories.png")

# =============================================================================
# FIGURE 2: Market Cap/Valuation Comparison (Horizontal Bar)
# =============================================================================

def create_valuation_chart():
    companies_with_values = {}

    for company, data in {**pre_2022_companies, **post_2022_companies}.items():
        if data[1] is not None and data[1] > 0:
            companies_with_values[company] = data[1]

    # Sort by value
    sorted_companies = sorted(companies_with_values.items(), key=lambda x: x[1], reverse=True)

    companies = [c[0] for c in sorted_companies]
    values = [c[1] for c in sorted_companies]

    # Color based on pre/post 2022
    colors = []
    for c in companies:
        if c in pre_2022_companies:
            colors.append('#2E86AB')  # Blue for pre-2022
        else:
            colors.append('#F18F01')  # Orange for post-2022

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(companies, values, color=colors)

    ax.set_xlabel('Valuation/Market Cap ($ Millions)', fontsize=12)
    ax.set_title('Utah Legal Sandbox Companies - Valuations & Market Caps\n(Companies with Known Financial Data)', fontsize=14, fontweight='bold')

    # Add value labels
    for bar, val in zip(bars, values):
        label = f'${val:,.0f}M'
        if val >= 1000:
            label = f'${val/1000:.2f}B'
        ax.annotate(label,
                   xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
                   ha='left', va='center', fontsize=10, xytext=(5, 0),
                   textcoords='offset points')

    # Add legend
    pre_patch = mpatches.Patch(color='#2E86AB', label='Pre-2022 Report')
    post_patch = mpatches.Patch(color='#F18F01', label='Post-2022 Report')
    ax.legend(handles=[pre_patch, post_patch], loc='lower right')

    ax.set_xlim(0, max(values) * 1.15)
    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_valuations.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_valuations.png")

# =============================================================================
# FIGURE 3: Sandbox Growth/Decline Over Time
# =============================================================================

def create_timeline_chart():
    years = ['2020\n(Launch)', '2021', '2022', '2023', '2024', '2025\n(April)']
    utah_entities = [5, 30, 39, 35, 20, 11]
    arizona_entities = [5, 15, 19, 45, 100, 136]

    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(years))
    width = 0.35

    bars1 = ax.bar(x - width/2, utah_entities, width, label='Utah Sandbox', color='#E63946')
    bars2 = ax.bar(x + width/2, arizona_entities, width, label='Arizona ABS', color='#457B9D')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Authorized Entities', fontsize=12)
    ax.set_title('Utah vs Arizona: Legal Regulatory Innovation Over Time\n(Utah Sandbox vs Arizona Alternative Business Structures)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=11)
    ax.legend(loc='upper left')

    # Add value labels
    for bar in bars1:
        ax.annotate(f'{int(bar.get_height())}',
                   xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
    for bar in bars2:
        ax.annotate(f'{int(bar.get_height())}',
                   xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                   ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Add annotations
    ax.annotate('Utah tightens\nrules (2024)', xy=(4, 20), xytext=(3.5, 50),
               fontsize=9, ha='center',
               arrowprops=dict(arrowstyle='->', color='gray'))
    ax.annotate('Arizona\nexplosive growth', xy=(5, 136), xytext=(4.3, 110),
               fontsize=9, ha='center',
               arrowprops=dict(arrowstyle='->', color='gray'))

    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_timeline.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_timeline.png")

# =============================================================================
# FIGURE 4: Company Status Pie Chart
# =============================================================================

def create_status_chart():
    all_companies = {**pre_2022_companies, **post_2022_companies}

    status_counts = {
        'Active': 0,
        'Exited/Acquired': 0,
        'Unknown': 0,
        'Nonprofit': 0
    }

    for company, data in all_companies.items():
        status = data[2]
        if 'Active' in status and 'Nonprofit' not in status:
            status_counts['Active'] += 1
        elif 'Nonprofit' in status:
            status_counts['Nonprofit'] += 1
        elif 'Exited' in status or 'Acquired' in status or 'Arizona' in status:
            status_counts['Exited/Acquired'] += 1
        else:
            status_counts['Unknown'] += 1

    labels = [k for k, v in status_counts.items() if v > 0]
    sizes = [v for v in status_counts.values() if v > 0]
    colors = ['#2E86AB', '#E63946', '#A8DADC', '#F4A261']

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                       colors=colors[:len(labels)],
                                       startangle=90, explode=[0.02]*len(labels))

    ax.set_title('Utah Legal Sandbox Companies by Current Status', fontsize=14, fontweight='bold')

    # Add count labels
    for i, (wedge, size) in enumerate(zip(wedges, sizes)):
        ang = (wedge.theta2 - wedge.theta1)/2. + wedge.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        ax.annotate(f'({size} companies)',
                   xy=(x*0.7, y*0.7),
                   ha='center', va='center',
                   fontsize=10)

    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_status.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_status.png")

# =============================================================================
# RUN ALL
# =============================================================================

if __name__ == "__main__":
    print("Generating Utah Legal Sandbox Analysis Charts...")
    create_category_chart()
    create_valuation_chart()
    create_timeline_chart()
    create_status_chart()
    print("\nAll charts generated successfully!")

    # Print summary statistics
    all_companies = {**pre_2022_companies, **post_2022_companies}
    total_valuation = sum(v[1] for v in all_companies.values() if v[1] is not None)

    print(f"\n{'='*60}")
    print("SUMMARY STATISTICS")
    print(f"{'='*60}")
    print(f"Total Companies Tracked: {len(all_companies)}")
    print(f"Pre-2022 Report Companies: {len(pre_2022_companies)}")
    print(f"Post-2022 Report Companies: {len(post_2022_companies)}")
    print(f"Companies with Known Valuations: {sum(1 for v in all_companies.values() if v[1] is not None)}")
    print(f"Total Known Valuations/Market Cap: ${total_valuation:,.2f} Million")
    print(f"{'='*60}")
