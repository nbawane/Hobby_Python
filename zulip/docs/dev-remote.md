# Developing on a remote machine

The Zulip developer environment works well on remote virtual machines. This can
be a good alternative for those with poor network connectivity or who have
limited storage/memory on their local machines.

We recommend giving the Zulip development environment its own virtual
machine, running Ubuntu 14.04 or
16.04, with at least 2GB of memory. If the Zulip development
environment will be the only thing running on the remote virtual
machine, we recommend installing
[directly][install-direct]. Otherwise, we recommend the
[Vagrant][install-vagrant] method so you can easily uninstall if you
need to.

## Connecting to the remote environment

The best way to connect to your server is using the command line tool `ssh`.

* On macOS and Linux/UNIX, `ssh` is a part of Terminal.
* On Windows, `ssh` comes with [Bash for Git][git-bash].

Open *Terminal* or *Bash for Git*, and connect with the following:

```
$ ssh username@host
```

If you have poor internet connectivity, we recommend using
[Mosh](https://mosh.org/) as it is more reliable over slow or unreliable
networks.

## Setting up the development environment

After you have connected to your remote server, you need to install the
development environment.

If the Zulip development environment will be the only thing running on
the remote virtual machine, we recommend installing
[directly][install-direct]. Otherwise, we recommend the
[Vagrant][install-vagrant] method so you can easily uninstall if you
need to.

## Running the development server

Once you have set up the development environment, you can start up the
development instance of Zulip with the following command in the directory where
you cloned Zulip:

```
./tools/run-dev.py --interface=''
```

This will start up the Zulip server on port 9991. You can then
navigate to `http://<REMOTE_IP>:9991` and you should see something like
this screenshot of the Zulip development environment:

![Image of Zulip development
environment](images/zulip-dev.png)

You can [port
forward](https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding) using
ssh instead of running the development environment on an exposed interface.

For more information, see [Using the development
environment][rtd-using-dev-env].

## Making changes to code on your remote development server

To see changes on your remote development server, you need to do one of the following:

* [Edit locally](#editing-locally): Clone Zulip code to your computer and
  then use your favorite editor to make changes. When you want to see changes
  on your remote Zulip development instance, sync with Git.
* [Edit remotely](#editing-remotely): Edit code directly on your remote
  Zulip development instance using a [Web-based IDE](#web-based-ide) (recommended for
  beginners) or a [command line editor](#command-line-editors).

#### Editing locally

If you want to edit code locally install your favorite text editor. If you
don't have a favorite, here are some suggestions:

* [atom](https://atom.io/)
* [emacs](https://www.gnu.org/software/emacs/)
* [vim](http://www.vim.org/)
* [spacemacs](https://github.com/syl20bnr/spacemacs)
* [sublime](https://www.sublimetext.com/)

Next, follow our [Git and GitHub Guide](git-guide.html) to clone and configure
your fork of zulip on your local computer.

Once you have cloned your code locally, you can get to work.

##### Syncing changes

The easiest way to see your changes on your remote development server
is to **push them to GitHub** and them **fetch and merge** them from
the remote server.

For more detailed instructions about how to do this, see our [Git & GitHub
Guide][rtd-git-guide]. In brief, the steps are as follows.

On your **local computer**:

1. Open *Terminal* (macOS/Linux) or *Git for BASH*.
2. Change directory to where you cloned Zulip (e.g. `cd zulip`).
3. Use `git add` and `git commit` to stage and commit your changes (if you
   haven't already).
4. Push your commits to GitHub with `git push origin branchname`.

Be sure to replace `branchname` with the name of your actual feature branch.

Once `git push` has completed successfully, you are ready to fetch the commits
from your remote development instance:

1. In *Terminal* or *Git BASH*, connect to your remote development
   instance with `ssh user@host`.
2. Change to the zulip directory (e.g., `cd zulip`).
3. Fetch new commits from GitHub with `git fetch origin`.
4. Change to the branch you want to work on with `git checkout branchname`.
5. Merge the new commits into your branch with `git merge origin/branchname`.

#### Editing remotely

##### Web-based IDE

If you are relatively new to working on the command line, or just want to get
started working quickly, we recommend web-based IDE
[Codeanywhere][codeanywhere].

To setup Codeanywhere for Zulip:

1. Create a [Codeanywhere][codeanywhere] account and log in.
2. Create a new **SFTP-SSH** project. Use *Public key* for authentication.
3. Click **GET YOUR PUBLIC KEY** to get the new public key that
   Codeanywhere generates when you create a new project. Add this public key to
   `~/.ssh/authorized_keys` on your remote development instance.
4. Once you've added the new public key to your remote development instance, click
   *CONNECT*.

Now your workspace should look similar this:
![Codeanywhere workspace][img-ca-workspace]

##### Command line editors

Another way to edit directly on the remote development server is with
a command line text editor on the remote machine.

Two editors often available by default on Linux systems are:

* **Nano**: A very simple, beginner-friendly editor. However, it lacks a lot of
  features useful for programming, such as syntax highlighting, so we only
  recommended it for quick edits to things like configuration files. Launch by
  running command `nano <filename>`. Exit by pressing *control-X*.

* **[Vim](http://www.vim.org/)**: A very powerful editor that can take a while
  to learn. Launch by running `vim <filename>`. Quit Vim by pressing *escape*,
  typing `:q`, and then pressing *return*. Vim comes with a program to learn it
  called `vimtutor` (just run that command to start it).

Other options include:

* [emacs](https://www.gnu.org/software/emacs/)
* [spacemacs](https://github.com/syl20bnr/spacemacs)

#### Next steps

Next, read the following to learn more about developing for Zulip:

* [Git & GitHub Guide][rtd-git-guide]
* [Using the Development Environment][rtd-using-dev-env]
* [Testing][rtd-testing]

[install-direct]: dev-setup-non-vagrant.html#installing-directly-on-ubuntu
[install-generic]: dev-setup-non-vagrant.html#installing-manually-on-linux
[install-vagrant]: dev-env-first-time-contributors.html
[rtd-git-guide]: git-guide.html
[rtd-using-dev-env]: using-dev-environment.html
[rtd-testing]: testing.html
[git-bash]: https://git-for-windows.github.io/
[codeanywhere]: https://codeanywhere.com/
[img-ca-settings]: images/codeanywhere-settings.png
[img-ca-workspace]: images/codeanywhere-workspace.png
