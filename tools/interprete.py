#!/usr/bin/env python

import sys

input1 = sys.argv[1] # reported
input2 = sys.argv[2] # summary 
input3 = sys.argv[3] # SVs
input4 = sys.argv[4] # DR_loci_annotation
input5 = sys.argv[5] # target region coverage
input6 = sys.argv[6] # samplename

variants = []
interpretation = []
mutations = []
position = []
diclofs = {"frameshift_variant": "R", "frameshift_variant&stop_gained": "R", "frameshift_variant&stop_lost&splice_region_variant": "R", "stop_gained": "R", "start_lost": "R", "synonymous_variant": "S", "missense_variant": "U", "upstream_gene_variant": "U", "downstream_gene_variant": "U", "disruptive_inframe_insertion": "R", "disruptive_inframe_deletion": "R", "conservative_inframe_insertion": "R", "conservative_inframe_deletion": "R", "stop_lost&splice_region_variant": "R", "start_lost&conservative_inframe_deletion": "R"}
diclofs2 = {"frameshift_variant": "R", "frameshift_variant&stop_gained": "R", "frameshift_variant&stop_lost&splice_region_variant": "R", "stop_gained": "R", "start_lost": "R", "synonymous_variant": "S", "missense_variant": "U", "upstream_gene_variant": "U", "downstream_gene_variant": "U", "disruptive_inframe_insertion": "U", "disruptive_inframe_deletion": "U", "conservative_inframe_insertion": "U", "conservative_inframe_deletion": "U", "stop_lost&splice_region_variant": "R", "start_lost&conservative_inframe_deletion": "R"}
diclofs3 = {"frameshift_variant": "U", "frameshift_variant&stop_gained": "U", "frameshift_variant&stop_lost&splice_region_variant": "U", "stop_gained": "U", "start_lost": "U", "synonymous_variant": "U", "missense_variant": "U", "upstream_gene_variant": "U", "downstream_gene_variant": "U", "disruptive_inframe_insertion": "U", "disruptive_inframe_deletion": "U", "conservative_inframe_insertion": "U", "conservative_inframe_deletion": "U", "stop_lost&splice_region_variant": "U", "start_lost&conservative_inframe_deletion": "U"}

dicdrugs = {"katG": "INH", "fabG1": "INH", "fabG1 upstream": "INH", "rpoB": "RIF", "pncA": "PZA", "pncA upstream": "PZA", "gyrA": "FQ", "gyrB": "FQ", "embB": "EMB", "inhA": "INH"}
dictargets = {}

arraylist = []
interplist = []
(inh_varstring, rif_varstring, pza_varstring, fq_varstring, emb_varstring) = ("", "", "", "", "")
(inh_interpstring, rif_interpstring, pza_interpstring, fq_interpstring, emb_interpstring) = ("", "", "", "", "")

# loop over reported
fh1 = open(input1, "r")
for lines in fh1:
    lined = lines.rstrip("\r\n").split("\t")
    variants.append(lined[0])
    interpretation.append(lined[1])

fh1.close()


print("Sample ID" + "\t" + "Drug" + "\t" + "Variant" + "\t" + "Interpretation")

# loop over summary
fh2 = open(input2, "r")
for lines in fh2:
    lined = lines.rstrip("\r\n").split("\t")
    if not lined[0].isdigit():
        continue
    if "upstream" in lined[1]:
        variant = lined[1] + "_" + lined[2]
    else:
        variant = lined[1] + "_" + lined[3]

    mutations.append(variant)
    position.append(lined[0])
    if variant in variants:
        ind = variants.index(variant)
        if interpretation[ind] == "S":
            arraylist.append(dicdrugs[lined[1]] + "\t" + variant + "\t" + dicdrugs[lined[1]] + "-" + interpretation[ind])
        else:
            arraylist.append(dicdrugs[lined[1]] + "\t" + variant + "\t" + interpretation[ind])


fh2.close()

# open summary report to add interpretation results
fh6 = open(input2, "a")

print("\n", file=fh6)
print("Interpretations Summary:", file=fh6)
print("Drug" + "\t" + "Variant" + "\t" + "Interpretation", file=fh6)

