import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print('SAY SOMETHING:')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print('{}'.format(text))
    except:
        print('SORRY')
x ='{}'.format(text)
alphabraille = ['⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓', '⠊', '⠚', '⠅', '⠇',
 '⠍', '⠝', '⠕', '⠏', '⠟', '⠗', '⠎', '⠞', '⠥', '⠧', '⠺', '⠭', '⠽', '⠵']
numbraille = ['⠼⠁', '⠼⠃', '⠼⠉', '⠼⠙', '⠼⠑', '⠼⠋', '⠼⠛', '⠼⠓', '⠼⠊', '⠼⠚']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
asciicodes = [' ','!','"','#','$','%','&','','(',')','*','+',',','-','.','/',
          ':',';','<','=','>','?','@','[','\\',']','^','_']

brailles = ['⠀','⠮','⠐','⠼','⠫','⠩','⠯','⠄','⠷','⠾','⠡','⠬','⠠','⠤','⠨','⠌','⠴',
        '⠰','⠣','⠿','⠜','⠹','⠈','⠪','⠳','⠻','⠘','⠸']

text = text.lower()
b =" "
for l in text:
    if l in alphabet:
        b += alphabraille[alphabet.index(l)]
    elif l in nums:
        b += numbraille[nums.index(l)]
    elif l in asciicodes:
        b += brailles[asciicodes.index(l)]
    else:
        b += '  ' 
print(b)
