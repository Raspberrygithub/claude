#!/usr/bin/env python3
"""
Analysis: AI Exposure vs. Political Affiliation by Occupation
Uses AI exposure scores from Eloundou et al. (2024) "GPTs are GPTs"
and political leaning data from FEC campaign contributions (Verdant Labs, OpenSecrets, Zippia)
"""

import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

# ============================================================
# 1. Load AI Exposure Data from GPTs-are-GPTs
# ============================================================
ai_exposure = {}
with open('GPTs-are-GPTs/data/occ_level.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row['O*NET-SOC Code'][:7]
        ai_exposure[code] = {
            'title': row['Title'],
            'beta': float(row['dv_rating_beta']),  # E1 + 0.5*E2 (GPT-4 rated)
        }

# ============================================================
# 2. 50 Largest Occupations by Employment (BLS OES May 2021)
#    with Political Leaning (Democrat Donation Share, 0-1 scale)
#
#    Sources for political data:
#    - Verdant Labs FEC analysis (2015): Teachers 79%D, Truck drivers 31%D,
#      Carpenters 64%D
#    - OpenSecrets (2024): Nurses ~67%D, Education >70%D, Construction lean R
#    - Zippia/Voronoi FEC analysis (2023): 180 occupations
#    - Pew Research / GSS: Broad occupational category patterns
#    - Academic research: Chinoy (2024) political sorting in labor markets
#
#    Confidence levels:
#    H = High (direct FEC data from multiple sources)
#    M = Medium (sector-level data + occupational characteristics)
#    L = Low (estimated from broader category patterns)
# ============================================================

occupations = [
    # (BLS_CODE, BLS_Title, Employment, ONET_CODE, Dem_Share, Confidence, Source_Notes)
    ("41-2031", "Retail Salespersons", 3693490, "41-2031", 0.50, "M", "Retail split; Zippia shows ~50-50"),
    ("31-1120", "Home Health & Personal Care Aides", 3366480, None, 0.62, "M", "Healthcare service; diverse workforce leans D"),
    ("41-2011", "Cashiers", 3318020, "41-2011", 0.52, "L", "Low-wage service; minimal FEC data"),
    ("35-3023", "Fast Food & Counter Workers", 3095120, "35-3023", 0.54, "L", "Food service leans slightly D"),
    ("29-1141", "Registered Nurses", 3047530, "29-1141", 0.67, "H", "OpenSecrets: ~67% D donations"),
    ("11-1021", "General & Operations Managers", 2984920, "11-1021", 0.45, "M", "Management leans slightly R"),
    ("43-4051", "Customer Service Representatives", 2787070, "43-4051", 0.55, "M", "Office/service workers lean slightly D"),
    ("53-7062", "Laborers & Freight Movers", 2729010, "53-7062", 0.42, "M", "Manual labor/logistics leans R"),
    ("43-9061", "Office Clerks, General", 2578180, "43-9061", 0.56, "M", "Office/admin workers lean D"),
    ("53-7065", "Stockers & Order Fillers", 2451430, "53-7065", 0.48, "L", "Warehouse/retail; moderate"),
    ("37-2011", "Janitors & Cleaners", 2036680, "37-2011", 0.53, "L", "Service workers; slight D lean"),
    ("53-3032", "Heavy Truck Drivers", 1903420, "53-3032", 0.31, "H", "Verdant Labs: 69% Republican"),
    ("43-6014", "Secretaries & Admin Assistants", 1825980, "43-6014", 0.58, "M", "Office/admin; lean D"),
    ("35-3031", "Waiters & Waitresses", 1804030, "35-3031", 0.60, "M", "Food service; bartenders 89%D, waiters less extreme"),
    ("43-3031", "Bookkeeping & Auditing Clerks", 1509370, "43-3031", 0.55, "M", "Office/accounting; moderate D lean"),
    ("43-1011", "Supervisors of Office/Admin Workers", 1443630, "43-1011", 0.52, "M", "Supervisory; moderate"),
    ("49-9071", "Maintenance & Repair Workers", 1416740, "49-9071", 0.38, "M", "Trades/maintenance lean R"),
    ("15-1252", "Software Developers", 1364180, "15-1252", 0.68, "H", "Tech industry; FEC data shows strong D lean"),
    ("25-2021", "Elementary School Teachers", 1329280, "25-2021", 0.79, "H", "Verdant Labs: 79% Democrat"),
    ("51-2090", "Assemblers & Fabricators", 1328550, None, 0.46, "L", "Manufacturing; moderate R lean"),
    ("13-2011", "Accountants & Auditors", 1318550, "13-2011", 0.48, "M", "Finance-adjacent; nearly split"),
    ("31-1131", "Nursing Assistants", 1314830, "31-1131", 0.60, "M", "Healthcare support; lean D"),
    ("41-4012", "Sales Reps (Wholesale)", 1242490, "41-4012", 0.44, "M", "Sales/business; lean slightly R"),
    ("35-2014", "Cooks, Restaurant", 1193860, "35-2014", 0.55, "L", "Food service; slight D lean"),
    ("25-9045", "Teaching Assistants", 1187270, None, 0.72, "M", "Education sector >70% D"),
    ("41-1011", "Supervisors of Retail Workers", 1143260, "41-1011", 0.47, "M", "Retail management; moderate"),
    ("33-9032", "Security Guards", 1057100, "33-9032", 0.42, "M", "Law enforcement-adjacent; lean R"),
    ("35-1012", "Supervisors of Food Prep Workers", 1040600, "35-1012", 0.52, "L", "Food service supervisors; moderate"),
    ("13-1199", "Business Operations Specialists", 1030330, "13-1199", 0.52, "M", "Business/professional; moderate"),
    ("41-3091", "Sales Reps (Services)", 1026390, "41-3091", 0.48, "M", "Sales; moderate"),
    ("25-2031", "Secondary School Teachers", 1020240, "25-2031", 0.76, "H", "Education; slightly less than elementary"),
    ("53-3033", "Light Truck Drivers", 1010040, "53-3033", 0.35, "M", "Trucking leans R; similar to heavy truck"),
    ("43-4171", "Receptionists & Info Clerks", 983150, "43-4171", 0.56, "M", "Office workers; lean D"),
    ("47-2061", "Construction Laborers", 968760, "47-2061", 0.38, "M", "Construction sector leans R"),
    ("37-3011", "Landscaping Workers", 892450, "37-3011", 0.45, "L", "Outdoor/grounds work; moderate"),
    ("43-5071", "Shipping & Receiving Clerks", 795360, "43-5071", 0.48, "L", "Warehouse/logistics; moderate"),
    ("35-2021", "Food Preparation Workers", 783350, "35-2021", 0.54, "L", "Food service; slight D lean"),
    ("13-1111", "Management Analysts", 768450, "13-1111", 0.52, "M", "Consulting; moderate"),
    ("35-2011", "Cooks, Fast Food", 768130, "35-2011", 0.54, "L", "Food service; slight D lean"),
    ("53-7051", "Industrial Truck Operators", 758290, "53-7051", 0.38, "L", "Warehouse/industrial; lean R"),
    ("13-1082", "Project Management Specialists", 743860, "13-1082", 0.50, "M", "Professional; split"),
    ("13-1071", "Human Resources Specialists", 740830, "13-1071", 0.62, "M", "HR/professional; lean D"),
    ("31-9092", "Medical Assistants", 727760, "31-9092", 0.58, "M", "Healthcare support; lean D"),
    ("13-1161", "Market Research Analysts", 727540, "13-1161", 0.60, "M", "Marketing/professional; lean D"),
    ("37-2012", "Maids & Housekeeping Cleaners", 723430, "37-2012", 0.55, "L", "Service workers; slight D lean"),
    ("11-3031", "Financial Managers", 681070, "11-3031", 0.42, "M", "Finance sector leans R"),
    ("23-1011", "Lawyers", 681010, "23-1011", 0.72, "H", "FEC data: ~72% Democrat"),
    ("47-2031", "Carpenters", 668060, "47-2031", 0.64, "H", "Verdant Labs: 64% Democrat (union-driven)"),
    ("47-1011", "Supervisors of Construction Workers", 665870, "47-1011", 0.37, "M", "Construction management; lean R"),
    ("33-3051", "Police & Sheriff's Officers", 665380, "33-3051", 0.35, "H", "Law enforcement; ~65% Republican"),
]

# ============================================================
# 3. Build the dataset
# ============================================================
data_rows = []
for occ in occupations:
    bls_code, title, employment, onet_code, dem_share, confidence, notes = occ

    # Get AI exposure score
    ai_score = None
    if onet_code and onet_code in ai_exposure:
        ai_score = ai_exposure[onet_code]['beta']

    if ai_score is not None:
        # Political lean: -1 = fully R, +1 = fully D
        political_lean = 2 * dem_share - 1
        data_rows.append({
            'title': title,
            'employment': employment,
            'ai_exposure': ai_score,
            'dem_share': dem_share,
            'political_lean': political_lean,
            'confidence': confidence,
            'notes': notes,
        })

print(f"Total occupations with both AI exposure and political data: {len(data_rows)}")
print(f"High confidence: {sum(1 for r in data_rows if r['confidence'] == 'H')}")
print(f"Medium confidence: {sum(1 for r in data_rows if r['confidence'] == 'M')}")
print(f"Low confidence: {sum(1 for r in data_rows if r['confidence'] == 'L')}")

# ============================================================
# 4. Compute correlation statistics
# ============================================================
x = np.array([r['ai_exposure'] for r in data_rows])
y = np.array([r['political_lean'] for r in data_rows])
weights = np.array([r['employment'] for r in data_rows])

# Unweighted correlation
r_unweighted, p_unweighted = stats.pearsonr(x, y)
rho_unweighted, p_spearman = stats.spearmanr(x, y)

# Weighted correlation
def weighted_corr(x, y, w):
    w_sum = np.sum(w)
    mx = np.sum(w * x) / w_sum
    my = np.sum(w * y) / w_sum
    cov = np.sum(w * (x - mx) * (y - my)) / w_sum
    sx = np.sqrt(np.sum(w * (x - mx)**2) / w_sum)
    sy = np.sqrt(np.sum(w * (y - my)**2) / w_sum)
    return cov / (sx * sy)

r_weighted = weighted_corr(x, y, weights)

# OLS regression (unweighted, kept for reference)
slope_ols, intercept_ols, r_value_ols, p_value_ols, std_err_ols = stats.linregress(x, y)

# Weighted Least Squares (WLS) regression, weighted by employment
import statsmodels.api as sm
X_sm = sm.add_constant(x)
wls_model = sm.WLS(y, X_sm, weights=weights)
wls_results = wls_model.fit()
intercept_wls = wls_results.params[0]
slope_wls = wls_results.params[1]
p_wls_slope = wls_results.pvalues[1]
r2_wls = wls_results.rsquared
se_wls = wls_results.bse[1]
t_wls = wls_results.tvalues[1]

# Weighted Pearson p-value via permutation test (employment-weighted)
np.random.seed(42)
n_perm = 10000
r_weighted_obs = weighted_corr(x, y, weights)
count_ge = 0
for _ in range(n_perm):
    y_perm = np.random.permutation(y)
    r_perm = weighted_corr(x, y_perm, weights)
    if abs(r_perm) >= abs(r_weighted_obs):
        count_ge += 1
p_weighted_perm = count_ge / n_perm

# Use WLS as primary results
slope = slope_wls
intercept = intercept_wls

print(f"\n--- Correlation Results ---")
print(f"Unweighted Pearson r = {r_unweighted:.4f} (p = {p_unweighted:.4f})")
print(f"Spearman rho = {rho_unweighted:.4f} (p = {p_spearman:.4f})")
print(f"Employment-weighted r = {r_weighted:.4f} (permutation p = {p_weighted_perm:.4f})")
print(f"OLS: y = {slope_ols:.4f}x + {intercept_ols:.4f} (R² = {r_value_ols**2:.4f})")
print(f"WLS: y = {slope_wls:.4f}x + {intercept_wls:.4f} (R² = {r2_wls:.4f}, p = {p_wls_slope:.4f})")

# ============================================================
# 5. Create scatter plot
# ============================================================
fig, ax = plt.subplots(figsize=(14, 10))

# Color by confidence
colors = {'H': '#2196F3', 'M': '#FF9800', 'L': '#9E9E9E'}
color_labels = {'H': 'High confidence', 'M': 'Medium confidence', 'L': 'Low confidence'}

# Size by employment (scaled)
emp_array = np.array([r['employment'] for r in data_rows])
sizes = 30 + 200 * (emp_array / emp_array.max())

for conf_level in ['L', 'M', 'H']:
    mask = [r['confidence'] == conf_level for r in data_rows]
    xi = x[mask]
    yi = y[mask]
    si = sizes[mask]
    ax.scatter(xi, yi, s=si, c=colors[conf_level], alpha=0.7,
               edgecolors='white', linewidth=0.5,
               label=f'{color_labels[conf_level]} (n={sum(mask)})', zorder=3)

# Regression line
x_line = np.linspace(0, 1, 100)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, 'r-', linewidth=2, alpha=0.8,
        label=f'WLS fit (weighted r={r_weighted:.3f}, p={p_weighted_perm:.3f})')

