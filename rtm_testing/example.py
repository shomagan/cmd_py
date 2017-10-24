import sys,time

def main():
  for i in range(10):
    if i%2==0:
      sys.stdout.write('\r'+"/")
      sys.stdout.flush()
    else:
      sys.stdout.write('\r'+"\\")
      sys.stdout.flush()
    time.sleep(1)


if __name__ == '__main__':
    main()

