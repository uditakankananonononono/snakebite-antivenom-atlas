#!/usr/bin/env python3
"""Region mapping + coverage gap table.
Regions = the four WHO appendix sections. ISO3->region validated against the WHO
PDF: each country's name must appear inside its assigned section's line range;
mismatches dumped to results/negatives/region_validation.txt."""
import csv, re, collections
lines = open("data/who/who_trs1004_annex5.txt", encoding="utf-8").read().splitlines()
SECT = [(7595,8166,"Africa and the Middle East"),(8166,8461,"Asia and Australasia"),
        (8461,8600,"Europe"),(8600,len(lines),"The Americas")]
sectext = {name:" ".join(lines[a-1:b-1]).lower() for a,b,name in SECT}
ISO = {  # iso3: (country-name-fragment, WHO section)
"ABW":("aruba","The Americas"),"AFG":("afghanistan","Asia and Australasia"),"AGO":("angola","Africa and the Middle East"),
"ALB":("albania","Europe"),"AND":("andorra","Europe"),"ARE":("united arab emirates","Africa and the Middle East"),
"ARG":("argentina","The Americas"),"ARM":("armenia","Asia and Australasia"),"AUS":("australia","Asia and Australasia"),
"AUT":("austria","Europe"),"BDI":("burundi","Africa and the Middle East"),"BEL":("belgium","Europe"),
"BEN":("benin","Africa and the Middle East"),"BFA":("burkina faso","Africa and the Middle East"),
"BGD":("bangladesh","Asia and Australasia"),"BGR":("bulgaria","Europe"),"BHR":("bahrain","Africa and the Middle East"),
"BIH":("bosnia","Europe"),"BLZ":("belize","The Americas"),"BOL":("bolivia","The Americas"),
"BRA":("brazil","The Americas"),"BRN":("brunei","Asia and Australasia"),"BWA":("botswana","Africa and the Middle East"),
"CAF":("central african","Africa and the Middle East"),"CAN":("canada","The Americas"),"CHE":("switzerland","Europe"),
"CHN":("china","Asia and Australasia"),"CIV":("cote d'ivoire","Africa and the Middle East"),
"CMR":("cameroon","Africa and the Middle East"),"COD":("congo","Africa and the Middle East"),
"COG":("congo","Africa and the Middle East"),"COL":("colombia","The Americas"),"CRI":("costa rica","The Americas"),
"CUB":("cuba","The Americas"),"CYP":("cyprus","Africa and the Middle East"),"DEU":("germany","Europe"),
"DZA":("algeria","Africa and the Middle East"),"ECU":("ecuador","The Americas"),"EGY":("egypt","Africa and the Middle East"),
"ERI":("eritrea","Africa and the Middle East"),"ESH":("western sahara","Africa and the Middle East"),
"ESP":("spain","Europe"),"ETH":("ethiopia","Africa and the Middle East"),"FRA":("france","Europe"),
"GAB":("gabon","Africa and the Middle East"),"GBR":("united kingdom","Europe"),"GEO":("georgia","Asia and Australasia"),
"GHA":("ghana","Africa and the Middle East"),"GIN":("guinea","Africa and the Middle East"),
"GMB":("gambia","Africa and the Middle East"),"GNB":("guinea-bissau","Africa and the Middle East"),
"GNQ":("equatorial guinea","Africa and the Middle East"),"GRC":("greece","Europe"),"GTM":("guatemala","The Americas"),
"GUF":("french guiana","The Americas"),"GUY":("guyana","The Americas"),"HKG":("hong kong","Asia and Australasia"),
"HND":("honduras","The Americas"),"HRV":("croatia","Europe"),"HUN":("hungary","Europe"),
"IDN":("indonesia","Asia and Australasia"),"IND":("india","Asia and Australasia"),"IRN":("iran","Africa and the Middle East"),
"IRQ":("iraq","Africa and the Middle East"),"ISR":("israel","Africa and the Middle East"),"ITA":("italy","Europe"),
"JOR":("jordan","Africa and the Middle East"),"JPN":("japan","Asia and Australasia"),
"KAZ":("kazakhstan","Asia and Australasia"),"KEN":("kenya","Africa and the Middle East"),
"KHM":("cambodia","Asia and Australasia"),"KOR":("korea","Asia and Australasia"),"LAO":("lao","Asia and Australasia"),
"LBR":("liberia","Africa and the Middle East"),"LBY":("libya","Africa and the Middle East"),
"LKA":("sri lanka","Asia and Australasia"),"LSO":("lesotho","Africa and the Middle East"),
"MAR":("morocco","Africa and the Middle East"),"MEX":("mexico","The Americas"),"MLI":("mali","Africa and the Middle East"),
"MMR":("myanmar","Asia and Australasia"),"MNG":("mongolia","Asia and Australasia"),
"MOZ":("mozambique","Africa and the Middle East"),"MRT":("mauritania","Africa and the Middle East"),
"MWI":("malawi","Africa and the Middle East"),"MYS":("malaysia","Asia and Australasia"),
"NAM":("namibia","Africa and the Middle East"),"NER":("niger","Africa and the Middle East"),
"NGA":("nigeria","Africa and the Middle East"),"NIC":("nicaragua","The Americas"),"NOR":("norway","Europe"),
"NPL":("nepal","Asia and Australasia"),"OMN":("oman","Africa and the Middle East"),"PAK":("pakistan","Asia and Australasia"),
"PAN":("panama","The Americas"),"PER":("peru","The Americas"),"PHL":("philippines","Asia and Australasia"),
"PNG":("papua new guinea","Asia and Australasia"),"POL":("poland","Europe"),"PRK":("korea","Asia and Australasia"),
"PRT":("portugal","Europe"),"PRY":("paraguay","The Americas"),"ROU":("romania","Europe"),
"RUS":("russia","Asia and Australasia"),"RWA":("rwanda","Africa and the Middle East"),
"SAU":("saudi arabia","Africa and the Middle East"),"SDN":("sudan","Africa and the Middle East"),
"SEN":("senegal","Africa and the Middle East"),"SGP":("singapore","Asia and Australasia"),
"SLE":("sierra leone","Africa and the Middle East"),"SLV":("el salvador","The Americas"),
"SOM":("somalia","Africa and the Middle East"),"SSD":("south sudan","Africa and the Middle East"),
"STP":("sao tome","Africa and the Middle East"),"SUR":("suriname","The Americas"),"SVN":("slovenia","Europe"),
"SWE":("sweden","Europe"),"SWZ":("eswatini","Africa and the Middle East"),"SYR":("syrian","Africa and the Middle East"),
"TGO":("togo","Africa and the Middle East"),"THA":("thailand","Asia and Australasia"),
"TKM":("turkmenistan","Asia and Australasia"),"TTO":("trinidad","The Americas"),"TUN":("tunisia","Africa and the Middle East"),
"TUR":("turkey","Africa and the Middle East"),"TZA":("tanzania","Africa and the Middle East"),
"UGA":("uganda","Africa and the Middle East"),"UKR":("ukraine","Europe"),"URY":("uruguay","The Americas"),
"USA":("united states","The Americas"),"UZB":("uzbekistan","Asia and Australasia"),"VEN":("venezuela","The Americas"),
"VNM":("viet nam","Asia and Australasia"),"YEM":("yemen","Africa and the Middle East"),
"ZAF":("south africa","Africa and the Middle East"),"ZMB":("zambia","Africa and the Middle East"),
"ZWE":("zimbabwe","Africa and the Middle East")}
rows, validation = [], []
for r in csv.DictReader(open("results/species_summary.csv")):
    codes = [c.strip() for c in r["countries"].replace('"','').split(",") if c.strip()]
    regions = set()
    for c in codes:
        if c not in ISO: validation.append(f"UNMAPPED|{c}|{r['species']}"); continue
        frag, reg = ISO[c]; regions.add(reg)
        if frag not in sectext[reg]: validation.append(f"CHECK|{c}|{frag}|{reg}|{r['species']}")
    cat = r["category"]; av = int(r["n_antivenom_products"]); nt = int(r["n_toxins"])
    if av == 0 and cat == "1": gap = "CRITICAL (Cat1, no antivenom listed)"
    elif av == 0: gap = "HIGH (no antivenom listed)"
    elif nt == 0: gap = "DATA GAP (covered, but no toxin records)"
    else: gap = "covered"
    rows.append({**r, "regions": "|".join(sorted(regions)), "n_countries": len(codes), "gap_class": gap})
with open("results/gap_table.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
open("results/negatives/region_validation.txt","w").write("\n".join(validation)+"\n")
c = collections.Counter(r["gap_class"] for r in rows)
print(dict(c)); print("validation flags:", len(validation))
reg = collections.Counter()
for r in rows:
    for x in r["regions"].split("|"):
        if x: reg[(x, r["gap_class"])] += 1
for k in sorted(reg): print(k, reg[k])