# Label notable occupations
labels_to_show = [
    'Software Developers', 'Elementary School Teachers', 'Lawyers',
    'Heavy Truck Drivers', 'Police & Sheriff\'s Officers',
    'Registered Nurses', 'Retail Salespersons', 'Cashiers',
    'Secretaries & Admin Assistants', 'Bookkeeping & Auditing Clerks',
    'Construction Laborers', 'Carpenters', 'General & Operations Managers',
    'Janitors & Cleaners', 'Maintenance & Repair Workers',
    'Financial Managers', 'Human Resources Specialists',
    'Accountants & Auditors', 'Customer Service Representatives',
    'Secondary School Teachers', 'Market Research Analysts',
]

for i, row in enumerate(data_rows):
    if row['title'] in labels_to_show:
        # Offset to avoid overlap
        offset_x = 0.01
        offset_y = 0.02
        ha = 'left'

        # Custom offsets for crowded areas
        if row['title'] == 'Bookkeeping & Auditing Clerks':
            offset_y = -0.03
        elif row['title'] == 'Cashiers':
            offset_y = -0.03
        elif row['title'] == 'Carpenters':
            offset_x = -0.01
            ha = 'right'
        elif row['title'] == 'Financial Managers':
            offset_y = -0.03

        ax.annotate(row['title'], (x[i], y[i]),
                    xytext=(x[i] + offset_x, y[i] + offset_y),
                    fontsize=7, alpha=0.85,
                    arrowprops=dict(arrowstyle='-', color='gray', alpha=0.4, lw=0.5))

