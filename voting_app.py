import sqlite3
import cv2
from deepface import DeepFace
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as KivyImage
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics.texture import Texture

# Initialize the database
def init_db():
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()

    # Create voters table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        face_path TEXT NOT NULL
    )
    """)

    # Create votes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        candidate_name TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Add a voter to the database
def add_voter(name, face_path):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voters (name, face_path) VALUES (?, ?)", (name, face_path))
    conn.commit()
    conn.close()

# Verify face using DeepFace
def recognize_face(captured_face_path):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, face_path FROM voters")
    voters = cursor.fetchall()

    for voter in voters:
        name, face_path = voter
        try:
            result = DeepFace.verify(captured_face_path, face_path)
            if result["verified"]:
                return name  # Return recognized user's name
        except Exception as e:
            print(f"Error during face recognition: {e}")

    return None  # No match found

# Cast a vote for a candidate
def cast_vote(user_name, candidate_name):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM votes WHERE user_name = ?", (user_name,))
    existing_vote = cursor.fetchone()

    if existing_vote:
        return False  # Duplicate vote detected

    cursor.execute("INSERT INTO votes (user_name, candidate_name) VALUES (?, ?)", (user_name, candidate_name))
    conn.commit()
    conn.close()

    print(f"Vote for {candidate_name} by {user_name} registered successfully.")
    return True

# Count votes
def count_votes():
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT candidate_name, COUNT(*) FROM votes GROUP BY candidate_name")
    results = cursor.fetchall()
    total_votes = sum(count for _, count in results)
    percentages = [(candidate, (count / total_votes) * 100) for candidate, count in results] if total_votes > 0 else []
    conn.close()
    return results, percentages, total_votes

# Kivy App for the user interface
class VotingApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Set background color to white
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # White background
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Add a title
        title = Label(text="Face Recognition Voting System", font_size='24sp', bold=True, color=(0, 0, 0, 1), size_hint=(1, 0.1))
        self.layout.add_widget(title)

        # Scrollable Candidate Profiles
        self.profile_scroll = ScrollView(size_hint=(1, 0.4), do_scroll_x=False, do_scroll_y=True)
        self.profile_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        self.profile_layout.bind(minimum_height=self.profile_layout.setter('height'))

        # Initialize candidates
        self.candidates = ["John Doe", "Jane Smith"]

        # Add candidate profiles
        self.add_candidate_profile("John Doe", "Book Symbol", "icons/book_icon.png", "John Doe is a community leader known for his work in education reform.")
        self.add_candidate_profile("Jane Smith", "Car Symbol", "icons/car_icon.png", "Jane Smith has spearheaded multiple environmental projects.")

        self.profile_scroll.add_widget(self.profile_layout)
        self.layout.add_widget(self.profile_scroll)

        # Action Panel for Voting
        self.action_panel = BoxLayout(orientation='vertical', size_hint=(1, 0.5), padding=10, spacing=10)

        # Camera Feed
        self.image = Image(size_hint=(1, 0.6))
        self.action_panel.add_widget(self.image)

        # Voting Buttons
        self.vote_label = Label(text="Capture your face to authenticate:", font_size='18sp', color=(0, 0, 0, 1), size_hint=(1, 0.2))
        self.action_panel.add_widget(self.vote_label)

        self.capture_button = Button(text="Capture Face", size_hint=(1, 0.2), background_color=(0.2, 0.5, 0.8, 1), on_press=self.capture_face)
        self.action_panel.add_widget(self.capture_button)

        self.vote_button_1 = Button(text="Vote for John Doe", size_hint=(1, 0.2), background_color=(0.3, 0.6, 0.8, 1), on_press=lambda x: self.vote("John Doe"), disabled=True)
        self.action_panel.add_widget(self.vote_button_1)

        self.vote_button_2 = Button(text="Vote for Jane Smith", size_hint=(1, 0.2), background_color=(0.3, 0.6, 0.8, 1), on_press=lambda x: self.vote("Jane Smith"), disabled=True)
        self.action_panel.add_widget(self.vote_button_2)

        self.layout.add_widget(self.action_panel)

        # Initialize video capture (OpenCV)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        # Initialize database and sample voters
        init_db()
        add_voter("Malini", "faces/Malini.jpg")
        add_voter("Dharanya", "faces/Dharanya.jpg")
        add_voter("Devadharshini", "faces/Devadharshini.jpg")

        return self.layout

    def add_candidate_profile(self, name, symbol, icon_path, description):
        """Add a candidate profile to the scrollable layout."""
        profile_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)

        # Candidate Icon
        icon = KivyImage(source=icon_path, size_hint=(0.2, 1))
        profile_box.add_widget(icon)

        # Candidate Info
        info_box = BoxLayout(orientation='vertical', spacing=5)
        name_label = Label(text=f"[b]{name}[/b]\nSymbol: {symbol}", markup=True, font_size='16sp', color=(0, 0, 0, 1))
        description_label = Label(text=description, font_size='14sp', color=(0, 0, 0, 1), halign='left', text_size=(500, None))
        info_box.add_widget(name_label)
        info_box.add_widget(description_label)

        profile_box.add_widget(info_box)
        self.profile_layout.add_widget(profile_box)

    def update_rect(self, *args):
        """Update the background rectangle."""
        self.rect.size = self.layout.size
        self.rect.pos = self.layout.pos

    def update(self, dt):
        """Update the camera feed."""
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture

    def capture_face(self, instance):
        """Capture a face and authenticate the user."""
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite("captured_face.jpg", frame)
            user_name = recognize_face("captured_face.jpg")
            if user_name:
                self.vote_label.text = f"Authenticated as {user_name}. Please vote for a candidate."
                self.vote_button_1.disabled = False
                self.vote_button_2.disabled = False
            else:
                self.vote_label.text = "Face not recognized. Please try again."

    def vote(self, candidate_name):
        """Cast a vote for the specified candidate."""
        user_name = self.vote_label.text.split(' ')[-3]  # Extract authenticated user's name
        success = cast_vote(user_name, candidate_name)
        if success:
            self.vote_label.text = f"Thank you for voting for {candidate_name}."
        else:
            self.vote_label.text = "You have already voted."

    def on_stop(self):
        """Display vote counts and release the camera resource."""
        # Release camera resource
        self.capture.release()

        # Fetch vote counts
        results, percentages, total_votes = count_votes()

        # # Print total votes to the console
        # print(f"Total Votes Casted: {total_votes}")

        # Determine the winning candidate
        if results:
            winning_candidate = max(results, key=lambda x: x[1])[0]  # Get candidate with max votes
        else:
            winning_candidate = "No votes cast"

        # Format the results for display
        result_text = f"Total Votes Casted: {total_votes}\n\n"
        for candidate, count in results:
            percentage = next(p[1] for p in percentages if p[0] == candidate)
            result_text += f"{candidate}: {count} votes ({percentage:.2f}%)\n"
        
        result_text += f"\nWinner: {winning_candidate}"

        # Print detailed results to console
        print(result_text)

        # Create a popup for vote results
        result_popup = Popup(
            title="Vote Results",
            content=Label(text=result_text, font_size='16sp', halign='center', valign='middle'),
            size_hint=(0.8, 0.6),
        )

        # Open the popup
        result_popup.open()

        # Ensure the app closes after displaying the popup
        result_popup.bind(on_dismiss=self.stop)

# Add this at the end to run the app
if __name__ == "__main__":
    VotingApp().run()