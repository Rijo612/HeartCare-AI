from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_report(filename, patient, result, confidence):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>HeartCare AI Medical Report</b>", styles['Title']))

    story.append(Paragraph(f"Age : {patient['Age']}", styles['BodyText']))
    story.append(Paragraph(f"Gender : {patient['Gender']}", styles['BodyText']))
    story.append(Paragraph(f"BMI : {patient['BMI']}", styles['BodyText']))

    story.append(Paragraph(f"<br/><b>Prediction :</b> {result}", styles['Heading2']))

    story.append(Paragraph(f"Confidence : {confidence:.2f}%", styles['BodyText']))

    story.build(story)