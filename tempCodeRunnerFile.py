import sys
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from typing import List, Tuple, Optional

# ===== CONSTANTS =====
DARK_BG = "#121212"
DARK_FRAME = "#1E1E1E"
ACCENT_COLOR = "#4CAF50"
SECONDARY_COLOR = "#2196F3"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#B0B0B0"
FONT_HEADING = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)
ICON_SIZE = 20
PADDING = 15
ANIMATION_SPEED = 200
SIZE = 5

# ===== CRYPTOGRAPHY FUNCTIONS =====
def print_hex(data: bytes, length: int) -> None:
    for i in range(length):
        print(f"{data[i]:02x}", end="")
    print()

# ===== CLASSICAL CIPHERS =====
def caesar_cipher(text: str, key: int, encrypt: bool) -> str:
    result = []
    for char in text:
        if char.isupper():
            if encrypt:
                new_char = chr((ord(char) - ord('A') + key) % 26 + ord('A'))
            else:
                new_char = chr((ord(char) - ord('A') - key + 26) % 26 + ord('A'))
            result.append(new_char)
        elif char.islower():
            if encrypt:
                new_char = chr((ord(char) - ord('a') + key) % 26 + ord('a'))
            else:
                new_char = chr((ord(char) - ord('a') - key + 26) % 26 + ord('a'))
            result.append(new_char)
        else:
            result.append(char)
    return "".join(result)

