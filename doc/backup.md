# Backup

A backup is a second copy of your files. Most people don't find out how important that is until they lose all of their work for their business or lose a book they've been writing or something else that involves many hours of work.

I've been asked many times, "How often should I back up?" The best rule of thumb I've heard is "backup anything you don't want to lose." Therefore, if you don't want to lose more than a day's work, backup every day, etc. If you can't afford even that, use some type of live synchronization such as Nextcloud.

Backup can be accomplished easily by installing BackupGoNow from [BackupGoNow releases](https://github.com/poikilos/BackupGoNow/releases) and running it once in a while.
- It requires a flash drive or other external drive. Depending on what you do, you may even want a 3 TB external drive or whatever drive is equal to or larger than your main drive.
- BackupGoNow keeps old copies of files in dated directories, so no special drive format is necessary. The most recent backup is a replica of the source drive(s) by volume name (or by letter on Windows).
- See also: The readme at the [BackupGoNow](https://github.com/poikilos/BackupGoNow) repository.

## Advanced options
The following programs are mostly for people who are in IT or are
accustomed to the CLI (Command-Line Interface) of Linux.

### borgmatic
I've also had success with borgmatic (only borg is required on the server, but borgmatic makes some of the client configuration easier).

### rsnapshot
For automation and generally doing a backup that is neatly accessible via dated folders, OldCoder recommends [rsnapshot](https://github.com/rsnapshot/rsnapshot) (See [INSTALL](https://github.com/rsnapshot/rsnapshot/blob/master/INSTALL.md))
- The dated folders are always available as if they were real folders but don't take up unnecessary space since rsnapshot uses hardlinks.

