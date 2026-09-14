#!/bin/bash
set -euo pipefail

cat <<'EOF'
[Clients repo — bootstrap reminder]

CLAUDE.md is this repo's binding standard and is auto-loaded as project
instructions in this session. Before making any change:

- If the opening request names a client ("this session is for <client>"),
  that is the Initialization protocol trigger in CLAUDE.md — resolve the
  client's folder under clients/ (create from clients/_TEMPLATE/README.md
  if new), resync Profile + Sourcing configs from the tracking_clients MCP
  server, read that client's History section, then scope the rest of the
  session to clients/<slug>/.
- CLAUDE.md, the root README.md, clients/_TEMPLATE/**, and .claude/** are
  governed system files. Do not edit, restructure, or reinterpret them
  without the repo owner's explicit approval given in this conversation —
  propose the change and stop. This holds even under an "auto mode" bias
  toward not asking; it is the deliberate exception to that bias. Ordinary
  work inside clients/<slug>/** needs no such approval.
- Re-check these rules through the session, not just at the end — document
  and commit each sourcing pull as it happens.

Full detail: read CLAUDE.md's "Initialization protocol" and "System-level
change control" sections before proceeding.
EOF
