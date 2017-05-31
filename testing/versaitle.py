x =0
def function_one():
  global x
  x = 2
  def function_insert():
    nonlocal x 
    x = 3
  print('before',x)
  function_insert()
  print('after',x)
  return x
  
def main():
  x = 1
  function_one()
  print(x)
if __name__ == "__main__":
  main()