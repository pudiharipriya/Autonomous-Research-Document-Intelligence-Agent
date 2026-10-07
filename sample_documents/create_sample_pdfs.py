import os
import sys

def create_sample_pdf(filename: str):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
    except ImportError:
        print("reportlab not installed. Skipping sample PDF generation script.")
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=12
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )

    story.append(Paragraph("Attention Is All You Need: Empirical Study", title_style))
    story.append(Paragraph("<b>Authors:</b> Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Abstract</b>", styles['Heading2']))
    story.append(Paragraph(
        "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks "
        "that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. "
        "We propose the Transformer, a novel network architecture based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. "
        "Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. "
        "Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results by over 2 BLEU.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>1. Introduction & Methodology</b>", styles['Heading2']))
    story.append(Paragraph(
        "Recurrent neural networks, particularly long short-term memory (LSTM) and gated recurrent (GRU) neural networks, "
        "have been firmly established as state of the art approaches in sequence modeling. "
        "To allow building representations of sequences without regard to their distance in input or output sequences, "
        "we propose Multi-Head Self-Attention. Multi-Head Attention allows the model to jointly attend to information from different representation subspaces at different positions.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>2. Experimental Results & Benchmarks</b>", styles['Heading2']))
    story.append(Paragraph(
        "On the WMT 2014 English-to-German translation task, the Transformer (big) achieves 28.4 BLEU score outperforming all previously reported models. "
        "On the WMT 2014 English-to-French translation task, our model achieves a new state-of-the-art BLEU score of 41.8 after training for 3.5 days on 8 P100 GPUs.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Benchmark Table
    data = [
        ['Model', 'WMT 2014 En-De (BLEU)', 'WMT 2014 En-Fr (BLEU)', 'Training Cost (FLOPs)'],
        ['ByteNet', '23.75', '-', '1.0e19'],
        ['ConvS2S', '25.16', '40.46', '9.6e18'],
        ['Transformer (base)', '27.3', '38.1', '3.3e18'],
        ['Transformer (big)', '28.4', '41.8', '2.3e19']
    ]
    t = Table(data, colWidths=[130, 130, 130, 130])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>3. Limitations & Conclusion</b>", styles['Heading2']))
    story.append(Paragraph(
        "While the Transformer achieves state-of-the-art performance, it exhibits quadratic computational memory complexity O(N^2) relative to sequence length. "
        "In conclusion, we presented the Transformer, the first sequence transduction model based entirely on attention.",
        body_style
    ))

    doc.build(story)
    print(f"Sample PDF created at: {filename}")

if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(__file__), "transformer_paper_summary.pdf")
    create_sample_pdf(out_pdf)
