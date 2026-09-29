#!/usr/bin/env python3
"""Validate local Markdown targets and required architecture coverage."""
from pathlib import Path
from urllib.parse import unquote
import re
import sys
root=Path(__file__).resolve().parents[1]
files=list(root.rglob('*.md'))
required=['architecture/component-model.md','architecture/service-contracts.md','architecture/admin-supervisor-agent.md','architecture/digital-outbound.md','architecture/recording-transcription-quality.md','architecture/data-reporting-wfm.md','migration/migration-strategy.md','validation/architecture-acceptance.md','architecture/routing-policy-engine.md','architecture/call-leg-ownership.md','call-flows/feature-scenarios.md','validation/routing-and-leg-acceptance.md','architecture/capability-map.md','architecture/customer-journey-case.md','architecture/automation-ai-knowledge.md','architecture/performance-management.md','architecture/developer-platform.md','implementation/build-sequence.md','architecture/deployment-blueprint.md','call-flows/cross-channel-journey.md','validation/coverage-review.md']
issues=[];count=0
for name in required:
    if not (root/name).is_file():issues.append(f'missing required domain: {name}')
for file in files:
    text=file.read_text()
    for match in re.finditer(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',text):
        url=unquote(match.group(1).split(' ')[0].strip('<>'))
        if not url or re.match(r'^(https?:|mailto:|#)',url):continue
        count+=1
        target=(file.parent/url.split('#')[0]).resolve()
        if not target.is_relative_to(root) or not target.exists():issues.append(f'{file.relative_to(root)}: {url}')
    if text.count('```')%2:issues.append(f'{file.relative_to(root)}: unmatched code fence')
print(f'Checked {len(files)} Markdown files and {count} local links; {len(issues)} issues.')
for issue in issues:print('ERROR:',issue)
sys.exit(bool(issues))
