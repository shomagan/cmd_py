from veros import Veros, veros_method

class MyVerosSetup(Veros):
    ...
    @veros_method
    def my_function(self):
        arr = np.array([1,2,3,4]) # "np" uses either NumPy or Bohrium

if __name__ == "__main__":
   simulation = MyVerosSetup()
   simulation.setup()
   simulation.run()
