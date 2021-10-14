from ebooklib import epub
from html_epub.settings import STATICFILES_DIRS
from api.utils import get_image_from_link, get_unique_string


PATH = STATICFILES_DIRS[0]


class EpubMaker:
    """
    This class creates an epub(*.epub) file
    """

    def __init__(self) -> None:
        self.book = epub.EpubBook()
        self.chapters = []

    def set_metadata(
        self,
        title: str,
        language: str,
        author: str,
        identifier: str = None,
    ):
        """
        This function sets the metadata of the epubfile

        Args:
            title (str): Title of the book, e.g "The Name of the Wind"
            language (str): Language of the ebook, e.g 'en'. When it comes to language code,
            recommended best practice is to use a controlled vocabulary such as RFC 4646 - http://www.ietf.org/rfc/rfc4646.txt.
            author (str): Author of the book e.g "Pat Rothfuss"
            identifier (str, optional): A unique identifier for book. Leave empty if you want the an automatically generated identifier.
        """
        self.book.set_title = title
        self.title = title
        self.book.set_language = language
        self.language = language
        self.book.add_author = author
        self.book.set_identifier = identifier if identifier else get_unique_string(20)

    def set_cover(self, cover: str, link=False):
        """
        This function sets the cover of the book

        Args:
            cover (str): Path to the cover image.
            link (bool): Set to True if the cover argument is a link to an image instead.
                            Cover must link to a .png or .jpg!

        """
        cover = f"{PATH}/{get_image_from_link(cover)}" if link else cover
        print(cover)

        self.book.set_cover(
            "image.jpg",
            open(cover, "rb").read(),
        )
        self.chapters.insert(0, "cover")

    def add_chapter(self, title: str, content: str):
        """
        This function adds chapter to the Epub file.

        Args:
            title (str): Title of the book.
            content (str): Contents of the book as HTML string.
        """

        chapter = epub.EpubHtml(
            title=title,
            file_name=f"{title}.xhtml",
            lang=self.language,
        )
        chapter.set_content(content)
        self.book.add_item(chapter)
        self.chapters.append(chapter)

    def publish(self):
        """
        This function compiles and returns the epub file

        Args:
            path (str): The path where the book will be created. DO NOT INCLUDE THE FILE NAME.
                        Only the Path.

        """
        path = f"{PATH}/{self.title}.epub"
        self.book.toc = self.chapters
        self.book.spine = self.chapters
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        epub.write_epub(path, self.book, {})
