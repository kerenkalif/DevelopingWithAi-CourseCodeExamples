print("### Usage 1 ###")

def foo(a, b):
    print(f"a is {a}, b is {b}")
 
params = {"a": 1, "b": 2}
 
foo(a=params["a"], b=params["b"])
foo(**params)


print("### Usage 2 ###")


def print_everything(**kwargs):
    print(kwargs)
 
print_everything(
    name="gogo",
    age=25,
    city="Tel Aviv"
)

user_data = {
    "name": "gogo",
    "age": 25,
    "city": "Tel Aviv"
}
print_everything(**user_data)
print_everything(user_data)

 
# Output:
# {"name": "Keren", "age": 40,
#  "city": "Tel Aviv"}

 
# Output: a is 1, b is 2


print("### Usage 3 ###")


dict_a = {"x": 10}
dict_b = {"y": 20}
 
# Unpack a, unpack b, add z:
merged = {**dict_a, **dict_b, "z": 30}
 
print(merged)
 
# Output:
# {"x": 10, "y": 20, "z": 30}
