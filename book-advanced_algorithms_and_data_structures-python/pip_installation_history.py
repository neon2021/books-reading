# work_date: 2023_09_03 begin

# refer to : https://stackoverflow.com/questions/24736316/see-when-packages-were-installed-updated-using-pip
import pkg_resources, os, time

for package in pkg_resources.working_set:
    print("%s: %s" % (package, time.ctime(os.path.getctime(package.location))))

# work_date: 2023_09_03 end