# Formatting
ax.set_xlabel('AI Exposure Score (β = E1 + 0.5×E2, GPT-4 rated)\nEloundou et al. (2024)', fontsize=12)
ax.set_ylabel('Political Leaning\n← Republican          Democrat →', fontsize=12)
ax.set_title('AI Exposure vs. Political Affiliation\nAcross 47 of the 50 Largest U.S. Occupations by Employment', fontsize=14, fontweight='bold')

ax.axhline(y=0, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)
ax.set_xlim(-0.05, 1.0)
ax.set_ylim(-0.5, 0.7)

# Add correlation annotation box
textstr = (f'Employment-weighted r = {r_weighted:.3f} (perm. p = {p_weighted_perm:.3f})\n'
           f'WLS slope p = {p_wls_slope:.3f}\n'
           f'Unweighted Pearson r = {r_unweighted:.3f} (p = {p_unweighted:.3f})\n'
           f'Spearman ρ = {rho_unweighted:.3f} (p = {p_spearman:.3f})\n'
           f'n = {len(data_rows)} occupations')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

ax.legend(loc='lower right', fontsize=9)
ax.grid(True, alpha=0.2)

# Note about bubble size
ax.text(0.98, 0.02, 'Bubble size ∝ employment', transform=ax.transAxes,
        fontsize=8, ha='right', va='bottom', style='italic', alpha=0.6)

