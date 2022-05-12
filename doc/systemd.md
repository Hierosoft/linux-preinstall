# systemd
## Startup order
In the "[Unit]" section, the following:
```
Wants=network-online.target
After=network-online.target
```
is better than
```
Wants=network.target
After=network.target
```
if a connection is required.
