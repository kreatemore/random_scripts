import time


def write(text: str, pause_duration_seconds = 0.1) -> None:
    typed_word = ''
    
    for letter in text:
        typed_word += letter
        
        print(f'{typed_word}\r', end='')
        time.sleep(pause_duration_seconds)

    print()

    
if __name__ == '__main__':
    try:
        write('Who are you?')
        name = input()
        write(f'Hello, {name}')
    except KeyboardInterrupt:
        write('Goodbye!')