# loop over SVs
fh3 = open(input3, "r")
for lines in fh3:
    lined = lines.rstrip("\r\n").split("\t")
    if lines.startswith("Sample ID"):
        continue
    if lined[2].isdigit() or lined[3] == "Complete deletion":
        if "katG" in lined[1] and lined[3] == "Complete deletion":
            arraylist.append("INH" + "\t" + lined[1] + "_" + "complete deletion" + "\t" + "INH-R")
        elif "katG" in lined[1] and lined[2].isdigit():
            arraylist.append("INH" + "\t" + lined[1] + "_deletion_" + lined[7] + "_" + lined[8] + "\t" + "INH-R")
        elif "Rv1909c" in lined[1] and lined[3] == "Complete deletion":
            arraylist.append("INH" + "\t" + lined[1] + "_" + "complete deletion" + "\t" + "INH-R")
        elif "Rv1909c" in lined[1] and lined[2].isdigit():
            arraylist.append("INH" + "\t" + lined[1] + "_deletion_" + lined[5] + "_" + lined[6] + "\t" + "INH-R")
        elif "furA" in lined[1] and lined[3] == "Complete deletion":
            arraylist.append("INH" + "\t" + lined[1] + "_" + "complete deletion" + "\t" + "INH-R")
        elif "furA" in lined[1] and lined[2].isdigit():
            arraylist.append("INH" + "\t" + lined[1] + "_deletion_" + lined[7] + "_" + lined[8] + "\t" + "INH-R")
        elif "pncA" in lined[1] and lined[3] == "Complete deletion":
            arraylist.append("PZA" + "\t" + lined[1] + "_" + "complete deletion" + "\t" + "PZA-R")
        elif "pncA" in lined[1] and lined[2].isdigit():
            arraylist.append("PZA" + "\t" + lined[1] + "_deletion_" + lined[7] + "_" + lined[8] + "\t" + "PZA-R")
        elif "Rv2043c" in lined[1] and lined[3] == "Complete deletion":
            arraylist.append("PZA" + "\t" + lined[1] + "_" + "complete deletion" + "\t" + "PZA-R")
        elif "Rv2043c" in lined[1] and lined[2].isdigit():
            arraylist.append("PZA" + "\t" + lined[1] + "_deletion_" + lined[5] + "_" + lined[6] + "\t" + "PZA-R")

fh3.close()

# loop over DR_loci_annotation
fh4 = open(input4, "r")
for lines in fh4:
    lined = lines.rstrip("\r\n").split("\t")
    if lines.startswith("Sample ID"):
        continue
    if lined[2] not in position:
        continue
    annot = lined[29].split(",")
    for x in annot:
        subannot = x.split("|")
        interprete1 = subannot[3] + "_" + subannot[10]
        interprete2 = subannot[3] + " upstream" + "_" + subannot[9]
        if interprete1 in mutations and interprete1 not in variants:
            if subannot[3] == "rpoB":
                if subannot[1] in diclofs and subannot[3] in dicdrugs:
                    arraylist.append(dicdrugs[subannot[3]] + "\t" + interprete1 + "\t" + dicdrugs[subannot[3]] + "-" + diclofs[subannot[1]])
            elif subannot[3] == "katG" or subannot[3] == "pncA":
                if subannot[1] in diclofs2 and subannot[3] in dicdrugs:
                    arraylist.append(dicdrugs[subannot[3]] + "\t" + interprete1 + "\t" + dicdrugs[subannot[3]] + "-" + diclofs2[subannot[1]])
            else:
                if subannot[1] in diclofs3 and subannot[3] in dicdrugs:
                    arraylist.append(dicdrugs[subannot[3]] + "\t" + interprete1 + "\t" + dicdrugs[subannot[3]] + "-" + diclofs3[subannot[1]])
        elif interprete2 in mutations and interprete2 not in variants:
            if subannot[3] == "rpoB":
                if subannot[1] in diclofs and subannot[3] in dicdrugs:
                    arraylist.append(dicdrugs[subannot[3]] + "\t" + interprete2 + "\t" + dicdrugs[subannot[3]] + "-" + diclofs[subannot[1]])
            elif subannot[3] == "katG" or subannot[3] == "pncA":
                if subannot[1] in diclofs2 and subannot[3] in dicdrugs:
                    arraylist.append(dicdrugs[subannot[3]] + "\t" + interprete2 + "\t" + dicdrugs[subannot[3]] + "-" + diclofs2[subannot[1]])
            else:
                if subannot[1] in diclofs3 and subannot[3] in dicdrugs:
                    arraylist.append(dicdrugs[subannot[3]] + "\t" + interprete2 + "\t" + dicdrugs[subannot[3]] + "-" + diclofs3[subannot[1]])
fh4.close()

# loop over target coverage
fh5 = open(input5, "r")
for lines in fh5:
    lined = lines.rstrip("\r\n").split("\t")
    if lines.startswith("Sample ID"):
        continue
    if "Review" in lined and lined[4] in dicdrugs:
        dictargets[lined[4]] = dicdrugs[lined[4]]

fh5.close()

#
for strings in arraylist:
    recs = strings.split("\t")
    interplist.append(recs[2])
    if recs[0] == "INH":
        if len(inh_varstring) < 2:
            inh_varstring += recs[1]
        else:
            inh_varstring += "," + recs[1]
    elif recs[0] == "RIF":
        if len(rif_varstring) < 2:
            rif_varstring += recs[1]
        else:
            rif_varstring += "," + recs[1]
    elif recs[0] == "PZA":
        if len(pza_varstring) < 2:
            pza_varstring += recs[1]
        else:
            pza_varstring += "," + recs[1]
    elif recs[0] == "FQ":
        if len(fq_varstring) < 2:
            fq_varstring += recs[1]
        else:
            fq_varstring += "," + recs[1]
    elif recs[0] == "EMB":
        if len(emb_varstring) < 2:
            emb_varstring += recs[1]
        else:
            emb_varstring += "," + recs[1]
