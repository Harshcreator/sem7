import re
def matchre(data, *args):
	for regstr in args:
		matchObj = re.search(regstr + '.*', data, re.M | re.I)
		if matchObj:
			print(matchObj.group(0).lstrip().rstrip())
		else:
			print("No ", regstr, "found")

filename = input("Enter the path for email header file:");
fo = open(filename, "r")
data = fo.read()
matchre(data, "MIME-version", "Date:", "Subject:","Delivered-to:","From:","^to:")
fo.close()

# Enter the path for email header file: sample_header.txt
# MIME-version: 1.0
# Date: Wed, 8 Oct 2025 10:00:00 +0000
# Subject: Test Email
# Delivered-to: user@example.com
# From: sender@example.com
# No ^to: found