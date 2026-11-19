# =============================================================================
# Streamy Core Platform Data Engine Modules - Production V1.0
# Miskolc University - Software Technology Laboratory Framework
# =============================================================================


class Title:
    """Represents the abstract parent media element inside the domain."""

    def __init__(self, name: str, release_year: int):
        self.name: str = name
        self.release_year: int = release_year
        # Enforcing Composition (*--) constraints: parent controls lifecycle
        self.seasons: list = []
        self.reviews: list = []
        # Enforcing Aggregation (o--) constraints: actors outlive the title
        self.cast_actors: list = []

    def play_media(self, access_token: str) -> bool:
        """Implements the dynamic authorization loop designed previously."""
        print(f"\n[App Engine] 1. Processing playback route request for: {self.name}")
        print(f"[Auth Service] 2. Checking authorization token state: {access_token}")

        if access_token == "EXPIRED_TOKEN" or access_token == "":
            print("[Auth Service] 3a. Token verification failed: Return 401 Unauthorized payload.")
            return False
        else:
            print("[Auth Service] 3b. Token authorized. Querying Media Catalog Engine.")
            print(f"[Catalog Engine] 4. Fetching content encryption descriptors for: {self.name}")
            print("[Catalog Engine] 5. Handshake OK: Return 200 OK + HLS Stream URL endpoint.")
            return True

    def add_review(self, rating: int, text: str):
        """Creates a tightly-coupled review record (Composition)."""
        new_review = Review(rating, text)
        self.reviews.append(new_review)

    def link_actor(self, actor: 'Actor'):
        """Associates an independent actor to this title (Aggregation)."""
        self.cast_actors.append(actor)

    def average_rating(self) -> float:
        """Extension feature: mean star rating across all attached reviews (0.0 when none)."""
        if not self.reviews:
            return 0.0
        return round(sum(r.rating_stars for r in self.reviews) / len(self.reviews), 2)

    def detail_lines(self) -> list:
        """Extension feature: human-readable detail lines used by the GUI catalog."""
        lines = [f"Year: {self.release_year}", f"Reviews: {len(self.reviews)}",
                 f"Average rating: {self.average_rating()} / 5",
                 f"Cast: {', '.join(a.full_name for a in self.cast_actors) or 'Unassigned'}"]
        return lines


class Film(Title):
    """Specialized media child type mapping feature films (Generalization)."""

    def __init__(self, name: str, release_year: int, length_minutes: int):
        super().__init__(name, release_year)
        self.length_minutes: int = length_minutes


class TVShow(Title):
    """Specialized media child type mapping episodic series (Generalization)."""

    def __init__(self, name: str, release_year: int, network: str):
        super().__init__(name, release_year)
        self.network: str = network

    def add_season(self, season: 'Season'):
        """Wires a tightly-coupled season container into the TV Show (Composition)."""
        self.seasons.append(season)

    def purge_tv_show_data(self):
        """Enforces Composition rules. Purging this parent clears all child data."""
        print(f"\n[Memory Management] Triggering cascading deletion for TV Show: {self.name}")
        total_seasons = len(self.seasons)

        # Cascading clean-up loop through composition structures
        for season in self.seasons:
            season.episodes.clear()  # Clear individual episode references
        self.seasons.clear()
        self.reviews.clear()

        print(f"[Memory Management] Cascading delete complete: {total_seasons} Season arrays cleared.")
        print(f"[Memory Management] Aggregation check: Cast ledger contains {len(self.cast_actors)} actors (Left Intact).")


class Season:
    """Child entity held under deep lifecycle Composition parameters."""

    def __init__(self, season_number: int):
        self.season_number: int = season_number
        self.episodes: list = []

    def add_episode(self, episode: 'Episode'):
        """Nests an episodic media container (Composition)."""
        self.episodes.append(episode)


class Episode:
    """Granular nested episodic operational media container data block."""

    def __init__(self, episode_title: str, duration_seconds: int):
        self.episode_title: str = episode_title
        self.duration_seconds: int = duration_seconds


