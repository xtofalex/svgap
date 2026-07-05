# Security

SV-Gap processes untrusted generated RTL by invoking external EDA tools. Treat
candidate files as untrusted input and run evaluations in an isolated container
or disposable worker. The v0.1 local runner does not provide a security sandbox.

Model generation and RTL evaluation should be separate trust domains. Generate
responses in the environment that holds model credentials, then evaluate the
saved responses in a network-disabled disposable worker with no inherited
credentials, read-only task inputs, a dedicated writable output volume, and
resource limits. The container recipe in
`docs/evaluate-your-model.md` demonstrates this separation.

Do not run contributed functional commands on a workstation containing secrets.
Public task packs must not contain credentials, proprietary RTL, or unreviewed
shell commands.

Do not publish exploit details for active vulnerabilities. Report them privately
to project maintainer Shraddha S at `shsridhar@nvidia.com`.
