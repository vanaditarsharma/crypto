import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import io
import math
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
        
        # Dictionary to store cipher frames
        self.cipher_frames = {}
        
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
        
        # Add more symmetric ciphers as needed...
    
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
            command=lambda: self.copy_to_clipboard(self.caesar_output.get("1.0", "end")))
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
        
        # Matrix visualizer (placeholder)
        matrix_frame = ctk.CTkFrame(parent, fg_color=DARK_FRAME)
        matrix_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(matrix_frame, text="Key Matrix", font=FONT_HEADING).pack(anchor="w", pady=(5, 10))
        
        # This would be updated when a key is entered
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
        
        # Matrix visualizer (placeholder)
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
        
        # Byte viewer (placeholder)
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
        self.rsa_pub_key = ctk.CTkLabel