def prepare_playfair_matrix(key: str) -> List[List[str]]:
    key = key.upper().replace("J", "I")
    used = [False] * 26
    matrix = [['' for _ in range(SIZE)] for _ in range(SIZE)]
    k = 0
    
    # Process key
    for ch in key:
        if ch == 'J':
            ch = 'I'
        if ch.isalpha() and not used[ord(ch) - ord('A')]:
            matrix[k // SIZE][k % SIZE] = ch
            used[ord(ch) - ord('A')] = True
            k += 1
    
    # Fill remaining letters
    for ch in range(ord('A'), ord('Z') + 1):
        ch = chr(ch)
        if ch == 'J':
            continue
        if not used[ord(ch) - ord('A')] and k < 25:
            matrix[k // SIZE][k % SIZE] = ch
            k += 1
    return matrix

def playfair_cipher(text: str, key: str, encrypt: bool) -> str:
    matrix = prepare_playfair_matrix(key)
    processed_text = []
    i = 0
    text = text.upper().replace("J", "I")
    
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = 'X'
        
        if a == b:
            b = 'X'
            i += 1
        else:
            i += 2
        
        # Find positions in matrix
        a_pos = (-1, -1)
        b_pos = (-1, -1)
        for row in range(SIZE):
            for col in range(SIZE):
                if matrix[row][col] == a:
                    a_pos = (row, col)
                if matrix[row][col] == b:
                    b_pos = (row, col)
        
        a_row, a_col = a_pos
        b_row, b_col = b_pos
        
        # Apply cipher rules
        if a_row == b_row:  # Same row
            new_a_col = (a_col + (1 if encrypt else -1)) % SIZE
            new_b_col = (b_col + (1 if encrypt else -1)) % SIZE
            processed_text.append(matrix[a_row][new_a_col])
            processed_text.append(matrix[b_row][new_b_col])
        elif a_col == b_col:  # Same column
            new_a_row = (a_row + (1 if encrypt else -1)) % SIZE
            new_b_row = (b_row + (1 if encrypt else -1)) % SIZE
            processed_text.append(matrix[new_a_row][a_col])
            processed_text.append(matrix[new_b_row][b_col])
        else:  # Rectangle
            processed_text.append(matrix[a_row][b_col])
            processed_text.append(matrix[b_row][a_col])
    
    return "".join(processed_text)

def hill_cipher(text: str, key: List[List[int]], encrypt: bool) -> str:
    # Calculate determinant
    det = key[0][0] * key[1][1] - key[0][1] * key[1][0]
    det = (det % 26 + 26) % 26
    
    # Find modular inverse of determinant
    det_inv = -1
    for i in range(26):
        if (det * i) % 26 == 1:
            det_inv = i
            break
    
    if not encrypt and det_inv == -1:
        raise ValueError("Invalid key - no inverse exists!")
    
    # Calculate inverse key for decryption
    if not encrypt:
        inv_key = [
            [(key[1][1] * det_inv) % 26, (-key[0][1] * det_inv) % 26],
            [(-key[1][0] * det_inv) % 26, (key[0][0] * det_inv) % 26]
        ]
        for i in range(2):
            for j in range(2):
                if inv_key[i][j] < 0:
                    inv_key[i][j] += 26
        key = inv_key
    
    # Process text in pairs
    result = []
    text = text.upper()
    for i in range(0, len(text), 2):
        a = ord(text[i]) - ord('A')
        b = ord(text[i + 1]) - ord('A') if i + 1 < len(text) else 23  # 'X'
        
        res_a = (key[0][0] * a + key[0][1] * b) % 26
        res_b = (key[1][0] * a + key[1][1] * b) % 26
        
        result.append(chr(res_a + ord('A')))
        result.append(chr(res_b + ord('A')))
    
    return "".join(result)

def vigenere_cipher(text: str, key: str, encrypt: bool) -> str:
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            key_char = key[key_index % len(key)].lower()
            shift = ord(key_char) - ord('a')
            if not encrypt:
                shift = -shift
            
            if char.isupper():
                new_char = chr((ord(char) - ord('A') + shift + 26) % 26 + ord('A'))
            else:
                new_char = chr((ord(char) - ord('a') + shift + 26) % 26 + ord('a'))
            
            result.append(new_char)
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

def rail_fence_cipher(text: str, rails: int, encrypt: bool) -> str:
    if encrypt:
        result = []
        for r in range(rails):
            i = r
            while i < len(text):
                result.append(text[i])
                if r != 0 and r != rails - 1:
                    next_i = i + 2 * (rails - r - 1)
                    if next_i < len(text):
                        result.append(text[next_i])
                i += 2 * (rails - 1)
        return "".join(result)
    else:
        decrypted = [''] * len(text)
        index = 0
        for r in range(rails):
            i = r
            while i < len(text):
                decrypted[i] = text[index]
                index += 1
                if r != 0 and r != rails - 1:
                    next_i = i + 2 * (rails - r - 1)
                    if next_i < len(text):
                        decrypted[next_i] = text[index]
                        index += 1
                i += 2 * (rails - 1)
        return "".join(decrypted)

# ===== HELPER FUNCTIONS =====
def validate_numeric_input(new_value: str) -> bool:
    """Validate that input contains only numbers"""
    return new_value == "" or new_value.isdigit()

def create_tooltip(widget, text: str) -> None:
    """Create a tooltip for a widget"""
    tooltip = ctk.CTkToplevel(widget)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    
    label = ctk.CTkLabel(tooltip, text=text, corner_radius=6)
    label.pack(ipadx=8, ipady=4)
    
    def enter(event):
        x = widget.winfo_rootx() + widget.winfo_width() + 5
        y = widget.winfo_rooty() + (widget.winfo_height() - label.winfo_reqheight()) // 2
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()
    
    def leave(event):
        tooltip.withdraw()
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

# ===== MAIN APPLICATION =====
class CryptographyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("Cryptography Toolkit")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Set theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        
        # Create custom title bar
        self.create_title_bar()
        
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color=DARK_BG)
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Initialize UI
        self.create_main_menu()
        self.create_status_bar()
        
    def create_title_bar(self) -> None:
        """Create a custom title bar with minimize/close buttons"""
        self.title_bar = ctk.CTkFrame(self, height=30, corner_radius=0, fg_color=DARK_FRAME)
        self.title_bar.pack(fill="x", padx=0, pady=0)
        
        # Title label
        title_label = ctk.CTkLabel(
            self.title_bar, 
            text="Cryptography Toolkit", 
            font=FONT_HEADING,
            fg_color="transparent"
        )
        title_label.pack(side="left", padx=10)
        
        # Minimize button
        minimize_btn = ctk.CTkButton(
            self.title_bar, 
            text="─", 
            width=30, 
            height=30,
            fg_color="transparent",
            hover_color="#333333",
            command=self._minimize_window
        )
        minimize_btn.pack(side="right", padx=0)
        
        # Close button
        close_btn = ctk.CTkButton(
            self.title_bar, 
            text="✕", 
            width=30, 
            height=30,
            fg_color="transparent",
            hover_color="#FF5555",
            command=self._close_window
        )
        close_btn.pack(side="right", padx=0)
        
        # Bind mouse events for window dragging
        self.title_bar.bind("<ButtonPress-1>", self._start_move)
        self.title_bar.bind("<B1-Motion>", self._on_move)
        
    def _start_move(self, event):
        self._x = event.x
        self._y = event.y
        
    def _on_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
        
    def _minimize_window(self):
        self.iconify()
        
    def _close_window(self):
        self.destroy()
    
    def create_main_menu(self) -> None:
        """Create the main menu with card-based navigation"""
        self.menu_frame = ctk.CTkFrame(self.main_container, fg_color=DARK_BG)
        self.menu_frame.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)
        
        # Title label
        title_label = ctk.CTkLabel(
            self.menu_frame,
            text="Select Cipher Category",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(pady=(0, PADDING))
        
        # Card container
        card_container = ctk.CTkFrame(self.menu_frame, fg_color=DARK_BG)
        card_container.pack(fill="both", expand=True)
        
        # Create cards
        cards = [
            ("Classical Ciphers", "scroll", self.show_classical_ciphers),
            ("Symmetric Encryption", "lock", self.show_symmetric_ciphers),
            ("Asymmetric Encryption", "key", self.show_asymmetric_ciphers),
            ("Digital Signature", "signature", self.show_signature_tools)
        ]
        
        # Grid layout for cards
        for i, (title, icon, command) in enumerate(cards):
            row = i // 2
            col = i % 2
            
            card = ctk.CTkFrame(
                card_container,
                width=300,
                height=200,
                corner_radius=12,
                fg_color=DARK_FRAME,
                border_color=ACCENT_COLOR,
                border_width=1
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)
            
            # Make cards expandable
            card_container.grid_rowconfigure(row, weight=1)
            card_container.grid_columnconfigure(col, weight=1)
            
            # Add hover effect
            card.bind("<Enter>", lambda e, c=card: self._on_card_hover(e, c))
            card.bind("<Leave>", lambda e, c=card: self._on_card_leave(e, c))
            
            # Card content
            # Icon (using emoji as placeholder - in real app use actual icons)
            icon_label = ctk.CTkLabel(
                card,
                text=self._get_icon_emoji(icon),
                font=("Segoe UI", 24),
                fg_color="transparent"
            )
            icon_label.pack(pady=(20, 10))
            
            # Title
            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=FONT_HEADING,
                fg_color="transparent"
            )
            title_label.pack(pady=(0, 10))
            
            # Button
            button = ctk.CTkButton(
                card,
                text="Open",
                width=100,
                command=command
            )
            button.pack(pady=(0, 20))
    
    def _get_icon_emoji(self, icon_name: str) -> str:
        """Return emoji representation of icons (replace with actual icons in production)"""
        icons = {
            "scroll": "📜",
            "lock": "🔒",
            "key": "🔑",
            "signature": "✍️"
        }
        return icons.get(icon_name, "⚙️")
    
    def _on_card_hover(self, event, card):
        """Animation when hovering over a card"""
        card.configure(border_color=SECONDARY_COLOR)
    
    def _on_card_leave(self, event, card):
        """Animation when leaving a card"""
        card.configure(border_color=ACCENT_COLOR)
    
    def create_status_bar(self) -> None:
        """Create a status bar at the bottom of the window"""
        self.status_bar = ctk.CTkFrame(self.main_container, height=25, corner_radius=0)
        self.status_bar.pack(fill="x", side="bottom", padx=0, pady=0)
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=FONT_BODY,
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10)
        
        # Theme toggle
        self.theme_btn = ctk.CTkButton(
            self.status_bar,
            text="☀️",
            width=30,
            height=25,
            fg_color="transparent",
            hover_color=DARK_FRAME,
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="right", padx=5)
    
    def toggle_theme(self) -> None:
        """Toggle between dark and light theme"""
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_btn.configure(text="🌙")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_btn.configure(text="☀️")
    
    def update_status(self, message: str) -> None:
        """Update the status bar message"""
        self.status_label.configure(text=message)
        self.after(3000, lambda: self.status_label.configure(text="Ready"))
    
    def clear_content_frame(self) -> None:
        """Clear the content frame to show new content"""
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
        
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color=DARK_BG)
        self.content_frame.pack(fill="both", expand=True, padx=PADDING, pady=(0, PADDING))
        
        # Add back button
        back_btn = ctk.CTkButton(
            self.content_frame,
            text="← Back to Menu",
            width=120,
            command=self.show_main_menu,
            fg_color="transparent",
            border_color=ACCENT_COLOR,
            border_width=1
        )
        back_btn.pack(anchor="nw", padx=5, pady=5)
    
    def show_main_menu(self) -> None:
        """Show the main menu"""
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
        self.menu_frame.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)
    
    def show_classical_ciphers(self) -> None:
        """Show classical cipher options"""
        self.menu_frame.pack_forget()
        self.clear_content_frame()
        
        # Create notebook for different ciphers
        notebook = ctk.CTkTabview(self.content_frame)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add tabs
        tabs = [
            ("Caesar", self.create_caesar_interface),
            ("Playfair", self.create_playfair_interface),
            ("Hill", self.create_hill_interface),
            ("Vigenère", self.create_vigenere_interface),
            ("Rail Fence", self.create_rail_fence_interface)
        ]
        
        for name, func in tabs:
            tab = notebook.add(name)
            func(tab)
    
    def show_symmetric_ciphers(self) -> None:
        """Show symmetric cipher options"""
        self.menu_frame.pack_forget()
        self.clear_content_frame()
        
        notebook = ctk.CTkTabview(self.content_frame)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add tabs
        des_tab = notebook.add("DES")
        self.create_des_interface(des_tab)
    
    def show_asymmetric_ciphers(self) -> None:
        """Show asymmetric cipher options"""
        self.menu_frame.pack_forget()
        self.clear_content_frame()
        
        notebook = ctk.CTkTabview(self.content_frame)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        rsa_tab = notebook.add("RSA")
        self.create_rsa_interface(rsa_tab)
    
    def show_signature_tools(self) -> None:
        """Show digital signature tools"""
        self.menu_frame.pack_forget()
        self.clear_content_frame()
        
        notebook = ctk.CTkTabview(self.content_frame)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        dsa_tab = notebook.add("DSA")
        self.create_dsa_interface(dsa_tab)
    
    # ===== CIPHER INTERFACE CREATORS =====
    def create_caesar_interface(self, parent) -> None:
        """Create Caesar cipher interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Caesar Cipher", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Text input
        self.caesar_text = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter text...",
            width=400
        )
        self.caesar_text.pack(fill="x", padx=5, pady=5)
        
        # Key input
        key_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        key_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(key_frame, text="Shift Key:").pack(side="left", padx=5)
        
        validate_num = (self.register(validate_numeric_input), "%P")
        self.caesar_key = ctk.CTkEntry(
            key_frame,
            placeholder_text="Number...",
            width=80,
            validate="key",
            validatecommand=validate_num
        )
        self.caesar_key.pack(side="left", padx=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Encrypt",
            command=self.caesar_encrypt,
            fg_color=ACCENT_COLOR
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Decrypt",
            command=self.caesar_decrypt,
            fg_color=SECONDARY_COLOR
        ).pack(side="left", padx=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Result", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.caesar_output = ctk.CTkTextbox(
            output_frame,
            height=100,
            wrap="word"
        )
        self.caesar_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            output_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.caesar_output.get("1.0", "end"))
        )
        copy_btn.pack(side="right", padx=5, pady=5)
    
    def create_playfair_interface(self, parent) -> None:
        """Create Playfair cipher interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Playfair Cipher", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Key input
        self.playfair_key = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter key...",
            width=400
        )
        self.playfair_key.pack(fill="x", padx=5, pady=5)
        
        # Text input
        self.playfair_text = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter text...",
            width=400
        )
        self.playfair_text.pack(fill="x", padx=5, pady=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Encrypt",
            command=self.playfair_encrypt,
            fg_color=ACCENT_COLOR
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Decrypt",
            command=self.playfair_decrypt,
            fg_color=SECONDARY_COLOR
        ).pack(side="left", padx=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Result", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.playfair_output = ctk.CTkTextbox(
            output_frame,
            height=100,
            wrap="word"
        )
        self.playfair_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            output_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.playfair_output.get("1.0", "end"))
        )
        copy_btn.pack(side="right", padx=5, pady=5)
        
        # Matrix visualizer
        matrix_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        matrix_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(matrix_frame, text="Key Matrix", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.matrix_display = ctk.CTkLabel(
            matrix_frame,
            text="Matrix will appear here",
            font=("Consolas", 10),
            justify="left"
        )
        self.matrix_display.pack(fill="x", padx=5, pady=5)
    
    def create_hill_interface(self, parent) -> None:
        """Create Hill cipher interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Hill Cipher (2x2)", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Key input
        key_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        key_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(key_frame, text="Key Matrix (a b c d):").pack(side="left", padx=5)
        
        validate_num = (self.register(validate_numeric_input), "%P")
        self.hill_key_a = ctk.CTkEntry(key_frame, width=50, validate="key", validatecommand=validate_num)
        self.hill_key_b = ctk.CTkEntry(key_frame, width=50, validate="key", validatecommand=validate_num)
        self.hill_key_c = ctk.CTkEntry(key_frame, width=50, validate="key", validatecommand=validate_num)
        self.hill_key_d = ctk.CTkEntry(key_frame, width=50, validate="key", validatecommand=validate_num)
        
        self.hill_key_a.pack(side="left", padx=2)
        self.hill_key_b.pack(side="left", padx=2)
        self.hill_key_c.pack(side="left", padx=2)
        self.hill_key_d.pack(side="left", padx=2)
        
        # Text input
        self.hill_text = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter text (even length)...",
            width=400
        )
        self.hill_text.pack(fill="x", padx=5, pady=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Encrypt",
            command=self.hill_encrypt,
            fg_color=ACCENT_COLOR
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Decrypt",
            command=self.hill_decrypt,
            fg_color=SECONDARY_COLOR
        ).pack(side="left", padx=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Result", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.hill_output = ctk.CTkTextbox(
            output_frame,
            height=100,
            wrap="word"
        )
        self.hill_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            output_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.hill_output.get("1.0", "end"))
        )
        copy_btn.pack(side="right", padx=5, pady=5)
        
        # Matrix visualizer
        matrix_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        matrix_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(matrix_frame, text="Key Matrix", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.hill_matrix_display = ctk.CTkLabel(
            matrix_frame,
            text="Matrix will appear here",
            font=("Consolas", 10),
            justify="left"
        )
        self.hill_matrix_display.pack(fill="x", padx=5, pady=5)
    
    def create_vigenere_interface(self, parent) -> None:
        """Create Vigenère cipher interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Vigenère Cipher", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Key input
        self.vigenere_key = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter key...",
            width=400
        )
        self.vigenere_key.pack(fill="x", padx=5, pady=5)
        
        # Text input
        self.vigenere_text = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter text...",
            width=400
        )
        self.vigenere_text.pack(fill="x", padx=5, pady=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Encrypt",
            command=self.vigenere_encrypt,
            fg_color=ACCENT_COLOR
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Decrypt",
            command=self.vigenere_decrypt,
            fg_color=SECONDARY_COLOR
        ).pack(side="left", padx=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Result", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.vigenere_output = ctk.CTkTextbox(
            output_frame,
            height=100,
            wrap="word"
        )
        self.vigenere_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            output_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.vigenere_output.get("1.0", "end"))
        )
        copy_btn.pack(side="right", padx=5, pady=5)
    
    def create_rail_fence_interface(self, parent) -> None:
        """Create Rail Fence cipher interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="Rail Fence Cipher", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Rails input
        rail_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        rail_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(rail_frame, text="Number of Rails:").pack(side="left", padx=5)
        
        validate_num = (self.register(validate_numeric_input), "%P")
        self.rail_fence_rails = ctk.CTkEntry(
            rail_frame,
            placeholder_text="Number...",
            width=80,
            validate="key",
            validatecommand=validate_num
        )
        self.rail_fence_rails.pack(side="left", padx=5)
        
        # Text input
        self.rail_fence_text = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter text...",
            width=400
        )
        self.rail_fence_text.pack(fill="x", padx=5, pady=5)
        
                # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Encrypt",
            command=self.rail_fence_encrypt,
            fg_color=ACCENT_COLOR
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Decrypt",
            command=self.rail_fence_decrypt,
            fg_color=SECONDARY_COLOR
        ).pack(side="left", padx=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Result", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.rail_fence_output = ctk.CTkTextbox(
            output_frame,
            height=100,
            wrap="word"
        )
        self.rail_fence_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            output_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.rail_fence_output.get("1.0", "end"))
        )
        copy_btn.pack(side="right", padx=5, pady=5)

    def create_des_interface(self, parent) -> None:
        """Create DES cipher interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="DES Encryption", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Key input
        self.des_key = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter 8-byte key (exactly 8 characters)...",
            width=400
        )
        self.des_key.pack(fill="x", padx=5, pady=5)
        
        # Text input
        self.des_text = ctk.CTkTextbox(
            input_frame,
            height=100,
            wrap="word"
        )
        self.des_text.pack(fill="x", padx=5, pady=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Encrypt",
            command=self.des_encrypt,
            fg_color=ACCENT_COLOR
        ).pack(side="left", padx=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Result", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.des_output = ctk.CTkTextbox(
            output_frame,
            height=100,
            wrap="word"
        )
        self.des_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            output_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.des_output.get("1.0", "end"))
        )
        copy_btn.pack(side="right", padx=5, pady=5)
        
        # Byte viewer
        byte_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        byte_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(byte_frame, text="Hex View", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.byte_display = ctk.CTkLabel(
            byte_frame,
            text="Hex output will appear here",
            font=("Consolas", 10),
            justify="left"
        )
        self.byte_display.pack(fill="x", padx=5, pady=5)

    def create_rsa_interface(self, parent) -> None:
        """Create RSA cipher interface"""
        # Notebook for different operations
        notebook = ctk.CTkTabview(parent)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Key generation tab
        keygen_tab = notebook.add("Key Generation")
        self.create_rsa_keygen_interface(keygen_tab)
        
        # Encryption/Decryption tab
        crypt_tab = notebook.add("Encryption/Decryption")
        self.create_rsa_crypt_interface(crypt_tab)

    def create_rsa_keygen_interface(self, parent) -> None:
        """Create RSA key generation interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="RSA Key Generation", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Prime inputs
        prime_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        prime_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(prime_frame, text="Prime p:").pack(side="left", padx=5)
        self.rsa_p = ctk.CTkEntry(prime_frame, width=120)
        self.rsa_p.pack(side="left", padx=5)
        
        ctk.CTkLabel(prime_frame, text="Prime q:").pack(side="left", padx=5)
        self.rsa_q = ctk.CTkEntry(prime_frame, width=120)
        self.rsa_q.pack(side="left", padx=5)
        
        # Generate button
        generate_btn = ctk.CTkButton(
            input_frame,
            text="Generate Keys",
            command=self.rsa_generate_keys,
            fg_color=ACCENT_COLOR
        )
        generate_btn.pack(pady=10)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Generated Keys", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Public key
        pub_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        pub_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(pub_frame, text="Public Key (e, n):").pack(side="left", padx=5)
        self.rsa_pub_key = ctk.CTkLabel(pub_frame, text="", font=("Consolas", 10))
        self.rsa_pub_key.pack(side="left", padx=5)
        
        # Private key
        priv_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        priv_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(priv_frame, text="Private Key (d, n):").pack(side="left", padx=5)
        self.rsa_priv_key = ctk.CTkLabel(priv_frame, text="", font=("Consolas", 10))
        self.rsa_priv_key.pack(side="left", padx=5)

    def create_rsa_crypt_interface(self, parent) -> None:
        """Create RSA encryption/decryption interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="RSA Encryption/Decryption", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Key input
        key_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        key_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(key_frame, text="Key (e/d, n):").pack(side="left", padx=5)
        self.rsa_key_e = ctk.CTkEntry(key_frame, width=120, placeholder_text="e/d")
        self.rsa_key_e.pack(side="left", padx=5)
        self.rsa_key_n = ctk.CTkEntry(key_frame, width=120, placeholder_text="n")
        self.rsa_key_n.pack(side="left", padx=5)
        
        # Message input
        self.rsa_message = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter message...",
            width=400
        )
        self.rsa_message.pack(fill="x", padx=5, pady=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Encrypt",
            command=self.rsa_encrypt,
            fg_color=ACCENT_COLOR
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Decrypt",
            command=self.rsa_decrypt,
            fg_color=SECONDARY_COLOR
        ).pack(side="left", padx=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Result", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.rsa_output = ctk.CTkTextbox(
            output_frame,
            height=100,
            wrap="word"
        )
        self.rsa_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            output_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.rsa_output.get("1.0", "end"))
        )
        copy_btn.pack(side="right", padx=5, pady=5)

    def create_dsa_interface(self, parent) -> None:
        """Create DSA interface"""
        # Notebook for different operations
        notebook = ctk.CTkTabview(parent)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Key generation tab
        keygen_tab = notebook.add("Key Generation")
        self.create_dsa_keygen_interface(keygen_tab)
        
        # Sign/Verify tab
        sign_tab = notebook.add("Sign/Verify")
        self.create_dsa_sign_interface(sign_tab)

    def create_dsa_keygen_interface(self, parent) -> None:
        """Create DSA key generation interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="DSA Key Generation", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Parameter inputs
        param_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        param_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(param_frame, text="Prime p:").pack(side="left", padx=5)
        self.dsa_p = ctk.CTkEntry(param_frame, width=120)
        self.dsa_p.pack(side="left", padx=5)
        
        ctk.CTkLabel(param_frame, text="Prime q:").pack(side="left", padx=5)
        self.dsa_q = ctk.CTkEntry(param_frame, width=120)
        self.dsa_q.pack(side="left", padx=5)
        
        ctk.CTkLabel(param_frame, text="Generator g:").pack(side="left", padx=5)
        self.dsa_g = ctk.CTkEntry(param_frame, width=120)
        self.dsa_g.pack(side="left", padx=5)
        
        # Generate button
        generate_btn = ctk.CTkButton(
            input_frame,
            text="Generate Keys",
            command=self.dsa_generate_keys,
            fg_color=ACCENT_COLOR
        )
        generate_btn.pack(pady=10)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Generated Keys", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Public key
        pub_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        pub_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(pub_frame, text="Public Key (y):").pack(side="left", padx=5)
        self.dsa_pub_key = ctk.CTkLabel(pub_frame, text="", font=("Consolas", 10))
        self.dsa_pub_key.pack(side="left", padx=5)
        
        # Private key
        priv_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        priv_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(priv_frame, text="Private Key (x):").pack(side="left", padx=5)
        self.dsa_priv_key = ctk.CTkLabel(priv_frame, text="", font=("Consolas", 10))
        self.dsa_priv_key.pack(side="left", padx=5)

    def create_dsa_sign_interface(self, parent) -> None:
        """Create DSA signing/verification interface"""
        # Input frame
        input_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(input_frame, text="DSA Sign/Verify", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # Parameters input
        param_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        param_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(param_frame, text="Parameters (p, q, g):").pack(side="left", padx=5)
        self.dsa_sign_p = ctk.CTkEntry(param_frame, width=80, placeholder_text="p")
        self.dsa_sign_p.pack(side="left", padx=2)
        self.dsa_sign_q = ctk.CTkEntry(param_frame, width=80, placeholder_text="q")
        self.dsa_sign_q.pack(side="left", padx=2)
        self.dsa_sign_g = ctk.CTkEntry(param_frame, width=80, placeholder_text="g")
        self.dsa_sign_g.pack(side="left", padx=2)
        
        # Key input
        key_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        key_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(key_frame, text="Key (x/y):").pack(side="left", padx=5)
        self.dsa_sign_key = ctk.CTkEntry(key_frame, width=120)
        self.dsa_sign_key.pack(side="left", padx=5)
        
        # Message input
        self.dsa_message = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter message...",
            width=400
        )
        self.dsa_message.pack(fill="x", padx=5, pady=5)
        
        # Signature input (for verification)
        sign_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        sign_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(sign_frame, text="Signature (r, s):").pack(side="left", padx=5)
        self.dsa_sign_r = ctk.CTkEntry(sign_frame, width=80, placeholder_text="r")
        self.dsa_sign_r.pack(side="left", padx=2)
        self.dsa_sign_s = ctk.CTkEntry(sign_frame, width=80, placeholder_text="s")
        self.dsa_sign_s.pack(side="left", padx=2)
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Sign",
            command=self.dsa_sign,
            fg_color=ACCENT_COLOR
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Verify",
            command=self.dsa_verify,
            fg_color=SECONDARY_COLOR
        ).pack(side="left", padx=5)
        
        # Output frame
        output_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        output_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ctk.CTkLabel(output_frame, text="Result", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        self.dsa_output = ctk.CTkTextbox(
            output_frame,
            height=100,
            wrap="word"
        )
        self.dsa_output.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Copy button
        copy_btn = ctk.CTkButton(
            output_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.dsa_output.get("1.0", "end"))
        )
        copy_btn.pack(side="right", padx=5, pady=5)

    # ===== CIPHER METHODS =====
    def caesar_encrypt(self) -> None:
        """Handle Caesar cipher encryption"""
        try:
            text = self.caesar_text.get()
            key = int(self.caesar_key.get())
            result = caesar_cipher(text, key, True)
            self.caesar_output.delete("1.0", "end")
            self.caesar_output.insert("1.0", result)
            self.update_status("Caesar encryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Caesar encryption failed: {str(e)}")

    def caesar_decrypt(self) -> None:
        """Handle Caesar cipher decryption"""
        try:
            text = self.caesar_text.get()
            key = int(self.caesar_key.get())
            result = caesar_cipher(text, key, False)
            self.caesar_output.delete("1.0", "end")
            self.caesar_output.insert("1.0", result)
            self.update_status("Caesar decryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Caesar decryption failed: {str(e)}")

    def playfair_encrypt(self) -> None:
        """Handle Playfair cipher encryption"""
        try:
            text = self.playfair_text.get()
            key = self.playfair_key.get()
            result = playfair_cipher(text, key, True)
            self.playfair_output.delete("1.0", "end")
            self.playfair_output.insert("1.0", result)
            
            # Update matrix display
            matrix = prepare_playfair_matrix(key)
            matrix_str = "\n".join([" ".join(row) for row in matrix])
            self.matrix_display.configure(text=matrix_str)
            
            self.update_status("Playfair encryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Playfair encryption failed: {str(e)}")

    def playfair_decrypt(self) -> None:
        """Handle Playfair cipher decryption"""
        try:
            text = self.playfair_text.get()
            key = self.playfair_key.get()
            result = playfair_cipher(text, key, False)
            self.playfair_output.delete("1.0", "end")
            self.playfair_output.insert("1.0", result)
            
            # Update matrix display
            matrix = prepare_playfair_matrix(key)
            matrix_str = "\n".join([" ".join(row) for row in matrix])
            self.matrix_display.configure(text=matrix_str)
            
            self.update_status("Playfair decryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Playfair decryption failed: {str(e)}")

    def hill_encrypt(self) -> None:
        """Handle Hill cipher encryption"""
        try:
            text = self.hill_text.get()
            key = [
                [int(self.hill_key_a.get()), int(self.hill_key_b.get())],
                [int(self.hill_key_c.get()), int(self.hill_key_d.get())]
            ]
            result = hill_cipher(text, key, True)
            self.hill_output.delete("1.0", "end")
            self.hill_output.insert("1.0", result)
            
            # Update matrix display
            matrix_str = f"Key Matrix:\n{key[0][0]} {key[0][1]}\n{key[1][0]} {key[1][1]}"
            self.hill_matrix_display.configure(text=matrix_str)
            
            self.update_status("Hill encryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Hill encryption failed: {str(e)}")

    def hill_decrypt(self) -> None:
        """Handle Hill cipher decryption"""
        try:
            text = self.hill_text.get()
            key = [
                [int(self.hill_key_a.get()), int(self.hill_key_b.get())],
                [int(self.hill_key_c.get()), int(self.hill_key_d.get())]
            ]
            result = hill_cipher(text, key, False)
            self.hill_output.delete("1.0", "end")
            self.hill_output.insert("1.0", result)
            
            # Update matrix display
            matrix_str = f"Key Matrix:\n{key[0][0]} {key[0][1]}\n{key[1][0]} {key[1][1]}"
            self.hill_matrix_display.configure(text=matrix_str)
            
            self.update_status("Hill decryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Hill decryption failed: {str(e)}")

    def vigenere_encrypt(self) -> None:
        """Handle Vigenère cipher encryption"""
        try:
            text = self.vigenere_text.get()
            key = self.vigenere_key.get()
            result = vigenere_cipher(text, key, True)
            self.vigenere_output.delete("1.0", "end")
            self.vigenere_output.insert("1.0", result)
            self.update_status("Vigenère encryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Vigenère encryption failed: {str(e)}")

    def vigenere_decrypt(self) -> None:
        """Handle Vigenère cipher decryption"""
        try:
            text = self.vigenere_text.get()
            key = self.vigenere_key.get()
            result = vigenere_cipher(text, key, False)
            self.vigenere_output.delete("1.0", "end")
            self.vigenere_output.insert("1.0", result)
            self.update_status("Vigenère decryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Vigenère decryption failed: {str(e)}")

    def rail_fence_encrypt(self) -> None:
        """Handle Rail Fence cipher encryption"""
        try:
            text = self.rail_fence_text.get()
            rails = int(self.rail_fence_rails.get())
            result = rail_fence_cipher(text, rails, True)
            self.rail_fence_output.delete("1.0", "end")
            self.rail_fence_output.insert("1.0", result)
            self.update_status("Rail Fence encryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Rail Fence encryption failed: {str(e)}")

    def rail_fence_decrypt(self) -> None:
        """Handle Rail Fence cipher decryption"""
        try:
            text = self.rail_fence_text.get()
            rails = int(self.rail_fence_rails.get())
            result = rail_fence_cipher(text, rails, False)
            self.rail_fence_output.delete("1.0", "end")
            self.rail_fence_output.insert("1.0", result)
            self.update_status("Rail Fence decryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"Rail Fence decryption failed: {str(e)}")

    def des_encrypt(self) -> None:
        """Handle DES encryption"""
        try:
            key = self.des_key.get()
            text = self.des_text.get("1.0", "end-1c")
            
            if len(key) != 8:
                raise ValueError("Key must be exactly 8 characters")
            
            # Convert to bytes
            key_bytes = key.encode('latin-1')
            text_bytes = text.encode('latin-1')
            
            # Pad text to be multiple of 8 bytes
            pad_len = 8 - (len(text_bytes) % 8)
            text_bytes += bytes([pad_len] * pad_len)
            
            # Simple XOR "encryption" for demonstration
            # In a real implementation, you would use proper DES here
            encrypted = bytes([text_bytes[i] ^ key_bytes[i % 8] for i in range(len(text_bytes))])
            
            # Display results
            self.des_output.delete("1.0", "end")
            self.des_output.insert("1.0", encrypted.hex())
            
            self.byte_display.configure(text=f"Hex: {encrypted.hex()}")
            self.update_status("DES encryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"DES encryption failed: {str(e)}")

    def rsa_generate_keys(self) -> None:
        """Generate RSA keys"""
        try:
            p = int(self.rsa_p.get())
            q = int(self.rsa_q.get())
            
            if not self.is_prime(p) or not self.is_prime(q):
                raise ValueError("Both numbers must be prime")
            
            n = p * q
            phi = (p - 1) * (q - 1)
            
            e = 2
            while e < phi:
                if math.gcd(e, phi) == 1:
                    break
                e += 1
            
            d = self.mod_inverse(e, phi)
            
            # Display keys
            self.rsa_pub_key.configure(text=f"{e}, {n}")
            self.rsa_priv_key.configure(text=f"{d}, {n}")
            self.update_status("RSA key generation successful!")
        except Exception as e:
            messagebox.showerror("Error", f"RSA key generation failed: {str(e)}")

    def rsa_encrypt(self) -> None:
        """Handle RSA encryption"""
        try:
            e = int(self.rsa_key_e.get())
            n = int(self.rsa_key_n.get())
            msg = int(self.rsa_message.get())
            
            cipher = pow(msg, e, n)
            self.rsa_output.delete("1.0", "end")
            self.rsa_output.insert("1.0", str(cipher))
            self.update_status("RSA encryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"RSA encryption failed: {str(e)}")

    def rsa_decrypt(self) -> None:
        """Handle RSA decryption"""
        try:
            d = int(self.rsa_key_e.get())
            n = int(self.rsa_key_n.get())
            cipher = int(self.rsa_message.get())
            
            msg = pow(cipher, d, n)
            self.rsa_output.delete("1.0", "end")
            self.rsa_output.insert("1.0", str(msg))
            self.update_status("RSA decryption successful!")
        except Exception as e:
            messagebox.showerror("Error", f"RSA decryption failed: {str(e)}")

    def dsa_generate_keys(self) -> None:
        """Generate DSA keys"""
        try:
            p = int(self.dsa_p.get())
            q = int(self.dsa_q.get())
            g = int(self.dsa_g.get())
            
            x = 2  # In real implementation, this would be a random number
            y = pow(g, x, p)
            
            # Display keys
            self.dsa_pub_key.configure(text=str(y))
            self.dsa_priv_key.configure(text=str(x))
            self.update_status("DSA key generation successful!")
        except Exception as e:
            messagebox.showerror("Error", f"DSA key generation failed: {str(e)}")

    def dsa_sign(self) -> None:
        """Handle DSA signing"""
        try:
            p = int(self.dsa_sign_p.get())
            q = int(self.dsa_sign_q.get())
            g = int(self.dsa_sign_g.get())
            x = int(self.dsa_sign_key.get())
            msg = self.dsa_message.get()
            
            # Simplified signing process
            k = 2  # In real implementation, this would be random
            r = pow(g, k, p) % q
            h = hash(msg) % q
            s = (self.mod_inverse(k, q) * (h + x * r)) % q
            
            self.dsa_output.delete("1.0", "end")
            self.dsa_output.insert("1.0", f"Signature (r, s): {r}, {s}")
            self.update_status("DSA signing successful!")
        except Exception as e:
            messagebox.showerror("Error", f"DSA signing failed: {str(e)}")

    def dsa_verify(self) -> None:
        """Handle DSA verification"""
        try:
            p = int(self.dsa_sign_p.get())
            q = int(self.dsa_sign_q.get())
            g = int(self.dsa_sign_g.get())
            y = int(self.dsa_sign_key.get())
            msg = self.dsa_message.get()
            r = int(self.dsa_sign_r.get())
            s = int(self.dsa_sign_s.get())
            
            # Simplified verification process
            w = self.mod_inverse(s, q)
            h = hash(msg) % q
            u1 = (h * w) % q
            u2 = (r * w) % q
            v = (pow(g, u1, p) * pow(y, u2, p) % p) % q
            
            if v == r:
                result = "Signature is valid!"
            else:
                result = "Signature is invalid!"
            
            self.dsa_output.delete("1.0", "end")
            self.dsa_output.insert("1.0", result)
            self.update_status("DSA verification successful!")
        except Exception as e:
            messagebox.showerror("Error", f"DSA verification failed: {str(e)}")

    # ===== HELPER METHODS =====
    def copy_to_clipboard(self, text: str) -> None:
        """Copy text to clipboard"""
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update_status("Copied to clipboard!")

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime"""
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """Find modular inverse of a under modulo m"""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return -1

if __name__ == "__main__":
    app = CryptographyApp()
    app.mainloop()
