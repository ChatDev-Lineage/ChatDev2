# OmniTag / Rosetta Partial-Join Contract

Status: design constraint for ChatDev/Intermediary context handling, derived from
archive archaeology and checked against the current Greater System field manual.

## The finding

A legacy record surface places two semantic notations side by side:

- a positional SMHT state vector;
- a glyph/MegaTag roster containing families such as Xenon, Almanac, NPC,
  Temple, OldestHouse, HouseLeaves, AltDims, Interviews, Modular, Expansion,
  Collection, RetainDS and Evolve.

The correspondence is **partial**, not a total dictionary.

The archive comparison supplied during the 2026-09-07 archaeology pass found a
shared envelope of eight semantic fields:

```text
Timestamp
User_ID
Session_ID
Priority
Status
Version
Checksum
SCP / constraint state
```

The two notations then retain private domains. The SMHT side carries additional
session/game-state fields. The glyph side carries additional world-model and
structural families.

The current Greater System field manual independently preserves the same shape:
SMHT defines the R-X tail as Timestamp, User ID, Session ID, Priority, Status,
Version and Checksum, while MegaTag lists those envelope families alongside
Xenon and the wider glyph roster. It also explicitly calls MegaTag a **context
manifest** and recommends preserving unknown extension namespaces rather than
flattening them away.

## Contract

Rosetta correspondence MUST be represented as:

```text
source record
+ target record
+ explicit join envelope
+ source-only fields
+ target-only fields
+ provenance
+ mapping confidence/status
```

It MUST NOT be represented as an assumed total field bijection.

### Why

A total mapping would force the compiler to invent correspondences for fields
that the evidence does not pair. That would convert absence of evidence into
fabricated semantics.

```text
correlated != equivalent
same position != same authority
same glyph family != same namespace owner
partial mapping != incomplete total mapping
unknown counterpart != null-valued known counterpart
```

## Proposed machine shape

This is a design candidate for a future `omnitag.record/v2` authority layer. It
is not declared canonical merely by appearing in ChatDev2.

```json
{
  "schema": "omnitag.rosetta-map/v1",
  "mapping_id": "...",
  "source": {
    "notation": "smht",
    "record_ref": "..."
  },
  "target": {
    "notation": "megaglyph",
    "record_ref": "..."
  },
  "join": [
    {"source": "R", "target": "Timestamp", "semantic": "timestamp"},
    {"source": "S", "target": "User_ID", "semantic": "user_id"},
    {"source": "T", "target": "Session_ID", "semantic": "session_id"},
    {"source": "U", "target": "Priority", "semantic": "priority"},
    {"source": "V", "target": "Status", "semantic": "status"},
    {"source": "W", "target": "Version", "semantic": "version"},
    {"source": "X", "target": "Checksum", "semantic": "checksum"}
  ],
  "additional_correspondence": [
    {
      "source": "O",
      "target": "SCP",
      "semantic": "constraint_state",
      "status": "supported"
    }
  ],
  "source_only": [],
  "target_only": [],
  "provenance": [],
  "confidence": "supported"
}
```

The arrays are intentionally open. A compiler records what is actually present
in the source material. It does not populate missing counterparts to make the
object look symmetrical.

## Namespace disagreement is data

The archive also preserves a vocabulary disagreement: one source places
Xenith/Xenon in a MegaTag context while another presents Xenon under OmniTag and
also in a MegaTag roster.

Do not resolve that by silently selecting one owner.

Represent it as a provenance-bearing namespace assertion, for example:

```json
{
  "family": "Xenon",
  "assertions": [
    {"namespace": "OmniTag", "source_ref": "..."},
    {"namespace": "MegaTag", "source_ref": "..."}
  ],
  "resolution": "unsettled"
}
```

Likewise, Xenith and Xenon can be recorded as the same **slot family** when the
marker, slot position and payload grammar support that relationship, without
claiming that the names are globally interchangeable in every historical
source.

## ChatDev / Intermediary requirement

Any task packet compiled from OmniTag/SMHT/Rosetta material should preserve:

- original notation and raw source reference;
- explicit join fields used for correlation;
- source-only fields;
- target-only fields;
- unresolved namespace disagreements;
- evidence level for each correspondence;
- checksum/version fields where present.

The context compiler should select only task-relevant fields for model context,
while retaining the full mapping packet in the receipt. This aligns with the
existing MegaTag compiler doctrine and prevents symbolic context from becoming
token-heavy decorative noise.

## Example compiler rule

```text
if correspondence is explicit:
    map it and cite provenance
elif semantic relationship is supported but not identical:
    record relationship + confidence
else:
    preserve source field as source-only
    do not synthesize a counterpart
```

## Relation to the factory

This is especially useful for large-game work. Project 144, Ash & Anvil, Player
Two, GAL and Furyline can each expose different state vocabularies while sharing
a small correlation envelope:

```text
project/task/run/session/version/checksum/time/status
```

ChatDev does not need to force every game into one universal schema. It needs a
reliable join spine plus domain-specific payloads.

That gives the colony a federation rather than a semantic monoculture.

## Provenance boundary

The archaeology pass supplied a short commit prefix `d27aae5`. A global short
SHA is not unique, so this document does not claim an independently resolved
repository/commit for that prefix. The exact source ref should be filled in when
the originating branch/repository is identified directly.

The design therefore distinguishes:

```text
archive finding supplied
!= exact Git object independently resolved
!= canonical schema ratified
```

ChatDev2 consumes the constraint. Schema authority belongs in the appropriate
modern OmniTag/Kilo_Core/NuSyQ contract layer after review.
