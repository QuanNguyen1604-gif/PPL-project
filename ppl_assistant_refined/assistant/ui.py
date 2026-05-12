from __future__ import annotations

from tkinter import Button, DISABLED, END, Entry, Label, NORMAL, Scrollbar, Text, Tk, WORD

from assistant.response_engine import ResponseEngine

BG_GRAY = '#ABB2B9'
BG_COLOR = '#17202A'
TEXT_COLOR = '#EAECEE'
FONT = 'Helvetica 14'
FONT_BOLD = 'Helvetica 13 bold'
BOT_NAME = 'VA'


class ChatApplicationUI:
    def __init__(self):
        self.window = Tk()
        self.engine = ResponseEngine()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title('PPL Assistant')
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text='Welcome', font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.text_widget = Text(
            self.window,
            width=18,
            height=2,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=FONT,
            padx=5,
            pady=5,
            wrap=WORD,
        )
        self.text_widget.place(relheight=0.745, relwidth=0.97, rely=0.08)
        self.text_widget.configure(cursor='arrow', state=DISABLED)

        scrollbar = Scrollbar(self.window)
        scrollbar.place(relx=0.97, rely=0.08, relheight=0.745)
        scrollbar.configure(command=self.text_widget.yview)
        self.text_widget['yscrollcommand'] = scrollbar.set

        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        self.input_box = Entry(bottom_label, bg='#2C3E50', fg=TEXT_COLOR, font=FONT)
        self.input_box.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.input_box.focus()
        self.input_box.bind('<Return>', self._on_enter_pressed)

        send_button = Button(bottom_label, text='Send', font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        input_msg = self.input_box.get()
        self._insert_message(input_msg, 'You')
        response_msg = self.engine.get_response(input_msg)
        self._insert_message(response_msg, BOT_NAME)

    def _insert_message(self, msg, sender):
        if not msg:
            return
        self.input_box.delete(0, END)
        text = f'{sender}: {msg}\n\n'
        self.text_widget.configure(cursor='arrow', state=NORMAL)
        self.text_widget.insert(END, text)
        self.text_widget.configure(cursor='arrow', state=DISABLED)
        self.text_widget.see(END)


if __name__ == '__main__':
    ChatApplicationUI().run()
