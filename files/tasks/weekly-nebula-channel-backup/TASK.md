---
slug: daily-nebula-full-backup-channels-files
title: Daily Nebula Full Backup (Channels + Files)
steps:
- description: Discover all current Nebula channels and all workspace files
  agent_slug: nebula
  format_guide: 1. Use manage_channels(action=list, include_archived=True) to get
    ALL channels. Extract name, is_archived status. Normalize names to folder-safe
    slugs. 2. Use browse_files(search_query=all, limit=50) and paginate ALL files.
    For each file collect path, filename, size_bytes, extension, folder_path. 3. Filter
    OUT tmp/ folders. Keep scripts, data, docs, code, outputs, agents, tasks, notes,
    images, misc. 4. Output channels array and files array plus total counts.
- description: 'Backup batch 1: first 8 channels chat history'
  agent_id: agt_069a1bc8c3647e88800074fd7b0a4b1d
  agent_slug: nebula-channel-backup-archiver
  format_guide: 'From step 1 channels, take items 0-7. For EACH: fetch full history
    via search_past_messages, paginate until has_more=false. Format as conversation.md.
    Create manifest.json. Push to uerzer/nebula-backup under channels/SLUG/. Commit:
    backup SLUG DATE.'
- description: 'Backup batch 2: channels 8-15 chat history'
  agent_id: agt_069a1bc8c3647e88800074fd7b0a4b1d
  agent_slug: nebula-channel-backup-archiver
  format_guide: 'From step 1 channels, take items 8-15. For EACH: fetch full history
    via search_past_messages, paginate until has_more=false. Format as conversation.md.
    Create manifest.json. Push to uerzer/nebula-backup under channels/SLUG/. Commit:
    backup SLUG DATE.'
- description: 'Backup batch 3: channels 16-23 chat history'
  agent_id: agt_069a1bc8c3647e88800074fd7b0a4b1d
  agent_slug: nebula-channel-backup-archiver
  format_guide: 'From step 1 channels, take items 16-23. For EACH: fetch full history,
    paginate until done. Format as conversation.md. Create manifest.json. Push to
    uerzer/nebula-backup under channels/SLUG/. Commit: backup SLUG DATE.'
- description: 'Backup batch 4: remaining channels 24+ chat history'
  agent_id: agt_069a1bc8c3647e88800074fd7b0a4b1d
  agent_slug: nebula-channel-backup-archiver
  format_guide: 'From step 1 channels, take items 24 onward. For EACH: fetch full
    history, paginate until done. Format as conversation.md. Create manifest.json.
    Push to uerzer/nebula-backup under channels/SLUG/. Commit: backup SLUG DATE.'
- description: 'Backup workspace files batch 1: scripts, code, and task recipes'
  agent_id: agt_069a1bc8c3647e88800074fd7b0a4b1d
  agent_slug: nebula-channel-backup-archiver
  format_guide: 'From step 1 files, filter for paths starting with scripts/ code/
    or tasks/. For EACH file: read content with text_editor view, then push to uerzer/nebula-backup
    under files/ORIGINAL_PATH. For files over 100KB create a metadata placeholder
    instead. Commit: backup files/PATH DATE. Report total pushed and failures.'
- description: 'Backup workspace files batch 2: data, docs, and output files'
  agent_id: agt_069a1bc8c3647e88800074fd7b0a4b1d
  agent_slug: nebula-channel-backup-archiver
  format_guide: 'From step 1 files, filter for paths starting with data/ docs/ outputs/
    notes/ or images/. For EACH file: read content with text_editor view, then push
    to uerzer/nebula-backup under files/ORIGINAL_PATH. For files over 100KB create
    a metadata placeholder. Commit: backup files/PATH DATE. Report total and failures.'
- description: 'Backup workspace files batch 3: agent skills and remaining files'
  agent_id: agt_069a1bc8c3647e88800074fd7b0a4b1d
  agent_slug: nebula-channel-backup-archiver
  format_guide: 'From step 1 files, filter for paths starting with agents/ misc/ or
    any other non-tmp paths NOT covered by steps 6-7. For EACH file: read content
    with text_editor view, push to uerzer/nebula-backup under files/ORIGINAL_PATH.
    Commit: backup files/PATH DATE. Report total and failures.'
- description: Generate changelog and push updated README with full stats
  agent_id: agt_06989c177bdb790b80009f281ba948d2
  agent_slug: github-agent
  format_guide: 'Fetch current README.md from uerzer/nebula-backup. Using all step
    results compile stats. Update README with: title, last backup date, frequency
    Daily 8AM WET, total channels, total files, backup structure docs, changelog with
    latest entry plus previous entries preserved, channel index table, file index
    table. Commit: docs daily backup README DATE.'
---