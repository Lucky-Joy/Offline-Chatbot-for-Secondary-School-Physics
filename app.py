import tkinter as tk
from tkinter import ttk, scrolledtext

from engine import ChatEngine

CLASS_OPTIONS = ["All", "8", "9", "10", "11", "12"]

TOPIC_OPTIONS = [
    "All",
    "Motion",
    "Force and Laws of Motion",
    "Work, Energy and Power",
    "Gravitation",
    "Pressure and Fluids",
    "Heat and Temperature",
    "Sound",
    "Electricity",
    "Magnetism",
    "Light",
    "Waves",
    "Modern Physics",
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Offline NCERT Physics Chatbot (Class 8–12)")
        self.geometry("840x520")

        self.engine = ChatEngine()

        self.class_var = tk.StringVar(value="All")
        self.topic_var = tk.StringVar(value="All")

        self._build_ui()

    def _build_ui(self):
        # Top controls: class + topic
        top = ttk.Frame(self, padding=8)
        top.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top, text="Class:").pack(side=tk.LEFT)
        class_cb = ttk.Combobox(
            top,
            textvariable=self.class_var,
            values=CLASS_OPTIONS,
            state="readonly",
            width=6,
        )
        class_cb.pack(side=tk.LEFT, padx=4)

        ttk.Label(top, text="Topic:").pack(side=tk.LEFT, padx=(12, 0))
        topic_cb = ttk.Combobox(
            top,
            textvariable=self.topic_var,
            values=TOPIC_OPTIONS,
            state="readonly",
            width=28,
        )
        topic_cb.pack(side=tk.LEFT, padx=4)

        btn_topics = ttk.Button(
            top, text="Show topics info", command=self._show_topics_info
        )
        btn_topics.pack(side=tk.RIGHT)

        mid = ttk.Frame(self, padding=(8, 0))
        mid.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.chat = scrolledtext.ScrolledText(
            mid, wrap=tk.WORD, state=tk.DISABLED
        )
        self.chat.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        bottom = ttk.Frame(self, padding=8)
        bottom.pack(side=tk.BOTTOM, fill=tk.X)

        self.entry = ttk.Entry(bottom)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self._on_send)

        send_btn = ttk.Button(bottom, text="Ask", command=self._on_send)
        send_btn.pack(side=tk.LEFT, padx=(6, 0))

        self._post_system(
            "Hello! I am an offline Physics assistant for NCERT classes 8–12.\n"
            "Select class/topic if you like, then ask your question."
        )

    def _show_topics_info(self):
        msg = (
            "I support key Physics concepts from NCERT classes 8–12, including:\n"
            "- Motion, force, Newton's laws\n"
            "- Work, energy and power\n"
            "- Gravitation, pressure and fluids\n"
            "- Heat and temperature\n"
            "- Sound and waves\n"
            "- Electricity and magnetism\n"
            "- Light and basic modern physics\n"
            "Coverage will grow as more questions and answers are added."
        )
        self._post_system(msg)

    def _on_send(self, event=None):
        q = self.entry.get().strip()
        if not q:
            return
        self.entry.delete(0, tk.END)

        self._post_user(q)

        cls = self.class_var.get()
        if cls == "All":
            cls_val = None
        else:
            try:
                cls_val = int(cls)
            except ValueError:
                cls_val = None

        topic = self.topic_var.get()
        topic_val = None if topic == "All" else topic

        ans, related = self.engine.handle(q, class_level=cls_val, topic=topic_val)
        self._post_bot(ans, related)

    def _post(self, prefix, text):
        self.chat.configure(state=tk.NORMAL)
        self.chat.insert(tk.END, f"{prefix}{text}\n\n")
        self.chat.configure(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _post_user(self, text):
        self._post("You: ", text)

    def _post_bot(self, ans, related):
        self._post("Bot: ", ans)
        if related:
            rel_text = "You can also ask:\n" + "\n".join(f"- {q}" for q in related)
            self._post("Bot: ", rel_text)

    def _post_system(self, text):
        self._post("[Info] ", text)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()