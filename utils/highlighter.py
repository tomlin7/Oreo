import json


class ColorSchemeLoader:
    def __init__(self, theme_config):
        with open(theme_config, 'r') as f:
            self.syntax_colors = json.load(f)["syntax"]
        self.set_token_colors()
    
    def get_color(self, tokentype):
        try:
            return self.syntax_colors[tokentype]
        except KeyError:
            return "#ffffff"
    
    def set_token_colors(self):
        # Special Token Types
        # ---
        # self.text = self.get_color("text")
        # self.escape = self.get_color("escape")
        #---

        # text that doesn't belong to kookie
        # self.other = self.get_color("other")
        
        # Common Types
        # ---
        self.keyword = self.get_color("keyword")
        self.name = self.get_color("name")
        self.string = self.get_color("string")
        self.number = self.get_color("number")
        self.punctuation = self.get_color("punctuation")
        self.operator = self.get_color("operator")
        self.comment = self.get_color("comment")
        # ---


class TokenTypes:
    keywords = [
        "print", "goto",
        "if", "then", "endif", 
        "while", "repeat",
        "label", "let", "input", "endwhile"
    ]

    strings = [
        "(\'(.)*\')", "(\"(.)*\")"
    ]
    
    comments = "#(.)*"


class Highlighter:
    def __init__(self, editorwindow):
        self.editorwindow = editorwindow
        
        self.tokentypes = TokenTypes()
        self.colors = ColorSchemeLoader(self.editorwindow.config.theme)

        self.configure_tags()
        self.highlight_all()
    
    def configure_tags(self):
        for keyword in self.tokentypes.keywords:
            self.editorwindow.editor.tag_configure(keyword, foreground=self.colors.keyword)
        
        self.editorwindow.editor.tag_configure("singlestring", foreground=self.colors.string)
        self.editorwindow.editor.tag_configure("doublestring", foreground=self.colors.string)
        self.editorwindow.editor.tag_configure("comment", foreground=self.colors.comment)
        # ...

    def highlight_all(self):
        self.highlight_keywords()
        self.highlight_strings()
        self.highlight_comments()

    def highlight_keywords(self):
        for keyword in self.tokentypes.keywords:
            self.editorwindow.editor.highlight_pattern(keyword, keyword)
    
    def highlight_strings(self):
        self.editorwindow.editor.highlight_pattern(self.tokentypes.strings[0], "singlestring", regexp=True)
        self.editorwindow.editor.highlight_pattern(self.tokentypes.strings[1], "doublestring", regexp=True)
    
    def highlight_comments(self):
        self.editorwindow.editor.highlight_pattern(self.tokentypes.comments, "comment", regexp=True)