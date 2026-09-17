from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

print("Loading AI model...")

# Smaller BART model - uses less memory
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

print("AI model loaded successfully!")


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Split long text into smaller chunks
def split_text(text, max_chars=1800):

    words = text.split()

    chunks = []
    current_chunk = ""

    for word in words:

        # Check whether adding the next word exceeds the limit
        if len(current_chunk) + len(word) + 1 <= max_chars:
            current_chunk += word + " "

        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "

    # Add the remaining text
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


# Summarization API
@app.route("/summarize", methods=["POST"])
def summarize():

    data = request.get_json()

    if not data:
        return jsonify({
            "summary": "No data received."
        })

    news = data.get("news", "").strip()

    # Maximum input limit = 10,000 characters
    if len(news) > 10000:
        return jsonify({
            "summary": "Please enter a maximum of 10,000 characters."
        })

    if not news:
        return jsonify({
            "summary": "Please enter some news."
        })

    try:

        print("Input characters:", len(news))

        # Split article into smaller chunks
        chunks = split_text(news, max_chars=1800)

        print("Number of chunks:", len(chunks))

        summaries = []

        # Summarize each chunk
        for i, chunk in enumerate(chunks):

            print("Summarizing chunk", i + 1, "of", len(chunks))

            result = summarizer(
                chunk,
                max_length=100,
                min_length=25,
                do_sample=False
            )

            summaries.append(result[0]["summary_text"])

        # Combine all chunk summaries
        combined_summary = " ".join(summaries)

        # If there are many summaries, summarize them again
        if len(combined_summary.split()) > 180:

            final_chunks = split_text(
                combined_summary,
                max_chars=1800
            )

            final_summaries = []

            for chunk in final_chunks:

                result = summarizer(
                    chunk,
                    max_length=120,
                    min_length=30,
                    do_sample=False
                )

                final_summaries.append(
                    result[0]["summary_text"]
                )

            combined_summary = " ".join(final_summaries)

        return jsonify({
            "summary": combined_summary
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "summary": "Error: " + str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)