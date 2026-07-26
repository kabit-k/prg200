text = """
Nepal is a beautiful country.
Nepal has Mount Everest.
Everest is the highest mountain in the world.
Many tourists visit Nepal every year to see Everest and other mountains.
Nepal is known for its mountains and natural beauty.
"""

def word_frequency(text):

    text = text.lower()

    text = text.replace(".", "")
    text = text.replace(",", "")

    words = text.split()

    counts = {}

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    items = list(counts.items())

    items.sort(key=lambda x: x[1], reverse=True)

    print("Top 3 words:")

    for word, count in items[:3]:
        print(word, "-", count, "times")


word_frequency(text)