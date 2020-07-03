# SSH Speedup
by OldCoder

Edit $HOME/.ssh/config
In the settings section at the top
That section usually reads as follows
```
host *
Protocol       2
Compression    no
```

Apparently Compression no is better
But if you use yes it may be suitable for you
Regardless the tip is
to add these 3 lines to that section:

```
ControlMaster  auto
ControlPath    /home/sally/%r@%h-%p
ControlPersist 1200
```

Where /home/sally is your home directory
Something like this may be better
```
mkdir -p $HOME/socket
```

Then

```
ControlPath    /home/sally/socket/%r@%h-%p
```

<Poikilos> "I assume it means something to do with not renegotiating
the connection all the time, by making something 'persistent'"

Exactly. Result: Instant ssh commands.
Only con:
Cons* plural:
* If things get confused or messed up, need to terminate all ssh connections and delete the contents of the $HOME/socket/ folder

and
* If you use ssh redirect to proxy to a VPS, and wish to change the redirect, must do the same thing

If you understand the cons, it's very nice.
Instant.
For ssh commands.

Try it out. I recommend `mkdir $HOME/socket`
to avoid cluttering $HOME w/sockets
then remember to adjust the relevant setting to use that directory
```
ControlPath    /home/sally/socket/%r@%h-%p
```
