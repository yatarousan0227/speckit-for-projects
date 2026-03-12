"""Typer application and agent config."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import typer


@dataclass(frozen=True)
class AgentConfig:
    """Agent-specific output location and runtime expectation."""

    key: str
    name: str
    folder: str | None
    commands_subdir: str | None
    requires_cli: bool
    cli_command: str | None
    install_url: str | None
    wrapper_style: Literal["plain", "frontmatter"]

    def command_directory(self, project_dir: str, ai_commands_dir: str | None = None) -> str:
        """Resolve the command output directory for a project path."""
        if self.key == "generic":
            if ai_commands_dir is None:
                raise ValueError("--ai-commands-dir is required for generic")
            return ai_commands_dir
        if self.folder is None or self.commands_subdir is None:
            raise ValueError(f"agent configuration incomplete for {self.key}")
        return f"{project_dir.rstrip('/')}/{self.folder}{self.commands_subdir}"


AI_ASSISTANT_ALIASES: dict[str, str] = {
    "kiro": "kiro-cli",
}

AGENT_SKILLS_DIR_OVERRIDES: dict[str, str] = {
    "codex": ".agents/skills",
}

DEFAULT_SKILLS_DIR = ".agents/skills"

AGENT_CONFIGS: dict[str, AgentConfig] = {
    "claude": AgentConfig(
        "claude",
        "Claude Code",
        ".claude/",
        "commands",
        True,
        "claude",
        "https://docs.anthropic.com/en/docs/claude-code/setup",
        "frontmatter",
    ),
    "gemini": AgentConfig(
        "gemini",
        "Gemini CLI",
        ".gemini/",
        "commands",
        True,
        "gemini",
        "https://github.com/google-gemini/gemini-cli",
        "frontmatter",
    ),
    "copilot": AgentConfig(
        "copilot", "GitHub Copilot", ".github/", "agents", False, None, None, "frontmatter"
    ),
    "cursor-agent": AgentConfig(
        "cursor-agent", "Cursor", ".cursor/", "commands", False, None, None, "frontmatter"
    ),
    "qwen": AgentConfig(
        "qwen",
        "Qwen Code",
        ".qwen/",
        "commands",
        True,
        "qwen",
        "https://github.com/QwenLM/qwen-code",
        "frontmatter",
    ),
    "opencode": AgentConfig(
        "opencode",
        "opencode",
        ".opencode/",
        "command",
        True,
        "opencode",
        "https://opencode.ai",
        "frontmatter",
    ),
    "codex": AgentConfig(
        "codex",
        "Codex CLI",
        ".codex/",
        "prompts",
        True,
        "codex",
        "https://github.com/openai/codex",
        "plain",
    ),
    "windsurf": AgentConfig(
        "windsurf", "Windsurf", ".windsurf/", "workflows", False, None, None, "frontmatter"
    ),
    "kilocode": AgentConfig(
        "kilocode", "Kilo Code", ".kilocode/", "workflows", False, None, None, "frontmatter"
    ),
    "auggie": AgentConfig(
        "auggie",
        "Auggie CLI",
        ".augment/",
        "commands",
        True,
        "auggie",
        "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "frontmatter",
    ),
    "roo": AgentConfig("roo", "Roo Code", ".roo/", "commands", False, None, None, "frontmatter"),
    "codebuddy": AgentConfig(
        "codebuddy",
        "CodeBuddy",
        ".codebuddy/",
        "commands",
        True,
        "codebuddy",
        "https://www.codebuddy.ai/cli",
        "frontmatter",
    ),
    "amp": AgentConfig(
        "amp",
        "Amp",
        ".agents/",
        "commands",
        True,
        "amp",
        "https://ampcode.com/manual#install",
        "frontmatter",
    ),
    "shai": AgentConfig(
        "shai",
        "SHAI",
        ".shai/",
        "commands",
        True,
        "shai",
        "https://github.com/ovh/shai",
        "frontmatter",
    ),
    "kiro-cli": AgentConfig(
        "kiro-cli",
        "Kiro CLI",
        ".kiro/",
        "prompts",
        True,
        "kiro",
        "https://kiro.dev/docs/cli/",
        "plain",
    ),
    "agy": AgentConfig(
        "agy", "Antigravity", ".agent/", "workflows", False, None, None, "frontmatter"
    ),
    "bob": AgentConfig("bob", "IBM Bob", ".bob/", "commands", False, None, None, "frontmatter"),
    "qodercli": AgentConfig(
        "qodercli",
        "Qoder CLI",
        ".qoder/",
        "commands",
        True,
        "qodercli",
        "https://qoder.com/cli",
        "frontmatter",
    ),
    "vibe": AgentConfig(
        "vibe",
        "Mistral Vibe",
        ".vibe/",
        "prompts",
        True,
        "vibe",
        "https://github.com/mistralai/mistral-vibe",
        "frontmatter",
    ),
    "generic": AgentConfig("generic", "Generic Agent", None, None, False, None, None, "plain"),
}


def resolve_ai_assistant(ai_assistant: str | None) -> str | None:
    """Resolve a user-facing assistant value to the canonical config key."""
    if ai_assistant is None:
        return None
    return AI_ASSISTANT_ALIASES.get(ai_assistant, ai_assistant)


def _build_ai_assistant_help() -> str:
    """Build help text from canonical agent config and supported aliases."""
    supported_values = ", ".join(sorted(AGENT_CONFIGS))
    base_help = f"AI assistant to configure. Supported values: {supported_values}."
    if not AI_ASSISTANT_ALIASES:
        return base_help
    alias_phrases = [
        f"Use '{alias}' as an alias for '{target}'."
        for alias, target in sorted(AI_ASSISTANT_ALIASES.items())
    ]
    return base_help + " " + " ".join(alias_phrases)


AI_ASSISTANT_HELP = _build_ai_assistant_help()


def create_app() -> typer.Typer:
    """Create the root Typer app."""
    return typer.Typer(
        add_completion=False,
        help="SpecKit for Projects scaffold setup and environment checks.",
        no_args_is_help=True,
    )
