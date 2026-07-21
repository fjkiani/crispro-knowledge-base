#!/usr/bin/env python3
"""
Zeta Vault — htsget range-slice fetcher (FEASIBLE in-sandbox alternative).

Instead of downloading whole 710 MB-2 GB BAMs, htsget lets us pull only the reads
overlapping targeted genomic regions. For mutational-signature (Sig7/HRD) and
copy-number-breakpoint work we often only need specific loci / whole-genome-sparse
coverage, so a slice is 1-3 orders of magnitude smaller than a full BAM.

pyega3 5.2.0 supports region slicing via:
    pyega3 ... fetch <EGAF_ID> --reference-name <chr> --start <s> --end <e> --output-dir <dir>

This script slices a small panel of HRD/Sig7-relevant regions from a list of EGAF IDs.
It is the recommended in-sandbox path when full-BAM download is infeasible.

NOTE: region coordinates below are ILLUSTRATIVE placeholders for the panel design.
Replace with the actual BriTROC-1 reference build (GRCh37/38) coordinates for the
signature/DDR loci you intend to profile before running for real analysis.

Usage:
  python htsget_slice.py --creds ~/.ega-credentials.json --egaf EGAF00008095569 \
      --out /workspace/zeta_vault/ega/slices
"""
import argparse, json, os, subprocess

# Illustrative HRD / DDR / Sig7-relevant gene loci (GRCh38-style; VERIFY before real use)
DEFAULT_PANEL = [
    {"gene": "BRCA1", "chr": "chr17", "start": 43044295, "end": 43125483},
    {"gene": "BRCA2", "chr": "chr13", "start": 32315474, "end": 32400266},
    {"gene": "RAD51C", "chr": "chr17", "start": 58692602, "end": 58735611},
    {"gene": "CCNE1", "chr": "chr19", "start": 29811991, "end": 29824312},
    {"gene": "CDK12", "chr": "chr17", "start": 39461486, "end": 39558462},
    {"gene": "RB1", "chr": "chr13", "start": 48303748, "end": 48481890},
    {"gene": "NF1", "chr": "chr17", "start": 31094927, "end": 31377677},
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--creds", required=True)
    ap.add_argument("--egaf", required=True, help="EGAF file accession to slice")
    ap.add_argument("--out", required=True)
    ap.add_argument("--panel", default=None, help="optional JSON file of regions")
    args = ap.parse_args()

    panel = DEFAULT_PANEL
    if args.panel:
        panel = json.load(open(args.panel))

    os.makedirs(args.out, exist_ok=True)
    for region in panel:
        dest = os.path.join(args.out, args.egaf, region["gene"])
        os.makedirs(dest, exist_ok=True)
        cmd = ["pyega3", "-cf", args.creds, "fetch", args.egaf,
               "--reference-name", region["chr"],
               "--start", str(region["start"]),
               "--end", str(region["end"]),
               "--output-dir", dest]
        print(f"[slice] {args.egaf} {region['gene']} {region['chr']}:"
              f"{region['start']}-{region['end']}")
        subprocess.call(cmd)
    print("[slice] done. Slices are far smaller than whole BAMs — feasible in-sandbox.")


if __name__ == "__main__":
    main()
