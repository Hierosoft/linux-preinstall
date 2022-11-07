# Slack

Slack downloads for linux are available at: <https://slack.com/intl/en-gb/downloads/linux>


## Slack GitHub App
Slack provides a GitHub app that Slack offers to install when you add a post that has any link to GitHub.

After installing and posting another GitHub link, it provides the following documentation:

> To see rich preview of links from private repositories, connect to your GitHub account using
> `/github signin`. You can mute the rich previews by running `/github settings`.

It also asks at this time to Connect to a GitHub account. After doing so, the information under "Subscribe to repositories" and "Create and edit issues" below appears.

### Subscribe to repositories
- Subscribe `/github subscribe owner/repo`
- Unsubscribe `/github unsubscribe owner/repo`
- Show subscriptions `/github subscribe list`

### Create and edit issues
- Create a new issue `/github open owner/repo`
- Close an issue as completed `/github close [issue link]`
- Close an issue as not planned `/github close [issue link] reason:"not planned"`
- Reopen an issue `/github reopen [issue link]`

### Advanced subscription commands
Under the "Subscribe to repositories" section is a button that says "Advanced subscription commands". Clicking it shows the following:

#### Configure subscriptions
You can customize your notifications by subscribing to activity that is relevant to your Slack channel.
- `/github subscribe owner/repo [feature]`
- `/github unsubscribe owner/repo [feature]`

Disabled by default and can be enabled\
`reviews` `comments` `branches` `discussions`

Enabled by default and can be disabled\
`issues` `pulls` `commits` `releases` `deployments`

#### Branch filters for commit
Branch filters allow filtering commit notifications. By default when you subscribe for commits feature, you will get notifications for your default branch (i.e. main). However, you can choose to filter on a specific branch, or a pattern of branches or all branches.
- `/github subscribe owner/repo commits:"mybranch/*"`

#### Label filters for issues, pull requests
Filter incoming events based on the user provided list of labels.\
`/github subscribe owner/repo +label:"my label"`\
`/github unsubscribe owner/repo +label:"my label"`

#### List active subscriptions
List all active subscriptions in a channel\
`/github subscribe list`

List all active subscriptions with subscription features\
`/github subscribe list features`

### Caveats
- `/github settings` makes a "Mute" button appear to control whether rich previews for private repos will be shown.
  - The rich previews don't seem to work on an account with lower privs


