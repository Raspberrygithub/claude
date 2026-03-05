from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.space_before = Pt(0)

def add_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_bold_para(label, value):
    p = doc.add_paragraph()
    run = p.add_run(label)
    run.bold = True
    p.add_run(value)
    return p

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.bold = True
        p.add_run(text)
    else:
        p.add_run(text)
    return p

# ---- TITLE ----
title = doc.add_heading('MEMORANDUM', level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
for run in title.runs:
    run.font.color.rgb = RGBColor(0, 0, 0)

doc.add_paragraph()
add_bold_para('RE: ', 'Research Security Risks Posed by Foreign Nationals from Countries of Risk at DOE National Laboratories')
add_bold_para('Hearing: ', 'U.S. Senate Committee on Energy and Natural Resources')
add_bold_para('Date: ', 'February 20, 2025')
add_bold_para('Location: ', 'Room 366, Dirksen Senate Office Building, Washington, D.C.')
add_bold_para('Chairman: ', 'Senator Mike Lee (R-UT)')

# Horizontal line
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(12)
pPr = p._p.get_or_add_pPr()
pBdr = pPr.makeelement(qn('w:pBdr'), {})
bottom = pBdr.makeelement(qn('w:bottom'), {
    qn('w:val'): 'single',
    qn('w:sz'): '6',
    qn('w:space'): '1',
    qn('w:color'): '000000'
})
pBdr.append(bottom)
pPr.append(pBdr)

# ---- EXECUTIVE SUMMARY ----
add_heading('Executive Summary', level=1)
doc.add_paragraph(
    'On February 20, 2025, the Senate Committee on Energy and Natural Resources convened a hearing '
    'examining espionage and research security vulnerabilities at the Department of Energy\u2019s 17 national '
    'laboratories. Three former senior DOE officials\u2014Dr. Geraldine Richmond, Anna B. Puglisi, and Paul M. '
    'Dabbar\u2014testified on the scope of the threat, existing mitigation frameworks, and the need for expanded '
    'legislative action. The hearing revealed that in FY2023 alone, approximately 40,000 foreign scientists '
    'accessed DOE laboratories, with nearly 8,000 from China and Russia\u2014meaning one in every five foreign '
    'scientists entering America\u2019s top labs came from adversarial nations. All three witnesses and the Committee '
    'agreed that current protections are insufficient, though they differed on the appropriate balance between '
    'security restrictions and the scientific openness that underpins American technological leadership.'
)

# ---- I. TESTIMONY SUMMARIES (CUT IN HALF) ----
add_heading('I. Witness Testimony Summaries', level=1)

# Richmond
add_heading('A. Dr. Geraldine L. Richmond', level=2)
p = doc.add_paragraph()
r = p.add_run('Former Under Secretary for Science and Innovation, DOE (2021\u20132025); Presidential Chair in Science, University of Oregon')
r.italic = True

doc.add_paragraph(
    'Richmond, who oversaw 13 DOE national laboratories, focused on the risk management architecture she helped build. '
    'She detailed DOE\u2019s S&T Risk Matrix\u2014authorized under the CHIPS and Science Act\u2014which uses a Red/Yellow/Green '
    'framework to categorize emerging research topics by sensitivity. "Red" topics require enhanced vetting and '
    'Secretarial approval for any engagement with countries of concern (China, Russia, Iran, North Korea).'
)
doc.add_paragraph(
    'Richmond described the 2019 ban on DOE personnel participating in foreign Talent Recruitment Programs, expanded '
    'in 2020 to cover all foreign government-sponsored activities\u2014requiring direct Secretary of Energy approval. She '
    'warned that mass layoffs and budget cuts could make displaced personnel with classified knowledge more vulnerable '
    'to foreign recruitment, disclosing that she herself had been recruited by China.'
)

# Puglisi
add_heading('B. Anna B. Puglisi', level=2)
p = doc.add_paragraph()
r = p.add_run('Visiting Fellow, Hoover Institution, Stanford University; Former National Counterintelligence Officer for East Asia')
r.italic = True

doc.add_paragraph(
    'Puglisi, a career intelligence professional who helped draft the U.S. National Counterintelligence Strategy, '
    'proposed three systemic reforms: (1) a national "pre-check" system\u2014modeled on TSA PreCheck\u2014to streamline '
    'vetting for trusted researchers while concentrating resources on higher-risk engagements; (2) a national '
    'open-source information center to give universities and labs actionable threat intelligence without requiring '
    'classified access; and (3) an international framework of research security standards for visiting scientists. '
    'She emphasized that China\u2019s technology acquisition strategy is systematic and state-directed, not opportunistic.'
)

# Dabbar
add_heading('C. Paul M. Dabbar', level=2)
p = doc.add_paragraph()
r = p.add_run('Former Under Secretary for Science, DOE (2017\u20132021); CEO, Bohr Quantum Technology; Subsequently Nominated as Deputy Secretary of Commerce')
r.italic = True

doc.add_paragraph(
    'Dabbar delivered the most forceful testimony, recommending a default ban on Chinese nationals at all 17 DOE '
    'national laboratories\u2014not just the three NNSA labs covered by the FY2025 NDAA\u2014with waivers granted only on a '
    'case-by-case basis. He noted that under China\u2019s National Security Law, "all PRC citizens are required \u2026 to hand '
    'over all information when directed by the Chinese state." He criticized existing DOE orders as providing "too '
    'much flexibility and discretion" and called for all access decisions to be authorized solely by lab under '
    'secretaries without delegation, with a defined waiver list subject to Congressional oversight. He characterized '
    'the threat bluntly: "There\u2019s been literally a whole generation of successful efforts by Communist China on '
    'stealing stuff."'
)

# ---- II. THREAT LANDSCAPE ----
add_heading('II. The Threat Landscape: Key Statistics and Evidence', level=1)

add_heading('Scale of Foreign Access to DOE Laboratories', level=2)

table = doc.add_table(rows=5, cols=3)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ['Metric', 'Figure', 'Source']
for i, h in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = h
    for p in cell.paragraphs:
        for r in p.runs:
            r.bold = True

data = [
    ('Foreign scientists visiting DOE labs annually', '~40,000', "Sen. Cotton's office / GATE Act"),
    ('PRC nationals visiting 16 national labs (FY2023)', '>7,000', 'Intelligence Auth. Act FY2024'),
    ('Chinese & Russian nationals visiting labs (FY2023)', '~8,000', "Sen. Cotton's office"),
    ('Share from adversarial nations', '~1 in 5 (20%)', "Sen. Cotton's office"),
]
for row_idx, (m, f, s) in enumerate(data, start=1):
    table.rows[row_idx].cells[0].text = m
    table.rows[row_idx].cells[1].text = f
    table.rows[row_idx].cells[2].text = s

doc.add_paragraph()

add_heading('Documented Espionage and Recruitment Cases', level=2)

add_bullet('At least 162 former Los Alamos scientists were recruited by Beijing to work on Chinese military programs over three decades.', 'Strider Technologies Report (2021): ')
add_bullet('Scientist Zhao Yusheng received nearly $20 million in U.S. taxpayer grants during 18 years at Los Alamos, held a top-secret Q clearance, led a deep-penetration bomb project, then joined a Chinese talent program in 2016 and left the U.S.', 'Zhao Yusheng Case: ')
add_bullet('DOE has documented individuals offered hundreds of thousands or millions of dollars to conduct research for foreign talent programs while receiving U.S. agency support. Lab personnel recruited by talent programs have subsequently affiliated with foreign military R&D.', 'DOE Internal Knowledge: ')
add_bullet('Harvard professor convicted (Dec. 2021) of lying about Thousand Talents Program participation and unreported Chinese income.', 'Charles Lieber: ')
add_bullet('Stole $1 billion in proprietary battery technology formulas for China\u2019s Thousand Talents Program. Sentenced to 24 months.', 'Hongjin Tan: ')
add_bullet('54 scientists have lost jobs for undisclosed Chinese funding; 20+ charged with espionage or fraud (as of 2025).', 'Aggregate Enforcement: ')

add_heading("China's Talent Recruitment Programs", level=2)
add_bullet('China\u2019s talent recruitment programs drew nearly 60,000 overseas professionals between 2008 and 2016 (official Chinese statistics).')
add_bullet('The Thousand Talents Plan attracted more than 7,000 participants within its first decade (launched 2008).')
add_bullet('DOE\u2019s 2019 prohibition on talent program participation appears to have reduced the brain drain, but enforcement challenges persist.')

add_heading('Intelligence Community Assessments', level=2)
add_bullet('The Senate Intelligence Committee found DOE-IN does not require comprehensive screening of foreign visitors from PRC, Russia, Iran, North Korea, and Cuba at National Laboratories.')
add_bullet('The Intelligence Committees directed DOE-IN to implement robust screening and vetting with appropriate counterintelligence oversight.')
add_bullet('A 2025 NCSC report confirmed Chinese intelligence services continue recruiting students and stealing research at U.S. universities.')

add_heading('Lack of Reciprocity', level=2)
doc.add_paragraph(
    'Senator Tom Cotton posed a pointed question: "Do you think one out of every five foreign scientists in a '
    'Chinese or Russian equivalent site is American?" He answered: "There is zero reciprocity on this issue." '
    'China\u2019s national laboratories and defense research institutions are closed systems with no comparable '
    'foreign access.'
)

# ---- III. LEGAL FRAMEWORK ----
add_heading('III. Current Legal and Policy Framework', level=1)

add_heading('FY2025 National Defense Authorization Act (Section 3112)', level=2)
doc.add_paragraph('Signed into law by President Biden in December 2024:')
add_bullet('Prohibits citizens or agents of China, Russia, Iran, and North Korea from accessing non-public areas of DOE\u2019s national security labs and nuclear weapons production facilities')
add_bullet('Effective April 15, 2025')
add_bullet('Scope limited to three NNSA labs: Los Alamos, Lawrence Livermore, Sandia')
add_bullet('Waivers permitted with Secretarial authorization; quarterly reporting to Congress')
add_bullet('Pared-down version of broader Senate Intelligence Committee proposal that would have covered all 17 DOE labs')

add_heading('DOE S&T Risk Matrix', level=2)
add_bullet('Authorized under the CHIPS and Science Act; uses Red/Yellow/Green categorization')
add_bullet('Red topics: restricted emerging technologies requiring enhanced vetting and Secretarial approval')
add_bullet('Applies to all national laboratory international transactions')
add_bullet('Countries of concern: China, Russia, Iran, North Korea')

add_heading('Talent Recruitment Program Restrictions', level=2)
add_bullet('2019: DOE prohibited participation in Talent Recruitment Programs from countries of concern')
add_bullet('2020: Expanded to all foreign government-sponsored activities; requires Secretary of Energy approval')

add_heading('NSPM-33', level=2)
doc.add_paragraph(
    'Presidential directive requiring enhanced disclosure of foreign funding and affiliations by researchers '
    'receiving federal grants, with standardized requirements across agencies.'
)

# ---- IV. GATE ACT ----
add_heading('IV. Proposed Legislation: The GATE Act', level=1)

doc.add_paragraph(
    'Following the hearing, Senator Tom Cotton introduced the Guarding American Technology from Exploitation '
    '(GATE) Act, cosponsored by Senators Lee (R-UT), Barrasso (R-WY), Collins (R-ME), and Lankford (R-OK).'
)

p = doc.add_paragraph()
r = p.add_run('Key provisions:')
r.bold = True
add_bullet('Prohibits non-citizen researchers from China, Russia, Iran, North Korea, and Cuba from visiting or working at all 17 DOE national laboratories')
add_bullet('Secretary of Energy may grant waivers if benefits "outweigh the national security and economic risks"')
add_bullet('Waivers require intelligence community coordination')
add_bullet('U.S. citizens and permanent residents unaffected')
add_bullet('A similar version passed the Senate Intelligence Committee 17-0 last Congress but was not included in the final NDAA')

p = doc.add_paragraph()
r = p.add_run('Opposition:')
r.bold = True
add_bullet('DOE: the proposal "would have a significant impact on our national laboratories"')
add_bullet('Critics warn it "would severely limit our ability to engage with Chinese and Russian experts on nonproliferation"')
add_bullet('Some scientists argue restrictions could drive talent to competitor nations')

# ---- V. POST-HEARING ----
add_heading('V. Post-Hearing Developments', level=1)
doc.add_paragraph(
    'Chairman Lee sent letters to the Directors of Oak Ridge, Los Alamos, and Argonne National Laboratories '
    'regarding reports that researchers at all three labs engaged in research collaborations leveraging PRC-based '
    'supercomputers\u2014including those linked to the PRC\u2019s military\u2014for federally funded research in sensitive '
    'fields. This underscored that security risks extend beyond physical presence to digital and computational '
    'collaborations that may circumvent existing access controls.'
)

# ---- VI. ANALYSIS ----
add_heading('VI. Analysis: Core Tensions', level=1)

add_heading('Security vs. Scientific Openness', level=2)
doc.add_paragraph(
    'The fundamental tension is between protecting sensitive research from adversarial exploitation and maintaining '
    'the scientific openness that has been the foundation of American technological leadership. Restricting access '
    'risks degrading precisely the qualities that make these institutions valuable.'
)

add_heading('Targeted vs. Blanket Restrictions', level=2)
add_bullet('Dabbar favored broad default bans with narrow waivers', 'Dabbar: ')
add_bullet('emphasized the S&T Risk Matrix for nuanced, topic-by-topic risk assessment rather than nationality-based restrictions', 'Richmond: ')
add_bullet('proposed systemic solutions (pre-check, open-source intelligence, international frameworks) to improve decision quality', 'Puglisi: ')

add_heading('Workforce Vulnerability', level=2)
doc.add_paragraph(
    'Displaced scientists with classified knowledge are high-value recruitment targets. Budget cuts intended to '
    'reduce spending may paradoxically increase the vulnerability of sensitive knowledge to adversarial acquisition.'
)

add_heading('The Reciprocity Gap', level=2)
doc.add_paragraph(
    'The U.S. opens its premier research institutions to foreign nationals at a scale with no parallel in Chinese, '
    'Russian, or Iranian practice. Whether this openness is a strategic vulnerability or competitive advantage is '
    'the central policy question.'
)

# ---- VII. KEY TAKEAWAYS ----
add_heading('VII. Key Takeaways', level=1)

for i, text in enumerate([
    'The threat is documented, quantified, and ongoing. With 162 recruited scientists from a single lab, '
    '$20M in taxpayer funds to a scientist who defected, and 8,000 adversarial-nation nationals accessing labs '
    'annually, the security challenge is substantial.',
    'Existing protections cover only a fraction of the risk. The FY2025 NDAA applies to 3 of 17 DOE labs. '
    'The remaining 14\u2014conducting research in AI, quantum, energy storage, and advanced materials\u2014have no '
    'comparable statutory protections.',
    'Bipartisan momentum exists for expanded restrictions. The GATE Act\u2019s predecessor passed the Senate '
    'Intelligence Committee 17-0.',
    'Implementation challenges are significant. DOE warns broad bans would significantly impact operations. '
    'The tension between security and scientific productivity requires ongoing Congressional oversight.',
    'New vulnerabilities are emerging. The use of PRC-linked supercomputers by U.S. lab researchers shows '
    'risks extend beyond physical access to digital collaboration channels.',
], start=1):
    p = doc.add_paragraph()
    r = p.add_run(f'{i}. ')
    r.bold = True
    p.add_run(text)

# ---- SOURCES ----
add_heading('Sources', level=1)

sources = [
    ('Senate Committee on Energy and Natural Resources \u2014 Hearing Page',
     'https://www.energy.senate.gov/hearings/2025/2/hearing-to-to-examine-research-security-risks-posed-by-foreign-nationals-from-countries-of-risk-working-at-the-department-of-energy-s-national-laboratories-and-necessary-mitigation-steps'),
    ('Written Testimony of Dr. Geraldine Richmond (PDF)',
     'https://www.energy.senate.gov/services/files/B1C92139-655C-4D9E-B52B-CACABF133A8B'),
    ('Written Testimony of Paul M. Dabbar (PDF)',
     'https://www.energy.senate.gov/services/files/EC4F7084-85AF-432C-B731-B9310EEF03A9'),
    ('Anna B. Puglisi Testimony \u2014 Hoover Institution',
     'https://www.hoover.org/research/hearing-examine-research-security-risks-posed-foreign-nationals-countries-risk-working'),
    ('C-SPAN: Hearing on Potential Espionage at National Labs (Video)',
     'https://www.c-span.org/program/senate-committee/hearing-on-potential-espionage-at-national-labs/656009'),
    ('Intelligence Authorization Act for FY2024, Joint Explanatory Statement',
     'https://www.intelligence.senate.gov/2023/12/14/publications-joint-explanatory-statement-accompany-intelligence-authorization-act-fiscal-year-2024/'),
    ('Sen. Cotton Press Release: GATE Act Introduction',
     'https://www.cotton.senate.gov/news/press-releases/cotton-colleagues-get-spies-out-of-our-national-labs'),
    ('MeriTalk: Hill Weighs Expanding Ban on Foreign Nationals at DOE Labs',
     'https://www.meritalk.com/articles/hill-weighs-expanding-ban-on-foreign-nationals-at-doe-labs/'),
    ('DOE: Introduction to the S&T Risk Matrix',
     'https://www.energy.gov/science/articles/science-technology-risk-matrix'),
    ('AIP FYI: Congress Poised to Restrict NNSA Labs',
     'https://www.aip.org/fyi/congress-poised-to-restrict-nnsa-labs-from-admitting-citizens-of-four-countries'),
    ('NBC News / Strider Technologies: Scientists Recruited by China',
     'https://www.nbcnews.com/news/world/scientists-americas-top-nuclear-lab-recruited-china-design-missiles-dr-rcna48834'),
    ('GovInfo: Securing the U.S. Research Enterprise from China\u2019s Talent Recruitment Plans',
     'https://www.govinfo.gov/content/pkg/CHRG-116shrg41995/html/CHRG-116shrg41995.htm'),
]

for title, url in sources:
    p = doc.add_paragraph(style='List Bullet')
    from docx.oxml import OxmlElement
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('w:history'), '1')
    r_elem = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rStyle = OxmlElement('w:rStyle')
    rStyle.set(qn('w:val'), 'Hyperlink')
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0563C1')
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(rStyle)
    rPr.append(color)
    rPr.append(u)
    r_elem.append(rPr)
    t = OxmlElement('w:t')
    t.text = title
    r_elem.append(t)
    hyperlink.append(r_elem)
    # Just add as text since proper hyperlinks need relationships
    p.text = f'{title}: {url}'

output_path = '/home/user/claude/Research_Security_DOE_National_Labs_Memo.docx'
doc.save(output_path)
print(f'Saved to {output_path}')
