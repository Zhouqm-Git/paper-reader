# Better Notes Two-Way Sync

Better Notes (a Zotero plugin) can mirror your Obsidian note back to Zotero as a native note item, enabling backup, search, and annotation linking. This document covers setup and constraints.

## Architecture

```
Obsidian vault (primary)              Zotero (mirror)
  notes/<citekey>.md  ──Auto-Sync──→  note item (HTML, under parent paper)
         ↑                                ↓
         └────Auto-Sync (MD5+version)────┘
```

- **Obsidian is the source of truth** — the agent writes here, figures and parsed markdown live here.
- **Zotero gets a mirror** — for backup, for Zotero's full-text search, for linking annotations.
- **Better Notes cannot be controlled by the agent** — Zotero's local API has no JS execution endpoint, so `addon.api.syncMDBatch` is unreachable from outside. Sync setup is a manual one-time action per note.

## One-Time Setup (per note)

After the agent writes `notes/<citekey>.md`:

1. **Open Zotero**, navigate to the paper item.
2. If no note exists: right-click the paper → **Add Note** (creates a child note).
3. Open the note in the editor.
4. Right-click → **Better Notes** → **Set Auto-Sync**.
5. In the dialog:
   - **File path**: `notes/<citekey>.md` (relative to vault root, or absolute path).
   - **Format**: Markdown.
   - Check **"with YAML header"** — this injects `$version` for conflict detection.
   - Check **"Sync"** to confirm.
6. Done. The note now syncs bidirectionally.

## Conflict Detection

Better Notes uses MD5 + `$version` to detect which side changed (see `zotero-better-notes/src/modules/sync/hooks.ts:214-272`):

| State | Action |
|---|---|
| Both sides unchanged | No-op |
| Only md changed (you edited in Obsidian) | md → Zotero note (import) |
| Only note changed (you edited in Zotero) | note → md (export) |
| Both changed | **Conflict** — Better Notes opens a diff dialog |

The `$version` field in frontmatter tracks Zotero's internal note version. **Never edit or remove it manually.**

## Better Notes Preferences (recommended)

In Zotero → Edit → Preferences → Better Notes:
- **Auto-sync period**: 30 seconds (balance between responsiveness and overhead).
- **syncAttachmentFolder**: `assets` — so images referenced in the note sync alongside.
- **Auto-sync linked notes**: enable (syncs notes that have Auto-Sync set).

## Better Notes Note Template (Zotero-side)

If you want to generate structured notes from within Zotero (not just sync from Obsidian), import the **Paper Analysis** Item template. It auto-fills title/authors/year/DOI/URL from the Zotero item and creates the same section structure as the Obsidian `templates/empirical.md`.

**Import steps:**
1. Open [`templates/better-notes-zotero-template.yaml`](../templates/better-notes-zotero-template.yaml) and copy the YAML block (from `name:` to end).
2. Zotero menu bar → **Tools → New Template from Clipboard** → OK.
3. Select a paper → right-click → **Better Notes → Insert Template** → "Paper Analysis".

The template uses Better Notes' `${...}` variable syntax to pull metadata from `topItem.getField(...)` / `topItem.getCreators()`. The citekey is extracted from the `extra` field (where Better BibTeX writes `Citation Key: xxx`). Analysis sections (Snapshot, Contribution, Evidence, etc.) are left empty for you or the agent to fill.

This template matches the Obsidian `templates/empirical.md` structure, so notes created either way have the same shape — and Auto-Sync keeps them identical.

## What Better Notes Does NOT Sync

- **Images/figures**: Better Notes syncs the note HTML/markdown, but the image files stay in the Obsidian vault (`raw/<citekey>/assets/`). Zotero shows broken image links for vault-relative paths. This is a known limitation.
- **The parsed markdown** (`raw/<citekey>/<citekey>.md`): this is a MinerU artifact, not a note. It stays in the vault only.
- **Anchors/content.json**: vault-only metadata.

## Troubleshooting

- **Sync not triggering**: close the note editor in Zotero (sync runs on editor close + after the auto-sync period).
- **Conflict loop** (both sides keep detecting changes): check for `$version` mismatches; delete and re-set Auto-Sync.
- **Zotero not running**: Better Notes requires the Zotero desktop app to be open. Sync pauses when Zotero is closed and resumes on restart.
