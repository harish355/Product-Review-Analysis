import eel
print("Test")
eel.init('web')

@eel.expose
def search(a):
    print("dummy param")
    return a+1


eel.start('index.html',size=(1000,600))
