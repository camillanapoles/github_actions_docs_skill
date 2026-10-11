---
title: Expressions
description: You can evaluate expressions in workflows and actions.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/concepts/workflows-and-actions/expressions.md
captured: '2026-10-11'
section: Concepts / Workflows and actions
---

# Expressions

_You can evaluate expressions in workflows and actions._

## About expressions

You can use expressions to programmatically set environment variables in workflow files and access contexts. An expression can be any combination of literal values, references to a context, or functions. You can combine literals, context references, and functions using operators. For more information about contexts, see [Contexts reference](../../reference/workflows-and-actions/contexts.md).

Expressions are commonly used with the conditional `if` keyword in a workflow file to determine whether a step should run. When an `if` conditional is `true`, the step will run.

You need to use specific syntax to tell GitHub to evaluate an expression rather than treat it as a string.

`${{ <expression> }}`

> [!NOTE]
> The exception to this rule is when you are using expressions in an `if` clause, where, optionally, you can usually omit `${{` and `}}`. For more information about `if` conditionals, see [Workflow syntax for GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idif#jobsjob_idif).

> [!WARNING]
> When creating workflows and actions, you should always consider whether your code might execute untrusted input from possible attackers. Certain contexts should be treated as untrusted input, as an attacker could insert their own malicious content. For more information, see [Secure use reference](../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks#good-practices-for-mitigating-script-injection-attacks).

### Example setting an environment variable

```yaml
env:
  MY_ENV_VAR: ${{ <expression> }}
```

## Further reading

For technical reference information about expressions you can use in workflows and actions, see [Evaluate expressions in workflows and actions](../../reference/workflows-and-actions/expressions.md).
