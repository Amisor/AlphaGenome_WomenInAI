#!/usr/bin/env python3
"""
predict_alphagenome.py — Obtain an AlphaGenome prediction for a BRCA1 test variant.

Target Variant:
  Default: BRCA1 c.4986+1G>T (NM_007294.4:c.4986+1G>T)
  Genomic Coordinate: chr17:43070927 (GRCh38 / hg38)
  Genomic Strand: Genomic plus strand ref=C, alt=A (reverse complement of cDNA G>T on minus strand)
  SpliceVarDB Label: Splice-altering (Score: 3)
  Location: Canonical splice donor site at exon 16 / intron 16 boundary

Model:
  AlphaGenome (Google DeepMind)
  Package: alphagenome (pip install alphagenome)
  Reference: Nature 649, 1206–1218 (2026), DOI: 10.1038/s41586-025-10014-0

Outputs:
  sample_prediction.json      — Real AlphaGenome prediction outputs
  sample_prediction.mock.json — Clearly labeled mock placeholder (if run with --mock)

Usage:
  # Live prediction with default 100KB context (~15s):
  python predict_alphagenome.py

  # Live prediction with 1MB context (~2.5 min):
  python predict_alphagenome.py --context 1MB

  # Offline test with synthetic mock placeholder:
  python predict_alphagenome.py --mock
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
import numpy as np

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Default test variant: BRCA1 c.4986+1G>T
DEFAULT_HGVS = "NM_007294.4:c.4986+1G>T"
DEFAULT_CHROM = "chr17"
DEFAULT_POS = 43_070_927
DEFAULT_REF = "C"   # Genomic plus strand
DEFAULT_ALT = "A"   # Genomic plus strand
DEFAULT_SPLICING_LABEL = "Splice-altering"
DEFAULT_SPLICEVARDB_SCORE = 3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT = os.path.join(BASE_DIR, "data", "sample_prediction.json")
DEFAULT_MOCK_OUTPUT = os.path.join(BASE_DIR, "data", "sample_prediction.mock.json")


def parse_args():
    parser = argparse.ArgumentParser(description="Obtain AlphaGenome prediction for a BRCA1 test variant.")
    parser.add_argument("--api-key", default=None, help="AlphaGenome API key (overrides ALPHAGENOME_API_KEY env var)")
    parser.add_argument("--context", choices=["16KB", "100KB", "500KB", "1MB"], default="100KB",
                        help="Genomic context length (default: 100KB, covers BRCA1 locus in ~15s)")
    parser.add_argument("--chrom", default=DEFAULT_CHROM, help=f"Chromosome (default: {DEFAULT_CHROM})")
    parser.add_argument("--pos", type=int, default=DEFAULT_POS, help=f"Genomic position 1-based (default: {DEFAULT_POS})")
    parser.add_argument("--ref", default=DEFAULT_REF, help=f"Reference base (default: {DEFAULT_REF})")
    parser.add_argument("--alt", default=DEFAULT_ALT, help=f"Alternate base (default: {DEFAULT_ALT})")
    parser.add_argument("--hgvs", default=DEFAULT_HGVS, help=f"HGVS name (default: {DEFAULT_HGVS})")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help=f"Path to write output JSON (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--mock", action="store_true", help="Run with clearly labeled synthetic mock data")
    return parser.parse_args()


def get_api_key(args) -> str | None:
    """Retrieve API key from CLI flag, environment, or .env file."""
    if args.api_key:
        return args.api_key.strip()
    key = os.environ.get("ALPHAGENOME_API_KEY")
    if key:
        return key.strip()
    return None


def run_mock_prediction(variant_meta: dict, output_path: str) -> dict:
    """Generate a clearly labeled synthetic mock prediction for pipeline testing."""
    print("\n" + "!" * 65)
    print("WARNING: Running in MOCK mode. This is synthetic test data.")
    print("!" * 65)

    mock_output_path = output_path
    if not mock_output_path.endswith(".mock.json"):
        if "sample_prediction.json" in mock_output_path:
            mock_output_path = mock_output_path.replace("sample_prediction.json", "sample_prediction.mock.json")
        else:
            mock_output_path = DEFAULT_MOCK_OUTPUT

    result = {
        "is_mock": True,
        "mock_disclaimer": "SYNTHETIC PLACEHOLDER ONLY. DO NOT USE FOR CLINICAL OR SCIENTIFIC INFERENCE.",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model_metadata": {
            "model_name": "AlphaGenome (Synthetic Mock)",
            "provider": "Mock / Local Pipeline Test",
            "version": "mock-v1",
        },
        "variant": variant_meta,
        "prediction_results": {
            "splicing": {
                "mock_delta_splice_sites": 0.884,
                "mock_delta_splice_site_usage": 0.742,
                "mock_delta_splice_junctions": 0.915,
                "mock_combined_splicing_score": 0.915,
                "mock_predicted_effect": "Disrupted splice donor site at exon 16 (+1 position)",
            }
        }
    }

    with open(mock_output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nSaved synthetic mock output to: {mock_output_path}")
    return result


def run_real_prediction(api_key: str, variant_meta: dict, context_choice: str, output_path: str) -> dict:
    """Execute live variant effect prediction using the real AlphaGenome API."""
    print("\nConnecting to AlphaGenome API...")

    from alphagenome.models.v1 import dna_client, dna_output
    from alphagenome.data import genome

    # 1. Initialize client
    client = dna_client.create(api_key)
    print("Initialized AlphaGenome client.")

    # 2. Define Variant
    variant = genome.Variant(
        chromosome=variant_meta["chrom"],
        position=variant_meta["pos"],
        reference_bases=variant_meta["ref"],
        alternate_bases=variant_meta["alt"],
    )
    print(f"Variant: {variant}")

    # 3. Define Interval based on selected context length
    context_map = {
        "16KB": dna_client.SEQUENCE_LENGTH_16KB,
        "100KB": dna_client.SEQUENCE_LENGTH_100KB,
        "500KB": dna_client.SEQUENCE_LENGTH_500KB,
        "1MB": dna_client.SEQUENCE_LENGTH_1MB,
    }
    seq_len = context_map[context_choice]
    interval = variant.reference_interval.resize(seq_len)
    print(f"Genomic context interval ({context_choice}, {seq_len} bp): {interval}")

    # 4. Request splicing outputs
    requested_outputs = [
        dna_output.OutputType.SPLICE_SITES,
        dna_output.OutputType.SPLICE_SITE_USAGE,
        dna_output.OutputType.SPLICE_JUNCTIONS,
    ]

    print("Submitting predict_variant request (splicing modalities)...")
    pred_output = client.predict_variant(
        interval=interval,
        variant=variant,
        requested_outputs=requested_outputs,
        ontology_terms=None,
    )
    print("Received prediction from AlphaGenome API successfully.")

    # 5. Extract and summarize track differences
    ref_out = pred_output.reference
    alt_out = pred_output.alternate

    summary = {}
    raw_details = {}

    # Analyze Splice Sites track (donor/acceptor probabilities)
    if ref_out.splice_sites is not None and alt_out.splice_sites is not None:
        ref_vals = np.asarray(ref_out.splice_sites.values)
        alt_vals = np.asarray(alt_out.splice_sites.values)
        diff = alt_vals - ref_vals
        max_abs_diff = float(np.max(np.abs(diff)))
        mean_abs_diff = float(np.mean(np.abs(diff)))

        # Also get local delta right at the variant position
        var_offset = variant.position - interval.start
        local_ref = [float(x) for x in ref_vals[var_offset]] if 0 <= var_offset < len(ref_vals) else None
        local_alt = [float(x) for x in alt_vals[var_offset]] if 0 <= var_offset < len(alt_vals) else None

        summary["splice_sites"] = {
            "track_resolution_bp": ref_out.splice_sites.resolution,
            "num_tracks": ref_out.splice_sites.num_tracks,
            "max_abs_delta": max_abs_diff,
            "mean_abs_delta": mean_abs_diff,
            "variant_position_ref_scores": local_ref,
            "variant_position_alt_scores": local_alt,
            "channel_names": list(ref_out.splice_sites.metadata["name"]),
        }
        raw_details["splice_sites"] = {
            "ref_shape": list(ref_vals.shape),
            "ref_min": float(np.min(ref_vals)),
            "ref_max": float(np.max(ref_vals)),
            "alt_min": float(np.min(alt_vals)),
            "alt_max": float(np.max(alt_vals)),
        }

    # Analyze Splice Site Usage track
    if ref_out.splice_site_usage is not None and alt_out.splice_site_usage is not None:
        ref_vals = np.asarray(ref_out.splice_site_usage.values)
        alt_vals = np.asarray(alt_out.splice_site_usage.values)
        diff = alt_vals - ref_vals
        max_abs_diff = float(np.max(np.abs(diff)))
        mean_abs_diff = float(np.mean(np.abs(diff)))
        summary["splice_site_usage"] = {
            "track_resolution_bp": ref_out.splice_site_usage.resolution,
            "num_tracks": ref_out.splice_site_usage.num_tracks,
            "max_abs_delta": max_abs_diff,
            "mean_abs_delta": mean_abs_diff,
        }
        raw_details["splice_site_usage"] = {
            "ref_shape": list(ref_vals.shape),
            "ref_min": float(np.min(ref_vals)),
            "ref_max": float(np.max(ref_vals)),
            "alt_min": float(np.min(alt_vals)),
            "alt_max": float(np.max(alt_vals)),
        }

    # Analyze Splice Junctions track
    if ref_out.splice_junctions is not None and alt_out.splice_junctions is not None:
        ref_vals = np.asarray(ref_out.splice_junctions.values)
        alt_vals = np.asarray(alt_out.splice_junctions.values)
        diff = alt_vals - ref_vals
        max_abs_diff = float(np.max(np.abs(diff)))
        mean_abs_diff = float(np.mean(np.abs(diff)))
        summary["splice_junctions"] = {
            "num_junctions": len(ref_out.splice_junctions.junctions),
            "num_tracks": ref_out.splice_junctions.num_tracks,
            "max_abs_delta": max_abs_diff,
            "mean_abs_delta": mean_abs_diff,
        }
        raw_details["splice_junctions"] = {
            "ref_shape": list(ref_vals.shape),
            "ref_min": float(np.min(ref_vals)),
            "ref_max": float(np.max(ref_vals)),
            "alt_min": float(np.min(alt_vals)),
            "alt_max": float(np.max(alt_vals)),
        }

    # Combined splicing disruption indicator
    max_ss = summary.get("splice_sites", {}).get("max_abs_delta", 0.0)
    max_ssu = summary.get("splice_site_usage", {}).get("max_abs_delta", 0.0)
    max_sj = summary.get("splice_junctions", {}).get("max_abs_delta", 0.0)
    combined_score = max_ss + max_ssu + (max_sj / 5.0)

    result = {
        "is_mock": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model_metadata": {
            "model_name": "AlphaGenome",
            "provider": "Google DeepMind",
            "api_endpoint": "gdmscience.googleapis.com",
            "package_version": "alphagenome-0.10.0",
            "citation": "Nature 649, 1206-1218 (2026), DOI: 10.1038/s41586-025-10014-0",
        },
        "variant": variant_meta,
        "interval": {
            "chromosome": interval.chromosome,
            "start": interval.start,
            "end": interval.end,
            "length_bp": interval.end - interval.start,
            "context_setting": context_choice,
        },
        "splicing_metrics": {
            "max_delta_splice_sites": max_ss,
            "max_delta_splice_site_usage": max_ssu,
            "max_delta_splice_junctions": max_sj,
            "combined_splicing_score": combined_score,
            "predicted_effect": "Disrupted splice donor site" if combined_score > 0.1 else "No significant disruption",
        },
        "splicing_prediction_summary": summary,
        "raw_track_metadata": raw_details,
    }

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nSuccessfully wrote real prediction output to: {output_path}")
    print("\n--- PREDICTION SUMMARY ---")
    print(f"  Max Delta Splice Sites:      {max_ss:.4f}")
    print(f"  Max Delta Splice Site Usage: {max_ssu:.4f}")
    print(f"  Max Delta Splice Junctions:  {max_sj:.4f}")
    print(f"  Combined Splicing Score:     {combined_score:.4f}")
    print(f"  Predicted Effect:            {result['splicing_metrics']['predicted_effect']}")
    print(f"  SpliceVarDB Ground Truth:    {variant_meta['splicevardb_label']} (Score: {variant_meta['splicevardb_score']})")

    return result


def main():
    args = parse_args()

    print("=" * 65)
    print(" predict_alphagenome.py — AlphaGenome Variant Predictor")
    print("=" * 65)

    # Variant metadata
    variant_meta = {
        "gene": "BRCA1",
        "hgvs": args.hgvs,
        "chrom": args.chrom,
        "pos": args.pos,
        "ref": args.ref,
        "alt": args.alt,
        "splicevardb_label": DEFAULT_SPLICING_LABEL,
        "splicevardb_score": DEFAULT_SPLICEVARDB_SCORE,
        "description": "Canonical splice donor site (+1 position) at exon 16 / intron 16 boundary",
    }

    print(f"Target Variant:")
    print(f"  HGVS:       {variant_meta['hgvs']}")
    print(f"  Genomic:    {variant_meta['chrom']}:{variant_meta['pos']} {variant_meta['ref']}>{variant_meta['alt']} (GRCh38)")
    print(f"  SpliceVar:  {variant_meta['splicevardb_label']} (score={variant_meta['splicevardb_score']})")

    api_key = get_api_key(args)

    if args.mock:
        run_mock_prediction(variant_meta, args.output)
        return

    if not api_key:
        print("\n" + "!" * 65)
        print("ERROR: No AlphaGenome API key detected.")
        print("!" * 65)
        print("To run with your live AlphaGenome API key, please provide it via:")
        print("  1. Environment variable:")
        print("       export ALPHAGENOME_API_KEY=\"your_key_here\"")
        print("  2. Local .env file:")
        print("       echo \"ALPHAGENOME_API_KEY=your_key_here\" > .env")
        print("  3. Command-line flag:")
        print(f"       python predict_alphagenome.py --api-key \"your_key_here\"")
        print("\nTo run an offline synthetic test pass without an API key, use:")
        print("  python predict_alphagenome.py --mock")
        print("=" * 65)
        sys.exit(1)

    try:
        run_real_prediction(api_key, variant_meta, args.context, args.output)
    except Exception as e:
        print(f"\nAPI Call Failed: {e}", file=sys.stderr)
        print("\nIf you are hitting rate limits or credentials errors, check your key at:")
        print("https://deepmind.google.com/science/alphagenome/account/terms")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("predict_alphagenome.py completed successfully.")
    print("=" * 65)


if __name__ == "__main__":
    main()
