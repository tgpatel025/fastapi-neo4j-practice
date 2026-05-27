# Agents

This repository does not currently include custom agent implementations.

## Guidelines

- Document agent purpose, ownership, and expected workflows.
- Keep agent definitions focused and easy to understand.
- Store agent configuration information in the repository, but keep secrets out of version control.
- Use `README.md` and `AGENTS.md` to explain how contributors should interact with agents.

## Rules

- Agent documentation must be reviewed together with the related code or workflow change.
- Any new agent must include owner and usage details in `AGENTS.md`.
- Sensitive data must be managed outside repository source files, using environment variables or secure secret stores.
- Maintain a clear link between agents and the feature or automation they support.
