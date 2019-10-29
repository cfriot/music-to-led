def valueChanger(old_value, value, max):

    new_value = old_value

    if(value >= max):
        new_value += 1
        if(new_value >= max):
            new_value = 0
    else:
        new_value = value

    return new_value


print(valueChanger(0,1,1))
print(valueChanger(1,10,1))
print(valueChanger(1,20,1))
print(valueChanger(1,20,10))
