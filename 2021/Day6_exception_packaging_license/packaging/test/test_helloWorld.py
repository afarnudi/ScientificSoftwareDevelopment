from helloWorld import say_hello

def test_helloWorld_no_params():
    assert say_hello() == "Hello, world!"

def test_hellowWorld_with_param():
    assert say_hello('Ali') == "Hello, Ali!"
