car = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "test" : None
}

x = car.items()


x_list = [i for  i in car.items() ]
x_list_pruned = {k:v for  k, v in car.items() if v is not None }


print(x_list)
print(x_list_pruned)