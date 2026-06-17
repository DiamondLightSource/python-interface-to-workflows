import re

import yaml


class A:
    def __init__(self, value: str):
        self.value = value


class_a = A(value="b")
dump_a = yaml.dump(class_a)

with open("test_yaml.yaml", "w") as f:
    f.write(dump_a)


# will write:
#!!python/object:__main__.A
# value: b
class Content:
    def __init__(self, value: str, other_value: str, third_value: str):
        self.value = value
        self.other_value = other_value
        self.third_value = third_value


class_with_more_content = Content("a", "b", "c")
x = yaml.dump(class_with_more_content)
print(x)
xlist = x.split("\n")
title = re.sub(r"!!python\/object:__main__\.", "", xlist[0]) + ":\n"
lst: list[str] = []
for key, value in vars(class_with_more_content).items():
    lst.append(f"  {key}: {value}\n")
rejoined = "".join(lst)
titlepluscontent = title + rejoined


with open("test_yaml.yaml", "a") as f:
    f.write(titlepluscontent)
# can use regex to edit this down like we see above^
# will write:
# A:
# {2x space}value: b

with open("test_yaml.yaml", "a") as f:
    f.write(
        yaml.dump(
            {
                "firstdict": {"key": "value"},
                "seconddict": {"secondsmallerkey": "secondsmallervalue"},
                "thirddict": {"with_even_more": {"layers": "ofpairs"}},
            }
        )
    )  # converts this to a yaml
# will write:
# firstdict:
#   key: value
# seconddict:
#   secondsmallerkey: secondsmallervalue
# thirddict:
#   with_even_more:
#     layers: ofpairs
