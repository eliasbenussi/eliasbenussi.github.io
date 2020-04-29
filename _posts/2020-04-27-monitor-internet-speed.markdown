---
layout: post
title:  "Programmatically monitor your Internet speed"
date:   2020-04-27 18:30:00 +0000
categories: jekyll update
---

I decided to monitor my internet speed over the course of the past few days, and had fun
figuring out how to do so programmatically. I decided to document the steps I followed.
I put all the code here: <https://github.com/eliasbenussi/speedtest>

First thing you want to do is to create a folder that will contain all the files we will need.
I stored everything under `~/Development/speedtest`. For simplicity I suggest to do the same
(execute `mkdir -p ~/Development/speedtest` in your terminal after opening it). If you are
confident with the command line and a bit of python feel free to choose your own folder, but beware
that you might have to make changes to the code/commands I will show below.

I did all of this on a macbook. I am sure you can make this work on Unix systems, potentially with
some tweaks. Windows is mostly a mistery to me.

Also open a terminal window and keep it there. We are going to use it quite a lot.


### Prerequisites

I assume below you know how to install packages and deal with python installations. If that's
not the case feel free to follow the opinionated steps below. I won't go into details as it's
beyond the scope of this post, I will just help you hack your way to victory for now.

First, install `brew` following the instructions at: <https://brew.sh/>

Then install `pyenv` and `virtualenv`. I recommend reading this blog  <https://acroz.dev/2016/12/21/pyenv/>.

Then setup your global environment. I assume you called it `global` below. If not just modify the
commands accordingly

### How to perform a speed test

I used `speedtest-cli` to perform my speed tests. Run `pip install speedtest-cli` to install it.
Like most command line tools executing `speedtest -h` shows some information on how to use the tool.
I suggest to play around with it a bit to explore what the options are and what you can do with it.
In the end I decided `speedtest --single --secure --json` gave me what I needed.

Next we want to be able to save the output to a file. Not only that, we want to be able to keep
adding the output of multiple calls of that command to the same file, to create a log. We do some
with the `>>` command.

First let's move to the directory we created with `cd ~/Development/speedtest` and create a `raw`
directory calling `mkdir raw`.

Then try executing:

```
date >> raw/speeds.json; speedtest --single --secure --json >> raw/speeds.json; echo -e "\n" >> raw/speeds.json
```

You can execute it two or three times and see that logs keep being added to that file.


### Perform regular speed tests

The next step is to be able to execute the above command every ten minutes (or however often you'd
like). We will use `crontab`, a tool to execute jobs on a schedule. Run `man crontab` to get more
information on how to use `crontab` and what it can do.
The format it takes for specifying jobs and schedule is: `<cron expression> <command>`. You can learn
about cron expressions, but they are a bit tricky and it's good to validate them. Personally I like
to use <https://crontab.guru/> to check (or maybe even generate ;) ) my expressions before using them.
To execute something every ten minutes the expression is `*/10 * * * *`.

The command we want to execute is similar to what we have been executing up to now, except that we
will use full instead of relative paths, to make sure it can be executed from whatever positions in
the file tree:

```
date >> ~/Development/speedtest/raw/speeds.json; ~/.pyenv/versions/global/bin/speedtest --single --secure --json >> ~/Development/speedtest/raw/speeds.json; echo -e "\n" >> ~/Development/speedtest/raw/speeds.json
```

Now that we know both the cron expression and the command, create a file in the `speedtest`
directory and call it `cronjobs-speedtest`, with this content:

```
*/10 * * * * date >> ~/Development/speedtest/raw/speeds.json; ~/.pyenv/versions/deleteme-3.7.0/bin/speedtest --single --secure --json >> ~/Development/speedtest/raw/speeds.json; echo -e "\n" >> ~/Development/speedtest/raw/speeds.json
```

Then in the terminal, in the `speedtest` directory, run `crontab cronjobs-speedtest` to establish a
scheduled job with the content of that file. You can run `crontab -l` to check the current schedule
after. You might want to test it initially with higher frequency, say once a minute: just find the
cron expression using <https://crontab.guru/>, update the file and then run `crontab cronjobs-speedtest` again.