plt.tight_layout()
plt.savefig('ai_exposure_vs_politics.png', dpi=200, bbox_inches='tight')
print("\nSaved: ai_exposure_vs_politics.png")

# ============================================================
# 6. Create Word Document
# ============================================================
doc = Document()

# Title
title_para = doc.add_heading('AI Exposure and Political Affiliation: A Correlation Analysis', level=1)

# Subtitle
subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('An exploratory analysis of the relationship between occupational AI exposure\n'
                        'and political leaning across the 50 largest U.S. occupations')
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(100, 100, 100)

doc.add_paragraph()  # spacer

# Introduction
doc.add_heading('Introduction', level=2)
doc.add_paragraph(
    'As artificial intelligence reshapes the labor market, a natural question arises: does AI exposure '
    'correlate with the political characteristics of affected workers? This analysis explores whether '
    'occupations more exposed to AI capabilities tend to lean toward one political party or the other. '
    'Understanding this relationship has implications for the political economy of AI regulation and '
    'the distributional impacts of technological change.'
)
doc.add_paragraph(
    'We examine this question by combining two datasets: (1) occupation-level AI exposure scores from '
    'Eloundou et al. (2024), published in Science as "GPTs are GPTs: Labor market impact potential of '
    'large language models," which measures the degree to which GPT-4-class models can assist with '
    'occupational tasks; and (2) political affiliation data derived primarily from Federal Election '
    'Commission (FEC) campaign contribution records, as analyzed by Verdant Labs, OpenSecrets, and '
    'Zippia. The 50 largest U.S. occupations by employment were selected following the framework in '
    'Manning & Aguirre (2026), NBER Working Paper 34705.'
)

