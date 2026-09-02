# Security Policy

## Reporting a vulnerability

Please do not report security vulnerabilities in public issues.

Open a private security advisory in the repository's **Security** tab. Include:

- A description of the vulnerability and its impact
- Steps to reproduce or a minimal proof of concept
- Affected versions
- Any suggested mitigation

You will receive an acknowledgement as soon as possible. Please allow time for investigation and coordinated disclosure before publishing details.

## Scope

`tuiify` runs decorated functions supplied by the application author. Treat function inputs and the functions themselves as trusted application code. Reports about arbitrary code execution through an intentionally supplied function are outside the package's threat model.
