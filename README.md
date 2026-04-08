# Shepherd plugin Postgres

[![license: AGPL v3](https://img.shields.io/badge/license-AGPL%20v3-blue)](LICENSE)
[![Commercial License Available](https://img.shields.io/badge/license-Commercial-orange)](LICENSE-COMMERCIAL)
[![codecov](https://codecov.io/gh/MoonyFringers/shepherd-plugin-postgres/branch/main/graph/badge.svg)](https://codecov.io/gh/MoonyFringers/shepherd-plugin-postgres)

## Plugin packaging and install

Shepherd installs plugins from archives containing `plugin.yaml` and the plugin
package.

From the repository root:

```bash
tar -czf postgres-plugin.tar.gz plugin.yaml -C src postgres_plugin
```

Then install with Shepherd:

```bash
shepctl plugin install postgres-plugin.tar.gz
shepctl plugin enable postgres
```