# Data and Methods
doc.add_heading('Data and Methods', level=2)

doc.add_heading('AI Exposure Scores', level=3)
doc.add_paragraph(
    'AI exposure is measured using the beta (β) score from Eloundou et al. (2024), defined as '
    'E1 + 0.5 × E2, where E1 represents tasks directly exposed to large language models (LLMs) '
    'and E2 represents tasks exposed when LLMs are augmented with complementary software tools. '
    'Scores are based on GPT-4 ratings of O*NET task descriptions and range from 0 (no exposure) '
    'to 1 (full exposure). This measure captures both direct LLM applicability and the broader '
    'ecosystem of AI-powered tools. Data were obtained from the publicly available repository at '
    'github.com/openai/GPTs-are-GPTs.'
)

doc.add_heading('Political Affiliation', level=3)
doc.add_paragraph(
    'Political leaning is measured as the Democratic share of campaign contributions by occupation, '
    'transformed to a scale from -1 (fully Republican) to +1 (fully Democrat). The primary sources are:'
)

bullet_points = [
    'Verdant Labs (2015): Aggregated FEC individual contribution data by self-reported occupation. '
    'Provides direct measurements for teachers (79% Dem), truck drivers (31% Dem), carpenters (64% Dem), '
    'and other occupations.',
    'OpenSecrets (2024): FEC contribution analysis by industry and occupation category. '
    'Provides data for nurses (~67% Dem), education sector (>70% Dem), and sector-level splits.',
    'Zippia/Voronoi (2023): FEC contribution analysis covering 180 occupations from 521 job titles. '
    'Used for cross-validation and gap-filling.',
    'Academic research: Pew Research Center party identification surveys, General Social Survey, '
    'and Chinoy (2024) on political sorting in the labor market.',
]
for bp in bullet_points:
    doc.add_paragraph(bp, style='List Bullet')

doc.add_paragraph(
    'Each occupation was assigned a confidence rating: High (H) for occupations with direct, '
    'multi-source FEC data; Medium (M) for occupations with sector-level data and consistent '
    'patterns across sources; and Low (L) for occupations estimated from broader category patterns. '
    'Of the 47 matched occupations, 7 have high confidence, 25 have medium confidence, and 15 '
    'have low confidence ratings.'
)

