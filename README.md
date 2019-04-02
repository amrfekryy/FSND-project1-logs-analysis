# [FSND](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) Project1 - Logs Analysis

This is a command line reporting tool that connects to the database of a newspaper website and provides insights derived from users activity.

Questions answered by the program:
- What are the most popular three articles of all time?
- What are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

### Requirements:
1. Set-up a virtual machine using Vagrant and VirtualBox.
   - install [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) package for your operating system.
   - install [Vagrant](https://www.vagrantup.com/downloads.html) package for your operating system.
   - download the [FSND Virtual Machine folder](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) and `cd` into the "vagrant" subdirectory.
   - run `vagrant up` to download the Linux operating system and install it.
   - run `vagrant ssh` to log in to your installed Linux vertual machine.
   - click [here](https://classroom.udacity.com/courses/ud197/lessons/3423258756/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0) for more detailed instructions  (course enrollment required).
   
2. download and unzip [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) into "vagrant" directory. This file contains the database design (tables), and data for each table.

### Usage:

1. set up the local database "news", and load data into it using the command
    `psql -d news -f newsdata.sql`

2. add the necessary views in "create_views.sql" using the command 
   `psql -d news -f create_views.sql`

3. run the python file from the command line
   `python3 report.py`
   and you will see the answers to the questions as in "output.txt" file.
