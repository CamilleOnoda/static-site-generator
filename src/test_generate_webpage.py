import unittest
from generate_content import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        text = extract_title(md)
        self.assertEqual(
            text,
            "Tolkien Fan Club"
        )


if __name__ == "__main__":
    unittest.main()