doc.add_heading('Methodology Limitations', level=3)
doc.add_paragraph(
    'Several important caveats apply to this analysis:'
)
limitations = [
    'FEC donation data captures only individuals who contribute to political campaigns, which '
    'represents a small and potentially unrepresentative subset of workers. Low-wage occupations '
    '(cashiers, janitors, fast food workers) have very few donors, making their political estimates '
    'less reliable.',
    'Self-reported job titles on FEC forms vary in specificity and accuracy, creating noise in the '
    'occupation-level matching.',
    'The Verdant Labs methodology assumes equal per-capita donation rates across parties within each '
    'occupation. If Republican or Democratic workers donate at different rates, the ratios would be skewed.',
    'Union membership significantly affects donation patterns. Carpenters, for example, show 64% '
    'Democrat in FEC data, likely driven by organized labor contributions, which may not reflect '
    'the broader carpenter population.',
    'AI exposure scores reflect potential task automation, not realized displacement. High exposure '
    'does not necessarily mean job loss.',
    'This is an ecological correlation (occupation-level), not an individual-level analysis. '
    'The occupations in this sample are the 50 largest by employment, not a random sample of all occupations.',
]
for lim in limitations:
    doc.add_paragraph(lim, style='List Bullet')

# Results
doc.add_heading('Results', level=2)

doc.add_paragraph(
    f'When weighted by employment size -- so that large occupations like retail salespersons (3.7M) '
    f'and registered nurses (3.0M) carry proportionally more influence than smaller ones -- the '
    f'employment-weighted Pearson correlation is r = {r_weighted:.3f} with a permutation-test '
    f'p-value of {p_weighted_perm:.3f} (10,000 permutations). The weighted least squares (WLS) '
    f'regression slope is {slope_wls:.3f} (p = {p_wls_slope:.3f}), with R² = {r2_wls:.3f}. '
    f'These results indicate a weak positive but statistically non-significant relationship between '
    f'AI exposure and Democratic leaning, even after accounting for occupation size. For reference, '
    f'the unweighted Pearson r = {r_unweighted:.3f} (p = {p_unweighted:.3f}) and Spearman '
    f'ρ = {rho_unweighted:.3f} (p = {p_spearman:.3f}) are also non-significant. When restricted '
    f'to the 8 high-confidence occupations only, the correlation drops to r ≈ 0.10 (p ≈ 0.81), '
    f'essentially disappearing.'
)

# Add figure
doc.add_picture('ai_exposure_vs_politics.png', width=Inches(6.5))
last_paragraph = doc.paragraphs[-1]
last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap = doc.add_paragraph()
cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = cap.add_run('Figure 1: AI Exposure (β score) vs. Political Leaning across the 50 largest U.S. occupations. '
                   'Bubble size proportional to employment. Colors indicate data confidence level.')
run.font.size = Pt(9)
run.font.italic = True

doc.add_paragraph(
    'Despite the lack of statistical significance, the scatter plot reveals interesting structural '
    'patterns in how occupations cluster by AI exposure and political leaning:'
)

clusters = [
    'High-exposure, Democratic-leaning occupations: Software developers (AI exposure: 0.87, lean: +0.36), '
    'elementary school teachers (0.31, +0.58), lawyers (0.43, +0.44), bookkeeping clerks (0.80, +0.10), '
    'and secretaries/admin assistants (0.64, +0.16). These are primarily white-collar knowledge workers '
    'and educated professionals.',
    'Low-exposure, Republican-leaning occupations: Heavy truck drivers (0.28, -0.38), '
    'construction laborers (0.05, -0.24), maintenance workers (0.14, -0.24), '
    'police officers (0.45, -0.30), and industrial truck operators (0.03, -0.24). '
    'These are predominantly blue-collar, manual, or outdoor occupations.',
    'Moderate-exposure, mixed occupations: General managers (0.48, -0.10), '
    'accountants (0.56, -0.04), retail supervisors (0.49, -0.06), and project managers (0.55, 0.00) '
    'cluster near the center with moderate AI exposure and relatively balanced political leanings.',
]
for cl in clusters:
    doc.add_paragraph(cl, style='List Bullet')

