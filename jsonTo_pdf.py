from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import black, blue, darkred,red
import json
def format_content(data1, data2):
    """
    Format content from the JSON data for saving to a PDF with proper line breaks and spacing.
    """
    formatted_lines = []

    formatted_lines.append(f"---- Full Summery Of The Audio Content ----")
    formatted_lines.append("   ")
    formatted_lines.append("   ")
    # Process the first JSON file data
    for idx, entry in enumerate(data1, start=1):
        formatted_lines.append(f"---- Key Point {idx} ----")
        if "gist" in entry:
            formatted_lines.append("   ")
            formatted_lines.extend(wrap_text(entry['gist'], width=80))
        if "summary" in entry:
            formatted_lines.append("    ")
            formatted_lines.extend(wrap_text(entry['summary'], width=80))
        formatted_lines.append("--------------------")
        formatted_lines.append("")

    # Process the second JSON file data
    if isinstance(data2, str):  # If the second file is a string summary
        cleaned_summary = clean_summary(data2)  # Clean the text before formatting
        formatted_lines.append("---- conclusion ----")
        formatted_lines.extend(wrap_text(cleaned_summary, width=80))
        formatted_lines.append("--------------------")
        formatted_lines.append("")
    
    return "\n".join(formatted_lines)

def clean_summary(text):
    """
    Remove specific unwanted phrases or patterns from the summary text.
    """
    unwanted_phrase = "Here is a concise summary of the key points from the conversation transcript:"
    return text.replace(unwanted_phrase, "").strip()


def wrap_text(text, width=80):
    """
    Wrap text into lines of a specified width for better readability.
    """
    import textwrap
    return textwrap.wrap(text, width)


class BorderedCanvas(canvas.Canvas):
    """
    Custom canvas to draw borders on every page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw_border(self):
        """
        Draw a border around the page.
        """
        width, height = letter
        margin = 20  # Margin for the border
        self.setStrokeColor(black)
        self.setLineWidth(2)
        self.rect(margin, margin, width - 2 * margin, height - 2 * margin)

    def showPage(self):
        """
        Override showPage to ensure the border is drawn on every page.
        """
        self.draw_border()  # Draw the border
        super().showPage()

    def save(self):
        """
        Ensure the last page's border is drawn before saving.
        """
        self.draw_border()
        super().save()

def save_to_pdf(content, filename="output_with_border.pdf"):
    """
    Save the formatted content to a PDF file with a border on each page.
    """
    # Set up the PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []  # List of elements to add to the PDF

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.textColor = red

    key_point_style = styles['Heading3']
    key_point_style.textColor = black

    conclusion_style = styles['Heading3']
    conclusion_style.textColor = blue

    default_style = styles['BodyText']
    default_style.textColor = blue

    gist_style = styles['BodyText']
    gist_style.textColor = black
    gist_style.fontName = "Helvetica-Bold"

    # Split content into lines and format them
    for line in content.split("\n"):
        if "---- Full Summery Of The Audio Content ----" in line:
            elements.append(Paragraph(line, title_style))
        elif "---- Key Point" in line:
            elements.append(Spacer(1, 12))  # Add some space before
            elements.append(Paragraph(line, key_point_style))
        elif "---- conclusion ----" in line:
            elements.append(Spacer(1, 12))  # Add some space before
            elements.append(Paragraph(line, conclusion_style))
        elif "Gist:" in line:
            elements.append(Paragraph(line, gist_style))
        else:
            elements.append(Paragraph(line, default_style))

        elements.append(Spacer(1, 4))  # Add spacing between lines

    # Build the PDF with a custom canvas
    doc.build(elements, canvasmaker=BorderedCanvas)
    print(f"PDF with borders saved as {filename}")
def pdf_generator(text1,text2,pdfName):
     
    # Load JSON data from files
    with open(text1, "r") as file1, open(text2, "r") as file2:
        data1 = json.load(file1)  # Load the first JSON file (list of objects)
        data2 = file2.read().strip()  # Read the second JSON file as a string

    # Format the content
    formatted_content = format_content(data1, data2)

    # Save the content to a PDF
    pdfName = pdfName+ ".pdf"
    save_to_pdf(formatted_content, filename=pdfName)
