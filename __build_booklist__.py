w = """
+
Building Machine Learning Systems with Python [eBook]

+
Python for Secret Agents [eBook]

+
Python 3 Object Oriented Programming [eBook]

+
Learning Python Design Patterns [eBook]

+
wxPython 2.8 Application Development Cookbook [eBook]"""

books = []
for line in w.split("\n"):
    if line.startswith("+") or line == "":
        pass
    else:
        books.append(line.replace(" [eBook]",""))
books.sort()

for book in books:
    print(book)

print(f"\n{ '-' * 20 }\nYou have { len(books) } books.")