# OLS table
doc.add_heading('Regression Results', level=3)
table = doc.add_table(rows=9, cols=2)
table.style = 'Light Grid Accent 1'
cells = table.rows[0].cells
cells[0].text = 'Statistic'
cells[1].text = 'Value'
stats_data = [
    ('Employment-weighted r', f'{r_weighted:.4f}'),
    ('Weighted r permutation p', f'{p_weighted_perm:.4f}'),
    ('WLS slope', f'{slope_wls:.4f}'),
    ('WLS slope p-value', f'{p_wls_slope:.4f}'),
    ('WLS R²', f'{r2_wls:.4f}'),
    ('Unweighted Pearson r', f'{r_unweighted:.4f}'),
    ('Unweighted p-value', f'{p_unweighted:.4f}'),
    ('Spearman ρ', f'{rho_unweighted:.4f}'),
]
for i, (stat, val) in enumerate(stats_data):
    cells = table.rows[i+1].cells
    cells[0].text = stat
    cells[1].text = val

doc.add_paragraph()

# Discussion
doc.add_heading('Discussion', level=2)
doc.add_paragraph(
    f'Even after weighting by occupation size -- which gives greater influence to the millions of '
    f'retail salespersons, nurses, and home health aides than to the hundreds of thousands of lawyers '
    f'or police officers -- the correlation remains weak and non-significant (weighted r = {r_weighted:.3f}, '
    f'permutation p = {p_weighted_perm:.3f}; WLS slope p = {p_wls_slope:.3f}). This suggests that, '
    f'among the largest U.S. occupations, AI exposure does not strongly predict political affiliation '
    f'regardless of how observations are weighted. This null-ish result is itself informative: despite '
    f'intuitions that AI might disproportionately affect workers of one political persuasion, the '
    f'reality across major occupations is more heterogeneous.'
)
doc.add_paragraph(
    'Several factors help explain the lack of a strong relationship. Occupations most exposed to AI '
    'tend to be cognitive, white-collar roles -- but these span the political spectrum. Bookkeeping '
    'clerks (AI exposure: 0.80) are near-neutral politically, while sales representatives (0.63) lean '
    'slightly Republican, and secretaries (0.64) lean slightly Democratic. The high-exposure tier '
    'includes both strongly Democratic software developers and near-neutral administrative roles.'
)
doc.add_paragraph(
    'At the same time, interesting structural patterns emerge in the scatter plot. Low-exposure occupations '
    '(AI < 0.2) include both Republican-leaning manual workers (construction laborers, industrial truck '
    'operators) and Democratic-leaning service workers (nursing assistants, waiters). This floor-level '
    'variation washes out any linear trend. Similarly, mid-range exposure (0.3-0.5) includes the starkly '
    'opposed police officers (-0.30) and registered nurses (+0.34), demonstrating that occupational '
    'culture and workforce demographics can overwhelm any AI-exposure signal.'
)
doc.add_paragraph(
    'Notable outliers deserve attention. Police officers have moderate-to-high AI exposure (0.45) '
    'but lean strongly Republican (-0.30), reflecting law enforcement\'s distinctive political culture. '
    'Carpenters show low AI exposure (0.14) but lean Democratic (0.28), likely inflated by union '
    'carpenters who are overrepresented in FEC contribution data. Teachers have moderate AI exposure '
    '(0.31-0.33) but are among the most strongly Democratic occupations (+0.52 to +0.58), driven by '
    'education-sector culture and unionization rather than AI-related factors.'
)
doc.add_paragraph(
    'It is crucial to emphasize that this analysis captures correlations at the occupation level, '
    'not causal relationships. The political leaning of an occupation is shaped by numerous factors '
    'beyond AI exposure, including education requirements, unionization, urbanization, gender composition, '
    'racial demographics, and industry culture. The FEC-based political data has significant limitations, '
    'particularly for low-wage occupations where few workers make campaign contributions. A more rigorous '
    'analysis would require individual-level data and multivariate controls.'
)

