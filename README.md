# TimescaleDB taxi data

This project contains supporting code for the TimescaleDB video on YouTube.

## Requirements

In order to use this project, you'll need to set up the following tools:

### TimescaleDB database

This project uses TimescaleDB as it's primary data store. There are a number
of ways to get a timescale DB instance up and running.

#### Timescale Managed

This is the easiest approach to get started, and it's free for 30 days. This
allows you to easily try timescale before commiting to any purchase or use case.

You can get the managed version of timescale on their [website](https://www.timescale.com/)

#### Timescale local

If you want to run it locally, you can do so by extending postgres. Timescale
have some great [documentation](https://docs.timescale.com/self-hosted/latest/install/)
on how to do that.

#### Timescale Docker

Finally, another great approach is to use docker. The
[documentation](https://docs.timescale.com/self-hosted/latest/install/installation-docker/)
providews instructions here as well. Be warned that if you're running docker
on a non linux machine, it will be slower due to having to run through a
hypervisor.

### Python3

Python3 is used as the primary language for downloading data and then
loading it into timescaleDB. The recommended version of python to use is
3.11.x or greater.

#### macOS

To install on macOS, one can use homebrew to do so using the following commands

```
$ brew install python
```

#### Arch Linux

```
$ sudo pacman -S python
```

### Debian

```
$ sudo apt install python
```

### psql

In the video we interact with the database using psql, which is a command line
tool provided by postgres.

#### macOS

To install it for macOS, you can use homebrew

```
$ brew install postgresql
```

#### Arch Linux

```
$ sudo pacman -S postgresql
```

### sqlx-cli

SQLx is used for database migrations. To install it, you can do so one of two
ways, depending on if you have rust installed on your system or not.

#### Cargo

```
$ cargo install sqlx-cli
```

#### macOS

```
$ brew install sqlx-cli
```

#### Arch Linux

```
$ sudo pacman -S sqlx-cli
```
