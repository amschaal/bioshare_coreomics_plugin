# bioshare_coreomics_plugin
Must ensure that 'bioshare' is in PLUGINS setting, and a couple of other settings are added:
``` Python
PLUGINS = ['bioshare']
BIOSHARE_SETTINGS = {
    'URL':'https://bioshare.mydomain.com',
    'DEFAULT_FILESYSTEM': 1
}
```
