# Query — 2026-10-21 catalog audit pilot on all 1,000 companies (deep-catalog-manufacturers)

Config `82d47d88-32b2-4dd8-8307-b12ac530aaf7`, campaign 6. **Expanding existing segment** (enrichment of `2026-10-21-companies-qualified-2.csv`, joined on `company_linkedin_url`). **Why:** owner asked to "do a sample on all and see what is more promising" for personalising Message 1 (`{number}` of missing/shared images).
**Tool:** direct HTTPS fetch (`2026-10-21-scripts/crawl_audit.py`, UA `catalog-audit/1.0`, robots.txt honored for product pages, <=~14 requests per domain, no login, no JS rendering). Per domain: homepage -> robots.txt -> sitemap(s) (<=8 files) -> up to 6 random product-like pages -> check images.
**Columns:** `status`/`fail_reason` (why a site could not be audited), `sitemap_url_count`, `sitemap_product_like` (URLs matching product/part/item/catalog paths), `product_pages_fetched`, `placeholder_pages` + `placeholder_examples` (image URL/alt matching coming-soon/no-image/placeholder), `placeholder_clean` (same minus lazy-load/captcha/social false positives), `shared_image_pages` (**unreliable**: og:image reused across sampled pages, often just a site logo), `line_drawing_hint_pages`, `platform` (HTML fingerprint), `cad_3d_text`, `configurator_text`, `sample_urls`.

## Result (1,000 companies)
- Auditable: 670 ok (67%); 236 unreachable (123 connection errors, 88 HTTP 403, rest 429/5xx); 83 no sitemap and no product links; 11 product pages unfetchable.
- Sitemap found: 618; product-like URLs found: 398; **146 with >=1,000 product-like URLs** (independent confirmation of catalog size).
- Placeholder image seen on a sampled product page: 42 raw, **36 after removing false positives** (about 5% of auditable sites). Real examples: Bosch Rexroth, LEMO, ABB, Stanley Engineered Fastening, Basler, Sunnen, Deublin, Power Packer, Peer Chain, MacPanel.
- CAD/3D text on page: 253; configurator text: 172; platform fingerprinted: 361 (WordPress 255, WooCommerce 122, Cadenas 36, Sitecore 24, TraceParts 18, 3D viewer 16, Magento 14, SAP Commerce 12, Shopify 12, Salsify 9).

## Caveats
- A 6-page random sample misses a placeholder rate under ~15%: **absence of a hit is not evidence of no gap**, and no total `{number}` can be derived from this. Needs a deeper per-site crawl (hundreds of pages) for the subset worth it.
- No JS rendering: JS-built catalogs show few images; bot-blocked sites (403) are unaudited.
- `shared_image_pages` is noise (74 of 150 flagged have 6 of 6 identical og:image, i.e. a logo). Do not use.
- Some placeholder hits are plugin or lazy-load assets; `placeholder_clean` filters the common ones but not all (e.g. Stanadyne's hit was an Instagram-feed plugin image, removed only if "instagram" is in the URL, which it is).
