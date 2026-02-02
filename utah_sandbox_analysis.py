#!/usr/bin/env python3
"""
Utah Legal Regulatory Sandbox - Company Analysis and Visualization
Based on March 2022 Pelican Policy Institute Report + Post-2022 Research
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# =============================================================================
# COMPLETE DATA: All Companies from 2022 Pelican Report (Page 7)
# Categories based on the report's classification
# =============================================================================

# Company Name: (Innovation Category, Service Category, Valuation in $M, Status, Notes)
pre_2022_companies = {
    # NON-LAWYER OWNED (23 companies in report)
    "Jordanelle Block": ("Non-Lawyer Owned", "Housing/Property", None, "Unknown", "Real estate legal services"),
    "LawGeex": ("Non-Lawyer Owned", "Business", 45, "Acquired 2023", "AI contract review - sold to LegalSifter/RobinAI"),
    "Legal Claims Benefits (Trajector Legal)": ("Non-Lawyer Owned", "Accident/Injury", 58.3, "Active", "Veterans disability claims - $58.3M revenue (2020)"),
    "FOCL Law": ("Non-Lawyer Owned", "Marriage/Family", None, "Active", "Family law services"),
    "Hello Divorce": ("Non-Lawyer Owned", "Marriage/Family", 8.5, "Active", "Family law tech platform"),
    "Mountain West Legal Protective": ("Non-Lawyer Owned", "Housing/Property", None, "Terminated", "Homebuyer legal protection - terminated from sandbox"),
    "Davis & Sanchez": ("Non-Lawyer Owned", "Accident/Injury", None, "Active", "Workers compensation law firm"),
    "Xira Connect": ("Non-Lawyer Owned", "Intermediary", None, "Unknown", "Legal marketplace platform"),
    "Pearson Butler": ("Non-Lawyer Owned", "Full Service", None, "Active", "Full-service law firm (Elysium Holdings subsidiary)"),
    "DSD Solutions": ("Non-Lawyer Owned", "Full Service", None, "Active", "Legal clinics with document software"),
    "Off the Record Inc.": ("Non-Lawyer Owned", "Civil/Criminal Justice", None, "Active", "Traffic ticket defense app"),
    "Law on Call": ("Non-Lawyer Owned", "Non-Lawyer Provider", None, "Active", "First nonlawyer-owned US law firm (Northwest Registered Agent)"),
    "Firmly, LLC": ("Non-Lawyer Owned", "Business", None, "Active", "Estate planning services"),
    "Estate Guru": ("Non-Lawyer Owned", "Business", None, "Active", "Estate planning platform"),
    "Lawpal": ("Non-Lawyer Owned", "Other", None, "Active", "Document automation for divorce/custody"),
    "R and R Legal Services": ("Non-Lawyer Owned", "Full Service", None, "Unknown", "Full service legal"),
    "Nuttall, Brown, and Coutts": ("Non-Lawyer Owned", "Accident/Injury", None, "Active", "Personal injury law firm - 40+ years"),
    "AGS Law": ("Non-Lawyer Owned", "Business", None, "Active", "Dental/business law firm with nonlawyer partner"),
    "Blue Bee Bankruptcy Law": ("Non-Lawyer Owned", "Finance Issues", None, "Active", "Bankruptcy law - paralegal ownership"),
    "Rocket Lawyer": ("Non-Lawyer Owned", "Business", 288, "Exited 2024", "Legal tech platform - exited Utah sandbox"),
    "LawHQ": ("Non-Lawyer Owned", "Accident/Injury", 0.25, "Active", "Consumer legal tech"),
    "1Law": ("Non-Lawyer Owned", "Non-Lawyer Provider", None, "Active", "Free/low-cost legal services with chatbots"),
    "Legal Atoms": ("Non-Lawyer Owned", "Other", None, "Active", "Court document automation - Seattle-based"),

    # ALT BUSINESS STRUCTURES (9 in report - some overlap)
    "Utah Legal Advocates": ("Alt Business Structure", "Non-Lawyer Provider", None, "Unknown", "Legal advocacy services"),

    # SOFTWARE (14 in report - some overlap)
    "AAA Fair Credit Foundation": ("Software", "Finance Issues", None, "Active (Nonprofit)", "Financial counseling nonprofit - acquired by NeighborWorks"),
    "Sudbury Consulting/Code for America": ("Software", "Civil/Criminal Justice", None, "Active", "Clean Slate expungement tech"),

    # NON-LAWYER PROVIDER (12 in report - some overlap)
    "Holy Cross Ministries": ("Non-Lawyer Provider", "Other", None, "Active (Nonprofit)", "Medical debt legal advocates - nonprofit"),
    "Timpanogos Legal Center": ("Non-Lawyer Provider", "Marriage/Family", None, "Active (Nonprofit)", "Domestic violence protection - CAPP program"),
    "Rasa Legal": ("Non-Lawyer Provider", "Civil/Criminal Justice", None, "Active", "Criminal record expungement"),
}

# =============================================================================
# POST-2022 REPORT: Companies Approved After March 2022
# =============================================================================

post_2022_companies = {
    "Darrow AI": ("AI Legal Intelligence", "Other", 63, "Active", "Approved Dec 2022 - AI-powered legal intelligence"),
    "Superlegal": ("AI Contract Review", "Business", 5, "Active", "LawGeex spinoff - maintains Utah license"),
}

# =============================================================================
# Service Categories from the report (for pie chart)
# =============================================================================

service_categories = {
    "Accident/Injury": 4,
    "Business": 6,
    "Housing/Property": 5,
    "Full Service": 3,
    "Finance Issues": 5,
    "Intermediary": 3,
    "Marriage/Family": 5,
    "Civil/Criminal Justice": 3,
    "Other": 9,
}

# =============================================================================
# Innovation Categories from the report
# =============================================================================

innovation_categories = {
    "Non-Lawyer Owned": 23,
    "Management by Non-Lawyers": 17,
    "Alt Business Structures": 9,
    "Software": 14,
    "Non-Lawyer Provider": 12,
}

# =============================================================================
# FIGURE 1: Innovation Categories (From Report Page 7)
# =============================================================================

def create_innovation_chart():
    categories = list(innovation_categories.keys())
    counts = list(innovation_categories.values())
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B']

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(categories, counts, color=colors)

    ax.set_xlabel('Number of Companies', fontsize=12)
    ax.set_title('Utah Legal Sandbox Companies by Innovation Category\n(From March 2022 Pelican Policy Report)', fontsize=14, fontweight='bold')

    # Add value labels
    for bar, val in zip(bars, counts):
        ax.annotate(f'{val}',
                   xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
                   ha='left', va='center', fontsize=12, fontweight='bold',
                   xytext=(5, 0), textcoords='offset points')

    ax.set_xlim(0, max(counts) * 1.15)
    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_innovation_categories.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_innovation_categories.png")

# =============================================================================
# FIGURE 2: Service Categories (From Report Page 7)
# =============================================================================

def create_service_chart():
    categories = list(service_categories.keys())
    counts = list(service_categories.values())
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))

    fig, ax = plt.subplots(figsize=(10, 10))
    wedges, texts, autotexts = ax.pie(counts, labels=categories, autopct='%1.1f%%',
                                       colors=colors, startangle=90,
                                       explode=[0.02]*len(categories))

    ax.set_title('Utah Legal Sandbox Companies by Service Category\n(From March 2022 Pelican Policy Report)', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_service_categories.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_service_categories.png")

# =============================================================================
# FIGURE 3: Market Cap/Valuation Comparison (Horizontal Bar)
# =============================================================================

def create_valuation_chart():
    all_companies = {**pre_2022_companies, **post_2022_companies}
    companies_with_values = {}

    for company, data in all_companies.items():
        if data[2] is not None and data[2] > 0:
            companies_with_values[company] = (data[2], company in pre_2022_companies)

    # Sort by value
    sorted_companies = sorted(companies_with_values.items(), key=lambda x: x[1][0], reverse=True)

    companies = [c[0] for c in sorted_companies]
    values = [c[1][0] for c in sorted_companies]
    is_pre_2022 = [c[1][1] for c in sorted_companies]

    # Color based on pre/post 2022
    colors = ['#2E86AB' if pre else '#F18F01' for pre in is_pre_2022]

    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.barh(companies, values, color=colors)

    ax.set_xlabel('Valuation/Revenue ($ Millions)', fontsize=12)
    ax.set_title('Utah Legal Sandbox Companies - Financial Data\n(Companies with Known Valuations/Revenue)', fontsize=14, fontweight='bold')

    # Add value labels
    for bar, val in zip(bars, values):
        label = f'${val:,.1f}M'
        if val >= 1000:
            label = f'${val/1000:.2f}B'
        ax.annotate(label,
                   xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
                   ha='left', va='center', fontsize=11, fontweight='bold',
                   xytext=(5, 0), textcoords='offset points')

    # Add legend
    pre_patch = mpatches.Patch(color='#2E86AB', label='From 2022 Report')
    post_patch = mpatches.Patch(color='#F18F01', label='Post-2022 Report')
    ax.legend(handles=[pre_patch, post_patch], loc='lower right', fontsize=11)

    ax.set_xlim(0, max(values) * 1.2)
    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_valuations.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_valuations.png")

# =============================================================================
# FIGURE 4: Sandbox Growth/Decline Over Time (Utah vs Arizona)
# =============================================================================

def create_timeline_chart():
    years = ['2020\n(Launch)', '2021', '2022\n(Report)', '2023', '2024', '2025\n(April)']
    utah_entities = [5, 30, 39, 35, 20, 11]
    arizona_entities = [5, 15, 19, 45, 100, 136]

    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(years))
    width = 0.35

    bars1 = ax.bar(x - width/2, utah_entities, width, label='Utah Sandbox', color='#E63946')
    bars2 = ax.bar(x + width/2, arizona_entities, width, label='Arizona ABS', color='#457B9D')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Authorized Entities', fontsize=12)
    ax.set_title('Utah vs Arizona: Legal Regulatory Innovation Over Time\n(Divergent Trajectories Since 2022)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=11)
    ax.legend(loc='upper left', fontsize=11)

    # Add value labels
    for bar in bars1:
        ax.annotate(f'{int(bar.get_height())}',
                   xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                   ha='center', va='bottom', fontsize=10, fontweight='bold', color='#E63946')
    for bar in bars2:
        ax.annotate(f'{int(bar.get_height())}',
                   xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                   ha='center', va='bottom', fontsize=10, fontweight='bold', color='#457B9D')

    # Add annotations
    ax.annotate('Utah tightens\nrules (2024)', xy=(4, 20), xytext=(3.2, 55),
               fontsize=10, ha='center',
               arrowprops=dict(arrowstyle='->', color='#E63946', lw=1.5))
    ax.annotate('Arizona:\n600%+ growth', xy=(5, 136), xytext=(4.2, 115),
               fontsize=10, ha='center',
               arrowprops=dict(arrowstyle='->', color='#457B9D', lw=1.5))

    # Highlight the 2022 report period
    ax.axvline(x=2, color='gray', linestyle='--', alpha=0.5)
    ax.text(2.1, 5, 'Pelican\nReport', fontsize=9, color='gray')

    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_timeline.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_timeline.png")

# =============================================================================
# FIGURE 5: Company Status Breakdown
# =============================================================================

def create_status_chart():
    all_companies = {**pre_2022_companies, **post_2022_companies}

    status_counts = {
        'Active (For-Profit)': 0,
        'Active (Nonprofit)': 0,
        'Exited/Acquired': 0,
        'Terminated': 0,
        'Unknown': 0,
    }

    for company, data in all_companies.items():
        status = data[3]
        if 'Active' in status and 'Nonprofit' in status:
            status_counts['Active (Nonprofit)'] += 1
        elif 'Active' in status:
            status_counts['Active (For-Profit)'] += 1
        elif 'Terminated' in status:
            status_counts['Terminated'] += 1
        elif 'Exited' in status or 'Acquired' in status:
            status_counts['Exited/Acquired'] += 1
        else:
            status_counts['Unknown'] += 1

    labels = [k for k, v in status_counts.items() if v > 0]
    sizes = [v for v in status_counts.values() if v > 0]
    colors = ['#2E86AB', '#A8DADC', '#E63946', '#F4A261', '#6C757D']

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct=lambda p: f'{p:.1f}%\n({int(p*sum(sizes)/100)})',
                                       colors=colors[:len(labels)],
                                       startangle=90, explode=[0.03]*len(labels))

    ax.set_title('Utah Legal Sandbox Companies - Current Status\n(Based on Research as of 2025)', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('/home/user/claude/utah_sandbox_status.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: utah_sandbox_status.png")

# =============================================================================
# RUN ALL AND PRINT SUMMARY
# =============================================================================

if __name__ == "__main__":
    print("="*70)
    print("UTAH LEGAL REGULATORY SANDBOX - COMPREHENSIVE ANALYSIS")
    print("Based on March 2022 Pelican Policy Institute Report + Post-2022 Research")
    print("="*70)

    print("\nGenerating Charts...")
    create_innovation_chart()
    create_service_chart()
    create_valuation_chart()
    create_timeline_chart()
    create_status_chart()
    print("\nAll charts generated successfully!")

    # Calculate statistics
    all_companies = {**pre_2022_companies, **post_2022_companies}
    companies_with_valuation = [(k, v[2]) for k, v in all_companies.items() if v[2] is not None]
    total_valuation = sum(v[2] for v in all_companies.values() if v[2] is not None)

    print(f"\n{'='*70}")
    print("SUMMARY STATISTICS")
    print(f"{'='*70}")
    print(f"Total Unique Companies Tracked from Report: {len(pre_2022_companies)}")
    print(f"Post-2022 Report Companies Added: {len(post_2022_companies)}")
    print(f"Grand Total: {len(all_companies)}")
    print(f"\nCompanies with Known Financial Data: {len(companies_with_valuation)}")
    print(f"Total Known Valuations/Revenue: ${total_valuation:,.2f} Million")

    print(f"\n{'='*70}")
    print("COMPANIES WITH KNOWN VALUATIONS (Sorted by Value)")
    print(f"{'='*70}")
    sorted_valuations = sorted(companies_with_valuation, key=lambda x: x[1], reverse=True)
    for company, val in sorted_valuations:
        source = "2022 Report" if company in pre_2022_companies else "Post-2022"
        print(f"  {company}: ${val:,.1f}M ({source})")

    print(f"\n{'='*70}")
    print("SANDBOX TRAJECTORY SUMMARY")
    print(f"{'='*70}")
    print("  2020 (Launch): 5 entities")
    print("  2021: 30 entities")
    print("  2022 (Report): 39 entities (PEAK)")
    print("  2023: 35 entities")
    print("  2024: 20 entities (Utah tightens rules)")
    print("  2025 (April): 11 entities (72% decline from peak)")
    print(f"{'='*70}")
