#!/usr/bin/env python3
"""Read-only campaign readiness check; no network, writes or publication.

Usage: python validate_campaign.py campaign.json [--ready | --publish-ready]
Draft mode permits pending work with warnings; ready checks delivery invariants;
publish-ready also checks the recorded authorization scope. Relative media paths
resolve against the manifest. Human semantic/visual review is still required.
"""
import argparse
import json
import math
from pathlib import Path
from urllib.parse import urlparse


def validate(data, base, ready=False, publish=False):
    errors, warnings = [], []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def gate(condition, message):
        if not condition:
            (errors if ready or publish else warnings).append(message)

    def string(value):
        return isinstance(value, str) and bool(value.strip())

    def strings(value):
        return isinstance(value, list) and all(string(v) for v in value)

    if not isinstance(data, dict):
        return ['manifest must be an object'], []
    require(string(data.get('campaign_id')), 'campaign_id is required')
    channels = data.get('channels', [])
    if not strings(channels) or not channels:
        errors.append('channels must be a nonempty string list')
        channels = []
    require(len(set(channels)) == len(channels), 'channels must be unique')
    brief = data.get('brief')
    if not isinstance(brief, dict):
        return errors + ['brief must be an object'], warnings
    for field in ('audience', 'objective', 'offer'):
        require(string(brief.get(field)), f'brief.{field} is required')
    variants = brief.get('variants', [])
    if not strings(variants) or not variants:
        errors.append('brief.variants must be a nonempty string list')
        variants = []
    require(len(set(variants)) == len(variants), 'brief.variants must be unique')
    cta = brief.get('cta', {})
    if not isinstance(cta, dict):
        cta = {}
    require(string(cta.get('text')), 'brief.cta.text is required')
    url = cta.get('url', '')
    parsed = urlparse(url) if isinstance(url, str) else urlparse('')
    require(parsed.scheme in ('https', 'http') and bool(parsed.netloc), 'brief.cta.url must be an HTTP(S) destination')
    points = brief.get('proofPoints', [])
    if not isinstance(points, list):
        errors.append('brief.proofPoints must be a list')
        points = []
    gate(bool(points), 'no proofPoints recorded')
    proof = {}
    for i, point in enumerate(points):
        label = f'proofPoints[{i}]'
        if not isinstance(point, dict):
            errors.append(f'{label} must be an object')
            continue
        pid = point.get('id')
        if not string(pid):
            errors.append(f'{label}.id is required')
            continue
        require(pid not in proof, f'duplicate proof id: {pid}')
        proof[pid] = point
        require(string(point.get('claim')), f'{pid}: claim is required')
        status = point.get('status')
        require(status in ('verified', 'pending', 'rejected'), f'{pid}: invalid proof status')
        require(status != 'rejected', f'{pid}: rejected claim must be removed')
        require(status != 'verified' or string(point.get('source')), f'{pid}: verified proof needs source')
        gate(status == 'verified', f'{pid}: proof is not verified')
    copy = data.get('copy', {})
    if not isinstance(copy, dict):
        errors.append('copy must be an object')
        copy = {}
    for channel in channels:
        row = copy.get(channel, {})
        if not isinstance(row, dict):
            row = {}
        gate(string(row.get('text')), f'{channel}: copy is missing')
        ids = row.get('claim_ids', [])
        if not strings(ids):
            errors.append(f'{channel}: claim_ids must be a string list')
            ids = []
        gate(bool(ids), f'{channel}: factual claim mapping is missing')
        for pid in ids:
            require(pid in proof, f'{channel}: unknown claim id {pid}')
    quantities = data.get('product_quantities', {})
    if not isinstance(quantities, dict):
        errors.append('product_quantities must be an object')
        quantities = {}
    for pid, count in quantities.items():
        require(isinstance(count, (int, float)) and not isinstance(count, bool) and math.isfinite(count) and count > 0, f'{pid}: quantity must be positive and finite')
    assets = data.get('assets', [])
    if not isinstance(assets, list):
        errors.append('assets must be a list')
        assets = []
    gate(bool(assets), 'no assets recorded')
    seen = set()
    for i, asset in enumerate(assets):
        label = f'assets[{i}]'
        if not isinstance(asset, dict):
            errors.append(f'{label} must be an object')
            continue
        aid = asset.get('id')
        if not string(aid):
            errors.append(f'{label}.id is required')
            continue
        require(aid not in seen, f'duplicate asset id: {aid}')
        seen.add(aid)
        status = asset.get('status')
        require(status in ('planned', 'rendered', 'approved'), f'{aid}: invalid asset status')
        require(asset.get('kind') in ('reference', 'generated', 'graphic', 'video'), f'{aid}: invalid asset kind')
        path = asset.get('path')
        exists = string(path) and (Path(base) / path).is_file() and (Path(base) / path).stat().st_size > 0
        if status in ('rendered', 'approved'):
            require(exists, f'{aid}: recorded finished asset is missing or empty')
        else:
            gate(exists, f'{aid}: planned file missing')
        gate(status == 'approved' and string(asset.get('review')), f'{aid}: visual review is incomplete')
        product_ids, variant_ids = asset.get('product_ids', []), asset.get('variant_ids', [])
        require(strings(product_ids), f'{aid}: product_ids must be a string list')
        require(strings(variant_ids), f'{aid}: variant_ids must be a string list')
        if strings(product_ids):
            for pid in product_ids:
                require(pid in quantities, f'{aid}: unknown product {pid}')
        if strings(variant_ids):
            for vid in variant_ids:
                require(vid in variants, f'{aid}: unknown variant {vid}')
        depicted = asset.get('depicted_quantities', {})
        if not isinstance(depicted, dict):
            errors.append(f'{aid}: depicted_quantities must be an object')
            continue
        for pid, count in depicted.items():
            require(pid in quantities and count == quantities.get(pid), f'{aid}: depicted quantity mismatch for {pid}')
    gates = data.get('gates', {})
    if not isinstance(gates, dict):
        gates = {}
    for name in ('facts', 'copy', 'visuals'):
        gate(gates.get(name) == 'approved', f'{name} review is not approved')
    if publish:
        auth = gates.get('authorization', {})
        if not isinstance(auth, dict):
            auth = {}
        scope = auth.get('channels', [])
        require(strings(scope), 'authorization.channels must be a string list')
        require(string(auth.get('source')) and string(auth.get('timing')), 'publication authorization needs source and timing')
        require(strings(scope) and set(channels).issubset(set(scope)), 'publication authorization does not cover campaign channels')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--ready', action='store_true')
    group.add_argument('--publish-ready', action='store_true')
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding='utf-8'))
        errors, warnings = validate(data, args.manifest.parent, args.ready, args.publish_ready)
    except (OSError, ValueError) as exc:
        errors, warnings = [str(exc)], []
    print(json.dumps({'status': 'FAIL' if errors else 'PASS', 'errors': errors, 'warnings': warnings}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
