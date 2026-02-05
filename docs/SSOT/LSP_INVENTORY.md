# LSP Inventory (SSOT)

Last updated: 2026-02-05

## Runtime Configuration
Source: `~/.config/opencode/opencode.json`

- No explicit LSP servers configured in runtime config.
- LSP availability depends on OpenCode defaults and installed toolchains.
 - Auto‑download can be disabled with `OPENCODE_DISABLE_LSP_DOWNLOAD=true`.

## References
- OpenCode LSP docs: https://opencode.ai/docs/lsp/

## Built‑in LSPs (OpenCode default)
See OpenCode LSP docs for the full list and requirements:
https://opencode.ai/docs/lsp/

Quick list (from OpenCode docs):
- astro (.astro) — auto‑install
- bash (.sh, .bash, .zsh, .ksh)
- clangd (C/C++) — auto‑install
- csharp (.cs) — .NET SDK
- clojure-lsp (.clj, .cljs, .cljc, .edn)
- dart (.dart)
- deno (.ts/.tsx/.js/.jsx/.mjs) — deno.json detection
- elixir-ls (.ex, .exs)
- eslint (.ts/.tsx/.js/.jsx/.mjs/.cjs/.mts/.cts/.vue)
- fsharp (.fs, .fsi, .fsx, .fsscript)
- gleam (.gleam)
- gopls (.go)
- hls (.hs, .lhs)
- jdtls (.java) — Java 21+
- kotlin-ls (.kt, .kts) — auto‑install
- lua-ls (.lua) — auto‑install
- nixd (.nix)
- ocaml-lsp (.ml, .mli)
- oxlint (.ts/.tsx/.js/.jsx/.mjs/.cjs/.mts/.cts/.vue/.astro/.svelte)
- php intelephense (.php) — auto‑install
- prisma (.prisma)
- pyright (.py, .pyi)
- ruby-lsp (rubocop) (.rb, .rake, .gemspec, .ru)
- rust‑analyzer (.rs)
- sourcekit‑lsp (.swift, .objc, .objcpp)
- svelte (.svelte) — auto‑install
- terraform (.tf, .tfvars) — auto‑install
- tinymist (.typ, .typc) — auto‑install
- typescript (.ts/.tsx/.js/.jsx/.mjs/.cjs/.mts/.cts)
- vue (.vue)
- yaml-ls (.yaml, .yml) — auto‑install
- zls (.zig, .zon)

## Next Steps
- Decide which LSP servers to enable (per language)
- Document per-language LSP settings once configured
