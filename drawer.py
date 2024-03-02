import subprocess as cmd
print("hell")
res = cmd.run(["python3", "./ai.py"], shell=True, capture_output=True).stdout.decode("utf-8")

print(res, "hell")