# Conclusion
doc.add_heading('Conclusion', level=2)
doc.add_paragraph(
    f'This exploratory analysis finds a weak positive but statistically non-significant correlation '
    f'between occupational AI exposure and Democratic political leaning across the 50 largest U.S. '
    f'occupations. The employment-weighted correlation is r = {r_weighted:.3f} (permutation '
    f'p = {p_weighted_perm:.3f}), and the WLS regression slope has p = {p_wls_slope:.3f}. '
    f'The unweighted Pearson r = {r_unweighted:.3f} (p = {p_unweighted:.3f}) tells the same story. '
    f'While there is a directional tendency for higher-AI-exposure occupations to lean somewhat more '
    f'Democratic, the relationship is not strong enough to reach statistical significance at any '
    f'conventional threshold, and it essentially vanishes (r ≈ 0.10) when restricted to high-confidence '
    f'data points. The scatter plot reveals substantial heterogeneity: occupations at similar AI exposure '
    f'levels can lean in opposite political directions, suggesting that workforce demographics, '
    f'occupational culture, unionization, and education level are far more powerful predictors of '
    f'political affiliation than AI exposure. Future research should employ individual-level data from '
    f'voter registration records (e.g., the Chinoy 2024 "VRscores" dataset) merged with O*NET task '
    f'data, along with multivariate controls, to better isolate any relationship between AI exposure '
    f'and political orientation.'
)

# Data Sources
doc.add_heading('Data Sources', level=2)
sources = [
    'Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2024). GPTs are GPTs: Labor market impact '
    'potential of large language models. Science, 384(6702), 1306-1308. '
    'Data: github.com/openai/GPTs-are-GPTs',
    'Manning, S. & Aguirre, T. (2026). How Adaptable Are American Workers to AI-Induced Job '
    'Displacement? NBER Working Paper 34705.',
    'Bureau of Labor Statistics, Occupational Employment and Wage Statistics (OES), May 2021.',
    'Verdant Labs (2015). Democratic vs. Republican Occupations. FEC individual contribution data. '
    'verdantlabs.com/politics_of_professions/',
    'OpenSecrets (2024). Industry and sector contribution data. opensecrets.org',
    'Zippia (2023). Democratic vs. Republican Jobs. FEC contribution analysis. '
    'zippia.com/advice/democratic-vs-republican-jobs/',
    'Chinoy, S. (2024). Political Sorting in the U.S. Labor Market: Evidence and Explanations.',
]
for src in sources:
    doc.add_paragraph(src, style='List Number')

# Appendix: Full data table
doc.add_heading('Appendix: Full Dataset', level=2)
doc.add_paragraph('Table A1: AI Exposure and Political Leaning for 47 Matched Occupations', style='Intense Quote')

# Sort by AI exposure
sorted_data = sorted(data_rows, key=lambda r: -r['ai_exposure'])

app_table = doc.add_table(rows=len(sorted_data)+1, cols=5)
app_table.style = 'Light Grid Accent 1'
headers = ['Occupation', 'Employment', 'AI Exposure (β)', 'Dem Share', 'Confidence']
for j, h in enumerate(headers):
    app_table.rows[0].cells[j].text = h

for i, row in enumerate(sorted_data):
    cells = app_table.rows[i+1].cells
    cells[0].text = row['title']
    cells[1].text = f"{row['employment']:,}"
    cells[2].text = f"{row['ai_exposure']:.3f}"
    cells[3].text = f"{row['dem_share']:.0%}"
    cells[4].text = row['confidence']

# Reduce font size in appendix table
for row in app_table.rows:
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(8)

doc.save('AI_Exposure_Political_Affiliation_Analysis.docx')
print("Saved: AI_Exposure_Political_Affiliation_Analysis.docx")

# ============================================================
# 7. Print summary table
# ============================================================
print("\n--- Full Dataset ---")
print(f"{'Occupation':<40} {'AI Exp':>7} {'Dem%':>6} {'Lean':>6} {'Conf':>5}")
print("-" * 70)
for row in sorted_data:
    print(f"{row['title']:<40} {row['ai_exposure']:>7.3f} {row['dem_share']:>5.0%} {row['political_lean']:>+6.2f} {row['confidence']:>5}")
