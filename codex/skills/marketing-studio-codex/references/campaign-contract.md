# Portable campaign contract

Keep `campaign.json` beside the project's deliverables; paths below are relative
to its directory (absolute paths are supported when the project already uses them).
This is a compact handoff/resume record, not upstream engine props. Extend it with
storyboard, chosen hook, review notes and operational evidence as needed.

```json
{
  "campaign_id": "brand-campaign",
  "channels": ["facebook"],
  "brief": {
    "audience": "Who and occasion",
    "objective": "What this campaign should achieve",
    "offer": "Approved price, delivery and gift conditions",
    "variants": ["standard"],
    "cta": {"text": "Order the set", "url": "https://example.com/product"},
    "proofPoints": [
      {"id": "price", "claim": "The set costs $798", "source": "client approval reference", "status": "verified"}
    ]
  },
  "copy": {"facebook": {"text": "Pasteable copy including the offer and ordering route", "claim_ids": ["price"]}},
  "product_quantities": {"product-sku": 2},
  "assets": [
    {"id": "real-photo", "path": "assets/product.jpg", "status": "approved", "kind": "reference",
     "product_ids": ["product-sku"], "variant_ids": ["standard"],
     "depicted_quantities": {}, "review": "Approved reference identity checked"}
  ],
  "gates": {"facts": "approved", "copy": "approved", "visuals": "approved", "authorization": "pending"}
}
```

`proofPoints` status is `verified`, `pending`, or `rejected`. Verified means the
claim is supported by the recorded source; it does not mean the validator visited
or independently confirmed that source. Every factual assertion used in customer
copy, including price/quantity, must be covered by its `claim_ids`; a human checks
whether the identifiers actually cover the wording. A pending source is allowed
in internal research, not customer-ready copy. Rejected claims always fail.

Asset `status`: `planned`, `rendered`, `approved`; `kind`: `reference`, `generated`,
`graphic`, `video`. Associate products and variants that actually appear; leave
arrays empty only for brand-only graphics. `depicted_quantities` records counts
when a graphic purports to show the complete purchasable quantity of a product.
Leave it empty for a partial illustrative plate, and clearly explain that decision
in review notes. Compare complete-set quantities to `product_quantities` and do
not confuse serving shots with pack weights/counts. Reference images showing a
different preparation/variant are unsuitable unless transparently explained.

```sh
python /path/to/skill/scripts/validate_campaign.py /path/to/campaign.json
python /path/to/skill/scripts/validate_campaign.py /path/to/campaign.json --ready
python /path/to/skill/scripts/validate_campaign.py /path/to/campaign.json --publish-ready
```

Draft mode allows missing planned assets and incomplete reviews with warnings.
`--ready` requires verified proof, approved copy/visual/fact reviews and existing
approved assets. `--publish-ready` additionally requires a nonempty
`authorization` object with `source`, `channels` and `timing`, with all campaign
channels covered. Record the actual user's instruction there; do not invent an
approval or require another approval when the existing authorization covers it.
These flags validate records only and never publish. Live destination/CTA,
checkout, inventory, gift-cap and channel restrictions still need their appropriate
operational checks before executing or making claims about them.