### Detect low speed:

This is great! We are now collecting the data we are interested in. However this will soon become a
lot to read, and it will accumulate in this single file making it hard to extract the information
you are actually interested in: what is my average upload and download speed in a day and in what
occasions was it especially low?

Here I provide the script I am using to parse through the data in `raw/speeds.json` and convert it
into human readable format. I won't go much into details other than saying it's a quick hack
to get the aforementioned information, and save it into into a `history` directory, using the date
as the file name.

So firstly in your terminal under `speedtest` create a `history` directory like you did before.
Then copy the following code in a file called `calculate-speed-statistics.py`:

{% highlight python %}
import os
import json
from datetime import datetime


HOME = os.getenv("HOME")
RAW_DATA = HOME + "/Development/speedtest/raw/speeds.json"


def read_raw_speeds():
    with open(RAW_DATA) as f:
        lines = f.read().splitlines()

    measurements = {}
    key = None
    for i, l in enumerate(lines):
        if i % 4 == 0:
            # It's a date
            key = l
        if i % 4 == 1:
            # It's an entry
            d = json.loads(l)
            download = float("%.5g" % (d["download"] / 10 ** 6))
            upload = float("%.5g" % (d["upload"] / 10 ** 6))
            measurements[key] = (download, upload)

    return measurements


def find_mean_speed(measurements):
    downloads, uploads = zip(*measurements.values())

    mean_download = sum(downloads) / len(downloads)
    mean_upload = sum(uploads) / len(uploads)

    mean_speeds = [
        "Download average speed is: {}Mbit/s".format(mean_download),
        "Upload average speed is: {}Mbit/s".format(mean_upload),
    ]

    return mean_speeds


def find_all_breaches(measurements):
    breaches = []
    for date, (download, upload) in measurements.items():
        if download < 50 and upload < 7:
            breaches.append(
                "{}: Breach with download at {}Mbit/s and upload at {}Mbit/s".format(
                    date, download, upload
                )
            )
        elif download < 50:
            breaches.append(
                "{}: Breach with download at {}Mbit/s".format(date, download)
            )
        elif upload < 7:
            breaches.append("{}: Breach with upload at {}Mbit/s".format(date, upload))

    return breaches


def write_history(mean_speeds, all_breaches):
    history_file = HOME + "/Development/speedtest/history/" + str(datetime.now())

    with open(history_file, "w") as outfile:
        for ms in mean_speeds:
            outfile.write(ms + "\n")

        outfile.write("\n")

        for ab in all_breaches:
            outfile.write(ab + "\n")


def main():
    measurements = read_raw_speeds()

    mean_speeds = find_mean_speed(measurements)
    all_breaches = find_all_breaches(measurements)

    write_history(mean_speeds, all_breaches)


if __name__ == "__main__":
    main()
{% endhighlight %}

If you manually run `python calculate-speed-statistics.py` you will see it creates a file under
`history` with a date as file name that contains the information we wanted.

Now we want to set a schedule to run this code every day at 23:55. To do so simply add this new line
to the `cronjobs-speedtest` file:

```
55 23 * * * /usr/bin/python ~/Development/speedtest/calculate-speed-statistics.py
```

Again, you might want to run it every minute initially for testing purposes.


### Remove old readings

Once you have extracted the useful information you don't need the content of `raw/speeds.json` any longer. Therefore, the last thing left to is to delete the file after the extraction is done. Let's
say we do this every day at 23:58. To do this we again modify our cronjob adding one more scheduled
command:

```
*/10 * * * * date >> ~/Development/speedtest/raw/speeds.json; ~/.pyenv/versions/global/bin/speedtest --single --secure --json >> ~/Development/speedtest/raw/speeds.json; echo -e "\n" >> ~/Development/speedtest/raw/speeds.json
55 23 * * * /usr/bin/python ~/Development/speedtest/calculate-speed-statistics.py
58 23 * * * rm ~/Development/speedtest/raw/*
```

And then run again `crontab cronjobs-speedtest`.

That's it! Remember to check it in 24h to validate everything worked correctly!
