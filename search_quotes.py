from models import Author, Quote

while True:
    command = input("Команда (наприклад: 'name:<...>' або 'tag:<...>' або 'tags:<...>,<...>' або 'exit'): ")
    if command.startswith("name:"):
        author_name = command[len("name:"):]
        authors = Author.objects(fullname__icontains=author_name)
        for author in authors:
            quotes = Quote.objects(author=author)
            for q in quotes:
                print(q.quote)
    elif command.startswith("tag:"):
        tag = command[len("tag:"):]
        quotes = Quote.objects(tags__icontains=tag)
        for q in quotes:
            print(q.quote)
    elif command.startswith("tags:"):
        tags = command[len("tags:"):].split(',')
        quotes = Quote.objects(tags__in=tags)
        for q in quotes:
            print(q.quote)
    elif command == "exit":
        break
    else:
        print("Невідома команда. Спробуйте ще раз.")