class Review:
    """User generated textual ratings string collection node."""

    def __init__(self, rating_stars: int, review_text: str):
        self.rating_stars: int = rating_stars
        self.review_text: str = review_text


class Actor:
    """Independent entity held via flexible system Aggregation bounds."""

    def __init__(self, full_name: str):
        self.full_name: str = full_name


class Genre:
    """Platform structural baseline lookup taxonomy index component."""

    def __init__(self, genre_name: str):
        self.genre_name: str = genre_name
        self.catalog_titles: list = []

    def register_title(self, title: Title):
        """Maps a loose mutual association reference link between domain classes."""
        self.catalog_titles.append(title)

    def display_catalog(self):
        """Prints out registered titles mapped under this taxonomy."""
        print(f"\n[Taxonomy Index] Titles registered under Genre Category: {self.genre_name}")
        for title in self.catalog_titles:
            print(f" - {title.name} ({title.release_year})")


class StreamyPlatform:
    """Extension feature: top-level catalog facade that aggregates titles, actors and genres,
    and exposes keyword search used by the desktop GUI."""

    def __init__(self):
        self.titles: list = []
        self.actors: list = []
        self.genres: list = []

    def add_title(self, title: Title):
        self.titles.append(title)

    def register_actor(self, actor: Actor):
        self.actors.append(actor)

    def add_genre(self, genre: Genre):
        self.genres.append(genre)

    def search_titles(self, keyword: str) -> list:
        """Case-insensitive keyword match against title name and cast member names."""
        kw = keyword.strip().lower()
        if not kw:
            return list(self.titles)
        return [
            t for t in self.titles
            if kw in t.name.lower()
            or any(kw in a.full_name.lower() for a in t.cast_actors)
        ]

    def title_summary(self, title: Title) -> str:
        """One-line catalog entry for a title, including its subtype."""
        subtype = type(title).__name__
        extra = ""
        if isinstance(title, TVShow):
            extra = f" | Network: {title.network}"
        elif isinstance(title, Film):
            extra = f" | Length: {title.length_minutes} min"
        return f"{title.name} ({title.release_year}) [{subtype}]{extra} | Avg {title.average_rating()}/5"


# =============================================================================
# INTEGRATION TESTING RUNTIME SIMULATION
# =============================================================================

if __name__ == "__main__":
    print("=== STREAMY BACKEND ARCHITECTURAL VERIFICATION RUNTIME ===")

    # 1. Initialize Independent Aggregated Entities (Actors)
    actor_one = Actor("Ashley Peacock")
    actor_two = Actor("Eddy Gerbil")

    # 2. Initialize Taxonomy Nodes (Genres)
    sci_fi = Genre("Sci-Fi")

    # 3. Construct Generalization and Composition Clusters (TV Show -> Seasons -> Episodes)
    show_entry = TVShow("Stranger Things", 2016, "Netflix")
    season_one = Season(1)
    episode_one = Episode("Chapter One: The Vanishing of Will Byers", 2880)

    # Wire the Composition relationships together
    season_one.add_episode(episode_one)
    show_entry.add_season(season_one)

    # Wire the Aggregation and Association bonds
    show_entry.link_actor(actor_one)
    show_entry.link_actor(actor_two)
    sci_fi.register_title(show_entry)

    # 4. Execute Behavior Verification Testing
    # Scenario A: Unhappy Path Execution (Expired Credentials)
    auth_pass_one = show_entry.play_media("EXPIRED_TOKEN")
    print(f"Scenario Verification Result: {auth_pass_one} (Expected: False)")

    # Scenario B: Happy Path Execution (Valid Credentials)
    auth_pass_two = show_entry.play_media("VALID_STREAM_TOKEN_2026")
    print(f"Scenario Verification Result: {auth_pass_two} (Expected: True)")

    # 5. Execute Structural Constraint Verification
    sci_fi.display_catalog()
    show_entry.purge_tv_show_data()
