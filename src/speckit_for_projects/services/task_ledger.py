"""Helpers for preserving mutable execution fields in tasks.md."""

from __future__ import annotations

import re

TASK_HEADING_PATTERN = re.compile(r"^###\s+(TASK-\d{3})\b.*$", re.MULTILINE)
LEVEL2_HEADING_PATTERN = re.compile(r"^##\s+", re.MULTILINE)
EXECUTION_STATUS_MARKER = "#### Execution Status"
ARCHIVED_HISTORY_HEADING = "## Archived Execution History"


def merge_task_execution_history(new_content: str, existing_content: str) -> str:
    """Merge generated tasks with existing execution state by task ID."""
    new_tasks, new_postamble = _extract_tasks_and_postamble(new_content)
    existing_tasks, existing_postamble = _extract_tasks_and_postamble(existing_content)
    if not new_tasks:
        return new_content

    existing_by_id = {task.task_id: task for task in existing_tasks}
    merged_content = new_content
    merged_segments: list[tuple[TaskBlock, str]] = []
    for task in new_tasks:
        existing_task = existing_by_id.get(task.task_id)
        replacement = task.raw
        if existing_task is not None:
            existing_mutable = _mutable_suffix(existing_task.raw)
            if existing_mutable is not None:
                replacement = _replace_mutable_suffix(task.raw, existing_mutable)
        merged_segments.append((task, replacement))

    for task, replacement in reversed(merged_segments):
        merged_content = (
            merged_content[: task.start] + replacement + merged_content[task.end :]
        )

    archived_tasks = _merge_archived_tasks(existing_tasks, new_tasks, existing_postamble)
    merged_content = _replace_archived_section(merged_content, new_postamble, archived_tasks)
    return merged_content


class TaskBlock:
    """One TASK section with its raw markdown span."""

    def __init__(self, task_id: str, start: int, end: int, raw: str):
        self.task_id = task_id
        self.start = start
        self.end = end
        self.raw = raw


def _extract_tasks_and_postamble(content: str) -> tuple[list[TaskBlock], str]:
    matches = list(TASK_HEADING_PATTERN.finditer(content))
    if not matches:
        return [], ""

    level2_matches = list(LEVEL2_HEADING_PATTERN.finditer(content))
    task_blocks: list[TaskBlock] = []
    first_task_start = matches[0].start()
    postamble_start = len(content)

    for index, match in enumerate(matches):
        start = match.start()
        next_task_start = matches[index + 1].start() if index + 1 < len(matches) else None
        next_level2_start = _next_level2_after(level2_matches, start + 1)
        candidate_endings = [
            value
            for value in (next_task_start, next_level2_start, len(content))
            if value is not None and value > start
        ]
        end = min(candidate_endings)
        if index == len(matches) - 1 and next_level2_start is not None:
            postamble_start = next_level2_start
        task_blocks.append(TaskBlock(match.group(1), start, end, content[start:end]))

    if postamble_start < first_task_start:
        postamble_start = len(content)
    return task_blocks, content[postamble_start:]


def _next_level2_after(matches: list[re.Match[str]], position: int) -> int | None:
    for match in matches:
        if match.start() >= position:
            return match.start()
    return None


def _mutable_suffix(task_content: str) -> str | None:
    marker_index = task_content.find(EXECUTION_STATUS_MARKER)
    if marker_index < 0:
        return None
    return task_content[marker_index:]


def _replace_mutable_suffix(task_content: str, mutable_suffix: str) -> str:
    marker_index = task_content.find(EXECUTION_STATUS_MARKER)
    if marker_index < 0:
        return task_content.rstrip() + "\n\n" + mutable_suffix.lstrip()
    return task_content[:marker_index] + mutable_suffix


def _merge_archived_tasks(
    existing_tasks: list[TaskBlock], new_tasks: list[TaskBlock], existing_postamble: str
) -> list[str]:
    archived_blocks = _extract_archived_task_blocks(existing_postamble)
    archived_ids = {
        match.group(1)
        for match in (TASK_HEADING_PATTERN.search(block) for block in archived_blocks)
        if match is not None
    }
    new_ids = {task.task_id for task in new_tasks}
    removed_tasks = [
        task.raw.strip()
        for task in existing_tasks
        if task.task_id not in new_ids and task.task_id not in archived_ids
    ]
    return archived_blocks + removed_tasks


def _extract_archived_task_blocks(postamble: str) -> list[str]:
    heading_index = postamble.find(ARCHIVED_HISTORY_HEADING)
    if heading_index < 0:
        return []
    archive_section = postamble[heading_index + len(ARCHIVED_HISTORY_HEADING) :].strip()
    archived_tasks, _ = _extract_tasks_and_postamble(archive_section)
    return [task.raw.strip() for task in archived_tasks]


def _replace_archived_section(
    merged_content: str, new_postamble: str, archived_tasks: list[str]
) -> str:
    if ARCHIVED_HISTORY_HEADING in merged_content:
        prefix, _, _ = merged_content.partition(ARCHIVED_HISTORY_HEADING)
        merged_content = prefix.rstrip() + "\n"

    base_postamble = new_postamble
    if ARCHIVED_HISTORY_HEADING in base_postamble:
        base_postamble = base_postamble.partition(ARCHIVED_HISTORY_HEADING)[0].rstrip() + "\n"

    merged_content = merged_content.rstrip() + "\n\n" + base_postamble.strip() + "\n"
    if not archived_tasks:
        return merged_content.rstrip() + "\n"

    archived_body = "\n\n".join(archived_tasks)
    return (
        merged_content.rstrip()
        + "\n\n"
        + ARCHIVED_HISTORY_HEADING
        + "\n\n"
        + archived_body
        + "\n"
    )
