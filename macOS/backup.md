# Backup macOS

## Time Machine
Time Machine requires HFS+ or APFS (designed for solid state drives; requires 10.15

## Non-Time-Machine Backup

### Exclusions

Exclude list for macOS X (Jan 2015)
- updated March 4, 2015 (added Windows excludes):
  ```
--exclude='$RECYCLE.BIN' --exclude='$Recycle.Bin' --exclude='.AppleDB' --exclude='.AppleDesktop' --exclude='.AppleDouble' --exclude='.com.apple.timemachine.supported' --exclude='.dbfseventsd' --exclude='.DocumentRevisions-V100*' --exclude='.DS_Store' --exclude='.fseventsd' --exclude='.PKInstallSandboxManager' --exclude='.Spotlight*' --exclude='.SymAV*' --exclude='.symSchedScanLockxz' --exclude='.TemporaryItems' --exclude='.Trash*' --exclude='.vol' --exclude='.VolumeIcon.icns' --exclude='Desktop DB' --exclude='Desktop DF' --exclude='hiberfil.sys' --exclude='lost+found' --exclude='Network Trash Folder' --exclude='pagefile.sys' --exclude='Recycled' --exclude='RECYCLER' --exclude='System Volume Information' --exclude='Temporary Items' --exclude='Thumbs.db'
```
