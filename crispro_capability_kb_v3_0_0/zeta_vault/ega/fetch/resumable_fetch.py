#!/usr/bin/env python3
"""
Zeta Vault — Resumable EGA BriTROC-1 (EGAD00001011049) BAM fetcher.

HONEST FEASIBILITY NOTE
-----------------------
Full dataset = 679 BAMs, 510.8 GB. Measured throughput in this sandbox = ~1.1 MB/s
(non-Europe egress), so a full download is 1.8-5.3 days and does NOT fit a 24h sandbox
wall-clock or a 512 GB disk once BAI/variant-calling intermediates are added.

Run this on:
  - an EGA-adjacent (Europe) VM with multi-TB scratch, OR
  - an HPC node with parallel pyega3 workers (`--connections N`).

It is resume-safe: state lives in download_checkpoint.json. Re-running skips files
already in state DOWNLOADED_VERIFIED and re-verifies MD5 against the manifest.

Usage:
  python resumable_fetch.py --creds ~/.ega-credentials.json \
      --checkpoint download_checkpoint.json --out /scratch/britroc --connections 4
"""
import argparse, hashlib, json, os, subprocess, sys, time


def md5_file(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def save_ckpt(ckpt, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(ckpt, fh, indent=2)
    os.replace(tmp, path)  # atomic


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--creds", required=True, help="pyega3 credentials JSON")
    ap.add_argument("--checkpoint", default="download_checkpoint.json")
    ap.add_argument("--out", required=True, help="output scratch dir (multi-TB)")
    ap.add_argument("--connections", type=int, default=4, help="pyega3 parallel connections")
    args = ap.parse_args()

    ckpt = json.load(open(args.checkpoint))
    os.makedirs(args.out, exist_ok=True)

    todo = [f for f in ckpt["files"] if f["state"] != "DOWNLOADED_VERIFIED"]
    print(f"[fetch] {len(todo)} files pending of {ckpt['total_files']}")

    for i, fr in enumerate(ckpt["files"]):
        if fr["state"] == "DOWNLOADED_VERIFIED":
            continue
        egaf = fr["egaf_id"]
        dest = os.path.join(args.out, egaf)
        os.makedirs(dest, exist_ok=True)
        t0 = time.time()
        # pyega3 5.2.0 uses --output-dir (NOT --saveto)
        cmd = ["pyega3", "-cf", args.creds, "-c", str(args.connections),
               "fetch", egaf, "--output-dir", dest]
        print(f"[fetch] ({i+1}/{ckpt['total_files']}) {egaf} {fr['filename']} "
              f"({fr['bytes']/1e6:.0f} MB) ...")
        rc = subprocess.call(cmd)
        # locate downloaded BAM
        got = None
        for root, _, fnames in os.walk(dest):
            for fn in fnames:
                if fn.endswith(".bam"):
                    got = os.path.join(root, fn)
        if rc != 0 or not got:
            fr["state"] = "FAILED"
            save_ckpt(ckpt, args.checkpoint)
            print(f"[fetch]   FAILED rc={rc}; state saved, will retry on next run")
            continue
        # verify MD5 against manifest
        digest = md5_file(got)
        if digest == fr["md5"]:
            fr["state"] = "DOWNLOADED_VERIFIED"
            fr["local_path"] = os.path.relpath(got, args.out)
            fr["verified"] = True
            print(f"[fetch]   OK MD5 verified ({time.time()-t0:.0f}s)")
        else:
            fr["state"] = "MD5_MISMATCH"
            print(f"[fetch]   MD5 MISMATCH expected {fr['md5']} got {digest}")
        save_ckpt(ckpt, args.checkpoint)  # checkpoint after every file

    done = sum(1 for f in ckpt["files"] if f["state"] == "DOWNLOADED_VERIFIED")
    print(f"[fetch] complete: {done}/{ckpt['total_files']} verified")


if __name__ == "__main__":
    main()