if "INH-R" in interplist:
    inh_interpstring = "INH-R"
elif "INH-U" in interplist:
    inh_interpstring = "INH-U"
elif "INH-S" in interplist:
    inh_interpstring = "INH-S"
if "RIF-R" in interplist:
    rif_interpstring = "RIF-R"
elif "RIF-U" in interplist:
    rif_interpstring = "RIF-U"
elif "RIF-S" in interplist:
    rif_interpstring = "RIF-S"
if "PZA-R" in interplist:
    pza_interpstring = "PZA-R"
elif "PZA-U" in interplist:
    pza_interpstring = "PZA-U"
elif "PZA-S" in interplist:
    pza_interpstring = "PZA-S"
if "FQ-R" in interplist:
    fq_interpstring = "FQ-R"
elif "FQ-U" in interplist:
    fq_interpstring = "FQ-U"
elif "FQ-S" in interplist:
    fq_interpstring = "FQ-S"
if "EMB-R" in interplist:
    emb_interpstring = "EMB-R"
elif "EMB-U" in interplist:
    emb_interpstring = "EMB-U"
elif "EMB-S" in interplist:
    emb_interpstring = "EMB-S"

if any("INH" in string for string in arraylist):
    print(input6 + "\t" + "INH" + "\t" + inh_varstring + "\t" + inh_interpstring)
    print("INH" + "\t" + inh_varstring + "\t" + inh_interpstring, file=fh6)
elif "INH" in list(dictargets.values()):
    print(input6 + "\t" + "INH" + "\t" + "No reportable variant detected" + "\t" + "Review coverage")
    print("INH" + "\t" + "No reportable variant detected" + "\t" + "Review coverage", file=fh6)
else:
    print(input6 + "\t" + "INH" + "\t" + "No reportable variant detected" + "\t" + "INH-S")
    print("INH" + "\t" + "No reportable variant detected" + "\t" + "INH-S", file=fh6)
if any("RIF" in string for string in arraylist):
    print(input6 + "\t" + "RIF" + "\t" + rif_varstring + "\t" + rif_interpstring)
    print("RIF" + "\t" + rif_varstring + "\t" + rif_interpstring, file=fh6)
elif "RIF" in list(dictargets.values()):
    print(input6 + "\t" + "RIF" + "\t" + "No reportable variant detected" + "\t" + "Review coverage")
    print("RIF" + "\t" + "No reportable variant detected" + "\t" + "Review coverage", file=fh6)
else:
    print(input6 + "\t" + "RIF" + "\t" + "No reportable variant detected" + "\t" + "RIF-S")
    print("RIF" + "\t" + "No reportable variant detected" + "\t" + "RIF-S", file=fh6)
if any("PZA" in string for string in arraylist):
    print(input6 + "\t" + "PZA" + "\t" + pza_varstring + "\t" + pza_interpstring)
    print("PZA" + "\t" + pza_varstring + "\t" + pza_interpstring, file=fh6)
elif "PZA" in list(dictargets.values()):
    print(input6 + "\t" + "PZA" + "\t" + "No reportable variant detected" + "\t" + "Review coverage")
    print("PZA" + "\t" + "No reportable variant detected" + "\t" + "Review coverage", file=fh6)
else:
    print(input6 + "\t" + "PZA" + "\t" + "No reportable variant detected" + "\t" + "PZA-S")
    print("PZA" + "\t" + "No reportable variant detected" + "\t" + "PZA-S", file=fh6)
if any("FQ" in string for string in arraylist):
    print(input6 + "\t" + "FQ" + "\t" + fq_varstring + "\t" + fq_interpstring)
    print("FQ" + "\t" + fq_varstring + "\t" + fq_interpstring, file=fh6)
elif "FQ" in list(dictargets.values()):
    print(input6 + "\t" + "FQ" + "\t" + "No reportable variant detected" + "\t" + "Review coverage")
    print("FQ" + "\t" + "No reportable variant detected" + "\t" + "Review coverage", file=fh6)
else:
    print(input6 + "\t" + "FQ" + "\t" + "No reportable variant detected" + "\t" + "FQ-S")
    print("FQ" + "\t" + "No reportable variant detected" + "\t" + "FQ-S", file=fh6)
if any("EMB" in string for string in arraylist):
    print(input6 + "\t" + "EMB" + "\t" + emb_varstring + "\t" + emb_interpstring)
    print("EMB" + "\t" + emb_varstring + "\t" + emb_interpstring, file=fh6)
elif "EMB" in list(dictargets.values()):
    print(input6 + "EMB" + "\t" + "No reportable variant detected" + "\t" + "Review coverage")
    print("EMB" + "\t" + "No reportable variant detected" + "\t" + "Review coverage", file=fh6)
else:
    print(input6 + "\t" + "EMB" + "\t" + "No reportable variant detected" + "\t" + "EMB-S")
    print("EMB" + "\t" + "No reportable variant detected" + "\t" + "EMB-S", file=fh6)
