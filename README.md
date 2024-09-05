# Pre-commit mirror for Prettier

> [!NOTE]
> This fork is a continuation of [github.com/pre-commit/mirrors-prettier](https://github.com/pre-commit/mirrors-prettier).

Mirror of the [Prettier](https://github.com/prettier/prettier) formatter for [pre-commit](https://github.com/pre-commit/pre-commit).

### Using prettier with pre-commit

Add this to your `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/ComPWA/prettier-pre-commit
    rev: v3.3.1
    hooks:
      - id: prettier
```

When using [Prettier plugins](https://prettier.io/docs/en/plugins), you'll need to declare them under [`additional_dependencies`](https://pre-commit.com/#config-additional_dependencies). For example:

```yaml
  - repo: https://github.com/ComPWA/prettier-pre-commit
    rev: v3.3.1
    hooks:
      - id: prettier
        additional_dependencies:
          - prettier@3.3.1
          - '@prettier/plugin-xml@3.4.1'
```

By default, all files are passed to `prettier`, if you want to limit the file list, adjust `types` / `types_or` / `files`:

```yaml
      - id: prettier
        types_or: [css, javascript]
```
