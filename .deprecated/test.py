def decorator(func):
    def wrapper(sender, receiver, *args, **kwargs):
        a = sender.a
        b = receiver
        print("a + b =", a + b)
        print(func(a, b, *args, **kwargs))
    
    return wrapper


class A:
    def __init__(self, a):
        self.a = a
    
    @decorator
    def send(self, receiver, msg):
        print(receiver, )
        return msg


if __name__ == '__main__':
    aa = A(1)
    aa.send(2, 'xxxx')
