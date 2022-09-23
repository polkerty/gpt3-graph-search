from gpt3_api import execute

def main():
    response = execute('Write a long story about a baby fish. The story should have the same plot as Hamlet.', max_tokens=1000)
    print(response)

if __name__ == '__main__':
    main()
