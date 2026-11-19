# =============================================================================
# Streamy Desktop GUI - Lab 11 Challenge Extension
# Tkinter front-end built on top of the streamy_core domain model.
# =============================================================================

import tkinter as tk
from tkinter import messagebox

from streamy_core import (
    StreamyPlatform, TVShow, Film, Season, Episode, Actor, Genre,
)


def build_demo_platform() -> StreamyPlatform:
    """Seed the GUI with sample titles, cast, reviews and genres."""
    platform = StreamyPlatform()

    ashley = Actor("Ashley Peacock")
    eddy = Actor("Eddy Gerbil")
    platform.register_actor(ashley)
    platform.register_actor(eddy)

    scifi = Genre("Sci-Fi")
    drama = Genre("Drama")
    platform.add_genre(scifi)
    platform.add_genre(drama)

    show = TVShow("Stranger Things", 2016, "Netflix")
    season_one = Season(1)
    season_one.add_episode(Episode("Chapter One: The Vanishing of Will Byers", 2880))
    show.add_season(season_one)
    show.link_actor(ashley)
    show.link_actor(eddy)
    show.add_review(5, "Strong mystery and character work.")
    show.add_review(4, "Great pacing in the first season.")
    scifi.register_title(show)
    platform.add_title(show)

    film = Film("Cosmic Drift", 2023, 118)
    film.link_actor(ashley)
    film.add_review(4, "Solid visuals and soundtrack.")
    drama.register_title(film)
    platform.add_title(film)

    return platform


class StreamyApp(tk.Tk):
    """Main desktop window: searchable catalog, detail panel and playback actions."""

    def __init__(self, platform: StreamyPlatform):
        super().__init__()
        self.platform = platform
        self._titles = list(platform.titles)
        self.selected = None

        self.title("Streamy Backend Platform - Demo GUI")
        self.geometry("760x520")

        # Search bar
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=10, pady=8)
        tk.Label(top, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.search_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        entry.bind("<Return>", lambda _e: self.apply_search())
        tk.Button(top, text="Search", command=self.apply_search).pack(side=tk.LEFT)
        tk.Button(top, text="Reset", command=self.reset_search).pack(side=tk.LEFT, padx=4)

        body = tk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        # Left: catalog list
        self.listbox = tk.Listbox(body, width=40)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Right: detail panel
        self.detail = tk.Text(body, wrap=tk.WORD, state=tk.DISABLED)
        self.detail.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Action buttons
        bottom = tk.Frame(self)
        bottom.pack(fill=tk.X, padx=10, pady=8)
        tk.Button(bottom, text="Play (Valid Token)", command=self.play_valid).pack(side=tk.LEFT)
        tk.Button(bottom, text="Play (Expired Token)", command=self.play_expired).pack(side=tk.LEFT, padx=6)

        self.refresh_list(self.platform.titles)

    def refresh_list(self, titles):
        self.listbox.delete(0, tk.END)
        self._titles = titles
        for title in titles:
            self.listbox.insert(tk.END, self.platform.title_summary(title))
        if titles:
            self.listbox.selection_set(0)
        self.on_select()

    def apply_search(self):
        self.refresh_list(self.platform.search_titles(self.search_var.get()))

    def reset_search(self):
        self.search_var.set("")
        self.refresh_list(self.platform.titles)

    def current_title(self):
        idx = self.listbox.curselection()
        if not idx:
            return None
        return self._titles[idx[0]]

    def on_select(self, _event=None):
        title = self.current_title()
        self.selected = title
        self.detail.config(state=tk.NORMAL)
        self.detail.delete("1.0", tk.END)
        if title is None:
            self.detail.insert(tk.END, "No title selected.")
        else:
            self.detail.insert(tk.END, f"{title.name}\n")
            for line in title.detail_lines():
                self.detail.insert(tk.END, f"{line}\n")
            if isinstance(title, TVShow):
                self.detail.insert(tk.END, f"Network: {title.network}\n")
                self.detail.insert(tk.END, f"Seasons: {len(title.seasons)}\n")
            elif isinstance(title, Film):
                self.detail.insert(tk.END, f"Length: {title.length_minutes} min\n")
        self.detail.config(state=tk.DISABLED)

    def play_valid(self):
        self._play("VALID_STREAM_TOKEN_2026")

    def play_expired(self):
        self._play("EXPIRED_TOKEN")

    def _play(self, token):
        title = self.selected
        if title is None:
            messagebox.showinfo("Streamy", "Select a title first.")
            return
        ok = title.play_media(token)
        if ok:
            messagebox.showinfo("Playback", f"200 OK - Streaming '{title.name}' (token accepted).")
        else:
            messagebox.showwarning("Playback", f"401 Unauthorized - cannot play '{title.name}' (token rejected).")


if __name__ == "__main__":
    app = StreamyApp(build_demo_platform())
    app.mainloop()
